# Indian Investment Data - Sample Database for Portfolio Generation
# This contains curated investment options available in India

MUTUAL_FUNDS = {
    "large_cap": [
        {
            "name": "HDFC Top 100 Fund",
            "category": "Large Cap",
            "risk": "medium",
            "expected_return": "12-14%",
            "min_investment": 5000,
            "expense_ratio": "0.46%",
            "aum": "?25,000 Cr"
        },
        {
            "name": "Axis Bluechip Fund",
            "category": "Large Cap",
            "risk": "medium",
            "expected_return": "11-13%",
            "min_investment": 5000,
            "expense_ratio": "0.42%",
            "aum": "?35,000 Cr"
        },
        {
            "name": "ICICI Prudential Bluechip Fund",
            "category": "Large Cap",
            "risk": "medium",
            "expected_return": "11-13%",
            "min_investment": 5000,
            "expense_ratio": "0.86%",
            "aum": "?40,000 Cr"
        },
        {
            "name": "Mirae Asset Large Cap Fund",
            "category": "Large Cap",
            "risk": "medium",
            "expected_return": "12-14%",
            "min_investment": 5000,
            "expense_ratio": "0.45%",
            "aum": "?30,000 Cr"
        }
    ],
    "mid_cap": [
        {
            "name": "Axis Midcap Fund",
            "category": "Mid Cap",
            "risk": "high",
            "expected_return": "14-16%",
            "min_investment": 5000,
            "expense_ratio": "0.52%",
            "aum": "?15,000 Cr"
        },
        {
            "name": "Kotak Emerging Equity Fund",
            "category": "Mid Cap",
            "risk": "high",
            "expected_return": "13-15%",
            "min_investment": 5000,
            "expense_ratio": "0.54%",
            "aum": "?18,000 Cr"
        },
        {
            "name": "DSP Midcap Fund",
            "category": "Mid Cap",
            "risk": "high",
            "expected_return": "13-16%",
            "min_investment": 5000,
            "expense_ratio": "0.67%",
            "aum": "?12,000 Cr"
        }
    ],
    "small_cap": [
        {
            "name": "Axis Small Cap Fund",
            "category": "Small Cap",
            "risk": "high",
            "expected_return": "15-18%",
            "min_investment": 5000,
            "expense_ratio": "0.56%",
            "aum": "?10,000 Cr"
        },
        {
            "name": "Nippon India Small Cap Fund",
            "category": "Small Cap",
            "risk": "high",
            "expected_return": "14-17%",
            "min_investment": 5000,
            "expense_ratio": "0.75%",
            "aum": "?8,000 Cr"
        }
    ],
    "debt": [
        {
            "name": "HDFC Corporate Bond Fund",
            "category": "Debt",
            "risk": "low",
            "expected_return": "7-8%",
            "min_investment": 5000,
            "expense_ratio": "0.35%",
            "aum": "?15,000 Cr"
        },
        {
            "name": "ICICI Prudential Corporate Bond Fund",
            "category": "Debt",
            "risk": "low",
            "expected_return": "7-8%",
            "min_investment": 5000,
            "expense_ratio": "0.39%",
            "aum": "?12,000 Cr"
        },
        {
            "name": "Axis Banking & PSU Debt Fund",
            "category": "Debt",
            "risk": "low",
            "expected_return": "7-8%",
            "min_investment": 5000,
            "expense_ratio": "0.31%",
            "aum": "?20,000 Cr"
        }
    ],
    "hybrid": [
        {
            "name": "HDFC Balanced Advantage Fund",
            "category": "Hybrid",
            "risk": "medium",
            "expected_return": "10-12%",
            "min_investment": 5000,
            "expense_ratio": "0.62%",
            "aum": "?55,000 Cr"
        },
        {
            "name": "ICICI Prudential Equity & Debt Fund",
            "category": "Hybrid",
            "risk": "medium",
            "expected_return": "10-12%",
            "min_investment": 5000,
            "expense_ratio": "0.95%",
            "aum": "?30,000 Cr"
        }
    ],
    "index": [
        {
            "name": "HDFC Index Nifty 50",
            "category": "Index",
            "risk": "medium",
            "expected_return": "11-13%",
            "min_investment": 5000,
            "expense_ratio": "0.20%",
            "aum": "?15,000 Cr"
        },
        {
            "name": "ICICI Prudential Nifty Index Fund",
            "category": "Index",
            "risk": "medium",
            "expected_return": "11-13%",
            "min_investment": 100,
            "expense_ratio": "0.19%",
            "aum": "?10,000 Cr"
        }
    ]
}

STOCKS = {
    "blue_chip": [
        {
            "name": "Reliance Industries",
            "sector": "Energy/Telecom",
            "exchange": "NSE/BSE",
            "risk": "medium",
            "market_cap": "?17 Lakh Cr",
            "approx_price": "?2,400"
        },
        {
            "name": "TCS",
            "sector": "IT Services",
            "exchange": "NSE/BSE",
            "risk": "low",
            "market_cap": "?14 Lakh Cr",
            "approx_price": "?3,800"
        },
        {
            "name": "HDFC Bank",
            "sector": "Banking",
            "exchange": "NSE/BSE",
            "risk": "low",
            "market_cap": "?12 Lakh Cr",
            "approx_price": "?1,600"
        },
        {
            "name": "Infosys",
            "sector": "IT Services",
            "exchange": "NSE/BSE",
            "risk": "low",
            "market_cap": "?6 Lakh Cr",
            "approx_price": "?1,450"
        },
        {
            "name": "ITC",
            "sector": "FMCG",
            "exchange": "NSE/BSE",
            "risk": "low",
            "market_cap": "?5 Lakh Cr",
            "approx_price": "?400"
        }
    ],
    "growth": [
        {
            "name": "Asian Paints",
            "sector": "Consumer Goods",
            "exchange": "NSE/BSE",
            "risk": "medium",
            "market_cap": "?2.5 Lakh Cr",
            "approx_price": "?2,600"
        },
        {
            "name": "Bajaj Finance",
            "sector": "NBFC",
            "exchange": "NSE/BSE",
            "risk": "medium",
            "market_cap": "?4 Lakh Cr",
            "approx_price": "?6,500"
        },
        {
            "name": "Titan Company",
            "sector": "Consumer Durables",
            "exchange": "NSE/BSE",
            "risk": "medium",
            "market_cap": "?2.5 Lakh Cr",
            "approx_price": "?2,800"
        }
    ]
}

