@echo off
call start_all.bat
call novnc_startup.bat

start python http_server.py > /tmp/server_logs.txt 2>&1
set STREAMLIT_SERVER_PORT=8501
start python -m streamlit run computer_use_demo/tools/streamlit.py > /tmp/streamlit_stdout.log

echo ✨ Computer Use Demo is ready!
echo Open http://localhost:8080 in your browser to begin

pause