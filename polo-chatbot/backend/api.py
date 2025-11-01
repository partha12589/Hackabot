# api.py
# Finance-Specific Chatbot Backend with Ollama

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama
import uuid
from sse_starlette.sse import EventSourceResponse
from typing import List, Dict, Optional
from finance_utils import FinanceQueryValidator
from investment_data import (
    MUTUAL_FUNDS, STOCKS, DEBT_INSTRUMENTS, 
    RISK_ALLOCATIONS, get_investment_recommendations
)
from market_data import MarketDataService

app = FastAPI(title="FinanceGPT API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active chats with conversation history and user profiles (in-memory)
chats: Dict[str, List[Dict]] = {}
user_profiles: Dict[str, Dict] = {}  # Store user profiles per chat

# Finance-specific system prompt - Portfolio Advisor Edition
def get_portfolio_prompt(user_profile=None):
    base_prompt = """You are FinanceGPT, an AI Portfolio Advisor specializing in Indian investments.

YOUR PRIMARY ROLE: Generate personalized investment portfolios for Indian investors based on their:
- Capital amount
- Monthly SIP investment
- Risk appetite (Low/Medium/High)
- Investment preferences (Mutual Funds, Stocks, Bonds, Debt Funds)

EXPERTISE AREAS:
- Indian Mutual Funds (HDFC, Axis, ICICI, Mirae Asset, etc.)
- NSE/BSE Listed Stocks (Reliance, TCS, HDFC Bank, etc.)
- Debt Instruments (FDs, PPF, NSC, Bonds)
- Tax-saving investments (ELSS, PPF, NPS)
- SIP planning and wealth creation

CRITICAL FORMATTING RULES:
1. ALWAYS use NORMAL spacing between words
2. Write naturally: "Based on your profile" NOT "Basedonyourprofile"
3. Use proper markdown with ** for bold text
4. Include spaces after punctuation

RESPONSE GUIDELINES:
1. Be SPECIFIC - recommend actual mutual funds and stocks available in India
2. Provide DIVERSIFICATION - spread across asset classes
3. Match RISK PROFILE - conservative for low risk, aggressive for high risk
4. Show ALLOCATION - give percentage breakdown
5. Estimate RETURNS - provide realistic return expectations
6. Be CONCISE - clear and actionable advice

PORTFOLIO STRUCTURE:
When generating a portfolio, always include:
- Asset allocation percentages
- Specific fund/stock names with brief reasoning
- Expected returns range
- Risk assessment
- Disclaimer to consult SEBI-registered advisor

"""
    
    if user_profile:
        profile_context = f"""
CURRENT USER PROFILE:
- Capital: ?{user_profile.get('capital', 'Not specified')}
- Monthly SIP: ?{user_profile.get('monthly_sip', 'Not specified')}
- Risk Appetite: {user_profile.get('risk_appetite', 'Not specified')}
- Preferred Investments: {', '.join(user_profile.get('preferences', ['Not specified']))}

Generate a customized portfolio for this user.
"""
        return base_prompt + profile_context
    
    return base_prompt


class UserProfile(BaseModel):
    capital: float
    monthly_sip: float
    risk_appetite: str  # low, medium, high
    preferences: List[str]  # mutual_funds, stocks, bonds, debt_funds


class ChatMessage(BaseModel):
    message: str
    user_profile: Optional[UserProfile] = None


class ChatResponse(BaseModel):
    id: str
    message: str


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "service": "FinanceGPT API",
        "version": "1.0.0",
        "status": "active",
        "description": "Finance-specific chatbot powered by Ollama"
    }


@app.post("/chats")
async def create_chat():
    """Create a new chat session"""
    chat_id = str(uuid.uuid4())
    chats[chat_id] = []
    user_profiles[chat_id] = None
    return {"id": chat_id, "message": "Chat session created successfully"}


@app.get("/chats/{chat_id}/history")
async def get_chat_history(chat_id: str):
    """Get conversation history for a chat"""
    if chat_id not in chats:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return {"chat_id": chat_id, "history": chats[chat_id]}


