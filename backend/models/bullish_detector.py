"""Bullish Pattern Detection"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from loguru import logger
from backend.models.technical_indicators import TechnicalIndicators

class BullishDetector:
    """Detect bullish patterns and signals in stock data"""
    
    def __init__(self, rsi_threshold: float = 50, confidence_min: float = 0.7):
        self.rsi_threshold = rsi_threshold
        self.confidence_min = confidence_min
        self.indicators = TechnicalIndicators()
    
    def analyze_stock(self, data: pd.DataFrame, symbol: str) -> Dict:
        """Perform complete bullish analysis on stock data"""
        try:
            logger.info(f"Analyzing stock {symbol}")
            
            # Calculate all indicators
            rsi = self.indicators.calculate_rsi(data)
            macd, signal, histogram = self.indicators.calculate_macd(data)
            upper_bb, middle_bb, lower_bb = self.indicators.calculate_bollinger_bands(data)
            sma_20 = self.indicators.calculate_sma(data, period=20)
            sma_50 = self.indicators.calculate_sma(data, period=50)
            volume_sma = self.indicators.calculate_volume_sma(data)
            
            # Get latest values
            latest_idx = len(data) - 1
            latest_price = data['Close'].iloc[latest_idx]
            latest_rsi = rsi.iloc[latest_idx]
            latest_macd = macd.iloc[latest_idx]
            latest_histogram = histogram.iloc[latest_idx]
            latest_volume = data['Volume'].iloc[latest_idx]
            latest_volume_avg = volume_sma.iloc[latest_idx]
            
            # Detect bullish signals
            signals = self._detect_signals(
                data, rsi, macd, signal, histogram,
                upper_bb, middle_bb, lower_bb,
                sma_20, sma_50, latest_idx
            )
            
            # Calculate overall bullish score
            bullish_score = self._calculate_bullish_score(signals)
            is_bullish = bullish_score >= self.confidence_min
            
            analysis = {
                'symbol': symbol,
                'current_price': float(latest_price),
                'date': data['Date'].iloc[latest_idx].strftime('%Y-%m-%d') if 'Date' in data.columns else '',
                'indicators': {
                    'rsi': float(latest_rsi) if not pd.isna(latest_rsi) else 0,
                    'macd': float(latest_macd) if not pd.isna(latest_macd) else 0,
                    'macd_signal': float(signal.iloc[latest_idx]) if not pd.isna(signal.iloc[latest_idx]) else 0,
                    'macd_histogram': float(latest_histogram) if not pd.isna(latest_histogram) else 0,
                    'sma_20': float(sma_20.iloc[latest_idx]) if not pd.isna(sma_20.iloc[latest_idx]) else 0,
                    'sma_50': float(sma_50.iloc[latest_idx]) if not pd.isna(sma_50.iloc[latest_idx]) else 0,
                    'bb_upper': float(upper_bb.iloc[latest_idx]) if not pd.isna(upper_bb.iloc[latest_idx]) else 0,
                    'bb_middle': float(middle_bb.iloc[latest_idx]) if not pd.isna(middle_bb.iloc[latest_idx]) else 0,
                    'bb_lower': float(lower_bb.iloc[latest_idx]) if not pd.isna(lower_bb.iloc[latest_idx]) else 0,
                    'volume': float(latest_volume),
                    'volume_avg': float(latest_volume_avg) if not pd.isna(latest_volume_avg) else 0
                },
                'signals': signals,
                'bullish_score': float(bullish_score),
                'is_bullish': bool(is_bullish)
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing stock {symbol}: {str(e)}")
            return {'error': str(e), 'symbol': symbol}
    
    def _detect_signals(self, data: pd.DataFrame, rsi: pd.Series, macd: pd.Series,
                       signal: pd.Series, histogram: pd.Series, upper_bb: pd.Series,
                       middle_bb: pd.Series, lower_bb: pd.Series, sma_20: pd.Series,
                       sma_50: pd.Series, latest_idx: int) -> Dict[str, bool]:
        """Detect bullish signals from indicators"""
        
        signals = {}
        
        # RSI Signal: RSI > 50 indicates bullish
        signals['rsi_bullish'] = rsi.iloc[latest_idx] > self.rsi_threshold
        
        # MACD Signal: MACD > Signal line and histogram > 0
        signals['macd_bullish'] = (macd.iloc[latest_idx] > signal.iloc[latest_idx]) and (histogram.iloc[latest_idx] > 0)
        
        # Price above moving averages
        price = data['Close'].iloc[latest_idx]
        signals['price_above_sma20'] = price > sma_20.iloc[latest_idx]
        signals['price_above_sma50'] = price > sma_50.iloc[latest_idx]
        signals['sma20_above_sma50'] = sma_20.iloc[latest_idx] > sma_50.iloc[latest_idx]
        
        # Bollinger Bands Signal: Price near lower band (oversold)
        signals['bb_breakout'] = price > middle_bb.iloc[latest_idx]
        
        # Volume Signal: Current volume > average volume
        signals['volume_increase'] = data['Volume'].iloc[latest_idx] > data['Volume'].iloc[max(0, latest_idx-20):latest_idx].mean()
        
        # Trend Signal: Check if price is higher than previous closes
        signals['higher_lows'] = all(data['Close'].iloc[latest_idx] > data['Close'].iloc[i] 
                                     for i in range(max(0, latest_idx-5), latest_idx))
        
        return signals
    
    def _calculate_bullish_score(self, signals: Dict[str, bool]) -> float:
        """Calculate overall bullish confidence score from signals"""
        total_signals = len(signals)
        bullish_signals = sum(1 for v in signals.values() if v)
        
        if total_signals == 0:
            return 0.0
        
        return bullish_signals / total_signals
    
    def get_bullish_stocks(self, stocks_data: List[Dict]) -> List[Dict]:
        """Filter and rank bullish stocks"""
        try:
            bullish_stocks = [stock for stock in stocks_data if stock.get('is_bullish', False)]
            
            # Sort by bullish score in descending order
            bullish_stocks.sort(key=lambda x: x.get('bullish_score', 0), reverse=True)
            
            return bullish_stocks
            
        except Exception as e:
            logger.error(f"Error getting bullish stocks: {str(e)}")
            return []
