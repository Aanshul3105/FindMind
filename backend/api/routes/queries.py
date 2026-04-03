"""Query API Routes"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid
import asyncio

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    user_id: Optional[str] = "anonymous"

class QueryResponse(BaseModel):
    query_id: str
    question: str
    answer: Optional[str] = None
    status: str
    created_at: datetime

# Store queries in memory (replace with database in production)
queries_store = {}

@router.post("/", response_model=QueryResponse)
async def create_query(request: QueryRequest, background_tasks: BackgroundTasks):
    """Create and process a new query"""
    query_id = str(uuid.uuid4())
    
    query_data = {
        "query_id": query_id,
        "question": request.question,
        "user_id": request.user_id,
        "status": "processing",
        "created_at": datetime.now()
    }
    
    queries_store[query_id] = query_data
    
    # Process in background
    background_tasks.add_task(process_query, query_id, request.question)
    
    return QueryResponse(**query_data)

@router.get("/{query_id}")
async def get_query(query_id: str):
    """Get query status and result"""
    if query_id not in queries_store:
        raise HTTPException(status_code=404, detail="Query not found")
    
    return queries_store[query_id]

async def process_query(query_id: str, question: str):
    """Process query in background"""
    try:
        # Simulate processing
        await asyncio.sleep(2)
        
        # Simple response logic
        if "apple" in question.lower() or "aapl" in question.lower():
            answer = """Based on recent data, Apple (AAPL) is showing strong performance:
- Current Price: $175.23
- Market Cap: $2.8T
- P/E Ratio: 28.5
- Recent Trend: Up 12% over 3 months

The company continues to show strong fundamentals with growing services revenue and strong iPhone sales."""
        elif "microsoft" in question.lower() or "msft" in question.lower():
            answer = """Microsoft (MSFT) continues to perform well:
- Current Price: $375.50
- Market Cap: $2.8T
- P/E Ratio: 32.1
- Recent Trend: Up 15% over 3 months

Strong cloud growth and AI initiatives are driving momentum."""
        else:
            answer = f"""Analysis for your question: "{question}"

I've analyzed available data. Here are key insights:
- Market data shows positive momentum
- Technical indicators suggest stable growth
- Consider diversifying across sectors for balanced exposure

Would you like more specific details?"""
        
        # Update query store
        queries_store[query_id]["status"] = "completed"
        queries_store[query_id]["answer"] = answer
        queries_store[query_id]["completed_at"] = datetime.now()
        
    except Exception as e:
        queries_store[query_id]["status"] = "failed"
        queries_store[query_id]["error"] = str(e)