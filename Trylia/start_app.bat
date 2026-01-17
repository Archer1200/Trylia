@echo off
title Virtual Try-On Application Launcher
color 0A

echo ========================================
echo    Virtual Try-On Application Launcher
echo ========================================
echo.

:: Check if we're in the correct directory
if not exist "backend\api_server.py" (
    echo [ERROR] Backend API server not found! Please run this script from the ShirtTryOn root directory.
    echo Current directory: %CD%
    pause
    exit /b 1
)

if not exist "frontend\package.json" (
    echo [ERROR] Frontend files not found! Please run this script from the ShirtTryOn root directory.
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo [INFO] Starting Virtual Try-On Application...
echo.

:: Create log directory if it doesn't exist
if not exist "logs" mkdir logs

:: Start Backend API Service
echo [1/2] Starting Backend API Service...
echo =====================================
cd backend

:: Check if virtual environment exists
if not exist "mp_env\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found at backend\mp_env\Scripts\activate.bat
    echo Please ensure the virtual environment is properly set up.
    cd ..
    pause
    exit /b 1
)

:: Start backend API server in a new window
start "Virtual Try-On API Server" cmd /k "mp_env\Scripts\activate.bat && echo [INFO] Backend virtual environment activated && echo [INFO] Starting API server on http://localhost:5000 && echo [INFO] Try-on service will start when you click 'Try On' button && python api_server.py"

:: Wait a moment for backend API to initialize
timeout /t 3 /nobreak >nul

cd ..

:: Start Frontend Service
echo.
echo [2/2] Starting Frontend Service...
echo =====================================
cd frontend

:: Check if node_modules exists
if not exist "node_modules" (
    echo [WARNING] node_modules not found. Installing dependencies...
    echo This may take a few minutes...
    call npm install
    if errorlevel 1 (
        echo [ERROR] Failed to install frontend dependencies.
        echo Please ensure Node.js and npm are installed.
        cd ..
        pause
        exit /b 1
    )
)

:: Start frontend in a new window
start "Virtual Try-On Frontend" cmd /k "echo [INFO] Starting frontend service on http://localhost:3000 && npm start"

cd ..

:: Display completion message
echo.
echo ========================================
echo    Application Started Successfully!
echo ========================================
echo.
echo Services Status:
echo   API Server: http://localhost:5000
echo   Frontend:   http://localhost:3000
echo.
echo Two new command windows have opened:
echo   1. Backend API Server (Ready for try-on requests)
echo   2. Frontend Service (React Website)
echo.
echo Instructions:
echo   - Wait for both services to fully load
echo   - Frontend will automatically open in your browser
echo   - Click 'Try On' button on any shirt to start camera
echo   - Camera window will open only when you try on a shirt
echo   - To stop try-on: Press 'q' in camera window or click 'Stop'
echo.
echo How it works:
echo   1. Browse shirts in the catalog
echo   2. Click 'Try On' button on any shirt
echo   3. Camera window opens with virtual try-on
echo   4. Press 'q' to stop or click 'Stop' button
echo.
echo Troubleshooting:
echo   - If camera doesn't work, check camera permissions
echo   - If frontend doesn't load, wait a moment and refresh
echo   - Check the individual service windows for error messages
echo.

:: Optional: Open browser automatically after a delay
echo [INFO] Opening application in browser in 10 seconds...
echo Press any key to skip auto-open or wait...
timeout /t 10 /nobreak >nul
start http://localhost:3000

echo.
echo [INFO] Application launcher completed.
echo [INFO] Keep this window open to see the startup log.
echo [INFO] Press any key to exit this launcher window.
pause >nul