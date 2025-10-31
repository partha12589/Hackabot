# ?? FinanceGPT Portfolio Advisor - Round 1 MVP

**AI-Powered Portfolio Generation for Indian Investors**

---

## ? Quick Setup (2 Steps!)

### Step 1: Backend
```bash
# 1. Pull Qwen 2.5 model (MUST DO THIS FIRST!)
ollama pull qwen2.5:7b

# 2. Start backend
cd /workspace/polo-chatbot/backend
uvicorn api:app --reload --port 8000
```

### Step 2: Frontend
```bash
# In a new terminal
cd /workspace/polo-chatbot/frontend
npm run dev
```

**Open:** http://localhost:5173

---

## ?? Features (Hackathon Requirements)

? **User Input Collection**
   - Capital amount
   - Monthly SIP
   - Risk appetite (Low/Medium/High)
   - Investment preferences

? **AI Portfolio Generation**
   - Personalized recommendations
   - Actual Indian mutual funds (HDFC, Axis, ICICI, Mirae)
   - NSE/BSE stocks (Reliance, TCS, HDFC Bank)
   - Debt instruments (FDs, PPF, NSC)

? **Diversification**
   - Asset allocation based on risk
   - Mix of equity, debt, stocks

? **Return Estimates**
   - Realistic projections
   - Risk-adjusted returns

? **Q&A Chatbot**
   - Answer follow-up questions
   - General investment queries

---

## ?? Demo Script (2-3 minutes)

### **1. Introduction (15 sec)**
"Hi! We built FinanceGPT - an AI Portfolio Advisor for Indian investors. It generates personalized portfolios based on your investment goals."

### **2. User Profile (30 sec)**
- **Show form:** "First, the user enters their details"
- **Fill in:**
  - Capital: ?5,00,000
  - Monthly SIP: ?10,000
  - Risk: Medium
  - Preferences: Mutual Funds ?
- **Click:** "Generate My Portfolio"

### **3. Portfolio Generation (60 sec)**
- **Show streaming:** "The AI generates a customized portfolio in real-time"
- **Highlight:**
  - Asset allocation percentages
  - Specific fund names (HDFC, Axis, etc.)
  - Expected returns
  - Diversification strategy

### **4. Follow-up Questions (30 sec)**
Ask chatbot:
- "Why did you recommend HDFC Top 100 Fund?"
- "What are the tax implications?"
- "Can I change my risk profile later?"

### **5. Different Risk Profile (30 sec)**
**Refresh page** and show:
- High risk portfolio (more stocks)
- OR Low risk portfolio (more debt)

### **6. Closing (15 sec)**
"Our solution combines AI intelligence with actual Indian market data to provide actionable, personalized investment advice. Thank you!"

---

## ?? Key Differentiators

1. **Real Indian Investments** - Not generic advice
2. **Beautiful Modern UI** - Professional look
3. **Real-time AI Generation** - Powered by Qwen 2.5
4. **Risk-adjusted** - Low/Medium/High profiles
5. **Interactive Chatbot** - Answer follow-up questions
6. **SIP Planning** - Monthly investment breakdown

---

## ?? Tech Stack

- **Frontend:** React + Vite + TailwindCSS
- **Backend:** FastAPI + Python
- **AI Model:** Qwen 2.5:7b (via Ollama)
- **Data:** Curated Indian investment database

---

## ?? Troubleshooting

### "Model not found"
```bash
ollama pull qwen2.5:7b
```

### Backend not starting
```bash
cd /workspace/polo-chatbot/backend
pip install -r requirements.txt
```

### Port already in use
```bash
# Kill existing process
lsof -ti:8000 | xargs kill -9
lsof -ti:5173 | xargs kill -9
```

---

## ?? Round 2 Enhancements (If Selected)

- [ ] Charts/graphs for allocation
- [ ] PDF export of portfolio
- [ ] Historical performance data
- [ ] Rebalancing suggestions
- [ ] Tax optimizer
- [ ] Multi-year projections

---

## ?? Sample Test Cases

### Test Case 1: Conservative Investor
- Capital: ?10,00,000
- SIP: ?5,000
- Risk: Low
- Expected: 60-70% debt, minimal stocks

### Test Case 2: Aggressive Investor
- Capital: ?3,00,000
- SIP: ?20,000
- Risk: High
- Expected: 60%+ equity, direct stocks

### Test Case 3: Balanced Investor
- Capital: ?5,00,000
- SIP: ?10,000
- Risk: Medium
- Expected: 50% equity, 30% debt, 20% mix

---

## ? Pre-Demo Checklist

- [ ] Ollama running with qwen2.5:7b
- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] Test portfolio generation once
- [ ] Prepare 2-3 follow-up questions
- [ ] Have different risk profiles ready
- [ ] Browser in fullscreen mode
- [ ] Close unnecessary tabs

---

**Good Luck! ??**
