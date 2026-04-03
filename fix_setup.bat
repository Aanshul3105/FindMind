@echo off
echo ========================================
echo Fixing FinMind Setup
echo ========================================
echo.

echo Step 1: Removing old virtual environment...
if exist backend\venv (
    rmdir /s /q backend\venv
    echo ✓ Old venv removed
) else (
    echo No old venv found
)

echo.
echo Step 2: Creating new virtual environment...
cd backend
python -m venv venv
echo ✓ New venv created

echo.
echo Step 3: Activating virtual environment...
call venv\Scripts\activate

echo.
echo Step 4: Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Step 5: Installing required packages...
pip install fastapi uvicorn yfinance pandas python-dotenv requests

echo.
echo Step 6: Verifying installations...
python -c "import fastapi; print('✓ FastAPI installed')"
python -c "import yfinance; print('✓ yfinance installed')"
python -c "import pandas; print('✓ pandas installed')"

cd ..

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the backend:
echo   cd backend
echo   venv\Scripts\activate
echo   python main.py
echo.
echo Then in another terminal:
echo   cd frontend
echo   npm run dev
pause