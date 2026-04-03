"""
FinMind Backend - Flask Version
No FastAPI required - runs with Flask
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
from datetime import datetime
import traceback

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def root():
    """Root endpoint"""
    return jsonify({
        "message": "FinMind API is running",
        "status": "online",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@app.route('/api/stocks/<ticker>')
def get_stock(ticker):
    """Get stock data from Yahoo Finance"""
    try:
        print(f"🔍 Fetching data for {ticker.upper()}...")
        
        # Get stock data
        stock = yf.Ticker(ticker.upper())
        hist = stock.history(period="1mo")
        
        if hist.empty:
            return jsonify({"error": f"No data found for {ticker.upper()}"})
        
        # Get current info
        info = stock.info
        
        # Calculate current price and change
        current_price = hist['Close'].iloc[-1]
        prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        price_change = ((current_price - prev_price) / prev_price) * 100
        
        # Get market cap
        market_cap = info.get('marketCap', 0)
        if market_cap:
            market_cap_billions = market_cap / 1e9
        else:
            market_cap_billions = 0
        
        # Prepare response
        result = {
            "ticker": ticker.upper(),
            "name": info.get('longName', ticker.upper()),
            "sector": info.get('sector', 'Unknown'),
            "current_price": round(float(current_price), 2),
            "change": round(float(price_change), 2),
            "volume": int(hist['Volume'].iloc[-1]),
            "market_cap": round(market_cap_billions, 2),
            "pe_ratio": info.get('trailingPE', 'N/A'),
            "high_52w": info.get('fiftyTwoWeekHigh', 0),
            "low_52w": info.get('fiftyTwoWeekLow', 0),
            "dates": [d.strftime('%Y-%m-%d') for d in hist.index[-20:].tolist()],
            "prices": [round(float(p), 2) for p in hist['Close'].iloc[-20:].tolist()]
        }
        
        print(f"✅ Successfully fetched {ticker.upper()} data")
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ Error fetching {ticker}: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)})

@app.route('/api/query', methods=['POST'])
def query():
    """Process a financial query"""
    try:
        data = request.get_json()
        question = data.get("question", "")
        print(f"🤔 Processing question: {question}")
        
        question_lower = question.lower()
        
        # Check for stock-related questions
        if "apple" in question_lower or "aapl" in question_lower:
            answer = """📊 Apple Inc. (AAPL) Analysis

Key Metrics:
• Current Price: $175.23
• Market Cap: $2.8 Trillion  
• P/E Ratio: 28.5
• 30-Day Change: +12.3%

💡 Insights:
Apple continues to show strong performance with growing services revenue. The company's ecosystem and brand loyalty provide competitive advantages.

⚠️ Risks:
• Supply chain dependencies
• Regulatory scrutiny in EU and US
• Slowing smartphone market growth

📈 Outlook:
Analysts remain bullish with an average price target of $190. Strong cash flow and share buybacks support shareholder value."""
        
        elif "microsoft" in question_lower or "msft" in question_lower:
            answer = """📊 Microsoft Corp. (MSFT) Analysis

Key Metrics:
• Current Price: $375.50
• Market Cap: $2.8 Trillion
• P/E Ratio: 32.1
• 30-Day Change: +15.2%

💡 Insights:
Microsoft's cloud business (Azure) continues to drive growth. AI integration across products and strong enterprise adoption are key catalysts.

⚠️ Risks:
• Competition from AWS and Google Cloud
• Enterprise spending slowdown
• Regulatory challenges

📈 Outlook:
Strong buy consensus with AI momentum expected to continue driving growth."""
        
        elif "tesla" in question_lower or "tsla" in question_lower:
            answer = """📊 Tesla Inc. (TSLA) Analysis

Key Metrics:
• Current Price: $245.50
• Market Cap: $780 Billion
• P/E Ratio: 65.2
• 30-Day Change: -5.3%

💡 Insights:
Tesla faces increasing competition in EV market. Production ramping and new model launches are key focus areas.

⚠️ Risks:
• Intense competition from traditional automakers
• Price wars affecting margins
• Leadership distractions

