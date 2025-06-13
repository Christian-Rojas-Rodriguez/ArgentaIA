from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class RecommendationLevel(str, Enum):
    COMPRAR = "comprar"
    MANTENER = "mantener"
    VENDER = "vender"

class ScoreBreakdown(BaseModel):
    """Desglose detallado de scores por categoría"""
    ticker: str
    technical_score: float = Field(..., ge=0, le=100, description="Score técnico (0-100)")
    fundamental_score: float = Field(..., ge=0, le=100, description="Score fundamental (0-100)")
    macro_score: float = Field(..., ge=0, le=100, description="Score macro (0-100)")
    sentiment_score: float = Field(..., ge=0, le=100, description="Score de sentimiento (0-100)")
    total_score: float = Field(..., ge=0, le=100, description="Score final ponderado")
    
    # Detalles técnicos
    rsi: Optional[float] = None
    macd_signal: Optional[str] = None
    moving_average_trend: Optional[str] = None
    
    # Detalles fundamentales
    roe: Optional[float] = None
    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None
    pe_ratio: Optional[float] = None
    
    # Detalles macro
    cer_stability: Optional[float] = None
    usd_stability: Optional[float] = None
    inflation_impact: Optional[float] = None
    
    # Detalles sentimiento
    news_sentiment: Optional[str] = None
    news_count: Optional[int] = None
    
    timestamp: datetime = Field(default_factory=datetime.now)

class RecommendationResponse(BaseModel):
    """Respuesta de recomendación de inversión"""
    ticker: str
    company_name: Optional[str] = None
    recommendation: RecommendationLevel
    total_score: float = Field(..., ge=0, le=100)
    confidence: float = Field(..., ge=0, le=100, description="Nivel de confianza en la recomendación")
    
    # Scores individuales
    technical_score: float
    fundamental_score: float
    macro_score: float
    sentiment_score: float
    
    # Información adicional
    current_price: Optional[float] = None
    target_price: Optional[float] = None
    risk_level: str = Field(default="medium", description="low, medium, high")
    
    # Datos para la UI
    color: str = Field(description="Color para la UI: green, yellow, red")
    summary: str = Field(description="Resumen de la recomendación")
    
    timestamp: datetime = Field(default_factory=datetime.now)

class TickerAnalysis(BaseModel):
    """Análisis completo y detallado de un ticker"""
    ticker: str
    company_name: Optional[str] = None
    sector: Optional[str] = None
    market_cap: Optional[float] = None
    
    # Información de precios
    current_price: Optional[float] = None
    price_change_24h: Optional[float] = None
    price_change_percent: Optional[float] = None
    
    # Análisis detallado
    score_breakdown: ScoreBreakdown
    recommendation: RecommendationLevel
    
    # Análisis técnico detallado
    technical_indicators: Dict[str, Any] = Field(default_factory=dict)
    
    # Análisis fundamental detallado
    financial_ratios: Dict[str, Any] = Field(default_factory=dict)
    
    # Noticias recientes
    recent_news: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Contexto macro
    macro_context: Dict[str, Any] = Field(default_factory=dict)
    
    # Histórico de recomendaciones (últimos 30 días)
    recommendation_history: List[Dict[str, Any]] = Field(default_factory=list)
    
    timestamp: datetime = Field(default_factory=datetime.now)

class TechnicalIndicators(BaseModel):
    """Indicadores técnicos específicos"""
    rsi: Optional[float] = None
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    macd_histogram: Optional[float] = None
    sma_20: Optional[float] = None
    sma_50: Optional[float] = None
    sma_200: Optional[float] = None
    bollinger_upper: Optional[float] = None
    bollinger_lower: Optional[float] = None
    volume_sma: Optional[float] = None
    
class FundamentalRatios(BaseModel):
    """Ratios fundamentales de una empresa"""
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    roe: Optional[float] = None
    roa: Optional[float] = None
    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None
    gross_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    net_margin: Optional[float] = None
    piotroski_score: Optional[int] = None
    
class NewsItem(BaseModel):
    """Item de noticia para análisis de sentimiento"""
    title: str
    description: Optional[str] = None
    url: Optional[str] = None
    published_at: datetime
    source: str
    sentiment: Optional[str] = None  # positive, negative, neutral
    sentiment_score: Optional[float] = None

class MacroIndicators(BaseModel):
    """Indicadores macroeconómicos"""
    cer_rate: Optional[float] = None
    usd_rate: Optional[float] = None
    inflation_rate: Optional[float] = None
    country_risk: Optional[float] = None
    stability_score: Optional[float] = None
    
class APIStatus(BaseModel):
    """Status de un servicio/API"""
    service_name: str
    status: str  # healthy, degraded, down
    last_check: datetime
    error_message: Optional[str] = None
    response_time_ms: Optional[float] = None 