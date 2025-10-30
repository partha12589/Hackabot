from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama
import uuid
from sse_starlette.sse import EventSourceResponse

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active chats (in-memory for prototype)
chats = {}

class ChatMessage(BaseModel):
    message: str

@app.post("/chats")
async def create_chat():
    """Create a new chat session"""
    chat_id = str(uuid.uuid4())
    chats[chat_id] = []
    return {"id": chat_id}

@app.post("/chats/{chat_id}")
async def send_message(chat_id: str, message: ChatMessage):
    """Send a message and get streaming response"""
    
    async def event_generator():
        try:
            # Stream response from Ollama
            stream = ollama.chat(
                model='phi3',
                messages=[{'role': 'user', 'content': message.message}],
                stream=True,
            )
            
            for chunk in stream:
                content = chunk['message']['content']
                yield {"data": content}
                
        except Exception as e:
            yield {"data": f"Error: {str(e)}"}
    
    return EventSourceResponse(event_generator())

@app.get("/health")
async def health_check():
    return {"status": "ok", "model": "phi3"}