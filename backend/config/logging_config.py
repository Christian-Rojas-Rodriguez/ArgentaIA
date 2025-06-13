import logging
import logging.config
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from config.settings import settings


class ColoredFormatter(logging.Formatter):
    """Formatter con colores para la consola"""
    
    # Códigos de color ANSI
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Verde
        'WARNING': '\033[33m',   # Amarillo
        'ERROR': '\033[31m',     # Rojo
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'       # Reset
    }
    
    def format(self, record):
        # Agregar color al nivel
        if record.levelname in self.COLORS:
            record.levelname = (
                f"{self.COLORS[record.levelname]}"
                f"{record.levelname}"
                f"{self.COLORS['RESET']}"
            )
        
        # Formatear timestamp
        record.asctime = datetime.fromtimestamp(record.created).strftime(
            '%Y-%m-%d %H:%M:%S'
        )
        
        return super().format(record)


class StructuredFormatter(logging.Formatter):
    """Formatter estructurado para archivos de log"""
    
    def format(self, record):
        # Crear log estructurado
        log_data = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Agregar información adicional si está disponible
        if hasattr(record, 'ticker'):
            log_data['ticker'] = record.ticker
        if hasattr(record, 'service'):
            log_data['service'] = record.service
        if hasattr(record, 'duration_ms'):
            log_data['duration_ms'] = record.duration_ms
        if hasattr(record, 'api_endpoint'):
            log_data['api_endpoint'] = record.api_endpoint
        
        # Si hay excepción, incluir traceback
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        # Convertir a string JSON-like (sin usar json para mejor rendimiento)
        log_parts = []
        for key, value in log_data.items():
            if isinstance(value, str) and '"' in value:
                value = value.replace('"', '\\"')
            log_parts.append(f'"{key}":"{value}"')
        
        return "{" + ",".join(log_parts) + "}"


def setup_logging() -> None:
    """Configura el sistema de logging para ArgentaIA"""
    
    # Crear directorio de logs si no existe
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configuración base
    config: Dict[str, Any] = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'console': {
                '()': ColoredFormatter,
                'format': '%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s'
            },
            'file': {
                '()': StructuredFormatter,
            },
            'simple': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'console',
                'stream': sys.stdout
            },
            'file_all': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'DEBUG',
                'formatter': 'file',
                'filename': log_dir / 'argenta_ia.log',
                'maxBytes': 10_000_000,  # 10MB
                'backupCount': 5,
                'encoding': 'utf8'
            },
            'file_errors': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'ERROR',
                'formatter': 'file',
                'filename': log_dir / 'errors.log',
                'maxBytes': 5_000_000,   # 5MB
                'backupCount': 3,
                'encoding': 'utf8'
            },
            'file_analysis': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'INFO',
                'formatter': 'simple',
                'filename': log_dir / 'analysis.log',
                'maxBytes': 20_000_000,  # 20MB
                'backupCount': 10,
                'encoding': 'utf8'
            }
        },
        'loggers': {
            # Logger raíz
            '': {
                'level': settings.LOG_LEVEL,
                'handlers': ['console', 'file_all', 'file_errors']
            },
            # Logger específico para análisis
            'analysis': {
                'level': 'INFO',
                'handlers': ['file_analysis'],
                'propagate': False
            },
            # Loggers de servicios
            'services.technical_analysis': {
                'level': 'INFO',
                'handlers': ['console', 'file_all'],
                'propagate': False
            },
            'services.fundamental_analysis': {
                'level': 'INFO',
                'handlers': ['console', 'file_all'],
                'propagate': False
            },
            'services.sentiment_analysis': {
                'level': 'INFO',
                'handlers': ['console', 'file_all'],
                'propagate': False
            },
            'services.macro_analysis': {
                'level': 'INFO',
                'handlers': ['console', 'file_all'],
                'propagate': False
            },
            'services.recommendation_engine': {
                'level': 'INFO',
                'handlers': ['console', 'file_all'],
                'propagate': False
            },
            # Silenciar logs verbosos de librerías externas
            'urllib3.connectionpool': {
                'level': 'WARNING',
                'propagate': True
            },
            'transformers': {
                'level': 'WARNING',
                'propagate': True
            },
            'yfinance': {
                'level': 'WARNING',
                'propagate': True
            }
        }
    }
    
    # Aplicar configuración
    logging.config.dictConfig(config)
    
    # Log inicial
    logger = logging.getLogger('argenta_ia.setup')
    logger.info("🚀 Sistema de logging configurado correctamente")
    logger.info(f"📂 Logs guardándose en: {log_dir.absolute()}")
    logger.info(f"📊 Nivel de log: {settings.LOG_LEVEL}")


def get_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger configurado para un módulo específico
    
    Args:
        name: Nombre del módulo (ej: 'services.technical_analysis')
    
    Returns:
        Logger configurado
    """
    return logging.getLogger(name)


def log_analysis_start(logger: logging.Logger, ticker: str, analysis_type: str) -> None:
    """Helper para loggear inicio de análisis"""
    logger.info(
        f"🔍 Iniciando análisis {analysis_type} para {ticker}",
        extra={'ticker': ticker, 'service': analysis_type}
    )


def log_analysis_end(logger: logging.Logger, ticker: str, analysis_type: str, 
                    duration_ms: float, success: bool = True) -> None:
    """Helper para loggear fin de análisis"""
    status = "✅" if success else "❌"
    logger.info(
        f"{status} Análisis {analysis_type} completado para {ticker} en {duration_ms:.2f}ms",
        extra={
            'ticker': ticker, 
            'service': analysis_type,
            'duration_ms': duration_ms,
            'success': success
        }
    )


def log_api_call(logger: logging.Logger, endpoint: str, status_code: int, 
                duration_ms: float) -> None:
    """Helper para loggear llamadas a APIs externas"""
    level = logging.INFO if 200 <= status_code < 300 else logging.WARNING
    logger.log(
        level,
        f"🌐 API call: {endpoint} -> {status_code} ({duration_ms:.2f}ms)",
        extra={
            'api_endpoint': endpoint,
            'status_code': status_code,
            'duration_ms': duration_ms
        }
    )


def log_score_calculation(logger: logging.Logger, ticker: str, scores: dict) -> None:
    """Helper para loggear cálculo de scores"""
    logger.info(
        f"🎯 Scores calculados para {ticker}: "
        f"Técnico={scores.get('technical', 0):.1f}, "
        f"Fundamental={scores.get('fundamental', 0):.1f}, "
        f"Macro={scores.get('macro', 0):.1f}, "
        f"Sentimiento={scores.get('sentiment', 0):.1f}, "
        f"Total={scores.get('total', 0):.1f}",
        extra={'ticker': ticker, 'scores': scores}
    ) 