DEBT_INSTRUMENTS = {
    "fixed_deposits": [
        {
            "bank": "HDFC Bank",
            "type": "Fixed Deposit",
            "tenure": "1-5 years",
            "interest_rate": "7.0-7.5%",
            "risk": "low",
            "min_investment": 10000
        },
        {
            "bank": "ICICI Bank",
            "type": "Fixed Deposit",
            "tenure": "1-5 years",
            "interest_rate": "7.0-7.5%",
            "risk": "low",
            "min_investment": 10000
        },
        {
            "bank": "SBI",
            "type": "Fixed Deposit",
            "tenure": "1-5 years",
            "interest_rate": "6.8-7.4%",
            "risk": "low",
            "min_investment": 1000
        }
    ],
    "government_schemes": [
        {
            "name": "Public Provident Fund (PPF)",
            "interest_rate": "7.1%",
            "tenure": "15 years",
            "risk": "very_low",
            "tax_benefit": "80C Deduction",
            "min_investment": 500,
            "max_investment": 150000
        },
        {
            "name": "National Savings Certificate (NSC)",
            "interest_rate": "7.7%",
            "tenure": "5 years",
            "risk": "very_low",
            "tax_benefit": "80C Deduction",
            "min_investment": 1000
        },
        {
            "name": "Senior Citizen Savings Scheme",
            "interest_rate": "8.2%",
            "tenure": "5 years",
            "risk": "very_low",
            "eligibility": "60+ years",
            "max_investment": 3000000
        }
    ],
    "bonds": [
        {
            "name": "RBI Bonds",
            "interest_rate": "7.15%",
            "tenure": "7 years",
            "risk": "very_low",
            "min_investment": 1000
        },
        {
            "name": "Corporate Bonds (AAA Rated)",
            "interest_rate": "8-9%",
            "tenure": "3-5 years",
            "risk": "low",
            "min_investment": 10000
        }
    ]
}

# Portfolio Allocation Templates Based on Risk Appetite
RISK_ALLOCATIONS = {
    "low": {
        "equity_mutual_funds": 20,  # 20% in equity
        "debt_mutual_funds": 40,    # 40% in debt funds
        "fixed_deposits": 30,        # 30% in FDs
        "government_schemes": 10,    # 10% in PPF/NSC
        "stocks": 0,                 # 0% in direct stocks
        "expected_return": "7-9%"
    },
    "medium": {
        "equity_mutual_funds": 50,  # 50% in equity
        "debt_mutual_funds": 25,    # 25% in debt funds
        "fixed_deposits": 10,        # 10% in FDs
        "stocks": 10,                # 10% in blue-chip stocks
        "hybrid_funds": 5,           # 5% in hybrid
        "expected_return": "10-13%"
    },
    "high": {
        "equity_mutual_funds": 60,  # 60% in equity (large+mid+small)
        "stocks": 25,                # 25% in stocks
        "debt_mutual_funds": 10,    # 10% in debt
        "hybrid_funds": 5,           # 5% in hybrid
        "expected_return": "13-16%"
    }
}

# SIP Allocation Guidelines
SIP_GUIDELINES = {
    "below_5000": {
        "recommendation": "Focus on 1-2 index funds for low cost",
        "suggested_funds": ["Index Funds"]
    },
    "5000_to_10000": {
        "recommendation": "Diversify across 2-3 mutual funds",
        "suggested_funds": ["Large Cap", "Debt Fund"]
    },
    "10000_to_25000": {
        "recommendation": "Diversify across 3-4 mutual funds",
        "suggested_funds": ["Large Cap", "Mid Cap", "Debt Fund"]
    },
    "above_25000": {
        "recommendation": "Comprehensive diversification with 4-6 funds",
        "suggested_funds": ["Large Cap", "Mid Cap", "Small Cap", "Debt", "Hybrid"]
    }
}

def get_investment_recommendations(capital, monthly_sip, risk_appetite, preferences):
    """
    Generate investment recommendations based on user input
    This is a helper function for the AI to use
    """
    allocation = RISK_ALLOCATIONS.get(risk_appetite.lower(), RISK_ALLOCATIONS["medium"])
    
    recommendations = {
        "risk_profile": risk_appetite,
        "allocation": allocation,
        "capital_breakdown": {},
        "sip_breakdown": {},
        "total_expected_return": allocation["expected_return"]
    }
    
    # Calculate capital allocation
    for asset_class, percentage in allocation.items():
        if asset_class != "expected_return":
            amount = (capital * percentage) / 100
            recommendations["capital_breakdown"][asset_class] = {
                "percentage": percentage,
                "amount": amount
            }
    
    # Calculate SIP allocation
    for asset_class, percentage in allocation.items():
        if asset_class != "expected_return":
            amount = (monthly_sip * percentage) / 100
            recommendations["sip_breakdown"][asset_class] = {
                "percentage": percentage,
                "amount": amount
            }
    
    return recommendations
