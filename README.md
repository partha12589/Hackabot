# 🤖Polo - AI Chatbot

An intelligent AI assistant powered by Ollama's Phi3 model with both voice and web interfaces.

## Features
- 💬 Web-based chat interface
- 🎤 Voice assistant (Python)
- 🤖 Powered by Ollama Phi3
- ⚡ Real-time streaming responses
- 📱 Responsive design

## Setup

### Prerequisites
- Python 3.8+
- Node.js 18+
- Ollama installed with phi3 model

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start API server
uvicorn api:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Voice Assistant
```bash
cd backend
python main.py
```

## Usage
1. Make sure Ollama is running: `ollama serve`
2. Start the backend API
3. Start the frontend
4. Visit http://localhost:5173
5. Start chatting!

## Tech Stack
- **Frontend**: React, Vite, TailwindCSS
- **Backend**: FastAPI, Python
- **AI**: Ollama (Phi3)
