@echo off
echo starting mutter
set XDG_SESSION_TYPE=x11
mutter --replace --sm-disable 2> /tmp/mutter_stderr.log

timeout /t 30 /nobreak > nul
:mutter_loop
    xdotool search --class "mutter" >nul 2>&1
    if %errorlevel% equ 0 (
       goto :mutter_ready
    )
    timeout /t 1 /nobreak > nul
    
goto :mutter_loop
:mutter_ready

if exist /tmp/mutter_stderr.log (
    echo mutter stderr output:
    type /tmp/mutter_stderr.log
)
del /f /q /tmp/mutter_stderr.log