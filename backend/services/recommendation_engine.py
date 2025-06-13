import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from config.settings import settings
from models.schemas import (
    RecommendationResponse, 
    TickerAnalysis, 
    ScoreBreakdown, 
    RecommendationLevel
)
from services.technical_analysis import TechnicalAnalyzer
from services.fundamental_analysis import FundamentalAnalyzer
from services.sentiment_analysis import SentimentAnalyzer
from services.macro_analysis import MacroAnalyzer

logger = logging.getLogger(__name__)

class RecommendationEngine:
    """Motor principal de recomendaciones que integra todos los análisis"""
    
    def __init__(self, technical_analyzer: TechnicalAnalyzer, 
                 fundamental_analyzer: FundamentalAnalyzer,
                 sentiment_analyzer: SentimentAnalyzer,
                 macro_analyzer: MacroAnalyzer):
        self.technical_analyzer = technical_analyzer
        self.fundamental_analyzer = fundamental_analyzer
        self.sentiment_analyzer = sentiment_analyzer
        self.macro_analyzer = macro_analyzer
        
    async def generate_daily_recommendations(self) -> List[RecommendationResponse]:
        """Genera recomendaciones diarias para todos los tickers argentinos"""
        recommendations = []
        
        # Obtener contexto macro una sola vez (es el mismo para todos)
        macro_context = await self.macro_analyzer.analyze_macro_context()
        macro_score = macro_context.get('macro_score', 50.0)
        
        logger.info(f"Generando recomendaciones para {len(settings.ARGENTINE_TICKERS)} tickers")
        
        # Procesar tickers en paralelo (en lotes para no sobrecargar APIs)
        batch_size = 3  # Procesar de a 3 para respetar rate limits
        
        for i in range(0, len(settings.ARGENTINE_TICKERS), batch_size):
            batch = settings.ARGENTINE_TICKERS[i:i + batch_size]
            batch_tasks = [
                self._analyze_single_ticker(ticker, macro_score, macro_context)
                for ticker in batch
            ]
            
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            
            for result in batch_results:
                if isinstance(result, Exception):
                    logger.error(f"Error en batch: {result}")
                    continue
                if result:
                    recommendations.append(result)
        
        # Ordenar por score descendente
        recommendations.sort(key=lambda x: x.total_score, reverse=True)
        
        logger.info(f"Generadas {len(recommendations)} recomendaciones")
        return recommendations
    
    async def _analyze_single_ticker(self, ticker: str, macro_score: float, 
                                   macro_context: Dict[str, Any]) -> Optional[RecommendationResponse]:
        """Analiza un ticker individual y genera recomendación"""
        try:
            logger.info(f"Analizando {ticker}...")
            
            # Ejecutar análisis en paralelo
            tasks = [
                self.technical_analyzer.analyze_ticker(ticker),
                self.fundamental_analyzer.analyze_ticker(ticker),
                self.sentiment_analyzer.analyze_ticker_sentiment(ticker)
            ]
            
            tech_result, fund_result, sent_result = await asyncio.gather(
                *tasks, return_exceptions=True
            )
            
            # Manejar excepciones
            if isinstance(tech_result, Exception):
                logger.error(f"Error técnico en {ticker}: {tech_result}")
                tech_result = {"technical_score": 50.0, "current_price": None}
                
            if isinstance(fund_result, Exception):
                logger.error(f"Error fundamental en {ticker}: {fund_result}")
                fund_result = {"fundamental_score": 50.0}
                
            if isinstance(sent_result, Exception):
                logger.error(f"Error sentimiento en {ticker}: {sent_result}")
                sent_result = {"sentiment_score": 50.0}
            
            # Extraer scores
            technical_score = tech_result.get('technical_score', 50.0)
            fundamental_score = fund_result.get('fundamental_score', 50.0)
            sentiment_score = sent_result.get('sentiment_score', 50.0)
            
            # Calcular score total ponderado según el prompt
            total_score = (
                settings.TECHNICAL_WEIGHT * technical_score +
                settings.FUNDAMENTAL_WEIGHT * fundamental_score +
                settings.MACRO_WEIGHT * macro_score +
                settings.SENTIMENT_WEIGHT * sentiment_score
            )
            
            # Determinar nivel de recomendación
            recommendation = self._determine_recommendation_level(total_score)
            
            # Calcular nivel de confianza
            confidence = self._calculate_confidence(
                tech_result, fund_result, sent_result, macro_context
            )
            
            # Obtener información adicional
            current_price = tech_result.get('current_price')
            company_name = fund_result.get('company_profile', {}).get('companyName') if isinstance(fund_result.get('company_profile'), dict) else None
            
            # Determinar color y generar resumen
            color = self._get_recommendation_color(recommendation)
            summary = self._generate_summary(ticker, recommendation, total_score, tech_result, fund_result)
            
            # Calcular precio objetivo (simplificado)
            target_price = self._calculate_target_price(current_price, total_score)
            
            # Determinar nivel de riesgo
            risk_level = self._assess_risk_level(total_score, sentiment_score, macro_score)
            
            return RecommendationResponse(
                ticker=ticker,
                company_name=company_name,
                recommendation=recommendation,
                total_score=round(total_score, 2),
                confidence=confidence,
                technical_score=round(technical_score, 2),
                fundamental_score=round(fundamental_score, 2),
                macro_score=round(macro_score, 2),
                sentiment_score=round(sentiment_score, 2),
                current_price=current_price,
                target_price=target_price,
                risk_level=risk_level,
                color=color,
                summary=summary
            )
            
        except Exception as e:
            logger.error(f"Error procesando {ticker}: {str(e)}")
            # Retornar recomendación neutral en caso de error
            return RecommendationResponse(
                ticker=ticker,
                company_name=None,
                recommendation=RecommendationLevel.MANTENER,
                total_score=50.0,
                confidence=30.0,
                technical_score=50.0,
                fundamental_score=50.0,
                macro_score=macro_score,
                sentiment_score=50.0,
                current_price=None,
                target_price=None,
                risk_level="high",
                color="yellow",
                summary=f"Error analizando {ticker} - recomendación neutral"
            )
    
    def _determine_recommendation_level(self, total_score: float) -> RecommendationLevel:
        """Determina el nivel de recomendación basado en el score total"""
        if total_score >= settings.SCORE_THRESHOLDS["buy"]:
            return RecommendationLevel.COMPRAR
        elif total_score >= settings.SCORE_THRESHOLDS["hold"]:
            return RecommendationLevel.MANTENER
        else:
            return RecommendationLevel.VENDER
    
    def _get_recommendation_color(self, recommendation: RecommendationLevel) -> str:
        """Obtiene el color correspondiente a la recomendación"""
        color_map = {
            RecommendationLevel.COMPRAR: "green",
            RecommendationLevel.MANTENER: "yellow",
            RecommendationLevel.VENDER: "red"
        }
        return color_map.get(recommendation, "yellow")
    
    def _calculate_confidence(self, tech_result: Dict, fund_result: Dict, 
                            sent_result: Dict, macro_context: Dict) -> float:
        """Calcula el nivel de confianza en la recomendación"""
        confidence_factors = []
        
        # Confianza técnica (basada en disponibilidad de indicadores)
        if tech_result.get('indicators'):
            indicators = tech_result['indicators']
            tech_confidence = sum(1 for v in indicators.values() if v is not None) / len(indicators) * 100
            confidence_factors.append(tech_confidence * 0.4)  # Peso técnico
        
        # Confianza fundamental
        if fund_result.get('supported', True):  # Si está soportado por FMP
            confidence_factors.append(80 * 0.3)  # Peso fundamental
        else:
            confidence_factors.append(50 * 0.3)  # Datos limitados
        
        # Confianza de sentimiento
        sent_confidence = sent_result.get('confidence', 0.5) * 100
        confidence_factors.append(sent_confidence * 0.1)  # Peso sentimiento
        
        # Confianza macro (siempre relativamente alta)
        confidence_factors.append(75 * 0.1)  # Peso macro
        
        # Penalizar si hay errores
        if tech_result.get('error') or fund_result.get('error') or sent_result.get('error'):
            confidence_factors = [f * 0.8 for f in confidence_factors]  # Reducir 20%
        
        total_confidence = sum(confidence_factors) if confidence_factors else 50.0
        return round(min(max(total_confidence, 20), 95), 1)  # Entre 20% y 95%
    
    def _generate_summary(self, ticker: str, recommendation: RecommendationLevel, 
                         total_score: float, tech_result: Dict, fund_result: Dict) -> str:
        """Genera un resumen textual de la recomendación"""
        try:
            action_text = {
                RecommendationLevel.COMPRAR: "Recomendado para compra",
                RecommendationLevel.MANTENER: "Mantener posición",
                RecommendationLevel.VENDER: "Considerar venta"
            }
            
            base_text = action_text.get(recommendation, "Sin recomendación")
            
            # Agregar contexto técnico
            tech_context = ""
            if tech_result.get('signals'):
                signals = tech_result['signals']
                if 'rsi' in signals and 'compra' in signals['rsi'].lower():
                    tech_context += " (RSI sobreventa)"
                elif 'trend' in signals and 'alcista' in signals['trend'].lower():
                    tech_context += " (tendencia alcista)"
            
            # Agregar contexto fundamental
            fund_context = ""
            if fund_result.get('supported', True):
                fund_context = " con análisis fundamental"
            else:
                fund_context = " (análisis fundamental limitado)"
            
            # Score context
            score_context = f" - Score: {total_score:.0f}/100"
            
            return f"{base_text}{tech_context}{fund_context}{score_context}"
            
        except Exception as e:
            logger.error(f"Error generando resumen: {str(e)}")
            return f"{ticker}: {recommendation.value} - Score: {total_score:.0f}/100"
    
    def _calculate_target_price(self, current_price: Optional[float], 
                              total_score: float) -> Optional[float]:
        """Calcula precio objetivo simplificado"""
        if not current_price:
            return None
        
        try:
            # Ajuste basado en score (muy simplificado)
            if total_score >= 80:
                multiplier = 1.15  # +15%
            elif total_score >= 70:
                multiplier = 1.10  # +10%
            elif total_score >= 60:
                multiplier = 1.05  # +5%
            elif total_score >= 40:
                multiplier = 1.0   # Sin cambio
            elif total_score >= 30:
                multiplier = 0.95  # -5%
            else:
                multiplier = 0.90  # -10%
            
            return round(current_price * multiplier, 2)
            
        except Exception:
            return None
    
    def _assess_risk_level(self, total_score: float, sentiment_score: float, 
                          macro_score: float) -> str:
        """Evalúa el nivel de riesgo"""
        try:
            # Riesgo bajo si todo está bien
            if total_score >= 70 and sentiment_score >= 60 and macro_score >= 60:
                return "low"
            
            # Riesgo alto si hay problemas importantes
            elif total_score < 40 or sentiment_score < 30 or macro_score < 30:
                return "high"
            
            # Riesgo medio en otros casos
            else:
                return "medium"
                
        except Exception:
            return "medium"
    
    async def analyze_ticker(self, ticker: str) -> TickerAnalysis:
        """Análisis completo y detallado de un ticker específico"""
        try:
            # Obtener contexto macro
            macro_context = await self.macro_analyzer.analyze_macro_context()
            
            # Ejecutar todos los análisis en paralelo
            tasks = [
                self.technical_analyzer.analyze_ticker(ticker),
                self.fundamental_analyzer.analyze_ticker(ticker),
                self.sentiment_analyzer.analyze_ticker_sentiment(ticker, None)
            ]
            
            tech_result, fund_result, sent_result = await asyncio.gather(
                *tasks, return_exceptions=True
            )
            
            # Manejar excepciones
            if isinstance(tech_result, Exception):
                tech_result = {"technical_score": 50.0, "error": str(tech_result)}
            if isinstance(fund_result, Exception):
                fund_result = {"fundamental_score": 50.0, "error": str(fund_result)}
            if isinstance(sent_result, Exception):
                sent_result = {"sentiment_score": 50.0, "error": str(sent_result)}
            
            # Crear score breakdown
            score_breakdown = ScoreBreakdown(
                ticker=ticker,
                technical_score=tech_result.get('technical_score', 50.0),
                fundamental_score=fund_result.get('fundamental_score', 50.0),
                macro_score=macro_context.get('macro_score', 50.0),
                sentiment_score=sent_result.get('sentiment_score', 50.0),
                total_score=self._calculate_total_score(
                    tech_result.get('technical_score', 50.0),
                    fund_result.get('fundamental_score', 50.0),
                    macro_context.get('macro_score', 50.0),
                    sent_result.get('sentiment_score', 50.0)
                ),
                # Detalles técnicos
                rsi=tech_result.get('indicators', {}).get('rsi') if tech_result.get('indicators') else None,
                macd_signal=tech_result.get('signals', {}).get('macd') if tech_result.get('signals') else None,
                # Detalles fundamentales
                roe=fund_result.get('ratios', {}).get('roe') if fund_result.get('ratios') else None,
                debt_to_equity=fund_result.get('ratios', {}).get('debt_to_equity') if fund_result.get('ratios') else None,
                # Detalles macro
                cer_stability=macro_context.get('indicators', {}).get('cer_rate') if macro_context.get('indicators') else None,
                # Detalles sentimiento
                news_sentiment=sent_result.get('overall_sentiment'),
                news_count=sent_result.get('news_count', 0)
            )
            
            # Determinar recomendación
            recommendation = self._determine_recommendation_level(score_breakdown.total_score)
            
            # Información de la empresa
            company_profile = fund_result.get('company_profile', {})
            company_name = company_profile.get('companyName') if isinstance(company_profile, dict) else None
            sector = company_profile.get('sector') if isinstance(company_profile, dict) else None
            market_cap = company_profile.get('mktCap') if isinstance(company_profile, dict) else None
            
            return TickerAnalysis(
                ticker=ticker,
                company_name=company_name,
                sector=sector,
                market_cap=market_cap,
                current_price=tech_result.get('current_price'),
                price_change_24h=tech_result.get('price_change'),
                price_change_percent=tech_result.get('price_change'),
                score_breakdown=score_breakdown,
                recommendation=recommendation,
                technical_indicators=tech_result.get('indicators', {}),
                financial_ratios=fund_result.get('ratios', {}),
                recent_news=sent_result.get('news_items', []),
                macro_context=macro_context,
                recommendation_history=[]  # Implementar si es necesario
            )
            
        except Exception as e:
            logger.error(f"Error en análisis detallado de {ticker}: {str(e)}")
            raise
    
    async def get_score_breakdown(self, ticker: str) -> ScoreBreakdown:
        """Obtiene el desglose detallado de scores para un ticker"""
        analysis = await self.analyze_ticker(ticker)
        return analysis.score_breakdown
    
    def _calculate_total_score(self, technical: float, fundamental: float, 
                             macro: float, sentiment: float) -> float:
        """Calcula el score total ponderado"""
        return (
            settings.TECHNICAL_WEIGHT * technical +
            settings.FUNDAMENTAL_WEIGHT * fundamental +
            settings.MACRO_WEIGHT * macro +
            settings.SENTIMENT_WEIGHT * sentiment
        )
    
    async def close_all_services(self):
        """Cierra todas las conexiones de los servicios"""
        await asyncio.gather(
            self.fundamental_analyzer.close(),
            self.sentiment_analyzer.close(),
            self.macro_analyzer.close(),
            return_exceptions=True
        ) 