@echo off
echo Starting Product Research Agent setup...

python -m venv venv
call venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt

python -m playwright install chromium

mkdir outputs
mkdir data

echo.
echo Setup complete!
echo.
echo Next steps:
echo   1. Add local-llm as submodule (see Phase 3)
echo   2. Activate environment: venv\Scripts\activate
echo   3. Start building!
pause