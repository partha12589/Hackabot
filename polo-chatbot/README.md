# 💼 CodeNCASH - AI Portfolio Advisor

**AI-Powered Investment Portfolio Generation for Indian Investors**

CodeNCASH is an intelligent portfolio advisor that generates personalized investment recommendations based on user's capital, risk appetite, and investment preferences. Built specifically for the Indian market with real mutual funds, NSE/BSE stocks, and debt instruments.

---

## 🎯 Features

### Core Features (Round 1 MVP)
- ✅ **Interactive Portfolio Generation** - AI creates customized portfolios based on user input
- ✅ **User Profile Collection** - Captures capital, monthly SIP, risk appetite, and preferences
- ✅ **Risk-Based Allocation** - Supports Low, Medium, and High risk profiles
- ✅ **Real Indian Investments** - Recommends actual mutual funds (HDFC, Axis, ICICI, Mirae Asset)
- ✅ **NSE/BSE Stocks** - Includes blue-chip stocks (Reliance, TCS, HDFC Bank, Infosys)
- ✅ **Debt Instruments** - FDs, PPF, NSC, Government bonds
- ✅ **Real-time Streaming** - AI generates responses in real-time
- ✅ **PDF Export** - One-click download of generated portfolio
- ✅ **Smart Text Formatting** - Intelligent parser handles formatting issues
- ✅ **Conversational Q&A** - Ask follow-up questions about recommendations
- ✅ **Stop Generation** - Ability to halt response mid-generation

### Visual Features
- 🎨 **Modern UI** - Beautiful dark theme with green accents
- 💚 **Highlighted Key Points** - Bold text with visual emphasis
- 📊 **Markdown Rendering** - Clean, formatted responses
- 🔄 **Responsive Design** - Works on desktop and mobile
- ⚡ **Smooth Animations** - Professional transitions and effects

---

## 🏗️ Tech Stack

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 19.1.1 | UI framework |
| **Vite** | 7.1.7 | Build tool & dev server |
| **TailwindCSS** | 3.4.1 | Styling framework |
| **React Markdown** | 10.1.0 | Markdown rendering |
| **KaTeX** | Latest | Math formula rendering |
| **jsPDF** | 2.5.2 | PDF generation |

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| **FastAPI** | Latest | Web framework |
| **Python** | 3.x | Backend language |
| **Ollama** | Latest | LLM runtime |
| **Qwen 2.5** | 7B | AI model |
| **Uvicorn** | Latest | ASGI server |
| **SSE Starlette** | Latest | Streaming responses |

### AI/ML
- **Model:** Qwen 2.5:7b (Local LLM via Ollama)
- **Context Window:** 4096 tokens
- **Response Length:** Up to 1000 tokens
- **Cost:** FREE (runs locally, no API costs!)

---

## 📋 Prerequisites

Before you begin, ensure you have:

1. **Node.js** (v16 or higher)
2. **Python** (3.8 or higher)
3. **Ollama** (for running the AI model)
4. **Git** (for cloning the repository)

---

## 🚀 Quick Start Guide

### Step 1: Install Ollama

