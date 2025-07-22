@echo off
echo Starting AI Research Agent...
cd /d "%~dp0"
python -m streamlit run app.py
pause
