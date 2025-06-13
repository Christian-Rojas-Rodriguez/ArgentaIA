import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # API Keys
    FMP_API_KEY: str = os.getenv("FMP_API_KEY", "")
    GNEWS_API_KEY: str = os.getenv("GNEWS_API_KEY", "")
    
    # URLs de APIs
    FMP_BASE_URL: str = "https://financialmodelingprep.com/api/v3"
    GNEWS_BASE_URL: str = "https://gnews.io/api/v4"
    
    # Configuración de la aplicación
    APP_NAME: str = "ArgentaIA Investment API"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001"
    ]
    
    # Configuración de análisis
    TECHNICAL_WEIGHT: float = 0.5
    FUNDAMENTAL_WEIGHT: float = 0.3
    MACRO_WEIGHT: float = 0.1
    SENTIMENT_WEIGHT: float = 0.1
    
    # Rate limits
    FMP_DAILY_LIMIT: int = 250
    GNEWS_DAILY_LIMIT: int = 100
    
    # Tickers principales argentinos
    ARGENTINE_TICKERS: List[str] = [
        "YPF",      # YPF S.A.
        "GGAL",     # Grupo Galicia
        "PAM",      # Pampa Energía
        "TEO",      # Telecom Argentina
        "TGS",      # Transportadora de Gas del Sur
        "CEPU",     # Central Puerto
        "BMA",      # Banco Macro
        "SUPV",     # Supervielle
        "CRESY",    # Cresud
        "LOMA",     # Loma Negra
        "IRCP",     # IRSA Propiedades Comerciales
        "VIST",     # Vista Oil & Gas
        "MELI",     # MercadoLibre (aunque es más regional)
        "GLOB",     # Globant (aunque es más global)
        "DESP",     # Despegar.com
    ]
    
    # ADRs para análisis fundamental con FMP
    FMP_SUPPORTED_TICKERS: List[str] = [
        "YPF", "GGAL", "PAM", "TEO", "TGS", "CEPU", 
        "BMA", "SUPV", "CRESY", "LOMA", "IRCP", "VIST",
        "MELI", "GLOB", "DESP"
    ]
    
    # Configuración de sentimiento
    SENTIMENT_MODEL: str = "finiteautomata/beto-sentiment-analysis"
    MAX_NEWS_PER_TICKER: int = 10
    NEWS_DAYS_LOOKBACK: int = 7
    
    # Configuración de scoring
    SCORE_THRESHOLDS: dict = {
        "buy": 70,      # >= 70 = COMPRAR (verde)
        "hold": 40,     # 40-69 = MANTENER (amarillo)  
        "sell": 0       # < 40 = VENDER (rojo)
    }
    
    # Configuración macro (APIs públicas argentinas)
    BCRA_API_URL: str = "https://api.estadisticasbcra.com"
    
    # Cache settings
    CACHE_EXPIRY_MINUTES: int = 30
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Instancia global de configuración
settings = Settings()

# Validaciones
def validate_settings():
    """Valida que las configuraciones críticas estén presentes"""
    warnings = []
    errors = []
    
    if not settings.FMP_API_KEY:
        warnings.append("FMP_API_KEY no configurada - análisis fundamental limitado")
    
    if not settings.GNEWS_API_KEY:
        warnings.append("GNEWS_API_KEY no configurada - análisis de sentimiento limitado")
    
    # Validar que los pesos sumen 1.0
    total_weight = (
        settings.TECHNICAL_WEIGHT + 
        settings.FUNDAMENTAL_WEIGHT + 
        settings.MACRO_WEIGHT + 
        settings.SENTIMENT_WEIGHT
    )
    
    if abs(total_weight - 1.0) > 0.01:
        errors.append(f"Los pesos de análisis deben sumar 1.0, actual: {total_weight}")
    
    return {
        "warnings": warnings,
        "errors": errors,
        "is_valid": len(errors) == 0
    }

# Ejecutar validación al importar
_validation = validate_settings()
if _validation["errors"]:
    raise ValueError(f"Errores de configuración: {_validation['errors']}")

if _validation["warnings"] and settings.DEBUG:
    print(f"Advertencias de configuración: {_validation['warnings']}") 