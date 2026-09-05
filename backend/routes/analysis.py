"""Analysis Routes - API endpoints for stock analysis"""

from flask import Blueprint, jsonify, request
from backend.utils.nse_fetcher import NSEFetcher
from backend.models.bullish_detector import BullishDetector
from backend.models.technical_indicators import TechnicalIndicators
from loguru import logger

analysis_bp = Blueprint('analysis', __name__)

fetcher = NSEFetcher()
detector = BullishDetector()
indicators = TechnicalIndicators()

@analysis_bp.route('/analysis/<symbol>', methods=['GET'])
def get_analysis(symbol: str):
    """Get technical analysis for a stock"""
    try:
        # Get period from query params (default 365 days)
        period = request.args.get('period', 365, type=int)
        
        # Fetch stock data
        data = fetcher.get_stock_data(symbol, days=period)
        
        if data is None:
            return jsonify({'error': 'Could not fetch stock data'}), 500
        
        # Perform analysis
        analysis = detector.analyze_stock(data, symbol)
        
        return jsonify({
            'status': 'success',
            'analysis': analysis
        }), 200
        
    except Exception as e:
        logger.error(f"Error analyzing {symbol}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/analysis/<symbol>/indicators', methods=['GET'])
def get_indicators(symbol: str):
    """Get technical indicators for a stock"""
    try:
        period = request.args.get('period', 365, type=int)
        data = fetcher.get_stock_data(symbol, days=period)
        
        if data is None:
            return jsonify({'error': 'Could not fetch stock data'}), 500
        
        # Calculate indicators
        rsi = indicators.calculate_rsi(data)
        macd, signal, histogram = indicators.calculate_macd(data)
        upper_bb, middle_bb, lower_bb = indicators.calculate_bollinger_bands(data)
        sma_20 = indicators.calculate_sma(data, period=20)
        sma_50 = indicators.calculate_sma(data, period=50)
        
        # Get latest values
        latest_idx = len(data) - 1
        
        return jsonify({
            'status': 'success',
            'symbol': symbol,
            'indicators': {
                'rsi': float(rsi.iloc[latest_idx]) if not rsi.isna().all() else 0,
                'macd': float(macd.iloc[latest_idx]) if not macd.isna().all() else 0,
                'macd_signal': float(signal.iloc[latest_idx]) if not signal.isna().all() else 0,
                'macd_histogram': float(histogram.iloc[latest_idx]) if not histogram.isna().all() else 0,
                'sma_20': float(sma_20.iloc[latest_idx]) if not sma_20.isna().all() else 0,
                'sma_50': float(sma_50.iloc[latest_idx]) if not sma_50.isna().all() else 0,
                'bb_upper': float(upper_bb.iloc[latest_idx]) if not upper_bb.isna().all() else 0,
                'bb_middle': float(middle_bb.iloc[latest_idx]) if not middle_bb.isna().all() else 0,
                'bb_lower': float(lower_bb.iloc[latest_idx]) if not lower_bb.isna().all() else 0
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching indicators for {symbol}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/analysis/compare', methods=['POST'])
def compare_stocks():
    """Compare multiple stocks"""
    try:
        data = request.get_json()
        symbols = data.get('symbols', [])
        
        if not symbols:
            return jsonify({'error': 'No symbols provided'}), 400
        
        comparisons = []
        
        for symbol in symbols:
            stock_data = fetcher.get_stock_data(symbol, days=365)
            if stock_data is not None:
                analysis = detector.analyze_stock(stock_data, symbol)
                comparisons.append(analysis)
        
        return jsonify({
            'status': 'success',
            'count': len(comparisons),
            'comparisons': comparisons
        }), 200
        
    except Exception as e:
        logger.error(f"Error comparing stocks: {str(e)}")
        return jsonify({'error': str(e)}), 500
