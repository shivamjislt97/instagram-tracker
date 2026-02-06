@echo off
cd /d "%~dp0"

echo Activating virtual environment...
call venv\Scripts\activate

echo Running bot...
python main.py

echo.
echo Bot finished. Press any key to close.
pause
