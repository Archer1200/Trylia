import os
import cv2
import math
import cvzone
from cvzone.PoseModule import PoseDetector

# --- Camera and Pose Detector ---
cap = cv2.VideoCapture(1)
detector = PoseDetector()
shirtRatio = 581 / 440  # Height/Width ratio of shirt images
selected_shirt = None

# --- Shirt lists ---
male_shirts = [f"male/{f}" for f in os.listdir("static/male") if f.lower().endswith((".png", ".jpg"))]
female_shirts = [f"female/{f}" for f in os.listdir("static/female") if f.lower().endswith((".png", ".jpg"))]

# --- Smoothing variables for stable overlay ---
prev_cx, prev_cy, prev_w, prev_h = 0, 0, 0, 0
smoothing = 0.2  # smaller = smoother

# --- Size and confidence tracking ---
size_recommendation = "N/A"
confidence_score = 0.0
current_gender = "male"
current_shirt_index = 1

# --- Functions ---

def calculate_size_recommendation(shoulder_dist):
    """
    Calculate size recommendation based on shoulder distance in pixels.
    Caps the size at XL maximum.
    """
    shoulder_dist = max(0, min(shoulder_dist, 140))  # Clamp to max 140 pixels
    if shoulder_dist < 80:
        return "XS"
    elif shoulder_dist < 100:
        return "S"
    elif shoulder_dist < 120:
        return "M"
    elif shoulder_dist < 140:
        return "L"
    else:
        return "XL"  # Max size

def calculate_confidence_score(lmList, shoulder_dist):
    if not lmList or len(lmList) < 25:
        return 0.0

    key_landmarks = [11, 12, 23, 24]  # shoulders and hips
    visible_count = 0

    for idx in key_landmarks:
        if idx < len(lmList) and len(lmList[idx]) >= 3:
            # Check if landmark has visibility/confidence
            if len(lmList[idx]) > 3 and lmList[idx][3] > 0.5:
                visible_count += 1
            elif len(lmList[idx]) == 3:
                visible_count += 1

    visibility_score = visible_count / len(key_landmarks)
    shoulder_stability = min(1.0, shoulder_dist / 150.0) if shoulder_dist > 0 else 0.0

    confidence = (visibility_score * 0.7 + shoulder_stability * 0.3) * 100
    return min(100.0, confidence)

def draw_info_panel(img, size_rec, confidence, gender, shirt_index):
    h, w = img.shape[:2]

    panel_width = 280
    panel_height = 120
    panel_x = w - panel_width - 20
    panel_y = h - panel_height - 20

    overlay = img.copy()
    cv2.rectangle(overlay, (panel_x, panel_y), (panel_x + panel_width, panel_y + panel_height), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.7, img, 0.3, 0, img)

    cv2.rectangle(img, (panel_x, panel_y), (panel_x + panel_width, panel_y + panel_height), (255, 255, 255), 2)

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    thickness = 2

    title_text = f"{gender.upper()} SHIRT {shirt_index}"
    cv2.putText(img, title_text, (panel_x + 10, panel_y + 25), font, 0.5, (255, 255, 255), 1)

    # Ensure size_rec is valid
    if size_rec not in ["XS", "S", "M", "L", "XL"]:
        size_rec = "XL"

    size_text = f"Recommended Size: {size_rec}"
    cv2.putText(img, size_text, (panel_x + 10, panel_y + 50), font, font_scale, (0, 255, 0), thickness)

    conf_text = f"Accuracy: {confidence:.1f}%"
    if confidence >= 80:
        conf_color = (0, 255, 0)
    elif confidence >= 60:
        conf_color = (0, 255, 255)
    else:
        conf_color = (0, 0, 255)
    cv2.putText(img, conf_text, (panel_x + 10, panel_y + 75), font, font_scale, conf_color, thickness)

    bar_x = panel_x + 10
    bar_y = panel_y + 90
    bar_width = 200
    bar_height = 15
    cv2.rectangle(img, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (50, 50, 50), -1)

    fill_width = int((confidence / 100.0) * bar_width)
    cv2.rectangle(img, (bar_x, bar_y), (bar_x + fill_width, bar_y + bar_height), conf_color, -1)
    cv2.rectangle(img, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (255, 255, 255), 1)

    return img

