@echo off
echo starting tint2 on display %DISPLAY% ...

start tint2 -c %USERPROFILE%\.config\tint2\tint2rc 2> /tmp/tint2_stderr.log

timeout /t 30 /nobreak > nul

:tint2_loop
xdotool search --class "tint2" >nul 2>&1
if %errorlevel% equ 0 (
  goto :tint2_ready
)
timeout /t 1 /nobreak > nul
goto :tint2_loop

:tint2_ready

if exist /tmp/tint2_stderr.log (
    echo tint2 stderr output:
    type /tmp/tint2_stderr.log
)
del /f /q /tmp/tint2_stderr.log