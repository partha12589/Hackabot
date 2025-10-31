# api.py
# Finance-Specific Chatbot Backend with Ollama

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama
import uuid
from sse_starlette.sse import EventSourceResponse
from typing import List, Dict
from finance_utils import FinanceQueryValidator

app = FastAPI(title="FinanceGPT API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active chats with conversation history (in-memory)
chats: Dict[str, List[Dict]] = {}

# Finance-specific system prompt with structured response requirements
FINANCE_SYSTEM_PROMPT = """You are FinanceGPT, an expert financial advisor and assistant specializing in:
- Personal finance and budgeting
- Investment strategies (stocks, mutual funds, bonds, ETFs)
- Banking and loans (EMI calculations, interest rates, mortgages)
- Insurance and risk management
- Taxation and tax planning
- Retirement planning
- Cryptocurrency and digital assets
- Real estate finance

CRITICAL RESPONSE FORMAT RULES:
1. BE CONCISE - Keep responses SHORT and TO THE POINT (3-5 key points maximum)
2. Only provide detailed explanations if user explicitly asks for "more details" or "explain in detail"
3. Use bullet points (•) for main points - each on a NEW LINE with blank line before
4. Use numbered lists (1., 2., 3.) for sequential steps - each on a NEW LINE
5. Each point should be 1-2 sentences MAXIMUM
6. Include REAL-TIME examples with actual companies or products (e.g., "Vanguard S&P 500 ETF (VOO)", "HDFC Bank FD")
7. Include specific numbers, percentages, or ranges where applicable
8. Use clear section headers when covering multiple topics
9. ALWAYS add blank lines between sections for better readability
10. Default to CRISP bullet points - expand only if asked

EXAMPLE CONCISE RESPONSE (Note the blank lines between points):

**Retirement Planning:**

• **Tax-Efficient Accounts:** Roth IRA (tax-free growth) or 401(k) (employer match)

• **Diversified Portfolio:** 60% stocks, 30% bonds, 10% alternatives

• **Start Early:** Compounding makes a huge difference over 20-30 years

**Important:** Consult a certified financial advisor before making decisions.

---

ONLY if user asks for MORE DETAILS, then provide:

**Detailed Investment Strategy:**

• **Diversification Benefits:**
  - Reduces portfolio risk by 30-40%
  - Example: Mix of equity (60%), debt (30%), gold (10%)

• **Top Funds 2024:**
  1. Axis Bluechip - 12.5% returns
  2. Mirae Asset Large Cap - 14.2% returns
  3. HDFC Index Sensex - 11.8% returns

• **Key Points:**
  - Min investment: ₹500-5000
  - Exit load: 1% before 1 year
  - Tax: LTCG 10% above ₹1 lakh

REMEMBER: Default to CONCISE responses. Expand only when asked!

IMPORTANT GUIDELINES:
- Provide accurate, helpful financial information
- Always include relevant disclaimers for investment advice
- Be conservative and risk-aware in recommendations
- ONLY answer finance-related questions. Politely decline non-finance queries
- For Indian users, reference INR, Indian tax laws, and Indian financial instruments when relevant
- Use real company names, fund names, and products (e.g., "ICICI Prudential", "PPF (Public Provident Fund)", "NSE Nifty 50")

Remember: You are a financial education and information assistant, not a replacement for professional financial advice."""


class ChatMessage(BaseModel):
    message: str


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
            # Build conversation context
            messages = [{"role": "system", "content": FINANCE_SYSTEM_PROMPT}]
            
            # Add conversation history (last 5 exchanges to keep context manageable)
            history_to_include = chats[chat_id][-10:]  # Last 10 messages (5 exchanges)
            for msg in history_to_include:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            # Stream response from Ollama
            full_response = ""
            stream = ollama.chat(
                model='qwen2.5:7b',  # Using Qwen 2.5 for best structured finance responses
                messages=messages,
                stream=True,
                options={
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "top_k": 40,
                    "repeat_penalty": 1.1,
                    "num_predict": 500  # Limit response length for conciseness
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
        "service": "FinanceGPT",
        "active_chats": len(chats)
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