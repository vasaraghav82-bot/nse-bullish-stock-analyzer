"""Stock Routes - API endpoints for stock data"""

from flask import Blueprint, jsonify, request
from backend.utils.nse_fetcher import NSEFetcher
from backend.models.bullish_detector import BullishDetector
from loguru import logger
from functools import lru_cache
import time

stocks_bp = Blueprint('stocks', __name__)

fetcher = NSEFetcher()
detector = BullishDetector()

@stocks_bp.route('/stocks', methods=['GET'])
def get_stocks():
    """Get list of top bullish stocks"""
    try:
        # Get list of top NSE stocks (hardcoded for demo)
        symbols = [
            'RELIANCE', 'TCS', 'INFY', 'HINDUNILVR', 'ICICIBANK',
            'HDFC', 'LT', 'AXISBANK', 'MARUTI', 'WIPRO'
        ]
        
        bullish_stocks = []
        
        for symbol in symbols:
            # Fetch stock data
            data = fetcher.get_stock_data(symbol, days=365)
            
            if data is not None:
                # Analyze for bullish signals
                analysis = detector.analyze_stock(data, symbol)
                
                if 'error' not in analysis:
                    bullish_stocks.append(analysis)
        
        # Filter and sort bullish stocks
        bullish_stocks = detector.get_bullish_stocks(bullish_stocks)
        
        return jsonify({
            'status': 'success',
            'count': len(bullish_stocks),
            'stocks': bullish_stocks
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching stocks: {str(e)}")
        return jsonify({'error': str(e)}), 500

@stocks_bp.route('/stocks/<symbol>', methods=['GET'])
def get_stock_details(symbol: str):
    """Get detailed information for a specific stock"""
    try:
        # Fetch current quote
        quote = fetcher.get_quote(symbol)
        
        if quote is None:
            return jsonify({'error': 'Stock not found'}), 404
        
        # Fetch historical data
        data = fetcher.get_stock_data(symbol, days=365)
        
        if data is None:
            return jsonify({'error': 'Could not fetch historical data'}), 500
        
        # Analyze stock
        analysis = detector.analyze_stock(data, symbol)
        
        return jsonify({
            'status': 'success',
            'quote': quote,
            'analysis': analysis
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching stock details for {symbol}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@stocks_bp.route('/stocks/<symbol>/quote', methods=['GET'])
def get_quote(symbol: str):
    """Get current quote for a stock"""
    try:
        quote = fetcher.get_quote(symbol)
        
        if quote is None:
            return jsonify({'error': 'Stock not found'}), 404
        
        return jsonify({
            'status': 'success',
            'quote': quote
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching quote for {symbol}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@stocks_bp.route('/market-summary', methods=['GET'])
def get_market_summary():
    """Get market summary"""
    try:
        summary = fetcher.get_market_summary()
        
        if summary is None:
            return jsonify({'error': 'Could not fetch market summary'}), 500
        
        return jsonify({
            'status': 'success',
            'summary': summary
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching market summary: {str(e)}")
        return jsonify({'error': str(e)}), 500
