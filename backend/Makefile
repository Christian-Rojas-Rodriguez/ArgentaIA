# ArgentaIA Backend - Comandos de desarrollo
.PHONY: help install run test lint format clean dev

# Variables
POETRY = poetry
PYTHON = $(POETRY) run python

help: ## Muestra esta ayuda
	@echo "🇦🇷 ArgentaIA Backend - Comandos disponibles:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Instala dependencias con Poetry
	@echo "📦 Instalando dependencias..."
	$(POETRY) install

dev-install: ## Instala dependencias de desarrollo
	@echo "🛠️ Instalando dependencias de desarrollo..."
	$(POETRY) install --with dev

run: ## Ejecuta el servidor FastAPI
	@echo "🚀 Iniciando servidor ArgentaIA..."
	$(PYTHON) run.py

server: ## Ejecuta servidor directamente (sin verificaciones)
	@echo "🚀 Iniciando servidor directo..."
	$(POETRY) run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

test: ## Ejecuta tests
	@echo "🧪 Ejecutando tests..."
	$(POETRY) run pytest -v

test-cov: ## Ejecuta tests con coverage
	@echo "🧪 Ejecutando tests con coverage..."
	$(POETRY) run pytest --cov=services --cov-report=html --cov-report=term

format: ## Formatea código con Black e isort
	@echo "🎨 Formateando código..."
	$(POETRY) run black .
	$(POETRY) run isort .

lint: ## Ejecuta linting
	@echo "🔍 Ejecutando linting..."
	$(POETRY) run flake8 .
	$(POETRY) run mypy .

check: format lint test ## Ejecuta format, lint y tests

clean: ## Limpia archivos temporales
	@echo "🧹 Limpiando archivos temporales..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf dist
	rm -rf build

logs: ## Muestra logs en tiempo real
	@echo "📋 Mostrando logs..."
	@if [ -f logs/argenta_ia.log ]; then \
		tail -f logs/argenta_ia.log; \
	else \
		echo "❌ No se encontró archivo de logs. Ejecuta 'make run' primero."; \
	fi

health: ## Verifica salud de la API
	@echo "🏥 Verificando salud de la API..."
	@curl -s http://localhost:8000/api/health | python -m json.tool || echo "❌ API no responde"

shell: ## Abre shell de Poetry
	@echo "🐚 Abriendo shell de Poetry..."
	$(POETRY) shell

update: ## Actualiza dependencias
	@echo "🔄 Actualizando dependencias..."
	$(POETRY) update

deps: ## Muestra dependencias instaladas
	@echo "📋 Dependencias instaladas:"
	$(POETRY) show

export-deps: ## Exporta requirements.txt
	@echo "📄 Exportando requirements.txt..."
	$(POETRY) export -f requirements.txt --output requirements.txt --without-hashes

dev: install ## Setup completo de desarrollo
	@echo "🚀 Configurando entorno de desarrollo..."
	@if [ ! -f .env ]; then \
		echo "📝 Copiando env.example a .env..."; \
		cp env.example .env; \
		echo "⚠️  Recuerda configurar las API keys en .env"; \
	fi
	@echo "✅ Entorno listo. Ejecuta 'make run' para iniciar."

prod-deps: ## Instala solo dependencias de producción
	@echo "🏭 Instalando dependencias de producción..."
	$(POETRY) install --only main

docker-build: ## Construye imagen Docker
	@echo "🐳 Construyendo imagen Docker..."
	docker build -t argenta-ia-backend .

docker-run: ## Ejecuta contenedor Docker
	@echo "🐳 Ejecutando contenedor Docker..."
	docker run -p 8000:8000 --env-file .env argenta-ia-backend

# Comandos de análisis específicos
analyze-ypf: ## Análisis detallado de YPF (ejemplo)
	@echo "📊 Analizando YPF..."
	@curl -s http://localhost:8000/api/analysis/YPF | python -m json.tool

daily-recs: ## Obtiene recomendaciones diarias
	@echo "📈 Obteniendo recomendaciones diarias..."
	@curl -s http://localhost:8000/api/recommendations/daily | python -m json.tool

setup-keys: ## Configurar API Keys interactivamente
	@echo "🔑 Configurando API Keys..."
	$(PYTHON) setup_api_keys.py

migration-plan: ## Mostrar plan de migración a batch
	@echo "📋 Plan de migración a análisis batch:"
	@cat migration_plan.md 