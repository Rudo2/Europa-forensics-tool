@echo off
REM Setup script for Windows: create venv and install dependencies
python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
echo Setup complete. Activate the environment with:
	echo call venv\Scripts\activate
pause
