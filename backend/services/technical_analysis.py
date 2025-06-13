import asyncio
import yfinance as yf
import pandas as pd
import numpy as np
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

from config.settings import settings
from models.schemas import TechnicalIndicators

logger = logging.getLogger(__name__)

class TechnicalAnalyzer:
    """Analizador técnico usando indicadores tradicionales"""
    
    def __init__(self):
        self.cache = {}
        self.cache_expiry = {}
        self.cache_duration = timedelta(minutes=settings.CACHE_EXPIRY_MINUTES)
    
    def _is_cache_valid(self, ticker: str) -> bool:
        """Verifica si el cache es válido"""
        if ticker not in self.cache_expiry:
            return False
        return datetime.now() < self.cache_expiry[ticker]
    
    async def _get_stock_data(self, ticker: str, period: str = "6mo") -> Optional[pd.DataFrame]:
        """Obtiene datos históricos de un ticker"""
        try:
            # Verificar cache
            cache_key = f"{ticker}_{period}"
            if self._is_cache_valid(cache_key):
                return self.cache[cache_key]
            
            # Para tickers argentinos, intentar múltiples sufijos
            ticker_variants = [
                ticker,
                f"{ticker}.BA",  # Buenos Aires
                f"{ticker}.MX",  # México (para algunos ADRs)
            ]
            
            stock_data = None
            for variant in ticker_variants:
                try:
                    stock = yf.Ticker(variant)
                    hist = stock.history(period=period)
                    
                    if not hist.empty and len(hist) > 20:  # Mínimo 20 días de datos
                        stock_data = hist
                        logger.info(f"Datos obtenidos para {ticker} usando {variant}")
                        break
                except Exception as e:
                    logger.debug(f"Error con {variant}: {str(e)}")
                    continue
            
            if stock_data is None or stock_data.empty:
                logger.warning(f"No se pudieron obtener datos para {ticker}")
                return None
            
            # Guardar en cache
            self.cache[cache_key] = stock_data
            self.cache_expiry[cache_key] = datetime.now() + self.cache_duration
            
            return stock_data
            
        except Exception as e:
            logger.error(f"Error obteniendo datos para {ticker}: {str(e)}")
            return None
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calcula el RSI (Relative Strength Index)"""
        try:
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi
        except Exception as e:
            logger.error(f"Error calculando RSI: {str(e)}")
            return pd.Series()
    
    def _calculate_macd(self, prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, pd.Series]:
        """Calcula MACD"""
        try:
            exp1 = prices.ewm(span=fast).mean()
            exp2 = prices.ewm(span=slow).mean()
            macd = exp1 - exp2
            signal_line = macd.ewm(span=signal).mean()
            histogram = macd - signal_line
            
            return {
                'macd': macd,
                'signal': signal_line,
                'histogram': histogram
            }
        except Exception as e:
            logger.error(f"Error calculando MACD: {str(e)}")
            return {}
    
    def _calculate_bollinger_bands(self, prices: pd.Series, period: int = 20, std_dev: int = 2) -> Dict[str, pd.Series]:
        """Calcula Bandas de Bollinger"""
        try:
            sma = prices.rolling(window=period).mean()
            std = prices.rolling(window=period).std()
            
            upper_band = sma + (std * std_dev)
            lower_band = sma - (std * std_dev)
            
            return {
                'upper': upper_band,
                'middle': sma,
                'lower': lower_band
            }
        except Exception as e:
            logger.error(f"Error calculando Bollinger Bands: {str(e)}")
            return {}
    
    def _calculate_moving_averages(self, prices: pd.Series) -> Dict[str, pd.Series]:
        """Calcula medias móviles"""
        try:
            return {
                'sma_20': prices.rolling(window=20).mean(),
                'sma_50': prices.rolling(window=50).mean(),
                'sma_200': prices.rolling(window=200).mean(),
                'ema_20': prices.ewm(span=20).mean(),
                'ema_50': prices.ewm(span=50).mean()
            }
        except Exception as e:
            logger.error(f"Error calculando medias móviles: {str(e)}")
            return {}
    
    def _calculate_technical_score(self, indicators: TechnicalIndicators, current_price: float) -> float:
        """
        Calcula el score técnico basado en indicadores
        Score de 0-100 basado en señales técnicas
        """
        score = 0.0
        signals_count = 0
        
        # RSI (30 puntos máximo)
        if indicators.rsi is not None:
            signals_count += 1
            if indicators.rsi < 30:          # Sobreventa - señal de compra
                score += 25
            elif indicators.rsi < 50:        # Territorio neutral-bajista
                score += 15
            elif indicators.rsi < 70:        # Territorio neutral-alcista
                score += 20
            elif indicators.rsi >= 70:       # Sobrecompra - señal de precaución
                score += 10
        
        # MACD (25 puntos máximo)
        if indicators.macd is not None and indicators.macd_signal is not None:
            signals_count += 1
            macd_diff = indicators.macd - indicators.macd_signal
            if macd_diff > 0 and indicators.macd_histogram and indicators.macd_histogram > 0:
                score += 25  # Señal alcista fuerte
            elif macd_diff > 0:
                score += 20  # Señal alcista
            elif macd_diff < 0 and indicators.macd_histogram and indicators.macd_histogram < 0:
                score += 5   # Señal bajista fuerte
            else:
                score += 10  # Señal bajista
        
        # Medias móviles (25 puntos máximo)
        ma_signals = 0
        ma_count = 0
        
        if indicators.sma_20 is not None:
            ma_count += 1
            if current_price > indicators.sma_20:
                ma_signals += 1
                
        if indicators.sma_50 is not None:
            ma_count += 1
            if current_price > indicators.sma_50:
                ma_signals += 1
                
        if indicators.sma_200 is not None:
            ma_count += 1
            if current_price > indicators.sma_200:
                ma_signals += 1
        
        if ma_count > 0:
            signals_count += 1
            ma_score = (ma_signals / ma_count) * 25
            score += ma_score
        
        # Bollinger Bands (20 puntos máximo)
        if indicators.bollinger_upper is not None and indicators.bollinger_lower is not None:
            signals_count += 1
            bb_middle = (indicators.bollinger_upper + indicators.bollinger_lower) / 2
            
            if current_price < indicators.bollinger_lower:
                score += 20  # Precio bajo, potencial compra
            elif current_price > indicators.bollinger_upper:
                score += 5   # Precio alto, precaución
            elif current_price > bb_middle:
                score += 15  # Por encima del medio
            else:
                score += 10  # Por debajo del medio
        
        # Si no hay señales, score neutral
        if signals_count == 0:
            return 50.0
        
        # Normalizar score
        max_possible = 100
        normalized_score = min(score, max_possible)
        
        return round(normalized_score, 2)
    
    async def get_technical_indicators(self, ticker: str) -> Optional[TechnicalIndicators]:
        """Obtiene indicadores técnicos para un ticker"""
        try:
            data = await self._get_stock_data(ticker)
            if data is None or data.empty:
                return None
            
            close_prices = data['Close']
            volume = data['Volume']
            
            # Calcular indicadores
            rsi = self._calculate_rsi(close_prices)
            macd_data = self._calculate_macd(close_prices)
            bb_data = self._calculate_bollinger_bands(close_prices)
            ma_data = self._calculate_moving_averages(close_prices)
            
            # Obtener valores más recientes
            latest_rsi = rsi.iloc[-1] if not rsi.empty else None
            latest_macd = macd_data.get('macd', pd.Series()).iloc[-1] if macd_data.get('macd') is not None else None
            latest_macd_signal = macd_data.get('signal', pd.Series()).iloc[-1] if macd_data.get('signal') is not None else None
            latest_macd_hist = macd_data.get('histogram', pd.Series()).iloc[-1] if macd_data.get('histogram') is not None else None
            
            return TechnicalIndicators(
                rsi=latest_rsi,
                macd=latest_macd,
                macd_signal=latest_macd_signal,
                macd_histogram=latest_macd_hist,
                sma_20=ma_data.get('sma_20', pd.Series()).iloc[-1] if ma_data.get('sma_20') is not None else None,
                sma_50=ma_data.get('sma_50', pd.Series()).iloc[-1] if ma_data.get('sma_50') is not None else None,
                sma_200=ma_data.get('sma_200', pd.Series()).iloc[-1] if ma_data.get('sma_200') is not None else None,
                bollinger_upper=bb_data.get('upper', pd.Series()).iloc[-1] if bb_data.get('upper') is not None else None,
                bollinger_lower=bb_data.get('lower', pd.Series()).iloc[-1] if bb_data.get('lower') is not None else None,
                volume_sma=volume.rolling(window=20).mean().iloc[-1] if len(volume) >= 20 else None
            )
            
        except Exception as e:
            logger.error(f"Error calculando indicadores técnicos para {ticker}: {str(e)}")
            return None
    
    async def analyze_ticker(self, ticker: str) -> Dict[str, Any]:
        """Análisis técnico completo de un ticker"""
        try:
            # Obtener datos y calcular indicadores
            data = await self._get_stock_data(ticker)
            if data is None or data.empty:
                logger.warning(f"No se pudieron obtener datos para {ticker}")
                return {
                    "ticker": ticker,
                    "technical_score": 50.0,
                    "indicators": None,
                    "current_price": None,
                    "price_change": None,
                    "error": "No se pudieron obtener datos históricos",
                    "timestamp": datetime.now().isoformat()
                }
            
            indicators = await self.get_technical_indicators(ticker)
            if indicators is None:
                return {
                    "ticker": ticker,
                    "technical_score": 50.0,
                    "indicators": None,
                    "current_price": None,
                    "price_change": None,
                    "error": "No se pudieron calcular indicadores",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Obtener precio actual y cambio
            current_price = data['Close'].iloc[-1]
            prev_price = data['Close'].iloc[-2] if len(data) > 1 else current_price
            price_change = ((current_price - prev_price) / prev_price) * 100
            
            # Calcular score técnico
            technical_score = self._calculate_technical_score(indicators, current_price)
            
            # Generar señales interpretables
            signals = self._generate_signals(indicators, current_price)
            
            return {
                "ticker": ticker,
                "technical_score": technical_score,
                "indicators": indicators.dict(),
                "current_price": round(current_price, 2),
                "price_change": round(price_change, 2),
                "signals": signals,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error en análisis técnico para {ticker}: {str(e)}")
            return {
                "ticker": ticker,
                "technical_score": 50.0,
                "indicators": None,
                "current_price": None,
                "price_change": None,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _generate_signals(self, indicators: TechnicalIndicators, current_price: float) -> Dict[str, str]:
        """Genera señales interpretables"""
        signals = {}
        
        # RSI
        if indicators.rsi is not None:
            if indicators.rsi < 30:
                signals['rsi'] = "Sobreventa - Posible compra"
            elif indicators.rsi > 70:
                signals['rsi'] = "Sobrecompra - Precaución"
            else:
                signals['rsi'] = "Neutral"
        
        # MACD
        if indicators.macd is not None and indicators.macd_signal is not None:
            if indicators.macd > indicators.macd_signal:
                signals['macd'] = "Señal alcista"
            else:
                signals['macd'] = "Señal bajista"
        
        # Medias móviles
        if indicators.sma_20 is not None and indicators.sma_50 is not None:
            if current_price > indicators.sma_20 > indicators.sma_50:
                signals['trend'] = "Tendencia alcista"
            elif current_price < indicators.sma_20 < indicators.sma_50:
                signals['trend'] = "Tendencia bajista"
            else:
                signals['trend'] = "Tendencia lateral"
        
        return signals
    
    async def health_check(self) -> bool:
        """Verifica si el servicio está funcionando"""
        try:
            # Test con un ticker conocido
            test_data = await self._get_stock_data("AAPL", period="1mo")
            return test_data is not None and not test_data.empty
        except Exception as e:
            logger.error(f"Health check técnico falló: {str(e)}")
            return False 