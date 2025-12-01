@echo off
echo Stopping existing server...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Administrator*" 2>nul
timeout /t 2 /nobreak >nul

echo Starting Amadeus API Server with UI...
cd /d C:\Coding\Web\backend
start "SkyPrice Server" cmd /k "C:\Coding\.venv\Scripts\python.exe test_server.py"

timeout /t 3 /nobreak >nul
echo.
echo ================================
echo Server starting...
echo Open: http://localhost:8000
echo ================================
echo.
pause
