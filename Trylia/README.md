<<<<<<< HEAD
# Virtual Try-On System

A full-stack virtual try-on application that allows users to try on shirts virtually using computer vision and pose detection.

## Features

- **Frontend**: React-based e-commerce website with shirt catalog
- **Backend**: Flask API server with computer vision integration
- **Real-time Try-On**: Live camera feed with shirt overlay using MediaPipe pose detection
- **Multiple Shirts**: Support for male and female shirt collections
- **Easy Integration**: Click "Try On" button to automatically start the camera application

## Project Structure

```
ShirtTryOn/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/          # Page components
│   │   └── styles/         # CSS styles
│   └── package.json
├── backend/                 # Flask backend server
│   ├── static/             # Shirt images
│   │   ├── male/           # Male shirt images (shirt1.png - shirt7.png)
│   │   └── female/         # Female shirt images (shirt1.png - shirt5.png)
│   ├── app.py              # Flask API server
│   ├── tryon_service.py    # Computer vision try-on logic
│   ├── start_backend.py    # Backend startup script
│   └── requirements.txt    # Python dependencies
└── README.md
```

## Prerequisites

### System Requirements
- **Python 3.8+** (for backend)
- **Node.js 16+** (for frontend)
- **Webcam** (for virtual try-on)
- **Windows/macOS/Linux**

### Python Dependencies
- Flask
- Flask-CORS
- OpenCV (cv2)
- CVZone
- MediaPipe

### Node.js Dependencies
- React
- React Router DOM

## Setup Instructions

### 1. Clone/Download the Project
```bash
cd ShirtTryOn
```

### Backend Setup

#### Option A: Using the improved backend (Recommended)
```bash
cd backend
python start_improved_backend.py
```

#### Option B: Using the original startup script
```bash
cd backend
python start_backend.py
```

#### Option C: Manual setup
```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start the Flask server
python app_improved.py
```

The backend server will start on `http://localhost:5000`

### 3. Frontend Setup

Open a new terminal window:

```bash
cd frontend

# Install Node.js dependencies
npm install

# Start the React development server
npm start
```

The frontend will start on `http://localhost:3000`

## Usage

1. **Start the Backend**: Run the backend server first (see setup instructions above)
2. **Start the Frontend**: Run the frontend development server
3. **Open the Website**: Navigate to `http://localhost:3000` in your browser
4. **Browse Catalog**: Click on "Catalog" to view available shirts
5. **Try On Shirts**: Click the "Try On" button on any shirt card
6. **Camera Window**: A camera window will open showing the live try-on
7. **Stop Try-On**: Press 'q' in the camera window or click the "Stop" button on the website

## API Endpoints

The backend provides the following REST API endpoints:

- `POST /api/try-on` - Start virtual try-on for a specific shirt
- `POST /api/stop` - Stop the current virtual try-on session
- `GET /api/status` - Check if try-on service is running
- `GET /api/test-camera` - Test camera access
- `GET /api/debug` - Get debug information
- `GET /health` - Health check endpoint

### Example API Usage

```javascript
// Start try-on for shirt ID 1 (male shirt 1)
fetch('http://localhost:5000/api/try-on', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ shirtId: 1 })
});

// Stop current try-on session
fetch('http://localhost:5000/api/stop', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' }
});
```

## Shirt ID Mapping

- **Male Shirts**: IDs 1-7 (maps to `static/male/shirt1.png` - `static/male/shirt7.png`)
- **Female Shirts**: IDs 101-105 (maps to `static/female/shirt1.png` - `static/female/shirt5.png`)

## Troubleshooting

### Quick Diagnosis

If the camera is not opening, run these diagnostic tests:

```bash
# Test camera access
cd backend
python test_camera.py

# Test full system flow
python test_full_flow.py
```

### Common Issues

1. **Camera not opening**
   - **Most Common**: Camera permissions not granted
   - **Solution**: Check system camera permissions
   - **Windows**: Settings > Privacy & Security > Camera
   - **macOS**: System Preferences > Security & Privacy > Camera
   - **Linux**: Add user to video group: `sudo usermod -a -G video $USER`

2. **"Backend server not running" error**
   - Make sure the Flask server is running on port 5000
   - Try the improved backend: `python start_improved_backend.py`
   - Check if any firewall is blocking the connection

3. **Camera already in use**
   - Close other applications using the camera (Zoom, Skype, etc.)
   - Restart your computer to release camera locks

4. **Shirt images not loading**
   - Verify that shirt images exist in `backend/static/male/` and `backend/static/female/`
   - Ensure images are named correctly (shirt1.png, shirt2.png, etc.)

5. **Python package errors**
   - Install missing packages: `pip install -r backend/requirements.txt`
   - Use a virtual environment if needed

6. **Node.js errors**
   - Delete `node_modules` and run `npm install` again
   - Ensure Node.js version is 16 or higher

### Detailed Troubleshooting

For comprehensive troubleshooting steps, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### Performance Tips

- **Camera Quality**: Use a good quality webcam for better pose detection
- **Lighting**: Ensure good lighting for optimal pose detection
- **Background**: Use a plain background for better results
- **Distance**: Stand at an appropriate distance from the camera

## Development

### Adding New Shirts

1. Add shirt images to the appropriate directory:
   - Male shirts: `backend/static/male/shirtN.png`
   - Female shirts: `backend/static/female/shirtN.png`

2. Update the frontend catalog in `frontend/src/pages/Catalog.js`:
   - Increase the array length for the respective gender
   - Update the ID mapping if needed

### Customizing the Try-On Logic

The computer vision logic is in `backend/tryon_service.py`. You can modify:
- Shirt positioning and sizing
- Pose detection parameters
- Smoothing algorithms
- Rotation and scaling logic

## Technical Details

### Frontend Architecture
- **React 18** with functional components and hooks
- **React Router** for navigation
- **CSS3** for styling with responsive design
- **Fetch API** for backend communication

### Backend Architecture
- **Flask** web framework with CORS support
- **OpenCV** for computer vision operations
- **MediaPipe** for pose detection
- **CVZone** for simplified pose processing
- **Threading** for concurrent request handling

### Computer Vision Pipeline
1. **Camera Capture**: Real-time video feed from webcam
2. **Pose Detection**: MediaPipe identifies body landmarks
3. **Shirt Positioning**: Calculate shirt position based on shoulder and torso landmarks
4. **Image Processing**: Resize, rotate, and overlay shirt image
5. **Smoothing**: Apply smoothing algorithms for stable overlay
6. **Display**: Show the final result with shirt overlay

## License

This project is for educational and demonstration purposes.

## Contributing

Feel free to submit issues and enhancement requests!

## Support

If you encounter any issues, please check the troubleshooting section or create an issue with detailed information about your setup and the problem you're experiencing.
=======
# Trylia
A Virtual Dressing Room
>>>>>>> 43822f64c05384ed96318366b6fb1ca921fecf0e
