@echo off
echo Starting College Connect Server...
cd /d "%~dp0"
python manage.py runserver
pause
