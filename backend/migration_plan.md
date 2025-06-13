# 🔄 Plan de Migración: Tiempo Real → Batch Diario

## 📋 Resumen del Cambio

**ACTUAL**: Análisis en tiempo real cada request  
**NUEVO**: Análisis batch 1x/día + almacenamiento en DB

## 🎯 Impacto del Cambio

### ✅ Ventajas
- **Menor latencia**: Frontend lee datos pre-calculados
- **Eficiencia de APIs**: Solo 1 análisis/día por ticker
- **Consistencia**: Todos los usuarios ven los mismos datos
- **Historial**: Tracking de evolución de scores
- **Escalabilidad**: Mejor rendimiento con muchos usuarios

### ⚠️ Desventajas  
- **Datos menos frescos**: Máximo 24h de antigüedad
- **Complejidad**: Sistema más complejo con DB + scheduler
- **Recursos**: Necesita más infraestructura

## 🛠️ Componentes a Modificar

### 1. **Nueva Dependencias** (pyproject.toml)
```toml
sqlalchemy = "^2.0.0"           # ORM
alembic = "^1.13.0"             # Migraciones DB
apscheduler = "^3.10.0"         # Scheduler
psycopg2-binary = "^2.9.0"      # PostgreSQL (opcional)
```

### 2. **Base de Datos** (nuevo)
```python
# database/
├── models.py          # Modelos SQLAlchemy
├── connection.py      # Configuración DB
└── migrations/        # Migraciones Alembic
```

### 3. **Scheduler** (nuevo)
```python
# scheduler/
├── job_scheduler.py   # APScheduler config
├── daily_analysis.py  # Job principal
└── job_monitoring.py  # Monitoreo de jobs
```

### 4. **Endpoints Modificados**
```python
# main.py - Cambios:
- /api/recommendations/daily → /api/recommendations/latest
- /api/analysis/{ticker} → /api/analysis/{ticker}/latest
+ /api/recommendations/history
+ /api/analysis/{ticker}/history
+ /api/jobs/status
```

### 5. **Servicios Adaptados**
```python
# services/ - Cambios mínimos:
- recommendation_engine.py: + save_to_db()
- Mantener lógica de análisis existente
- Agregar persistencia de resultados
```

## 📅 Plan de Implementación

### **Fase 1: Preparación (1-2 días)**
1. Agregar dependencias de DB
2. Configurar SQLAlchemy + modelos
3. Crear migraciones iniciales
4. Setup de testing con DB

### **Fase 2: Batch System (2-3 días)**
1. Crear job scheduler
2. Adaptar recommendation_engine para persistir datos
3. Implementar daily_analysis job
4. Sistema de monitoreo de jobs

### **Fase 3: API Migration (1 día)**
1. Modificar endpoints para leer de DB
2. Mantener endpoints legacy como deprecated
3. Agregar endpoints de historial
4. Update documentación

### **Fase 4: Testing & Deploy (1 día)**
1. Tests de integración
2. Migration scripts
3. Deployment con DB
4. Monitoreo y alertas

## 🗄️ Esquema de Base de Datos

### **Tabla: daily_recommendations**
```sql
CREATE TABLE daily_recommendations (
    id SERIAL PRIMARY KEY,
    analysis_date DATE NOT NULL,
    ticker VARCHAR(10) NOT NULL,
    recommendation VARCHAR(20) NOT NULL,  -- COMPRAR/MANTENER/VENDER
    total_score DECIMAL(5,2) NOT NULL,
    confidence DECIMAL(5,2) NOT NULL,
    technical_score DECIMAL(5,2),
    fundamental_score DECIMAL(5,2),
    macro_score DECIMAL(5,2),
    sentiment_score DECIMAL(5,2),
    current_price DECIMAL(10,2),
    target_price DECIMAL(10,2),
    risk_level VARCHAR(20),
    summary TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(analysis_date, ticker)
);
```

