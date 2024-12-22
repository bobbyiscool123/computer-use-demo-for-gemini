@echo off

set DISPLAY=:%DISPLAY_NUM%
call xvfb_startup.bat
call tint2_startup.bat
call mutter_startup.bat
call x11vnc_startup.bat