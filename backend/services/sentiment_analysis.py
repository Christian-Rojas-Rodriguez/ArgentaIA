import asyncio
import aiohttp
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import re

from config.settings import settings
from models.schemas import NewsItem

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """Analizador de sentimiento usando noticias y BERT"""
    
    def __init__(self):
        self.gnews_api_key = settings.GNEWS_API_KEY
        self.gnews_base_url = settings.GNEWS_BASE_URL
        self.session: Optional[aiohttp.ClientSession] = None
        self.sentiment_pipeline = None
        self.last_request_time = {}
        
    async def _get_session(self) -> aiohttp.ClientSession:
        """Obtiene o crea una sesión HTTP"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30)
            )
        return self.session
    
    def _load_sentiment_model(self):
        """Carga el modelo de sentimiento BERT (lazy loading)"""
        if self.sentiment_pipeline is None:
            try:
                from transformers import pipeline
                logger.info(f"Cargando modelo de sentimiento: {settings.SENTIMENT_MODEL}")
                self.sentiment_pipeline = pipeline(
                    "sentiment-analysis", 
                    model=settings.SENTIMENT_MODEL,
                    device=-1  # CPU para evitar problemas de GPU
                )
                logger.info("Modelo de sentimiento cargado exitosamente")
            except Exception as e:
                logger.error(f"Error cargando modelo de sentimiento: {str(e)}")
                # Fallback a un análisis básico de palabras clave
                self.sentiment_pipeline = "fallback"
    
    async def _get_news_gnews(self, ticker: str, company_name: str = None) -> List[NewsItem]:
        """Obtiene noticias de GNews API"""
        if not self.gnews_api_key:
            logger.warning("GNews API key no configurada")
            return []
        
        # Rate limiting
        now = datetime.now()
        if "gnews" in self.last_request_time:
            time_since_last = (now - self.last_request_time["gnews"]).total_seconds()
            if time_since_last < 2:  # 2 segundos entre requests
                await asyncio.sleep(2 - time_since_last)
        
        self.last_request_time["gnews"] = now
        
        try:
            # Construir query de búsqueda
            search_terms = [ticker]
            if company_name:
                search_terms.append(company_name)
            
            # Agregar términos específicos para empresas argentinas
            if ticker in ["YPF", "GGAL", "PAM", "TEO", "TGS"]:
                search_terms.append("Argentina")
            
            query = " OR ".join(search_terms)
            
            params = {
                'q': query,
                'lang': 'es',
                'country': 'ar',
                'max': min(settings.MAX_NEWS_PER_TICKER, 10),  # GNews free tier
                'from': (datetime.now() - timedelta(days=settings.NEWS_DAYS_LOOKBACK)).isoformat(),
                'token': self.gnews_api_key
            }
            
            session = await self._get_session()
            async with session.get(f"{self.gnews_base_url}/search", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    articles = data.get('articles', [])
                    
                    news_items = []
                    for article in articles:
                        news_item = NewsItem(
                            title=article.get('title', ''),
                            description=article.get('description', ''),
                            url=article.get('url', ''),
                            published_at=datetime.fromisoformat(
                                article.get('publishedAt', '').replace('Z', '+00:00')
                            ),
                            source=article.get('source', {}).get('name', 'Unknown')
                        )
                        news_items.append(news_item)
                    
                    logger.info(f"Obtenidas {len(news_items)} noticias para {ticker}")
                    return news_items
                    
                elif response.status == 429:
                    logger.warning("Rate limit alcanzado para GNews API")
                    return []
                else:
                    logger.error(f"Error en GNews API: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error obteniendo noticias para {ticker}: {str(e)}")
            return []
    
    def _analyze_sentiment_bert(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Analiza sentimiento usando BERT"""
        if not texts:
            return []
            
        try:
            self._load_sentiment_model()
            
            if self.sentiment_pipeline == "fallback":
                return self._analyze_sentiment_fallback(texts)
            
            # Procesar textos en lotes pequeños para evitar problemas de memoria
            batch_size = 5
            results = []
            
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                batch_results = self.sentiment_pipeline(batch)
                
                for j, result in enumerate(batch_results):
                    # Convertir labels del modelo BETO
                    label_map = {
                        'POS': 'positive',
                        'NEG': 'negative', 
                        'NEU': 'neutral'
                    }
                    
                    sentiment = label_map.get(result['label'], 'neutral')
                    confidence = result['score']
                    
                    results.append({
                        'text': batch[j],
                        'sentiment': sentiment,
                        'confidence': confidence
                    })
            
            return results
            
        except Exception as e:
            logger.error(f"Error en análisis BERT: {str(e)}")
            return self._analyze_sentiment_fallback(texts)
    
    def _analyze_sentiment_fallback(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Análisis de sentimiento básico usando palabras clave (fallback)"""
        positive_words = [
            'subió', 'sube', 'aumentó', 'ganancia', 'beneficio', 'crecimiento', 
            'positivo', 'bueno', 'excelente', 'récord', 'éxito', 'rentable',
            'inversión', 'oportunidad', 'alza', 'recuperación'
        ]
        
        negative_words = [
            'bajó', 'baja', 'cayó', 'pérdida', 'crisis', 'problema', 'negativo',
            'malo', 'declive', 'riesgo', 'preocupación', 'caída', 'recesión',
            'déficit', 'deuda', 'conflicto', 'incertidumbre'
        ]
        
        results = []
        for text in texts:
            text_lower = text.lower()
            
            pos_count = sum(1 for word in positive_words if word in text_lower)
            neg_count = sum(1 for word in negative_words if word in text_lower)
            
            if pos_count > neg_count:
                sentiment = 'positive'
                confidence = min(0.6 + (pos_count - neg_count) * 0.1, 0.9)
            elif neg_count > pos_count:
                sentiment = 'negative'
                confidence = min(0.6 + (neg_count - pos_count) * 0.1, 0.9)
            else:
                sentiment = 'neutral'
                confidence = 0.5
            
            results.append({
                'text': text,
                'sentiment': sentiment,
                'confidence': confidence
            })
        
        return results
    
    def _calculate_sentiment_score(self, sentiment_results: List[Dict[str, Any]]) -> float:
        """
        Calcula score de sentimiento de 0-100
        Implementa la lógica del prompt: positivo=100, neutral=50, negativo=0
        """
        if not sentiment_results:
            return 50.0  # Neutral si no hay datos
        
        total_score = 0.0
        total_weight = 0.0
        
        for result in sentiment_results:
            sentiment = result['sentiment']
            confidence = result.get('confidence', 1.0)
            
            if sentiment == 'positive':
                score = 100.0
            elif sentiment == 'negative':
                score = 0.0
            else:  # neutral
                score = 50.0
            
            # Ponderar por confidence
            total_score += score * confidence
            total_weight += confidence
        
        if total_weight == 0:
            return 50.0
            
        final_score = total_score / total_weight
        return round(final_score, 2)
    
    async def analyze_ticker_sentiment(self, ticker: str, company_name: str = None) -> Dict[str, Any]:
        """Análisis completo de sentimiento para un ticker"""
        try:
            # Obtener noticias
            news_items = await self._get_news_gnews(ticker, company_name)
            
            if not news_items:
                logger.info(f"No se encontraron noticias para {ticker}, usando score neutral")
                return {
                    "ticker": ticker,
                    "sentiment_score": 50.0,
                    "news_count": 0,
                    "news_items": [],
                    "overall_sentiment": "neutral",
                    "confidence": 0.5,
                    "timestamp": datetime.now().isoformat()
                }
            
            # Preparar textos para análisis
            texts = []
            for news in news_items:
                # Combinar título y descripción
                text = news.title
                if news.description:
                    text += ". " + news.description
                texts.append(text)
            
            # Analizar sentimiento
            sentiment_results = self._analyze_sentiment_bert(texts)
            
            # Calcular score final
            sentiment_score = self._calculate_sentiment_score(sentiment_results)
            
            # Determinar sentimiento general
            if sentiment_score >= 65:
                overall_sentiment = "positive"
            elif sentiment_score <= 35:
                overall_sentiment = "negative"
            else:
                overall_sentiment = "neutral"
            
            # Agregar sentimiento a las noticias
            for i, news in enumerate(news_items):
                if i < len(sentiment_results):
                    news.sentiment = sentiment_results[i]['sentiment']
                    news.sentiment_score = sentiment_results[i].get('confidence', 0.5)
            
            # Calcular confidence promedio
            avg_confidence = sum(r.get('confidence', 0.5) for r in sentiment_results) / len(sentiment_results)
            
            return {
                "ticker": ticker,
                "sentiment_score": sentiment_score,
                "news_count": len(news_items),
                "news_items": [news.dict() for news in news_items],
                "overall_sentiment": overall_sentiment,
                "confidence": round(avg_confidence, 3),
                "sentiment_distribution": self._get_sentiment_distribution(sentiment_results),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error en análisis de sentimiento para {ticker}: {str(e)}")
            return {
                "ticker": ticker,
                "sentiment_score": 50.0,
                "news_count": 0,
                "news_items": [],
                "overall_sentiment": "neutral",
                "confidence": 0.5,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _get_sentiment_distribution(self, sentiment_results: List[Dict[str, Any]]) -> Dict[str, int]:
        """Obtiene la distribución de sentimientos"""
        distribution = {"positive": 0, "negative": 0, "neutral": 0}
        
        for result in sentiment_results:
            sentiment = result.get('sentiment', 'neutral')
            distribution[sentiment] += 1
            
        return distribution
    
    async def health_check(self) -> bool:
        """Verifica si el servicio está funcionando"""
        try:
            # Verificar API key
            if not self.gnews_api_key:
                return False
            
            # Test básico del modelo
            test_texts = ["Esta es una noticia positiva", "Texto neutral"]
            results = self._analyze_sentiment_bert(test_texts)
            
            return len(results) == 2
            
        except Exception as e:
            logger.error(f"Health check de sentimiento falló: {str(e)}")
            return False
    
    async def close(self):
        """Cierra las conexiones"""
        if self.session and not self.session.closed:
            await self.session.close() 