def select_shirt(gender, index):
    global selected_shirt, current_gender, current_shirt_index
    if gender == "male":
        if 1 <= index <= len(male_shirts):
            selected_shirt = male_shirts[index - 1]
        else:
            raise ValueError("Invalid male shirt index")
    elif gender == "female":
        if 1 <= index <= len(female_shirts):
            selected_shirt = female_shirts[index - 1]
        else:
            raise ValueError("Invalid female shirt index")
    else:
        raise ValueError("Invalid gender")
    current_gender = gender
    current_shirt_index = index
    print(f"[INFO] Selected shirt: {selected_shirt}")

def process_frame():
    global selected_shirt, prev_cx, prev_cy, prev_w, prev_h, size_recommendation, confidence_score

    success, img = cap.read()
    if not success:
        return None

    img = detector.findPose(img, draw=False)
    lmList, _ = detector.findPosition(img, bboxWithHands=False, draw=False)

    if not lmList or len(lmList) < 25:
        size_recommendation = "N/A"
        confidence_score = 0.0
        return draw_info_panel(img, size_recommendation, confidence_score, current_gender, current_shirt_index)

    try:
        lm11, lm12 = lmList[11], lmList[12]
        lm23, lm24 = lmList[23], lmList[24]

        shoulderDist = math.hypot(lm12[0]-lm11[0], lm12[1]-lm11[1])
        confidence_score = calculate_confidence_score(lmList, shoulderDist)
        size_recommendation = calculate_size_recommendation(shoulderDist)

        if selected_shirt:
            w = int(shoulderDist * 1.6)
            h = int(w * shirtRatio)

            cx = (lm11[0]+lm12[0])//2
            cy = (lm11[1]+lm12[1])//2
            torso_y = (lm23[1]+lm24[1])//2
            cy_torso = (cy+torso_y)//2

            cx = int(prev_cx + (cx-prev_cx)*smoothing)
            cy_torso = int(prev_cy + (cy_torso-prev_cy)*smoothing)
            w = int(prev_w + (w-prev_w)*smoothing)
            h = int(prev_h + (h-prev_h)*smoothing)
            prev_cx, prev_cy, prev_w, prev_h = cx, cy_torso, w, h

            path = os.path.join("static", selected_shirt)
            if os.path.exists(path):
                imgShirt = cv2.imread(path, cv2.IMREAD_UNCHANGED)
                imgShirt = cv2.resize(imgShirt, (w, h))

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
        print(f"[WARN] Overlay skipped: {e}")

    img = draw_info_panel(img, size_recommendation, confidence_score, current_gender, current_shirt_index)
    return img

# --- Main Loop ---
if __name__ == "__main__":
    print("Starting Virtual Try-On Stream...")
    select_shirt("male", 1)

    import tkinter as tk
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    cv2.namedWindow("Virtual Try-On", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Virtual Try-On", screen_width, screen_height)
    cv2.moveWindow("Virtual Try-On", 0, 0)
    cv2.setWindowProperty("Virtual Try-On", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        frame = process_frame()
        if frame is None:
            break

        cv2.imshow("Virtual Try-On", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif key == ord('1'):
            select_shirt("male", 1)
        elif key == ord('2'):
            select_shirt("male", 2)
        elif key == ord('3'):
            select_shirt("female", 1)
        elif key == ord('4'):
            select_shirt("male", 3)
        elif key == ord('5'):
            select_shirt("female", 2)

    cap.release()
    cv2.destroyAllWindows()
