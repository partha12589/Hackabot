# api.py
# Finance-Specific Chatbot Backend with Ollama

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama
import uuid
import re
from sse_starlette.sse import EventSourceResponse
from typing import List, Dict, Optional
from finance_utils import FinanceQueryValidator
from investment_data import (
    MUTUAL_FUNDS, STOCKS, DEBT_INSTRUMENTS, 
    RISK_ALLOCATIONS, get_investment_recommendations
)


def clean_text(text: str) -> str:
    """
    Clean text from AI model output to fix spacing issues
    """
    if not text:
        return text
    
    # Fix spaced numbers: "1 2 3" -> "123", "5 0 0 , 0 0 0" -> "500,000"
    text = re.sub(r'(\d)\s+(\d)', r'\1\2', text)
    
    # Fix spaced punctuation: " , " -> ",", " . " -> "."
    text = re.sub(r'\s+,\s+', ',', text)
    text = re.sub(r'(\d)\s+\.', r'\1.', text)
    
    # Fix common abbreviations with spaces
    abbreviations = {
        r'\bE\s*L\s*S\s*S\b': 'ELSS',
        r'\bP\s*P\s*F\b': 'PPF',
        r'\bN\s*S\s*C\b': 'NSC',
        r'\bS\s*S\s*Y\b': 'SSY',
        r'\bK\s*V\s*P\b': 'KVP',
        r'\bS\s*C\s*S\s*S\b': 'SCSS',
        r'\bH\s*D\s*F\s*C\b': 'HDFC',
        r'\bI\s*C\s*I\s*C\s*I\b': 'ICICI',
        r'\bT\s*C\s*S\b': 'TCS',
        r'\bS\s*B\s*I\b': 'SBI',
        r'\bN\s*S\s*E\b': 'NSE',
        r'\bB\s*S\s*E\b': 'BSE',
        r'\bE\s*M\s*I\b': 'EMI',
        r'\bS\s*I\s*P\b': 'SIP',
        r'\bS\s*E\s*B\s*I\b': 'SEBI',
        r'\bN\s*P\s*S\b': 'NPS',
        r'\bI\s*T\s*R\b': 'ITR',
        r'\bG\s*S\s*T\b': 'GST',
        r'\bT\s*D\s*S\b': 'TDS',
        r'\bP\s*F\b': 'PF',
        r'\bE\s*P\s*F\b': 'EPF',
        r'\bE\s*T\s*F\b': 'ETF',
        r'\bR\s*O\s*I\b': 'ROI',
    }
    
    for pattern, replacement in abbreviations.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    # Fix currency spacing: "? 5" -> "?5", "Rs . " -> "Rs."
    text = re.sub(r'?\s+', '?', text)
    text = re.sub(r'Rs\s*\.\s*', 'Rs.', text)
    
    # Fix percentage spacing: "1 5 %" -> "15%"
    text = re.sub(r'(\d+)\s*%', r'\1%', text)
    
    # Fix section references: "Section 8 0 C" -> "Section 80C"
    text = re.sub(r'Section\s+(\d)\s+(\d)\s+([A-Z])', r'Section \1\2\3', text)
    
    # Fix year ranges: "2 0 2 3 - 2 4" -> "2023-24"
    text = re.sub(r'(\d)\s+(\d)\s+(\d)\s+(\d)\s*-\s*(\d)\s+(\d)', r'\1\2\3\4-\5\6', text)
    
    # Fix common words that get spaced
    text = re.sub(r'\bH\s*istor\s*ically\b', 'Historically', text, flags=re.IGNORECASE)
    text = re.sub(r'\bModer\s*ately\b', 'Moderately', text, flags=re.IGNORECASE)
    text = re.sub(r'\bBenef\s*icial\b', 'Beneficial', text, flags=re.IGNORECASE)
    
    return text

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

CRITICAL FORMATTING RULES - FOLLOW STRICTLY:
1. Write numbers without spaces: "1.5" NOT "1 . 5", "500,000" NOT "5 0 0 , 0 0 0"
2. Write abbreviations without spaces: "ELSS" NOT "E L S S", "HDFC" NOT "H D F C"
3. Write percentages without spaces: "15%" NOT "1 5 %"
4. Write currency properly: "?1.5 lakh" NOT "? 1 . 5 lakh"
5. Write years properly: "2023-24" NOT "2 0 2 3 - 2 4"
6. Use proper markdown: **bold** for emphasis
7. Use proper spacing between words

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
                if content:
                    # Clean text to fix spacing issues from AI model
                    cleaned_content = clean_text(content)
                    full_response += cleaned_content
                    yield {"data": cleaned_content}
            
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