@app.post("/chats/{chat_id}")
async def send_message(chat_id: str, message: ChatMessage):
    """
    Send a message and get streaming response
    Only accepts finance-related queries
    """
    
    # Validate chat session exists
    if chat_id not in chats:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    # Store user profile if provided
    if message.user_profile:
        user_profiles[chat_id] = {
            "capital": message.user_profile.capital,
            "monthly_sip": message.user_profile.monthly_sip,
            "risk_appetite": message.user_profile.risk_appetite,
            "preferences": message.user_profile.preferences
        }
    
    # Validate that query is finance-related
    is_finance, category = FinanceQueryValidator.is_finance_query(message.message)
    
    if not is_finance:
        # Return error for non-finance queries
        rejection_msg = FinanceQueryValidator.get_rejection_message()
        raise HTTPException(
            status_code=400, 
            detail={
                "error": "non_finance_query",
                "message": rejection_msg
            }
        )
    
    # Add user message to history
    chats[chat_id].append({
        "role": "user",
        "content": message.message,
        "category": category
    })
    
    async def event_generator():
        try:
            # Get user profile for this chat
            profile = user_profiles.get(chat_id)
            
            # Build conversation context with user profile
            system_prompt = get_portfolio_prompt(profile)
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add conversation history (last 5 exchanges to keep context manageable)
            history_to_include = chats[chat_id][-10:]  # Last 10 messages (5 exchanges)
            for msg in history_to_include:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            # Stream response from Ollama using Qwen 2.5
            full_response = ""
            stream = ollama.chat(
                model='qwen2.5:7b',
                messages=messages,
                stream=True,
                options={
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "top_k": 40,
                    "num_predict": 1000,
                    "repeat_penalty": 1.0,
                }
            )
            
            for chunk in stream:
                content = chunk['message']['content']
                # Skip empty chunks
                if content and content.strip():
                    full_response += content
                    yield {"data": content}
            
            # Store assistant response in history
            chats[chat_id].append({
                "role": "assistant",
                "content": full_response
            })
                
        except Exception as e:
            error_message = f"Error: {str(e)}"
            yield {"data": error_message}
    
    return EventSourceResponse(event_generator())


@app.delete("/chats/{chat_id}")
async def delete_chat(chat_id: str):
    """Delete a chat session"""
    if chat_id not in chats:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    del chats[chat_id]
    return {"message": "Chat session deleted successfully"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "model": "qwen2.5:7b",
        "service": "FinanceGPT Portfolio Advisor",
        "active_chats": len(chats)
    }


@app.get("/investment-options")
async def get_investment_options():
    """Get available investment options for reference"""
    return {
        "mutual_funds": {
            "large_cap": [fund["name"] for fund in MUTUAL_FUNDS["large_cap"][:3]],
            "mid_cap": [fund["name"] for fund in MUTUAL_FUNDS["mid_cap"][:2]],
            "debt": [fund["name"] for fund in MUTUAL_FUNDS["debt"][:2]]
        },
        "stocks": {
            "blue_chip": [stock["name"] for stock in STOCKS["blue_chip"][:5]]
        },
        "risk_allocations": RISK_ALLOCATIONS
    }


@app.get("/sample-queries")
async def get_sample_queries():
    """Get sample finance queries for UI"""
    return {
        "queries": FinanceQueryValidator.get_sample_queries()
    }


# ============= LIVE MARKET DATA API ENDPOINTS =============

@app.get("/market/stock/{symbol}")
async def get_stock_price(symbol: str):
    """
    Get real-time stock price from NSE
    Example: /market/stock/TCS
    """
    data = MarketDataService.get_stock_price(symbol)
    if not data:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")
    return data


@app.get("/market/mutual-fund/{scheme_code}")
async def get_mutual_fund_nav(scheme_code: str):
    """
    Get mutual fund NAV from MFapi
    Example: /market/mutual-fund/119551
    """
    data = MarketDataService.get_mutual_fund_nav(scheme_code)
    if not data:
        raise HTTPException(status_code=404, detail=f"Fund {scheme_code} not found")
    return data


@app.get("/market/indices")
async def get_market_indices():
    """
    Get Nifty 50 and Sensex current values
    """
    return MarketDataService.get_market_indices()


@app.post("/market/portfolio-data")
async def get_portfolio_live_data(symbols: Dict[str, List[str]]):
    """
    Get all live data for a portfolio at once
    Request body: {"stocks": ["TCS", "INFY"], "mutual_funds": ["119551"]}
    """
    stocks = symbols.get("stocks", [])
    mutual_funds = symbols.get("mutual_funds", [])
    return MarketDataService.get_portfolio_live_data(stocks, mutual_funds)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)