@echo off
echo 🚀 Fixing FinMind Setup...
echo ============================

echo.
echo 📦 Setting up Backend...
cd backend

REM Activate virtual environment
if not exist "venv" (
    python -m venv venv
)

call venv\Scripts\activate

REM Install packages
pip install fastapi uvicorn yfinance pandas python-dotenv

REM Initialize database
python scripts\init_db.py

cd ..

echo.
echo 🎨 Setting up Frontend...
cd frontend

REM Create package.json if missing
if not exist "package.json" (
    echo { > package.json
    echo   "name": "finmind-frontend", >> package.json
    echo   "version": "1.0.0", >> package.json
    echo   "private": true, >> package.json
    echo   "type": "module", >> package.json
    echo   "scripts": { >> package.json
    echo     "dev": "vite", >> package.json
    echo     "build": "vite build", >> package.json
    echo     "preview": "vite preview" >> package.json
    echo   }, >> package.json
    echo   "dependencies": { >> package.json
    echo     "react": "^18.2.0", >> package.json
    echo     "react-dom": "^18.2.0", >> package.json
    echo     "axios": "^1.6.2", >> package.json
    echo     "react-hot-toast": "^2.4.1" >> package.json
    echo   }, >> package.json
    echo   "devDependencies": { >> package.json
    echo     "@vitejs/plugin-react": "^4.2.0", >> package.json
    echo     "vite": "^5.0.0" >> package.json
    echo   } >> package.json
    echo } >> package.json
)

REM Install dependencies
call npm install

cd ..

echo.
echo ✅ Setup complete!
echo.
echo To start the application:
echo =========================
echo 1. Open TWO terminals
echo.
echo Terminal 1 (Backend):
echo   cd backend
echo   venv\Scripts\activate
echo   python main.py
echo.
echo Terminal 2 (Frontend):
echo   cd frontend
echo   npm run dev
echo.
echo Then open http://localhost:3000 in your browser@echo off
echo 🚀 Fixing FinMind Setup...
echo ============================

echo.
echo 📦 Setting up Backend...
cd backend

REM Activate virtual environment
if not exist "venv" (
    python -m venv venv
)

call venv\Scripts\activate

REM Install packages
pip install fastapi uvicorn yfinance pandas python-dotenv

REM Initialize database
python scripts\init_db.py

cd ..

echo.
echo 🎨 Setting up Frontend...
cd frontend

REM Create package.json if missing
if not exist "package.json" (
    echo { > package.json
    echo   "name": "finmind-frontend", >> package.json
    echo   "version": "1.0.0", >> package.json
    echo   "private": true, >> package.json
    echo   "type": "module", >> package.json
    echo   "scripts": { >> package.json
    echo     "dev": "vite", >> package.json
    echo     "build": "vite build", >> package.json
    echo     "preview": "vite preview" >> package.json
    echo   }, >> package.json
    echo   "dependencies": { >> package.json
    echo     "react": "^18.2.0", >> package.json
    echo     "react-dom": "^18.2.0", >> package.json
    echo     "axios": "^1.6.2", >> package.json
    echo     "react-hot-toast": "^2.4.1" >> package.json
    echo   }, >> package.json
    echo   "devDependencies": { >> package.json
    echo     "@vitejs/plugin-react": "^4.2.0", >> package.json
    echo     "vite": "^5.0.0" >> package.json
    echo   } >> package.json
    echo } >> package.json
)

REM Install dependencies
call npm install

cd ..

echo.
echo ✅ Setup complete!
echo.
echo To start the application:
echo =========================
echo 1. Open TWO terminals
echo.
echo Terminal 1 (Backend):
echo   cd backend
echo   venv\Scripts\activate
echo   python main.py
echo.
echo Terminal 2 (Frontend):
echo   cd frontend
echo   npm run dev
echo.
echo Then open http://localhost:3000 in your browser