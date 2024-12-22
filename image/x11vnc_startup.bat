@echo off
echo starting vnc

start "" /b x11vnc -display %DISPLAY% ^
    -forever ^
    -shared ^
    -wait 50 ^
    -rfbport 5900 ^
    -nopw ^
    2> /tmp/x11vnc_stderr.log
set x11vnc_pid=

timeout /t 10 /nobreak > nul
:x11vnc_loop
netstat -tuln | findstr ":5900 " >nul 2>&1
if %errorlevel% equ 0 (
   goto :x11vnc_ready
)
timeout /t 1 /nobreak > nul
goto :x11vnc_loop

:x11vnc_ready
echo x11vnc started
> /tmp/x11vnc_stderr.log

:monitor_loop
    timeout /t 5 /nobreak > nul
    tasklist /fi "imagename eq x11vnc.exe" | find /i "x11vnc.exe" >nul 2>&1
    if %errorlevel% neq 0 (
         echo x11vnc process crashed, restarting...
         if exist /tmp/x11vnc_stderr.log (
              echo x11vnc stderr output:
              type /tmp/x11vnc_stderr.log
         )
         del /f /q /tmp/x11vnc_stderr.log
         call %0
         exit /b
    )
goto :monitor_loop