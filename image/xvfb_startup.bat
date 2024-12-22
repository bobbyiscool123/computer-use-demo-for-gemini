@echo off
setlocal
set DPI=96
set RES_AND_DEPTH=%WIDTH%x%HEIGHT%x24

REM Function to check if Xvfb is already running
:check_xvfb_running
    if exist /tmp/.X%DISPLAY_NUM%-lock (
        exit /b 0
    ) else (
        exit /b 1
    )

REM Function to check if Xvfb is ready
:wait_for_xvfb
    set timeout=10
    set start_time=
    for /f "tokens=*" %%a in ('powershell -command "(Get-Date).Ticks"') do set start_time=%%a
    
    :xvfb_loop
      powershell -command "Start-Sleep -Milliseconds 100"
      xdpyinfo >nul 2>&1
      if %errorlevel% equ 0 (
         exit /b 0
      )
      
      set current_time=
      for /f "tokens=*" %%a in ('powershell -command "(Get-Date).Ticks"') do set current_time=%%a
      set /a elapsed_seconds = (current_time - start_time) / 10000000
      if %elapsed_seconds% gtr %timeout% (
          echo Xvfb failed to start within %timeout% seconds
          exit /b 1
      )
      
    goto :xvfb_loop

REM Check if Xvfb is already running
call :check_xvfb_running
if %errorlevel% equ 0 (
    echo Xvfb is already running on display %DISPLAY%
    exit /b 0
)

REM Start Xvfb
start "" /b Xvfb %DISPLAY% -ac -screen 0 %RES_AND_DEPTH% -retro -dpi %DPI% -nolisten tcp -nolisten unix
set XVFB_PID=

REM Wait for Xvfb to start
call :wait_for_xvfb
if %errorlevel% equ 0 (
    echo Xvfb started successfully on display %DISPLAY%
    echo Xvfb PID: %XVFB_PID%
) else (
    echo Xvfb failed to start
    taskkill /im Xvfb.exe /f
    exit /b 1
)

endlocal