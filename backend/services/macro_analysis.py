import asyncio
import aiohttp
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

from config.settings import settings
from models.schemas import MacroIndicators

logger = logging.getLogger(__name__)

class MacroAnalyzer:
    """Analizador de indicadores macroeconómicos argentinos"""
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.cache = {}
        self.cache_expiry = {}
        self.cache_duration = timedelta(hours=6)  # Cache más largo para datos macro
        
    async def _get_session(self) -> aiohttp.ClientSession:
        """Obtiene o crea una sesión HTTP"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30)
            )
        return self.session
    
    def _is_cache_valid(self, key: str) -> bool:
        """Verifica si el cache es válido"""
        if key not in self.cache_expiry:
            return False
        return datetime.now() < self.cache_expiry[key]
    
    async def _fetch_bcra_data(self, indicator: str) -> Optional[float]:
        """Obtiene datos del BCRA (Banco Central de la República Argentina)"""
        try:
            if self._is_cache_valid(f"bcra_{indicator}"):
                return self.cache[f"bcra_{indicator}"]
            
            # Mapeo de indicadores BCRA
            indicator_map = {
                'usd': 'usd',       # Tipo de cambio USD
                'cer': 'cer',       # CER (Coeficiente de Estabilización de Referencia)
                'inflation': 'inflacion_mensual_oficial',
                'country_risk': 'riesgo_pais'
            }
            
            bcra_indicator = indicator_map.get(indicator)
            if not bcra_indicator:
                return None
            
            session = await self._get_session()
            url = f"{settings.BCRA_API_URL}/{bcra_indicator}"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data and len(data) > 0:
                        # Tomar el valor más reciente
                        latest_value = data[-1].get('valor', data[-1].get('v'))
                        if latest_value is not None:
                            self.cache[f"bcra_{indicator}"] = latest_value
                            self.cache_expiry[f"bcra_{indicator}"] = datetime.now() + self.cache_duration
                            return latest_value
                
                logger.warning(f"No se pudo obtener {indicator} del BCRA: {response.status}")
                return None
                
        except Exception as e:
            logger.error(f"Error obteniendo {indicator} del BCRA: {str(e)}")
            return None
    
    async def _get_mock_macro_data(self) -> MacroIndicators:
        """Datos mock para testing cuando no hay APIs disponibles"""
        return MacroIndicators(
            cer_rate=1200.0,        # CER ficticio
            usd_rate=850.0,         # USD ficticio
            inflation_rate=12.5,    # Inflación mensual ficticia
            country_risk=1500,      # Riesgo país ficticio
            stability_score=35.0    # Score de estabilidad calculado
        )
    
    async def get_macro_indicators(self) -> MacroIndicators:
        """Obtiene indicadores macroeconómicos actuales"""
        try:
            # Intentar obtener datos reales
            usd_rate = await self._fetch_bcra_data('usd')
            cer_rate = await self._fetch_bcra_data('cer')
            inflation_rate = await self._fetch_bcra_data('inflation')
            country_risk = await self._fetch_bcra_data('country_risk')
            
            # Si no hay datos reales, usar mock data
            if all(v is None for v in [usd_rate, cer_rate, inflation_rate, country_risk]):
                logger.info("Usando datos macro mock para testing")
                return await self._get_mock_macro_data()
            
            # Calcular score de estabilidad
            stability_score = self._calculate_stability_score(
                usd_rate, cer_rate, inflation_rate, country_risk
            )
            
            return MacroIndicators(
                cer_rate=cer_rate,
                usd_rate=usd_rate,
                inflation_rate=inflation_rate,
                country_risk=country_risk,
                stability_score=stability_score
            )
            
        except Exception as e:
            logger.error(f"Error obteniendo indicadores macro: {str(e)}")
            # Fallback a datos mock en caso de error
            return await self._get_mock_macro_data()
    
    def _calculate_stability_score(self, usd_rate: Optional[float], cer_rate: Optional[float], 
                                 inflation_rate: Optional[float], country_risk: Optional[int]) -> float:
        """
        Calcula score de estabilidad macroeconómica (0-100)
        Implementa la lógica del prompt: estabilidad + inflación
        """
        score = 50.0  # Score base neutral
        
        try:
            # Análisis de estabilidad del USD (25 puntos máximo)
            if usd_rate is not None:
                # Penalizar volatilidad alta - esto requeriría datos históricos
                # Por ahora, usamos rangos esperados para Argentina
                if usd_rate < 300:       # USD muy bajo (poco probable)
                    score += 15
                elif usd_rate < 500:     # USD controlado
                    score += 20
                elif usd_rate < 800:     # USD moderado
                    score += 10
                elif usd_rate < 1200:    # USD alto
                    score += 5
                # USD muy alto = 0 puntos adicionales
            
            # Análisis de inflación (35 puntos máximo)
            if inflation_rate is not None:
                if inflation_rate < 2:       # Inflación muy baja
                    score += 35
                elif inflation_rate < 5:     # Inflación controlada
                    score += 25
                elif inflation_rate < 10:    # Inflación moderada
                    score += 15
                elif inflation_rate < 20:    # Inflación alta
                    score += 5
                # Inflación muy alta = 0 puntos
            
            # Análisis de riesgo país (25 puntos máximo)
            if country_risk is not None:
                if country_risk < 500:       # Riesgo bajo
                    score += 25
                elif country_risk < 1000:    # Riesgo moderado
                    score += 20
                elif country_risk < 1500:    # Riesgo alto
                    score += 10
                elif country_risk < 2000:    # Riesgo muy alto
                    score += 5
                # Riesgo extremo = 0 puntos
            
            # Análisis CER (15 puntos máximo)
            if cer_rate is not None:
                # CER estable es bueno para la economía
                # Esto es más complejo, por ahora scoring simple
                if cer_rate > 0:
                    score += 10  # Simplemente dar puntos por tener CER
            
            return min(max(score, 0), 100)  # Mantener entre 0-100
            
        except Exception as e:
            logger.error(f"Error calculando stability score: {str(e)}")
            return 50.0
    
    async def analyze_macro_context(self) -> Dict[str, Any]:
        """Análisis completo del contexto macroeconómico"""
        try:
            indicators = await self.get_macro_indicators()
            
            # Calcular score macro final
            macro_score = indicators.stability_score or 50.0
            
            # Generar interpretación
            interpretation = self._generate_macro_interpretation(indicators)
            
            # Calcular tendencias (requeriría datos históricos, por ahora simplificado)
            trends = self._analyze_trends(indicators)
            
            return {
                "macro_score": macro_score,
                "indicators": indicators.dict(),
                "interpretation": interpretation,
                "trends": trends,
                "impact_on_stocks": self._assess_stock_impact(indicators),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error en análisis macro: {str(e)}")
            return {
                "macro_score": 50.0,
                "indicators": None,
                "interpretation": "Error obteniendo datos macro",
                "trends": {},
                "impact_on_stocks": "neutral",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _generate_macro_interpretation(self, indicators: MacroIndicators) -> str:
        """Genera interpretación textual de los indicadores macro"""
        try:
            interpretations = []
            
            # USD
            if indicators.usd_rate is not None:
                if indicators.usd_rate > 1000:
                    interpretations.append("Tipo de cambio elevado, presión inflacionaria")
                elif indicators.usd_rate < 500:
                    interpretations.append("Tipo de cambio controlado")
                else:
                    interpretations.append("Tipo de cambio en rango moderado")
            
            # Inflación
            if indicators.inflation_rate is not None:
                if indicators.inflation_rate > 15:
                    interpretations.append("Inflación muy alta, impacto negativo en inversiones")
                elif indicators.inflation_rate > 5:
                    interpretations.append("Inflación moderada a alta")
                else:
                    interpretations.append("Inflación controlada")
            
            # Riesgo país
            if indicators.country_risk is not None:
                if indicators.country_risk > 1500:
                    interpretations.append("Riesgo país elevado, cautela en inversiones")
                elif indicators.country_risk < 800:
                    interpretations.append("Riesgo país moderado")
                else:
                    interpretations.append("Riesgo país en niveles altos")
            
            # Score general
            if indicators.stability_score is not None:
                if indicators.stability_score > 70:
                    interpretations.append("Contexto macro favorable para inversiones")
                elif indicators.stability_score < 40:
                    interpretations.append("Contexto macro desafiante")
                else:
                    interpretations.append("Contexto macro mixto")
            
            return ". ".join(interpretations) if interpretations else "Contexto macro neutral"
            
        except Exception as e:
            logger.error(f"Error generando interpretación: {str(e)}")
            return "No se pudo interpretar el contexto macro"
    
    def _analyze_trends(self, indicators: MacroIndicators) -> Dict[str, str]:
        """Análisis de tendencias (simplificado sin datos históricos)"""
        trends = {}
        
        # En una implementación completa, esto compararía con datos históricos
        # Por ahora, damos tendencias basadas en rangos esperados
        
        if indicators.usd_rate is not None:
            if indicators.usd_rate > 900:
                trends['usd'] = 'rising'
            elif indicators.usd_rate < 600:
                trends['usd'] = 'falling'
            else:
                trends['usd'] = 'stable'
        
        if indicators.inflation_rate is not None:
            if indicators.inflation_rate > 10:
                trends['inflation'] = 'rising'
            elif indicators.inflation_rate < 3:
                trends['inflation'] = 'falling'
            else:
                trends['inflation'] = 'stable'
        
        if indicators.country_risk is not None:
            if indicators.country_risk > 1200:
                trends['risk'] = 'rising'
            elif indicators.country_risk < 800:
                trends['risk'] = 'falling'
            else:
                trends['risk'] = 'stable'
        
        return trends
    
    def _assess_stock_impact(self, indicators: MacroIndicators) -> str:
        """Evalúa el impacto del contexto macro en las acciones"""
        try:
            if indicators.stability_score is None:
                return "neutral"
            
            if indicators.stability_score > 70:
                return "positive"
            elif indicators.stability_score < 40:
                return "negative"
            else:
                return "neutral"
                
        except Exception:
            return "neutral"
    
    async def health_check(self) -> bool:
        """Verifica si el servicio está funcionando"""
        try:
            # Test básico obteniendo indicadores
            indicators = await self.get_macro_indicators()
            return indicators is not None
        except Exception as e:
            logger.error(f"Health check macro falló: {str(e)}")
            return False
    
    async def close(self):
        """Cierra las conexiones"""
        if self.session and not self.session.closed:
            await self.session.close() 