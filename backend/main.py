from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import asyncio
from datetime import datetime, timedelta

# Importar módulos propios
from config.logging_config import setup_logging, get_logger
from services.technical_analysis import TechnicalAnalyzer
from services.fundamental_analysis import FundamentalAnalyzer
from services.sentiment_analysis import SentimentAnalyzer
from services.macro_analysis import MacroAnalyzer
from services.recommendation_engine import RecommendationEngine
from models.schemas import RecommendationResponse, TickerAnalysis, ScoreBreakdown

# Configurar logging
setup_logging()
logger = get_logger('argenta_ia.main')

app = FastAPI(
    title="ArgentaIA Investment API",
    description="API para análisis de inversiones con AI - Técnico, Fundamental, Macro y Sentimiento",
    version="1.0.0"
)

# Configurar CORS para el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Puertos comunes de Next.js
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar servicios
technical_analyzer = TechnicalAnalyzer()
fundamental_analyzer = FundamentalAnalyzer()
sentiment_analyzer = SentimentAnalyzer()
macro_analyzer = MacroAnalyzer()
recommendation_engine = RecommendationEngine(
    technical_analyzer,
    fundamental_analyzer,
    sentiment_analyzer,
    macro_analyzer
)

@app.get("/")
async def root():
    """Endpoint de salud de la API"""
    return {
        "message": "ArgentaIA Investment API",
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/recommendations/daily", response_model=List[RecommendationResponse])
async def get_daily_recommendations():
    """
    Obtiene las recomendaciones diarias de inversión con scoring completo
    """
    try:
        logger.info("Generando recomendaciones diarias...")
        recommendations = await recommendation_engine.generate_daily_recommendations()
        return recommendations
    except Exception as e:
        logger.error(f"Error generando recomendaciones: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.get("/api/analysis/{ticker}", response_model=TickerAnalysis)
async def get_ticker_analysis(ticker: str):
    """
    Análisis detallado de un ticker específico
    """
    try:
        ticker = ticker.upper()
        logger.info(f"Analizando ticker: {ticker}")
        
        analysis = await recommendation_engine.analyze_ticker(ticker)
        return analysis
    except Exception as e:
        logger.error(f"Error analizando {ticker}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analizando {ticker}: {str(e)}")

@app.get("/api/scores/{ticker}", response_model=ScoreBreakdown)
async def get_score_breakdown(ticker: str):
    """
    Desglose detallado de scores por categoría para un ticker
    """
    try:
        ticker = ticker.upper()
        breakdown = await recommendation_engine.get_score_breakdown(ticker)
        return breakdown
    except Exception as e:
        logger.error(f"Error obteniendo breakdown de {ticker}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error obteniendo scores de {ticker}: {str(e)}")

@app.get("/api/health")
async def health_check():
    """
    Endpoint de salud detallado con status de servicios
    """
    services_status = {
        "technical": await technical_analyzer.health_check(),
        "fundamental": await fundamental_analyzer.health_check(),
        "sentiment": await sentiment_analyzer.health_check(),
        "macro": await macro_analyzer.health_check()
    }
    
    all_healthy = all(services_status.values())
    
    return {
        "status": "healthy" if all_healthy else "degraded",
        "timestamp": datetime.now().isoformat(),
        "services": services_status
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 