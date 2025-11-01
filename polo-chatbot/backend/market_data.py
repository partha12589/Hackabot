"""
Market Data Service - Real-time financial data from APIs
Integrates: Yahoo Finance (stocks), MFapi (mutual funds)
"""

import yfinance as yf
import requests
from typing import Dict, Optional, List
from datetime import datetime


class MarketDataService:
    """Service to fetch real-time market data from various sources"""
    
    @staticmethod
    def get_stock_price(symbol: str) -> Optional[Dict]:
        """
        Get real-time NSE stock price using Yahoo Finance
        
        Args:
            symbol: Stock symbol (e.g., 'TCS', 'INFY', 'HDFCBANK')
        
        Returns:
            Dict with price, change, name, etc. or None if error
        """
        try:
            ticker = yf.Ticker(f"{symbol}.NS")
            info = ticker.info
            
            return {
                "symbol": symbol,
                "name": info.get('longName', symbol),
                "price": info.get('currentPrice', info.get('regularMarketPrice')),
                "currency": "INR",
                "change_percent": info.get('regularMarketChangePercent'),
                "market_cap": info.get('marketCap'),
                "exchange": "NSE",
                "last_updated": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error fetching stock data for {symbol}: {e}")
            return None
    
    @staticmethod
    def get_multiple_stocks(symbols: List[str]) -> Dict[str, Dict]:
        """
        Get prices for multiple stocks at once
        
        Args:
            symbols: List of stock symbols
        
        Returns:
            Dict mapping symbol to price data
        """
        results = {}
        for symbol in symbols:
            data = MarketDataService.get_stock_price(symbol)
            if data:
                results[symbol] = data
        return results
    
    @staticmethod
    def get_mutual_fund_nav(scheme_code: str) -> Optional[Dict]:
        """
        Get mutual fund NAV from MFapi.in
        
        Args:
            scheme_code: AMFI scheme code (e.g., '119551' for HDFC Top 100)
        
        Returns:
            Dict with NAV, date, fund name, etc. or None if error
        """
        try:
            url = f"https://api.mfapi.in/mf/{scheme_code}"
            response = requests.get(url, timeout=5)
            
            if response.ok:
                data = response.json()
                latest_nav = data['data'][0]
                
                return {
                    "scheme_code": scheme_code,
                    "fund_name": data['meta']['scheme_name'],
                    "nav": float(latest_nav['nav']),
                    "date": latest_nav['date'],
                    "scheme_type": data['meta'].get('scheme_type', 'N/A'),
                    "fund_house": data['meta'].get('fund_house', 'N/A'),
                    "last_updated": datetime.now().isoformat()
                }
            else:
                return None
        except Exception as e:
            print(f"Error fetching mutual fund NAV for {scheme_code}: {e}")
            return None
    
    @staticmethod
    def get_multiple_funds(scheme_codes: List[str]) -> Dict[str, Dict]:
        """
        Get NAV for multiple mutual funds at once
        
        Args:
            scheme_codes: List of AMFI scheme codes
        
        Returns:
            Dict mapping scheme_code to NAV data
        """
        results = {}
        for code in scheme_codes:
            data = MarketDataService.get_mutual_fund_nav(code)
            if data:
                results[code] = data
        return results
    
    @staticmethod
    def get_market_indices() -> Dict[str, Dict]:
        """
        Get Nifty 50 and Sensex index values
        
        Returns:
            Dict with current index values and changes
        """
        try:
            nifty = yf.Ticker("^NSEI")
            sensex = yf.Ticker("^BSESN")
            
            nifty_info = nifty.info
            sensex_info = sensex.info
            
            return {
                "nifty_50": {
                    "name": "Nifty 50",
                    "value": nifty_info.get('regularMarketPrice'),
                    "change_percent": nifty_info.get('regularMarketChangePercent'),
                    "last_updated": datetime.now().isoformat()
                },
                "sensex": {
                    "name": "Sensex",
                    "value": sensex_info.get('regularMarketPrice'),
                    "change_percent": sensex_info.get('regularMarketChangePercent'),
                    "last_updated": datetime.now().isoformat()
                }
            }
        except Exception as e:
            print(f"Error fetching market indices: {e}")
            return {
                "nifty_50": {"name": "Nifty 50", "value": None, "error": str(e)},
                "sensex": {"name": "Sensex", "value": None, "error": str(e)}
            }
    
    @staticmethod
    def get_portfolio_live_data(stocks: List[str], mutual_funds: List[str]) -> Dict:
        """
        Get all live data for a portfolio at once
        
        Args:
            stocks: List of stock symbols
            mutual_funds: List of mutual fund scheme codes
        
        Returns:
            Dict with all live market data
        """
        return {
            "stocks": MarketDataService.get_multiple_stocks(stocks),
            "mutual_funds": MarketDataService.get_multiple_funds(mutual_funds),
            "indices": MarketDataService.get_market_indices(),
            "timestamp": datetime.now().isoformat()
        }


# Quick test function
if __name__ == "__main__":
    print("?? Testing Market Data Service...\n")
    
    # Test stock price
    print("1. Testing TCS stock price...")
    tcs = MarketDataService.get_stock_price("TCS")
    if tcs:
        print(f"   ? TCS: ?{tcs['price']} ({tcs['change_percent']:.2f}%)")
    
    # Test mutual fund NAV
    print("\n2. Testing HDFC Top 100 Fund NAV...")
    hdfc = MarketDataService.get_mutual_fund_nav("119551")
    if hdfc:
        print(f"   ? {hdfc['fund_name']}: ?{hdfc['nav']} (as of {hdfc['date']})")
    
    # Test indices
    print("\n3. Testing market indices...")
    indices = MarketDataService.get_market_indices()
    print(f"   ? Nifty 50: {indices['nifty_50']['value']}")
    print(f"   ? Sensex: {indices['sensex']['value']}")
    
    print("\n? All tests complete!")
