# ?? Portfolio Advisor Hackathon - Implementation Plan

## Current Status: 40% Complete ?

### What You Already Have:
- ? FastAPI backend with streaming
- ? React frontend with beautiful UI
- ? Ollama integration
- ? Finance chatbot base
- ? Chat history & validation

---

## ?? Key Requirements Mapping

### 1. User Input Collection
**Status:** Need to Add
- [ ] Capital amount input
- [ ] Monthly SIP amount input
- [ ] Risk appetite selector (Low/Medium/High)
- [ ] Investment preferences (Mutual Funds, Stocks, Bonds, Debt Funds)
- [ ] Investment horizon (optional but good to have)

**Implementation:** Add a form/wizard before chat starts

---

### 2. Portfolio Generation Engine
**Status:** Need to Add
- [ ] Portfolio allocation logic based on risk
- [ ] Diversification rules
- [ ] Asset allocation percentages
- [ ] Return projection calculations

**Implementation:** Backend service with calculation logic

---

### 3. Indian Investment Data
**Status:** Need to Add
- [ ] Popular Indian mutual funds database (Top 50-100)
- [ ] NSE/BSE stock recommendations (Blue chip, mid-cap)
- [ ] Debt instruments (FDs, Bonds, Government schemes)
- [ ] Current approximate return rates

**Implementation:** Static JSON database or API integration

---

### 4. Enhanced AI Prompting
**Status:** Partially Done, Need Enhancement
- [ ] Portfolio generation prompt
- [ ] Risk-based allocation prompt
- [ ] Specific fund recommendation prompt
- [ ] Return calculation guidance

**Implementation:** Update system prompt with portfolio context

---

### 5. Output Formatting
**Status:** Need to Add
- [ ] Portfolio summary view
- [ ] Breakdown by asset class
- [ ] Detailed fund/stock list with allocation %
- [ ] Projected returns visualization
- [ ] Export/Download feature

**Implementation:** Enhanced frontend components

---

## ?? Development Phases

### Phase 1: Core Portfolio Logic (2-3 hours)
1. Create user profile collection form
2. Build portfolio allocation algorithm
3. Create Indian investments database (JSON)
4. Add portfolio generation endpoint

### Phase 2: AI Integration (1-2 hours)
1. Switch to Qwen 2.5 model
2. Update system prompt for portfolio generation
3. Add structured output parsing
4. Test portfolio recommendations

### Phase 3: Frontend Enhancement (2-3 hours)
1. Add user input form/wizard
2. Create portfolio display component
3. Add charts for allocation (optional but impressive)
4. Style portfolio breakdown

### Phase 4: Testing & Polish (1-2 hours)
1. Test with different risk profiles
2. Validate calculations
3. Polish UI/UX
4. Prepare demo script

---

## ?? Recommended Tech Stack Additions

### For Portfolio Visualization:
```bash
npm install recharts  # Simple charts
# or
npm install chart.js react-chartjs-2  # More options
```

### For Data Management:
- JSON files for investment database
- Python pandas for calculations (optional)

---

## ?? Risk-Based Allocation Framework

### Low Risk (Conservative)
- 60-70% Debt instruments (FDs, Bonds, Debt Funds)
- 20-30% Large-cap mutual funds
- 10% Gold/Liquid funds

### Medium Risk (Balanced)
- 40-50% Equity (Large-cap + Mid-cap mutual funds)
- 30-40% Debt instruments
- 10-20% Stocks (Blue chip)

### High Risk (Aggressive)
- 60-70% Equity (Mix of large, mid, small cap)
- 20-30% Direct stocks (NSE/BSE)
- 10% Small-cap/Thematic funds

---

## ?? Winning Features (Differentiators)

1. **Real-time chat + Portfolio generation** ?
2. **Risk-adjusted recommendations** ??
3. **Actual Indian mutual funds & stocks** ????
4. **SIP planning included** ??
5. **Projected returns calculator** ??
6. **Beautiful, modern UI** ??
7. **Export portfolio as PDF** (if time permits) ??

---

## ?? Demo Script Outline

1. **Introduction**: "AI Portfolio Advisor for Indian Investors"
2. **User Input**: Show form - ?5L capital, ?10K SIP, Medium Risk
3. **AI Generation**: Show chatbot generating portfolio in real-time
4. **Portfolio Display**: Beautiful breakdown with specific funds
5. **Q&A**: Ask chatbot questions about recommendations
6. **Highlight**: Show how it adapts to different risk profiles

---

## ?? Estimated Timeline: 8-10 hours

- Phase 1: 3 hours
- Phase 2: 2 hours  
- Phase 3: 3 hours
- Phase 4: 2 hours

**Goal:** Build, test, and polish in 1-2 days max!

---

## ?? Success Criteria

? User can input investment details
? System generates diversified portfolio
? Shows specific Indian investments (funds, stocks)
? Provides projected returns
? Chatbot answers follow-up questions
? Works smoothly in demo
? Looks professional and polished

---

## ?? Next Steps

1. Choose model (Qwen 2.5:7b recommended)
2. Create investment database
3. Build portfolio allocation logic
4. Enhance frontend with input form
5. Test & refine
6. Prepare demo
