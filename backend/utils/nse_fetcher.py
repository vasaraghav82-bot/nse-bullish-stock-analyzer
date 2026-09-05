"""NSE Data Fetcher - Fetch real-time stock data from NSE"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Optional
from loguru import logger

class NSEFetcher:
    """Fetch stock data from NSE API"""
    
    BASE_URL = 'https://www.nseindia.com/api'
    
    # Headers to mimic browser request
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
    
    def get_stock_data(self, symbol: str, days: int = 365) -> Optional[pd.DataFrame]:
        """Fetch historical stock data for a given symbol"""
        try:
            logger.info(f"Fetching data for symbol: {symbol}")
            # Using alternative approach with yfinance for demonstration
            import yfinance as yf
            
            # Convert NSE symbol to Yahoo Finance format
            nse_symbol = f"{symbol}.NS"
            
            # Fetch data
            data = yf.download(nse_symbol, period=f"{days}d", progress=False)
            
            if data is None or data.empty:
                logger.warning(f"No data found for {symbol}")
                return None
            
            # Reset index to make Date a column
            data.reset_index(inplace=True)
            
            logger.info(f"Successfully fetched {len(data)} records for {symbol}")
            return data
            
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
    def get_quote(self, symbol: str) -> Optional[Dict]:
        """Get current quote for a stock"""
        try:
            logger.info(f"Fetching quote for symbol: {symbol}")
            import yfinance as yf
            
            nse_symbol = f"{symbol}.NS"
            ticker = yf.Ticker(nse_symbol)
            info = ticker.info
            
            quote = {
                'symbol': symbol,
                'price': info.get('currentPrice', 0),
                'change': info.get('regularMarketChange', 0),
                'changePercent': info.get('regularMarketChangePercent', 0),
                'bid': info.get('bid', 0),
                'ask': info.get('ask', 0),
                '52WeekHigh': info.get('fiftyTwoWeekHigh', 0),
                '52WeekLow': info.get('fiftyTwoWeekLow', 0),
                'marketCap': info.get('marketCap', 0),
                'volume': info.get('volume', 0),
                'timestamp': datetime.now().isoformat()
            }
            
            return quote
            
        except Exception as e:
            logger.error(f"Error fetching quote for {symbol}: {str(e)}")
            return None
    
    def get_top_gainers(self, limit: int = 10) -> List[Dict]:
        """Get top gaining stocks"""
        try:
            logger.info("Fetching top gainers")
            # This would need NSE specific implementation
            # Placeholder for demonstration
            return []
        except Exception as e:
            logger.error(f"Error fetching top gainers: {str(e)}")
            return []
    
    def get_top_losers(self, limit: int = 10) -> List[Dict]:
        """Get top losing stocks"""
        try:
            logger.info("Fetching top losers")
            return []
        except Exception as e:
            logger.error(f"Error fetching top losers: {str(e)}")
            return []
    
    def get_market_summary(self) -> Optional[Dict]:
        """Get market summary"""
        try:
            logger.info("Fetching market summary")
            # Fetch NIFTY 50 index data
            import yfinance as yf
            nifty = yf.Ticker("^NSEI")
            
            summary = {
                'index': 'NIFTY 50',
                'price': nifty.info.get('currentPrice', 0),
                'change': nifty.info.get('regularMarketChange', 0),
                'changePercent': nifty.info.get('regularMarketChangePercent', 0),
                'timestamp': datetime.now().isoformat()
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error fetching market summary: {str(e)}")
            return None