**macOS/Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Download from [ollama.com/download](https://ollama.com/download)

### Step 2: Pull the AI Model

```bash
ollama pull qwen2.5:7b
```

*This downloads ~4.7GB. Takes 3-5 minutes depending on your internet speed.*

### Step 3: Clone the Repository

```bash
git clone <your-repo-url>
cd polo-chatbot
```

### Step 4: Setup Backend

```bash
cd backend
pip install -r requirements.txt
```

### Step 5: Setup Frontend

```bash
cd ../frontend
npm install
```

---

## 🎮 Running the Application

### Terminal 1: Start Backend

```bash
cd backend
uvicorn api:app --reload --port 8000
```

**Backend will run on:** http://localhost:8000

### Terminal 2: Start Frontend

```bash
cd frontend
npm run dev
```

**Frontend will run on:** http://localhost:5173

---

## 📖 How to Use

### 1. Fill the Profile Form
- **Capital Amount:** Your initial investment (e.g., ₹500,000)
- **Monthly SIP:** Regular monthly investment (e.g., ₹10,000)
- **Risk Appetite:** Choose Low, Medium, or High
- **Preferences:** Select investment types (Mutual Funds, Stocks, Bonds, Debt Funds)

### 2. Generate Portfolio
Click **"Generate My Portfolio 🚀"** and watch the AI create a personalized investment plan!

### 3. Download PDF
Click **"📄 Download Portfolio as PDF"** to save your portfolio

### 4. Ask Follow-up Questions
Continue chatting to ask questions like:
- "Why did you recommend HDFC Top 100 Fund?"
- "What are the tax implications?"
- "Can you explain the risk assessment?"

### 5. Start New Portfolio
Click **"← New Portfolio"** to create a different portfolio

---

## 🎯 Portfolio Features

### Risk-Based Allocation

**Low Risk (Conservative)**
- 60-70% Debt instruments (FDs, Bonds, Debt Funds)
- 20-30% Large-cap mutual funds
- 10% Gold/Liquid funds

**Medium Risk (Balanced)**
- 50% Equity mutual funds (Large + Mid cap)
- 25% Debt instruments
- 15% Fixed deposits
- 10% Direct stocks

**High Risk (Aggressive)**
- 60-70% Equity (Large, Mid, Small cap funds)
- 25% Direct stocks (NSE/BSE)
- 10% Hybrid funds

### Investment Database

**Mutual Funds (50+):**
- Large Cap: HDFC Top 100, Axis Bluechip, ICICI Prudential, Mirae Asset
- Mid Cap: Axis Midcap, Kotak Emerging, DSP Midcap
- Small Cap: Axis Small Cap, Nippon India Small Cap
- Debt: HDFC Corporate Bond, ICICI Prudential Debt, Axis Banking & PSU
- Hybrid: HDFC Balanced Advantage, ICICI Equity & Debt

**Stocks (Blue-chip):**
- Tech: TCS, Infosys, Tech Mahindra
- Banking: HDFC Bank, ICICI Bank, SBI
- Energy: Reliance Industries
- FMCG: ITC, Asian Paints
- Auto: Tata Motors, Bajaj Finance

**Debt Instruments:**
- Fixed Deposits (HDFC, ICICI, SBI)
- PPF (Public Provident Fund)
- NSC (National Savings Certificate)
- Government Bonds & Corporate Bonds

---

## 🏆 Key Differentiators

1. **Local AI (No API Costs)** - Runs entirely on your machine
2. **Real Indian Market Data** - Actual funds and stocks, not generic advice
3. **Risk-Adjusted Portfolios** - Tailored to user's risk appetite
4. **PDF Export** - Professional portfolio documents
5. **Interactive Chat** - Ask follow-up questions
6. **Modern UI** - Beautiful, responsive design
7. **Fast & Free** - No usage limits, no subscriptions

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Frontend (React)                  │
│  ┌──────────────────────────────────────────────┐   │
│  │ User Profile Form → Chat Interface → PDF Gen │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────┘
                      │ HTTP/SSE
┌─────────────────────▼───────────────────────────────┐
│                Backend (FastAPI)                     │
│  ┌──────────────────────────────────────────────┐   │
│  │ Profile Storage → AI Context → Stream Handler│   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────┘
                      │ Ollama API
┌─────────────────────▼───────────────────────────────┐
│              Ollama (Qwen 2.5:7b)                    │
│  ┌──────────────────────────────────────────────┐   │
│  │ Portfolio Generation + Financial Knowledge   │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## 🔧 Configuration

### Backend Configuration (`api.py`)

**Model Parameters:**
```python
{
    "temperature": 0.7,      # Creativity level
    "top_p": 0.9,            # Nucleus sampling
    "top_k": 40,             # Token selection
    "num_predict": 1000,     # Max response length
    "repeat_penalty": 1.0    # Repetition control
}
```

**Change Model:**
```python
# In api.py, line ~190
model='qwen2.5:7b'  # Change to 'llama3.1:8b' or other models
```

### Frontend Configuration

**API URL:** Update in `App.jsx` line ~86
```javascript
const API_URL = 'http://localhost:8000';
```

---

## 🐛 Troubleshooting

### Issue: "Connection Refused"
**Solution:** Ollama not running
```bash
# Start Ollama
ollama serve
```

### Issue: "Model not found"
**Solution:** Pull the model
```bash
ollama pull qwen2.5:7b
```

### Issue: Port already in use
**Solution:** Kill existing processes
```bash
# Kill backend
lsof -ti:8000 | xargs kill -9

# Kill frontend
lsof -ti:5173 | xargs kill -9
```

### Issue: Frontend shows blank
**Solution:** Check browser console for errors, restart frontend

### Issue: Formatting looks broken
**Solution:** Hard refresh browser (Ctrl+Shift+R)

---

## 📁 Project Structure

```
polo-chatbot/
├── backend/
│   ├── api.py                  # FastAPI routes & streaming
│   ├── finance_utils.py        # Query validation
│   ├── investment_data.py      # Indian investment database
│   ├── main.py                 # Voice assistant (bonus)
│   └── requirements.txt        # Python dependencies
│
├── frontend/
│   ├── public/
│   │   └── logo.png            # CodeNCASH logo
│   ├── src/
│   │   ├── App.jsx             # Main React component
│   │   ├── App.css             # Styling
│   │   ├── main.jsx            # Entry point
│   │   └── index.css           # Global styles
│   ├── package.json            # Node dependencies
│   └── vite.config.js          # Vite configuration
│
├── HACKATHON_PLAN.md           # Implementation roadmap
├── DEMO_README.md              # Demo guide
└── README.md                   # This file
```

---

## 🎬 Demo Script (2-3 minutes)

### Introduction (15 seconds)
"Hi! I'm presenting CodeNCASH - an AI Portfolio Advisor for Indian investors that generates personalized investment portfolios."

### Demo (2 minutes)

**1. Show Profile Form (20 sec)**
- "Users enter their investment details"
- Fill: Capital ₹500,000, SIP ₹10,000, Medium Risk, Mutual Funds

**2. Portfolio Generation (45 sec)**
- Click "Generate Portfolio"
- "The AI generates a customized portfolio in real-time with:"
  - Asset allocation percentages
  - Specific mutual funds (HDFC, Axis, ICICI)
  - NSE/BSE stocks
  - Expected returns
  - Risk assessment

**3. Interactive Q&A (30 sec)**
- Ask: "Why did you recommend HDFC Top 100 Fund?"
- Show AI responds with reasoning

**4. PDF Export (15 sec)**
- Click "Download as PDF"
- Show downloaded professional portfolio

**5. Different Risk Profile (20 sec)**
- Click "New Portfolio"
- Show High Risk = more stocks
- OR Low Risk = more debt

### Closing (10 seconds)
"CodeNCASH combines AI intelligence with actual Indian market data for actionable, personalized investment advice. Thank you!"

---

## 🚀 Future Enhancements (Round 2+)

### Planned Features
- [ ] **Charts & Graphs** - Pie charts for allocation visualization
- [ ] **User Accounts** - Save portfolios with JWT authentication
- [ ] **Database** - PostgreSQL for persistent storage
- [ ] **Live Data** - Yahoo Finance API for real-time stock prices
- [ ] **Portfolio Tracking** - Monitor performance over time
- [ ] **Rebalancing Suggestions** - AI-powered portfolio adjustments
- [ ] **Tax Calculator** - Estimate capital gains tax
- [ ] **SIP Calculator** - Project future value
- [ ] **Goal-based Planning** - Retirement, education, home purchase
- [ ] **Multi-language** - Hindi, Tamil, Bengali support

### Technical Improvements
- [ ] Better model (Llama 3.1:8b or Qwen 2.5:14b)
- [ ] Caching with Redis
- [ ] Rate limiting
- [ ] Error monitoring (Sentry)
- [ ] Analytics (Google Analytics)
- [ ] PWA support

---

## 💰 Cost Analysis

| Item | Cost |
|------|------|
| Development | FREE |
| AI Model (Qwen 2.5) | FREE (local) |
| Hosting (Vercel + Railway) | FREE tier |
| APIs (Yahoo Finance) | FREE |
| Database (Supabase) | FREE tier |
| Domain | ~₹1,000/year |
| **Total for MVP** | **₹0** 🎉 |

---

## 📜 License

This project is created for hackathon purposes.

---

## 👥 Team

**Your Team Name**
- Your Name - Role
- Team Member 2 - Role
- Team Member 3 - Role

---

## 🙏 Acknowledgments

- **Ollama** - For local LLM runtime
- **Qwen Team** - For the amazing Qwen 2.5 model
- **Hackathon Organizers** - For the opportunity
- **Open Source Community** - For amazing tools

---

## 📞 Contact

- **GitHub:** [your-repo-link]
- **Email:** your-email@example.com
- **Demo Video:** [link-to-demo-video]

---

## ⭐ Star Us!

If you find this project helpful, please give it a star ⭐

---

**Built with ❤️ for Indian investors**

**CodeNCASH - Your AI Portfolio Advisor** 💼💰
