@echo off
echo starting noVNC

REM Start noVNC with explicit websocket settings
start /b /wait  python /opt/noVNC/utils/novnc_proxy  ^
    --vnc localhost:5900 ^
    --listen 6080 ^
    --web /opt/noVNC ^
    > /tmp/novnc.log 2>&1

REM Wait for noVNC to start
timeout /t 10 /nobreak > nul

:novnc_loop
netstat -tuln | findstr ":6080 " >nul 2>&1
if %errorlevel% equ 0 (
    goto :novnc_ready
)
timeout /t 1 /nobreak > nul
goto :novnc_loop

:novnc_ready
echo noVNC started successfully