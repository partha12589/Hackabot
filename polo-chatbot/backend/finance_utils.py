# finance_utils.py
# Finance Query Detection and Validation Utility

import re
from typing import Dict, List, Tuple

class FinanceQueryValidator:
    """
    Validates if user queries are finance-related
    """
    
    # Comprehensive finance keywords
    FINANCE_KEYWORDS = {
        "banking": ["bank", "account", "savings", "checking", "deposit", "atm", "debit", "credit card"],
        "investments": ["stock", "share", "equity", "mutual fund", "etf", "bond", "portfolio", "invest", "dividend", "capital gains"],
        "loans": ["loan", "mortgage", "emi", "interest rate", "principal", "borrowing", "credit", "refinance", "down payment"],
        "insurance": ["insurance", "premium", "policy", "life insurance", "health insurance", "term insurance", "coverage"],
        "taxation": ["tax", "income tax", "gst", "tds", "itr", "deduction", "exemption", "tax saving", "capital gains tax"],
        "retirement": ["retirement", "pension", "pf", "provident fund", "epf", "nps", "retirement planning", "401k"],
        "budgeting": ["budget", "expense", "income", "savings", "financial planning", "cash flow", "spending"],
        "cryptocurrency": ["crypto", "bitcoin", "ethereum", "blockchain", "cryptocurrency", "altcoin", "wallet"],
        "real_estate": ["property", "real estate", "home loan", "rent", "housing", "reit"],
        "market": ["market", "trading", "forex", "commodity", "gold", "silver", "nifty", "sensex", "dow jones"],
        "finance_general": ["finance", "money", "wealth", "financial", "asset", "liability", "net worth", "roi", "return on investment"]
    }
    
    # Non-finance indicators (to reject)
    NON_FINANCE_INDICATORS = [
        "recipe", "weather", "movie", "music", "game", "sports", 
        "celebrity", "travel", "health", "medical", "disease",
        "programming", "code", "software", "hardware", "computer"
    ]
    
    @classmethod
    def is_finance_query(cls, query: str) -> Tuple[bool, str]:
        """
        Check if query is finance-related
        
        Args:
            query: User input string
            
        Returns:
            Tuple of (is_finance: bool, category: str)
        """
        query_lower = query.lower()
        
        # Check for non-finance indicators first
        for indicator in cls.NON_FINANCE_INDICATORS:
            if indicator in query_lower:
                return False, "non_finance"
        
        # Check for finance keywords
        for category, keywords in cls.FINANCE_KEYWORDS.items():
            for keyword in keywords:
                if keyword in query_lower:
                    return True, category
        
        # Check for financial amounts/numbers (e.g., "₹10000", "$500", "10 lakhs")
        financial_pattern = r'(₹|rs\.?|inr|usd|\$|€|£)\s*\d+|(\d+\s*(lakh|crore|thousand|million|billion))'
        if re.search(financial_pattern, query_lower):
            return True, "financial_calculation"
        
        return False, "unknown"
    
    @classmethod
    def get_rejection_message(cls) -> str:
        """Return message for non-finance queries"""
        return (
            "I apologize, but I can only assist with finance-related questions. "
            "Please ask me about banking, investments, loans, taxes, insurance, "
            "budgeting, retirement planning, or other financial topics."
        )
    
    @classmethod
    def get_sample_queries(cls) -> List[str]:
        """Return sample finance queries for UI"""
        return [
            "What is the best investment option for retirement?",
            "How do I calculate EMI for a home loan?",
            "Explain mutual funds vs stocks",
            "What are tax-saving investment options?",
            "How to create a monthly budget?",
            "What is compound interest?",
            "Should I invest in FD or mutual funds?",
            "How to improve credit score?"
        ]


# Convenience function for quick checks
def is_finance_query(query: str) -> bool:
    """Quick check if query is finance-related"""
    is_finance, _ = FinanceQueryValidator.is_finance_query(query)
    return is_finance