### **Tabla: analysis_details**
```sql
CREATE TABLE analysis_details (
    id SERIAL PRIMARY KEY,
    recommendation_id INTEGER REFERENCES daily_recommendations(id),
    analysis_type VARCHAR(20) NOT NULL,  -- technical/fundamental/macro/sentiment
    raw_data JSONB,
    indicators JSONB,
    score DECIMAL(5,2),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### **Tabla: job_runs**
```sql
CREATE TABLE job_runs (
    id SERIAL PRIMARY KEY,
    job_name VARCHAR(50) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    status VARCHAR(20) NOT NULL,  -- running/completed/failed
    tickers_processed INTEGER,
    errors_count INTEGER,
    log_data JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## ⚙️ Configuración de Scheduler

### **Cron Expression**
```python
# Ejecutar todos los días a las 6:00 AM
DAILY_ANALYSIS_CRON = "0 6 * * *"

# Ejecutar días laborales a las 6:00 AM (más conservador)
WEEKDAY_ANALYSIS_CRON = "0 6 * * 1-5"
```

### **Job Configuration**
```python
# config/scheduler.py
SCHEDULER_JOBS = [
    {
        'id': 'daily_analysis',
        'func': 'scheduler.daily_analysis:run_daily_analysis',
        'trigger': 'cron',
        'hour': 6,
        'minute': 0,
        'max_instances': 1,
        'coalesce': True
    }
]
```

## 🔧 Variables de Entorno Nuevas

```env
# Base de datos
DATABASE_URL=sqlite:///./argenta_ia.db
# O PostgreSQL: postgresql://user:pass@localhost/argenta_ia

# Scheduler
SCHEDULER_ENABLED=true
DAILY_ANALYSIS_HOUR=6
DAILY_ANALYSIS_TIMEZONE=America/Argentina/Buenos_Aires

# Jobs
JOB_TIMEOUT_MINUTES=60
MAX_RETRIES=3
```

## 🧪 Testing Strategy

### **Tests de Base de Datos**
```python
# tests/test_database.py
- Test de conexión
- Test de modelos
- Test de queries
- Test de migraciones
```

### **Tests de Scheduler**
```python
# tests/test_scheduler.py  
- Test de job execution
- Test de error handling
- Test de concurrencia
- Test de monitoreo
```

### **Tests de Migración**
```python
# tests/test_migration.py
- Test de compatibilidad endpoints
- Test de performance DB vs tiempo real
- Test de datos históricos
```

## 📊 Métricas y Monitoreo

### **Métricas Clave**
- Tiempo de ejecución de job diario
- Tickers procesados exitosamente
- Errores por tipo de análisis
- Latencia de endpoints
- Uso de recursos de DB

### **Alertas**
- Job fallido > 3 veces
- Tiempo de ejecución > 1 hora
- DB connection errors
- Espacio en disco bajo

## 🚀 Deployment Considerations

### **Opción 1: SQLite (Simple)**
- Archivo local `argenta_ia.db`
- No requiere servidor DB externo
- Ideal para desarrollo/testing

### **Opción 2: PostgreSQL (Producción)**
- Base de datos externa
- Mejor para concurrencia
- Backup y recovery robusto

### **Docker Compose**
```yaml
services:
  api:
    build: .
    depends_on: [db]
    environment:
      - DATABASE_URL=postgresql://user:pass@db/argenta_ia
  
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: argenta_ia
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

## ❓ Decisiones Pendientes

1. **Base de datos**: ¿SQLite o PostgreSQL?
2. **Scheduler**: ¿APScheduler o Celery?
3. **Migración**: ¿Gradual o completa?
4. **Historial**: ¿Cuántos días mantener?
5. **Fallback**: ¿Mantener análisis en tiempo real como backup?

## 💡 Recomendación

**Sugiero implementación gradual:**

1. **Fase MVP**: SQLite + APScheduler integrado
2. **Mantener endpoints actuales** como fallback
3. **Nuevos endpoints** para datos de DB
4. **Frontend puede elegir** tiempo real vs cached
5. **Migración completa** una vez validado

¿Te parece bien este approach? ¿Qué prefieres para la base de datos? 