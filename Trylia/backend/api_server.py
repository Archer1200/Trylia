from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import threading
import os
import sys
import signal
import time
import logging
from datetime import datetime

# Load environment variables
try:
    from dotenv import load_dotenv # type: ignore
    load_dotenv()
except ImportError:
    # dotenv not installed, environment variables should be set manually
    pass

# Import contact form modules
from email_service import email_service
from validation_utils import ContactFormValidator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_server.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variable to track the current try-on process
current_process = None
process_lock = threading.Lock()

def map_shirt_id_to_selection(shirt_id):
    """
    Map frontend shirt ID to backend gender and index.
    Frontend IDs: 1-7 for male, 101-105 for female
    Backend expects: gender ('male'/'female') and 1-based index
    """
    if 1 <= shirt_id <= 7:
        return "male", shirt_id
    elif 101 <= shirt_id <= 105:
        return "female", shirt_id - 100
    else:
        raise ValueError(f"Invalid shirt ID: {shirt_id}")

def test_camera_access():
    """
    Test if camera is accessible before starting the try-on service.
    """
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return False, "Camera could not be opened"
        
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            return False, "Could not read frame from camera"
        
        return True, "Camera is accessible"
    except Exception as e:
        return False, f"Camera test failed: {str(e)}"

def create_tryon_script_with_args(gender, shirt_index):
    """
    Create a try-on service script that accepts command line arguments.
    """
    script_content = f'''
import os
import cv2
import math
import cvzone
import sys
from cvzone.PoseModule import PoseDetector

def calculate_size_recommendation(shoulder_dist):
    """
    Calculate size recommendation based on shoulder distance.
    """
    # Size mapping based on shoulder distance in pixels
    if shoulder_dist < 80:
        return "XS"
    elif shoulder_dist < 100:
        return "S"
    elif shoulder_dist < 120:
        return "M"
    elif shoulder_dist < 140:
        return "L"
    elif shoulder_dist < 160:
        return "XL"
    else:
        return "XXL"

def calculate_confidence_score(lmList, shoulder_dist):
    """
    Calculate confidence/accuracy score based on pose detection quality.
    """
    if not lmList or len(lmList) < 25:
        return 0.0
    
    # Check visibility of key landmarks
    key_landmarks = [11, 12, 23, 24]  # shoulders and hips
    visible_count = 0
    
    for idx in key_landmarks:
        if idx < len(lmList) and len(lmList[idx]) >= 3:
            # Check if landmark is visible (confidence > 0.5)
            if len(lmList[idx]) > 3 and lmList[idx][3] > 0.5:
                visible_count += 1
            elif len(lmList[idx]) == 3:  # No confidence score available
                visible_count += 1
    
    visibility_score = visible_count / len(key_landmarks)
    
    # Check shoulder distance stability (good pose)
    shoulder_stability = min(1.0, shoulder_dist / 50.0) if shoulder_dist > 0 else 0.0
    
    # Combine scores
    confidence = (visibility_score * 0.7 + shoulder_stability * 0.3) * 100
    return min(100.0, confidence)

def draw_info_panel(img, size_rec, confidence, gender, shirt_index):
    """
    Draw size recommendation and confidence score at bottom right corner.
    """
    h, w = img.shape[:2]
    
    # Panel dimensions
    panel_width = 280
    panel_height = 120
    panel_x = w - panel_width - 20
    panel_y = h - panel_height - 20
    
    # Draw semi-transparent background
    overlay = img.copy()
    cv2.rectangle(overlay, (panel_x, panel_y), (panel_x + panel_width, panel_y + panel_height), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.7, img, 0.3, 0, img)
    
    # Draw border
    cv2.rectangle(img, (panel_x, panel_y), (panel_x + panel_width, panel_y + panel_height), (255, 255, 255), 2)
    
    # Text properties
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    thickness = 2
    
    # Title
    title_text = f"{{gender.upper()}} SHIRT {{shirt_index}}"
    cv2.putText(img, title_text, (panel_x + 10, panel_y + 25), font, 0.5, (255, 255, 255), 1)
    
    # Size recommendation
    size_text = f"Recommended Size: {{size_rec}}"
    cv2.putText(img, size_text, (panel_x + 10, panel_y + 50), font, font_scale, (0, 255, 0), thickness)
    
    # Confidence score with color coding
    conf_text = f"Accuracy: {{confidence:.1f}}%"
    if confidence >= 80:
        conf_color = (0, 255, 0)  # Green
    elif confidence >= 60:
        conf_color = (0, 255, 255)  # Yellow
    else:
        conf_color = (0, 0, 255)  # Red
    
    cv2.putText(img, conf_text, (panel_x + 10, panel_y + 75), font, font_scale, conf_color, thickness)
    
    # Confidence bar
    bar_x = panel_x + 10
    bar_y = panel_y + 90
    bar_width = 200
    bar_height = 15
    
    # Background bar
    cv2.rectangle(img, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (50, 50, 50), -1)
    
    # Confidence bar fill
    fill_width = int((confidence / 100.0) * bar_width)
    cv2.rectangle(img, (bar_x, bar_y), (bar_x + fill_width, bar_y + bar_height), conf_color, -1)
    
    # Bar border
    cv2.rectangle(img, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (255, 255, 255), 1)
    
    return img

def main():
    gender = "{gender}"
    shirt_index = {shirt_index}
    
    print(f"[INFO] Starting Virtual Try-On for {{gender}} shirt {{shirt_index}}")
    
    # --- Camera and Pose Detector ---
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Could not open camera")
        return 1
    
    print("[INFO] Camera opened successfully")
    
    detector = PoseDetector()
    shirtRatio = 581 / 440  # Height/Width ratio of shirt images
    selected_shirt = None
    
    # --- Shirt lists ---
    try:
        male_shirts = [f"male/{{f}}" for f in os.listdir("static/male") if f.lower().endswith((".png", ".jpg", ".jpeg"))]
        female_shirts = [f"female/{{f}}" for f in os.listdir("static/female") if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    except Exception as e:
        print(f"[ERROR] Could not load shirt lists: {{e}}")
        cap.release()
        return 1
    
    # --- Select shirt ---
    try:
        if gender == "male":
            if 1 <= shirt_index <= len(male_shirts):
                selected_shirt = male_shirts[shirt_index - 1]
            else:
                raise ValueError(f"Invalid male shirt index: {{shirt_index}} (available: 1-{{len(male_shirts)}})")
        elif gender == "female":
            if 1 <= shirt_index <= len(female_shirts):
                selected_shirt = female_shirts[shirt_index - 1]
            else:
                raise ValueError(f"Invalid female shirt index: {{shirt_index}} (available: 1-{{len(female_shirts)}})")
        
        print(f"[INFO] Selected shirt: {{selected_shirt}}")
        
        # Check if shirt file exists
        shirt_path = os.path.join("static", selected_shirt)
        if not os.path.exists(shirt_path):
            raise ValueError(f"Shirt file not found: {{shirt_path}}")
        
    except Exception as e:
        print(f"[ERROR] Shirt selection failed: {{e}}")
        cap.release()
        return 1
    
    # --- Smoothing variables for stable overlay ---
    prev_cx, prev_cy, prev_w, prev_h = 0, 0, 0, 0
    smoothing = 0.2  # smaller = smoother
    
    # --- Size and confidence tracking ---
    size_recommendation = "M"
    confidence_score = 0.0
    
    print("[INFO] Virtual Try-On started! Press 'q' to quit.")
    
    try:
        while True:
            success, img = cap.read()
            if not success:
                print("[ERROR] Could not read frame from camera")
                break
            
            img = detector.findPose(img, draw=False)
            lmList, _ = detector.findPosition(img, bboxWithHands=False, draw=False)
            
            # Calculate confidence score
            confidence_score = calculate_confidence_score(lmList, 0)
            
            if lmList and selected_shirt:
                try:
                    # Shoulder and hip landmarks
                    lm11, lm12 = lmList[11], lmList[12]
                    lm23, lm24 = lmList[23], lmList[24]
                    
                    shoulderDist = math.hypot(lm12[0]-lm11[0], lm12[1]-lm11[1])
                    
                    # Update confidence score with shoulder distance
                    confidence_score = calculate_confidence_score(lmList, shoulderDist)
                    
                    # Calculate size recommendation
                    size_recommendation = calculate_size_recommendation(shoulderDist)
                    
                    if shoulderDist < 50:
                        # Draw info panel even when pose is not good enough for overlay
                        img = draw_info_panel(img, size_recommendation, confidence_score, gender, shirt_index)
                        cv2.imshow("Virtual Try-On", img)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                        continue
                    
                    # Shirt size
                    w = int(shoulderDist * 1.6)
                    h = int(w * shirtRatio)
                    
                    # Midpoint for overlay
                    cx = (lm11[0]+lm12[0])//2
                    cy = (lm11[1]+lm12[1])//2
                    torso_y = (lm23[1]+lm24[1])//2
                    cy_torso = (cy+torso_y)//2
                    
                    # Smooth overlay
                    cx = int(prev_cx + (cx-prev_cx)*smoothing)
                    cy_torso = int(prev_cy + (cy_torso-prev_cy)*smoothing)
                    w = int(prev_w + (w-prev_w)*smoothing)
                    h = int(prev_h + (h-prev_h)*smoothing)
                    prev_cx, prev_cy, prev_w, prev_h = cx, cy_torso, w, h
                    
                    # Load and overlay shirt
                    path = os.path.join("static", selected_shirt)
                    if os.path.exists(path):
                        imgShirt = cv2.imread(path, cv2.IMREAD_UNCHANGED)
                        if imgShirt is not None:
                            imgShirt = cv2.resize(imgShirt, (w, h))
                            imgShirt = cv2.flip(imgShirt, 1)
                            
                            dx = lm12[0] - lm11[0]
                            dy = lm12[1] - lm11[1]
                            angle = math.degrees(math.atan2(dy, dx))
                            
                            if dx < 0:
                                angle += 180
                            
                            M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1)
                            imgShirt = cv2.warpAffine(imgShirt, M, (w, h), borderMode=cv2.BORDER_TRANSPARENT)
                            
                            x = max(cx - w//2, 0)
                            y = max(cy_torso - h//2, 0)
                            img = cvzone.overlayPNG(img, imgShirt, [x, y])
                
                except Exception as e:
                    print(f"[WARN] Shirt overlay skipped: {{e}}")
            
            # Always draw the info panel
            img = draw_info_panel(img, size_recommendation, confidence_score, gender, shirt_index)
            
            cv2.imshow("Virtual Try-On", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except KeyboardInterrupt:
        print("\\n[INFO] Interrupted by user")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {{e}}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("[INFO] Virtual Try-On stopped.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''
    
    # Write the script
    script_path = os.path.join(os.path.dirname(__file__), 'temp_tryon_service.py')
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    return script_path

def start_tryon_service(gender, shirt_index):
    """
    Start the try-on service with the selected shirt.
    """
    global current_process
    
    try:
        # Stop any existing process
        stop_current_process()
        
        # Test camera access first
        camera_ok, camera_msg = test_camera_access()
        if not camera_ok:
            logger.error(f"Camera test failed: {camera_msg}")
            return False, camera_msg
        
        logger.info(f"Camera test passed: {camera_msg}")
        
        # Create the try-on script with arguments
        script_path = create_tryon_script_with_args(gender, shirt_index)
        
        # Start the new process
        with process_lock:
            current_process = subprocess.Popen([
                sys.executable, script_path
            ], 
            cwd=os.path.dirname(__file__),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
            )
            
        logger.info(f"Started try-on service for {gender} shirt {shirt_index} (PID: {current_process.pid})")
        
        # Start a thread to monitor the process output
        monitor_thread = threading.Thread(target=monitor_process_output, daemon=True)
        monitor_thread.start()
        
        return True, f"Try-on service started successfully"
        
    except Exception as e:
        logger.error(f"Failed to start try-on service: {e}")
        return False, f"Failed to start try-on service: {str(e)}"

def monitor_process_output():
    """
    Monitor the output of the try-on process for debugging.
    """
    global current_process
    
    if current_process is None:
        return
    
    try:
        # Read stdout and stderr
        while current_process.poll() is None:
            if current_process.stdout:
                line = current_process.stdout.readline()
                if line:
                    logger.info(f"TryOn Process: {line.strip()}")
            
            if current_process.stderr:
                line = current_process.stderr.readline()
                if line:
                    logger.error(f"TryOn Process Error: {line.strip()}")
            
            time.sleep(0.1)
    except Exception as e:
        logger.error(f"Error monitoring process output: {e}")

def stop_current_process():
    """
    Stop the current try-on process if it's running.
    """
    global current_process
    
    with process_lock:
        if current_process and current_process.poll() is None:
            try:
                logger.info(f"Stopping try-on process (PID: {current_process.pid})")
                # Try graceful termination first
                current_process.terminate()
                current_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Force kill if graceful termination fails
                logger.warning("Graceful termination failed, force killing process")
                current_process.kill()
                current_process.wait()
            except Exception as e:
                logger.error(f"Error stopping process: {e}")
            finally:
                current_process = None
                logger.info("Try-on process stopped")

@app.route('/api/try-on', methods=['POST'])
def try_on():
    """
    API endpoint to start virtual try-on for a specific shirt.
    """
    try:
        data = request.get_json()
        shirt_id = data.get('shirtId')
        
        logger.info(f"Received try-on request for shirt ID: {shirt_id}")
        
        if not shirt_id:
            return jsonify({
                'success': False,
                'message': 'Shirt ID is required'
            }), 400
        
        # Map shirt ID to gender and index
        try:
            gender, shirt_index = map_shirt_id_to_selection(shirt_id)
            logger.info(f"Mapped shirt ID {shirt_id} to {gender} shirt {shirt_index}")
        except ValueError as e:
            logger.error(f"Invalid shirt ID mapping: {e}")
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400
        
        # Start the try-on service
        success, message = start_tryon_service(gender, shirt_index)
        
        if success:
            return jsonify({
                'success': True,
                'message': message,
                'gender': gender,
                'shirtIndex': shirt_index
            })
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 500
            
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@app.route('/api/stop', methods=['POST'])
def stop_tryon():
    """
    API endpoint to stop the current virtual try-on session.
    """
    try:
        logger.info("Received stop request")
        stop_current_process()
        return jsonify({
            'success': True,
            'message': 'Virtual try-on stopped'
        })
    except Exception as e:
        logger.error(f"Error stopping try-on: {e}")
        return jsonify({
            'success': False,
            'message': f'Error stopping try-on: {str(e)}'
        }), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """
    API endpoint to check if try-on service is running.
    """
    global current_process
    
    with process_lock:
        is_running = current_process is not None and current_process.poll() is None
        pid = current_process.pid if current_process else None
    
    return jsonify({
        'isRunning': is_running,
        'pid': pid,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/test-camera', methods=['GET'])
def test_camera():
    """
    API endpoint to test camera access.
    """
    try:
        camera_ok, camera_msg = test_camera_access()
        return jsonify({
            'success': camera_ok,
            'message': camera_msg
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Camera test error: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    """
    return jsonify({
        'status': 'healthy',
        'message': 'Virtual Try-On API Server is running',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/contact', methods=['POST'])
def contact_form():
    """
    API endpoint to handle contact form submissions.
    """
    try:
        # Get form data
        form_data = request.get_json()
        
        if not form_data:
            return jsonify({
                'success': False,
                'message': 'No form data provided'
            }), 400
        
        logger.info(f"Received contact form submission from {form_data.get('companyName', 'Unknown')}")
        
        # Validate form data
        is_valid, errors, validated_data = ContactFormValidator.validate_contact_form(form_data)
        
        if not is_valid:
            logger.warning(f"Contact form validation failed: {errors}")
            return jsonify({
                'success': False,
                'message': 'Form validation failed',
                'errors': errors
            }), 400
        
        # Send email notification (optional - don't fail if email fails)
        email_sent, email_message = email_service.send_contact_email(validated_data)
        
        if not email_sent:
            logger.warning(f"Email sending failed: {email_message}")
            # Don't fail the entire request if email fails
            # Just log the issue and continue
        
        # Send confirmation email to customer (optional, don't fail if this fails)
        confirmation_sent, confirmation_message = email_service.send_confirmation_email(validated_data)
        if not confirmation_sent:
            logger.warning(f"Failed to send confirmation email: {confirmation_message}")
        
        logger.info(f"Contact form processed successfully for {validated_data.get('companyName')}")
        
        # Determine success message based on email status
        if email_sent:
            message = 'Thank you for your inquiry! We will get back to you within 24 hours.'
        else:
            message = 'Thank you for your inquiry! Your form has been submitted successfully. (Email notification temporarily unavailable)'
        
        return jsonify({
            'success': True,
            'message': message,
            'emailSent': email_sent,
            'confirmationSent': confirmation_sent
        })
        
    except Exception as e:
        logger.error(f"Contact form API error: {e}")
        return jsonify({
            'success': False,
            'message': 'An unexpected error occurred. Please try again later.'
        }), 500

@app.route('/api/contact/options', methods=['GET'])
def get_contact_options():
    """
    API endpoint to get dropdown options for the contact form.
    """
    try:
        return jsonify({
            'success': True,
            'options': {
                'companySizes': ContactFormValidator.COMPANY_SIZES,
                'inquiryTypes': ContactFormValidator.INQUIRY_TYPES,
                'meetingModes': ContactFormValidator.MEETING_MODES,
                'countries': ContactFormValidator.COUNTRIES
            }
        })
    except Exception as e:
        logger.error(f"Error getting contact options: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to load form options'
        }), 500

# Cleanup on exit
def cleanup():
    """
    Cleanup function to stop any running processes.
    """
    logger.info("Cleaning up...")
    stop_current_process()
    
    # Clean up temporary files
    temp_script = os.path.join(os.path.dirname(__file__), 'temp_tryon_service.py')
    if os.path.exists(temp_script):
        try:
            os.remove(temp_script)
            logger.info("Removed temporary script")
        except Exception as e:
            logger.error(f"Error removing temporary script: {e}")

def signal_handler(sig, frame):
    """
    Handle shutdown signals.
    """
    logger.info("Received shutdown signal")
    cleanup()
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    logger.info("Starting Virtual Try-On API Server...")
    logger.info("Server will be available at: http://localhost:5000")
    logger.info("API endpoints:")
    logger.info("  POST /api/try-on - Start virtual try-on")
    logger.info("  POST /api/stop - Stop virtual try-on")
    logger.info("  GET /api/status - Check service status")
    logger.info("  GET /api/test-camera - Test camera access")
    logger.info("  POST /api/contact - Submit contact form")
    logger.info("  GET /api/contact/options - Get form dropdown options")
    logger.info("  GET /health - Health check")
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
    finally:
        cleanup()