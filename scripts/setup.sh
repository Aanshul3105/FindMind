#!/bin/bash

echo "🚀 Setting up FinMind Project..."
echo "=================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.11+"
    exit 1
fi

# Check Node
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+"
    exit 1
fi

# Setup Backend
echo ""
echo "📦 Setting up Backend..."
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Initialize database
python scripts/init_db.py

cd ..

# Setup Frontend
echo ""
echo "🎨 Setting up Frontend..."
cd frontend

# Install dependencies
npm install

cd ..

# Create .env file
cat > backend/.env << 'EOF'
DATABASE_URL=sqlite:///finmind.db
CHROMA_PATH=./chroma_store
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_EMBED_MODEL=nomic-embed-text
OLLAMA_LLM_MODEL=llama3
SEC_USER_AGENT=finmind@example.com
TRACKED_TICKERS=AAPL,MSFT,GOOGL,NVDA,TSLA
EOF

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo "1. Open VS Code: code ."
echo "2. Press F5 to start debugging"
echo "3. Or run manually:"
echo "   - Backend: cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "   - Frontend: cd frontend && npm run dev"
echo ""
echo "Open http://localhost:3000 in your browser"