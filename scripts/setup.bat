@echo off
echo 🚀 Setting up FinMind Project...
echo ==================================

echo.
echo 📦 Setting up Backend...
cd backend

python -m venv venv
call venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt

python scripts\init_db.py

cd ..

echo.
echo 🎨 Setting up Frontend...
cd frontend

call npm install

cd ..

echo.
echo ✅ Setup complete!
echo.
echo To start the application:
echo 1. Open VS Code: code .
echo 2. Press F5 to start debugging
echo 3. Open http://localhost:3000 in your browser