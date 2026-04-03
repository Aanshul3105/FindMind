"""Stock API Routes"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/{ticker}")
async def get_stock(ticker: str, period: str = Query("1mo", regex="^(1d|5d|1mo|3mo|6mo|1y)$")):
    """Get stock data"""
    try:
        stock = yf.Ticker(ticker.upper())
        hist = stock.history(period=period)
        
        if hist.empty:
            raise HTTPException(status_code=404, detail="Stock not found")
        
        info = stock.info
        
        # Calculate metrics
        current_price = hist['Close'].iloc[-1]
        prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        price_change = ((current_price - prev_price) / prev_price) * 100
        
        return {
            "ticker": ticker.upper(),
            "name": info.get('longName', ticker),
            "sector": info.get('sector', 'Unknown'),
            "current_price": round(current_price, 2),
            "price_change": round(price_change, 2),
            "volume": int(hist['Volume'].iloc[-1]),
            "market_cap": info.get('marketCap', 0),
            "pe_ratio": info.get('trailingPE', 'N/A'),
            "chart_data": {
                "dates": hist.index.strftime('%Y-%m-%d').tolist(),
                "prices": hist['Close'].tolist(),
                "volume": hist['Volume'].tolist()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{ticker}/history")
async def get_stock_history(
    ticker: str,
    days: int = Query(30, ge=1, le=365)
):
    """Get historical stock data"""
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        stock = yf.Ticker(ticker.upper())
        hist = stock.history(start=start_date, end=end_date)
        
        if hist.empty:
            raise HTTPException(status_code=404, detail="No data found")
        
        return {
            "ticker": ticker.upper(),
            "data": [
                {
                    "date": idx.strftime('%Y-%m-%d'),
                    "open": row['Open'],
                    "high": row['High'],
                    "low": row['Low'],
                    "close": row['Close'],
                    "volume": row['Volume']
                }
                for idx, row in hist.iterrows()
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/compare")
async def compare_stocks(tickers: list[str], period: str = "1mo"):
    """Compare multiple stocks"""
    try:
        results = {}
        for ticker in tickers:
            stock = yf.Ticker(ticker.upper())
            hist = stock.history(period=period)
            
            if not hist.empty:
                results[ticker] = {
                    "price": round(hist['Close'].iloc[-1], 2),
                    "change": round(((hist['Close'].iloc[-1] - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2]) * 100, 2) if len(hist) > 1 else 0,
                    "volume": int(hist['Volume'].iloc[-1]),
                    "data": hist['Close'].tolist()
                }
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))