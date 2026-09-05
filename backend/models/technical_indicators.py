"""Technical Indicators Calculation"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
from loguru import logger

class TechnicalIndicators:
    """Calculate technical indicators for stock analysis"""
    
    @staticmethod
    def calculate_sma(data: pd.DataFrame, period: int = 20, column: str = 'Close') -> pd.Series:
        """Calculate Simple Moving Average"""
        try:
            return data[column].rolling(window=period).mean()
        except Exception as e:
            logger.error(f"Error calculating SMA: {str(e)}")
            return pd.Series()
    
    @staticmethod
    def calculate_ema(data: pd.DataFrame, period: int = 20, column: str = 'Close') -> pd.Series:
        """Calculate Exponential Moving Average"""
        try:
            return data[column].ewm(span=period, adjust=False).mean()
        except Exception as e:
            logger.error(f"Error calculating EMA: {str(e)}")
            return pd.Series()
    
    @staticmethod
    def calculate_rsi(data: pd.DataFrame, period: int = 14, column: str = 'Close') -> pd.Series:
        """Calculate Relative Strength Index (RSI)"""
        try:
            delta = data[column].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi
        except Exception as e:
            logger.error(f"Error calculating RSI: {str(e)}")
            return pd.Series()
    
    @staticmethod
    def calculate_macd(data: pd.DataFrame, fast: int = 12, slow: int = 26, 
                      signal: int = 9, column: str = 'Close') -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Calculate MACD (Moving Average Convergence Divergence)"""
        try:
            ema_fast = data[column].ewm(span=fast, adjust=False).mean()
            ema_slow = data[column].ewm(span=slow, adjust=False).mean()
            macd = ema_fast - ema_slow
            signal_line = macd.ewm(span=signal, adjust=False).mean()
            histogram = macd - signal_line
            
            return macd, signal_line, histogram
        except Exception as e:
            logger.error(f"Error calculating MACD: {str(e)}")
            return pd.Series(), pd.Series(), pd.Series()
    
    @staticmethod
    def calculate_bollinger_bands(data: pd.DataFrame, period: int = 20, 
                                 std_dev: int = 2, column: str = 'Close') -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Calculate Bollinger Bands"""
        try:
            middle_band = data[column].rolling(window=period).mean()
            std = data[column].rolling(window=period).std()
            upper_band = middle_band + (std * std_dev)
            lower_band = middle_band - (std * std_dev)
            
            return upper_band, middle_band, lower_band
        except Exception as e:
            logger.error(f"Error calculating Bollinger Bands: {str(e)}")
            return pd.Series(), pd.Series(), pd.Series()
    
    @staticmethod
    def calculate_adx(data: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Average Directional Index (ADX)"""
        try:
            high = data['High']
            low = data['Low']
            close = data['Close']
            
            # Calculate True Range
            tr1 = high - low
            tr2 = abs(high - close.shift())
            tr3 = abs(low - close.shift())
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            atr = tr.rolling(window=period).mean()
            
            # Calculate Directional Movement
            up = high.diff()
            down = -low.diff()
            
            pos_dm = up.where((up > down) & (up > 0), 0)
            neg_dm = down.where((down > up) & (down > 0), 0)
            
            pos_di = 100 * (pos_dm.rolling(window=period).mean() / atr)
            neg_di = 100 * (neg_dm.rolling(window=period).mean() / atr)
            
            di_diff = abs(pos_di - neg_di)
            di_sum = pos_di + neg_di
            
            dx = 100 * (di_diff / di_sum)
            adx = dx.rolling(window=period).mean()
            
            return adx
        except Exception as e:
            logger.error(f"Error calculating ADX: {str(e)}")
            return pd.Series()
    
    @staticmethod
    def calculate_volume_sma(data: pd.DataFrame, period: int = 20) -> pd.Series:
        """Calculate Volume Moving Average"""
        try:
            return data['Volume'].rolling(window=period).mean()
        except Exception as e:
            logger.error(f"Error calculating Volume SMA: {str(e)}")
            return pd.Series()
