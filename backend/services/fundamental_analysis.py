import asyncio
import aiohttp
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

from config.settings import settings
from models.schemas import FundamentalRatios

logger = logging.getLogger(__name__)

class FundamentalAnalyzer:
    """Analizador de datos fundamentales usando FMP API"""
    
    def __init__(self):
        self.base_url = settings.FMP_BASE_URL
        self.api_key = settings.FMP_API_KEY
        self.session: Optional[aiohttp.ClientSession] = None
        self.last_request_time = {}  # Para rate limiting
        
    async def _get_session(self) -> aiohttp.ClientSession:
        """Obtiene o crea una sesión HTTP"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30)
            )
        return self.session
    
    async def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Hace una request a la API de FMP con rate limiting"""
        if not self.api_key:
            logger.warning("FMP API key no configurada")
            return None
            
        # Rate limiting básico
        now = datetime.now()
        if endpoint in self.last_request_time:
            time_since_last = (now - self.last_request_time[endpoint]).total_seconds()
            if time_since_last < 1:  # Min 1 segundo entre requests al mismo endpoint
                await asyncio.sleep(1 - time_since_last)
        
        self.last_request_time[endpoint] = now
        
        url = f"{self.base_url}/{endpoint}"
        params = params or {}
        params['apikey'] = self.api_key
        
        try:
            session = await self._get_session()
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                elif response.status == 429:
                    logger.warning(f"Rate limit alcanzado para FMP API: {endpoint}")
                    return None
                else:
                    logger.error(f"Error en FMP API: {response.status} - {await response.text()}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error conectando a FMP API: {str(e)}")
            return None
    
    async def get_financial_ratios(self, ticker: str) -> Optional[FundamentalRatios]:
        """Obtiene ratios financieros de un ticker"""
        try:
            # Obtener ratios clave
            ratios_data = await self._make_request(f"ratios/{ticker}")
            
            if not ratios_data or not isinstance(ratios_data, list) or len(ratios_data) == 0:
                logger.warning(f"No se encontraron ratios para {ticker}")
                return None
                
            # Tomar los datos más recientes (primer elemento)
            latest_ratios = ratios_data[0]
            
            return FundamentalRatios(
                pe_ratio=latest_ratios.get('priceEarningsRatio'),
                pb_ratio=latest_ratios.get('priceToBookRatio'),
                roe=latest_ratios.get('returnOnEquity'),
                roa=latest_ratios.get('returnOnAssets'),
                debt_to_equity=latest_ratios.get('debtEquityRatio'),
                current_ratio=latest_ratios.get('currentRatio'),
                quick_ratio=latest_ratios.get('quickRatio'),
                gross_margin=latest_ratios.get('grossProfitMargin'),
                operating_margin=latest_ratios.get('operatingProfitMargin'),
                net_margin=latest_ratios.get('netProfitMargin'),
            )
            
        except Exception as e:
            logger.error(f"Error obteniendo ratios fundamentales para {ticker}: {str(e)}")
            return None
    
    async def get_company_profile(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Obtiene el perfil de la empresa"""
        try:
            profile_data = await self._make_request(f"profile/{ticker}")
            
            if not profile_data or not isinstance(profile_data, list) or len(profile_data) == 0:
                return None
                
            return profile_data[0]
            
        except Exception as e:
            logger.error(f"Error obteniendo perfil para {ticker}: {str(e)}")
            return None
    
    def _calculate_fundamental_score(self, ratios: FundamentalRatios) -> float:
        """
        Calcula el score fundamental basado en ratios
        Implementa la lógica del prompt: ROE alto + deuda baja + liquidez buena
        """
        if not ratios:
            return 50.0  # Score neutral si no hay datos
            
        score = 0.0
        max_score = 100.0
        
        # ROE (Return on Equity) - Peso 40%
        if ratios.roe is not None:
            if ratios.roe > 15:      # ROE excelente
                score += 40
            elif ratios.roe > 10:    # ROE bueno
                score += 30
            elif ratios.roe > 5:     # ROE regular
                score += 20
            elif ratios.roe > 0:     # ROE positivo pero bajo
                score += 10
            # ROE negativo = 0 puntos
        else:
            score += 20  # Penalty por falta de datos, pero no severa
            
        # Debt to Equity - Peso 30%
        if ratios.debt_to_equity is not None:
            if ratios.debt_to_equity < 0.5:      # Muy poca deuda
                score += 30
            elif ratios.debt_to_equity < 1.0:    # Deuda controlada
                score += 25
            elif ratios.debt_to_equity < 1.5:    # Deuda moderada
                score += 15
            elif ratios.debt_to_equity < 2.0:    # Deuda alta
                score += 5
            # Deuda muy alta = 0 puntos
        else:
            score += 15  # Penalty menor
            
        # Current Ratio (Liquidez) - Peso 30%
        if ratios.current_ratio is not None:
            if ratios.current_ratio > 2.0:       # Liquidez excelente
                score += 30
            elif ratios.current_ratio > 1.5:     # Liquidez buena
                score += 25
            elif ratios.current_ratio > 1.2:     # Liquidez aceptable
                score += 20
            elif ratios.current_ratio > 1.0:     # Liquidez justa
                score += 10
            # Liquidez problemática = 0 puntos
        else:
            score += 15  # Penalty menor
            
        # Bonificaciones por otros indicadores
        if ratios.pe_ratio is not None and 5 < ratios.pe_ratio < 20:
            score += 5  # PE ratio razonable
            
        if ratios.gross_margin is not None and ratios.gross_margin > 0.3:
            score += 5  # Buenos márgenes
            
        return min(score, max_score)
    
    async def analyze_ticker(self, ticker: str) -> Dict[str, Any]:
        """Análisis fundamental completo de un ticker"""
        if ticker not in settings.FMP_SUPPORTED_TICKERS:
            logger.info(f"Ticker {ticker} no soportado por FMP, usando score neutral")
            return {
                "ticker": ticker,
                "fundamental_score": 50.0,
                "ratios": None,
                "company_profile": None,
                "supported": False,
                "message": "Ticker no disponible en FMP - usando score neutral"
            }
        
        # Obtener datos en paralelo
        ratios_task = self.get_financial_ratios(ticker)
        profile_task = self.get_company_profile(ticker)
        
        ratios, profile = await asyncio.gather(ratios_task, profile_task, return_exceptions=True)
        
        # Manejar excepciones
        if isinstance(ratios, Exception):
            logger.error(f"Error obteniendo ratios: {ratios}")
            ratios = None
            
        if isinstance(profile, Exception):
            logger.error(f"Error obteniendo perfil: {profile}")
            profile = None
        
        # Calcular score
        fundamental_score = self._calculate_fundamental_score(ratios)
        
        return {
            "ticker": ticker,
            "fundamental_score": fundamental_score,
            "ratios": ratios.dict() if ratios else None,
            "company_profile": profile,
            "supported": True,
            "timestamp": datetime.now().isoformat()
        }
    
    async def health_check(self) -> bool:
        """Verifica si el servicio está funcionando"""
        try:
            if not self.api_key:
                return False
                
            # Test con un ticker conocido
            test_data = await self._make_request("profile/AAPL")  # Ticker siempre disponible
            return test_data is not None
            
        except Exception as e:
            logger.error(f"Health check falló: {str(e)}")
            return False
    
    async def close(self):
        """Cierra las conexiones"""
        if self.session and not self.session.closed:
            await self.session.close() 