📈 Outlook:
Mixed analyst sentiment. Long-term EV adoption supports growth, but near-term challenges persist."""
        
        elif "nvidia" in question_lower or "nvda" in question_lower:
            answer = """📊 NVIDIA Corp. (NVDA) Analysis

Key Metrics:
• Current Price: $485.00
• Market Cap: $1.2 Trillion
• P/E Ratio: 65.8
• 30-Day Change: +25.3%

💡 Insights:
NVIDIA dominates AI chip market. Data center growth is exceptional. Strong demand for AI processors continues.

⚠️ Risks:
• Competition from AMD and custom chips
• Export restrictions to China
• Valuation concerns

📈 Outlook:
Very bullish on AI momentum. Strong growth expected in data center and automotive segments."""
        
        else:
            # Try to detect if it's about any other stock
            words = question_lower.split()
            possible_tickers = ['aapl', 'msft', 'googl', 'amzn', 'tsla', 'nvda', 'meta', 'jpm', 'v']
            detected_ticker = None
            
            for word in words:
                if word in possible_tickers:
                    detected_ticker = word.upper()
                    break
            
            if detected_ticker:
                try:
                    # Fetch real-time data for the detected ticker
                    stock = yf.Ticker(detected_ticker)
                    hist = stock.history(period="5d")
                    if not hist.empty:
                        current = hist['Close'].iloc[-1]
                        change = ((current - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2]) * 100 if len(hist) > 1 else 0
                        info = stock.info
                        answer = f"""📊 {info.get('longName', detected_ticker)} ({detected_ticker}) Analysis

Current Price: ${current:.2f}
Change: {change:+.2f}%
Market Cap: ${info.get('marketCap', 0)/1e9:.1f}B
P/E Ratio: {info.get('trailingPE', 'N/A')}

💡 Quick Analysis:
Looking for detailed analysis on {detected_ticker}? Ask me specific questions about its performance, fundamentals, or outlook!"""
                    else:
                        answer = f"I found {detected_ticker} but couldn't fetch real-time data. Please check the ticker symbol and try again."
                except Exception as e:
                    answer = f"I detected you're asking about {detected_ticker}, but I need more information to provide a detailed analysis."
            else:
                answer = f"""I received your question: "{question}"

I can help you with:
• Stock analysis (AAPL, MSFT, NVDA, TSLA)
• Market trends and outlook
• Financial metrics and ratios
• Investment insights

Try asking:
• "How is Apple performing?"
• "What's the outlook for Microsoft?"
• "Analyze Tesla's recent performance"
• "Should I invest in NVIDIA?" """
        
        print(f"✅ Generated answer")
        return jsonify({
            "question": question,
            "answer": answer,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Error processing query: {e}")
        traceback.print_exc()
        return jsonify({
            "question": question if 'question' in locals() else "Unknown",
            "answer": f"Sorry, I encountered an error: {str(e)}",
            "timestamp": datetime.now().isoformat()
        })

@app.route('/api/market-overview')
def market_overview():
    """Get market overview"""
    try:
        indices = {
            "S&P 500": "^GSPC",
            "NASDAQ": "^IXIC",
            "Dow Jones": "^DJI"
        }
        
        overview = {}
        for name, symbol in indices.items():
            try:
                stock = yf.Ticker(symbol)
                hist = stock.history(period="2d")
                if not hist.empty and len(hist) >= 2:
                    current = hist['Close'].iloc[-1]
                    prev = hist['Close'].iloc[-2]
                    change = ((current - prev) / prev) * 100
                    overview[name] = {
                        "value": round(current, 2),
                        "change": round(change, 2),
                        "high": round(hist['High'].iloc[-1], 2),
                        "low": round(hist['Low'].iloc[-1], 2)
                    }
            except:
                overview[name] = {"error": "Data unavailable"}
        
        return jsonify(overview)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Starting FinMind Backend (Flask)")
    print("=" * 50)
    print("📍 Server will run at: http://localhost:5000")
    print("🔍 Health Check: http://localhost:5000/api/health")
    print("📊 Test Stock: http://localhost:5000/api/stocks/AAPL")
    print("=" * 50)
    print("\nPress CTRL+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)