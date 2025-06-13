#!/usr/bin/env python3
"""
Script de inicio para ArgentaIA Backend
Verifica la configuración y ejecuta el servidor FastAPI
"""

import os
import sys
import subprocess
import asyncio
from pathlib import Path

def print_banner():
    """Imprime el banner de ArgentaIA"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                        🇦🇷 ArgentaIA 🇦🇷                        ║
║              API de Análisis de Inversiones                  ║
║                                                              ║
║  📊 Técnico (50%) + 💰 Fundamental (30%) +                   ║
║  🌍 Macro (10%) + 📰 Sentimiento (10%)                       ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Verifica la versión de Python"""
    if sys.version_info < (3, 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

def check_virtual_env():
    """Verifica si está en un entorno virtual"""
    in_venv = (
        hasattr(sys, 'real_prefix') or 
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    )
    
    if not in_venv:
        print("⚠️  Advertencia: No se detectó entorno virtual")
        print("   Recomendado: python -m venv venv && source venv/bin/activate")
    else:
        print("✅ Entorno virtual activo")

def check_poetry():
    """Verifica si Poetry está instalado"""
    try:
        result = subprocess.run(["poetry", "--version"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ {version}")
            return True
        else:
            print("❌ Poetry no encontrado")
            print("   Instala Poetry: https://python-poetry.org/docs/#installation")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Poetry no encontrado")
        print("   Instala Poetry: https://python-poetry.org/docs/#installation")
        return False

def check_dependencies():
    """Verifica las dependencias principales"""
    # Verificar si existe pyproject.toml
    if not Path("pyproject.toml").exists():
        print("❌ pyproject.toml no encontrado")
        return False
    
    print("✅ pyproject.toml encontrado")
    
    # Verificar si las dependencias están instaladas
    try:
        result = subprocess.run(["poetry", "check"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Dependencias válidas")
        else:
            print("⚠️  Problemas con dependencias")
            print(f"   {result.stdout}")
    except Exception as e:
        print(f"⚠️  No se pudo verificar dependencias: {str(e)}")
    
    # Test de importación básica
    required_packages = [
        "fastapi",
        "uvicorn", 
        "pydantic",
        "yfinance",
        "pandas",
        "aiohttp"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Faltan dependencias: {', '.join(missing_packages)}")
        print("   Ejecuta: poetry install")
        return False
    
    return True

def check_env_file():
    """Verifica la configuración del archivo .env"""
    env_path = Path(".env")
    env_example_path = Path("env.example")
    
    if not env_path.exists():
        if env_example_path.exists():
            print("⚠️  Archivo .env no encontrado")
            print("   Copia env.example a .env y configura las API keys")
            print("   cp env.example .env")
        else:
            print("❌ No se encontró configuración de entorno")
        return False
    
    print("✅ Archivo .env encontrado")
    
    # Verificar API keys
    from dotenv import load_dotenv
    load_dotenv()
    
    fmp_key = os.getenv("FMP_API_KEY", "")
    gnews_key = os.getenv("GNEWS_API_KEY", "")
    
    if fmp_key and fmp_key != "your_fmp_api_key_here":
        print("✅ FMP API Key configurada")
    else:
        print("⚠️  FMP API Key no configurada (análisis fundamental limitado)")
    
    if gnews_key and gnews_key != "your_gnews_api_key_here":
        print("✅ GNews API Key configurada")
    else:
        print("⚠️  GNews API Key no configurada (análisis de sentimiento limitado)")
    
    return True

async def test_services():
    """Test básico de los servicios"""
    try:
        print("\n🔄 Probando servicios...")
        
        # Import solo si las dependencias están disponibles
        from services.technical_analysis import TechnicalAnalyzer
        from services.macro_analysis import MacroAnalyzer
        
        # Test básico del analizador técnico
        tech_analyzer = TechnicalAnalyzer()
        health = await tech_analyzer.health_check()
        print(f"📈 Análisis técnico: {'✅' if health else '⚠️'}")
        
        # Test básico del analizador macro
        macro_analyzer = MacroAnalyzer()
        health = await macro_analyzer.health_check()
        print(f"🌍 Análisis macro: {'✅' if health else '⚠️'}")
        
        await macro_analyzer.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando servicios: {str(e)}")
        return False

def get_server_info():
    """Información del servidor"""
    info = """
🚀 Servidor FastAPI iniciando...

📍 URLs importantes:
   • API: http://localhost:8000
   • Docs: http://localhost:8000/docs
   • Health: http://localhost:8000/api/health

📊 Endpoints principales:
   • GET /api/recommendations/daily - Recomendaciones diarias
   • GET /api/analysis/{ticker} - Análisis detallado
   • GET /api/scores/{ticker} - Desglose de scores

📈 Tickers soportados:
   YPF, GGAL, PAM, TEO, TGS, CEPU, BMA, SUPV, CRESY, LOMA,
   IRCP, VIST, MELI, GLOB, DESP

💡 Ctrl+C para detener el servidor
    """
    print(info)

async def main():
    """Función principal"""
    print_banner()
    
    print("🔍 Verificando configuración...\n")
    
    # Verificaciones
    check_python_version()
    check_virtual_env()
    
    print("\n📦 Verificando Poetry:")
    if not check_poetry():
        print("\n💡 Para instalar Poetry:")
        print("   curl -sSL https://install.python-poetry.org | python3 -")
        print("   O visita: https://python-poetry.org/docs/#installation")
        sys.exit(1)
    
    print("\n📦 Verificando dependencias:")
    if not check_dependencies():
        sys.exit(1)
    
    print("\n⚙️ Verificando configuración:")
    check_env_file()
    
    # Test de servicios opcional
    print("\n🧪 Test rápido de servicios:")
    try:
        await test_services()
    except Exception as e:
        print(f"⚠️  No se pudo probar servicios: {str(e)}")
        print("   (Se probará al iniciar el servidor)")
    
    get_server_info()
    
    # Iniciar servidor con Poetry
    try:
        print("🚀 Iniciando servidor con Poetry...\n")
        # Ejecutar con poetry run para asegurar el entorno correcto
        result = subprocess.run([
            "poetry", "run", "uvicorn", "main:app",
            "--host", "0.0.0.0",
            "--port", "8000", 
            "--reload",
            "--log-level", "info"
        ])
        
    except KeyboardInterrupt:
        print("\n\n👋 ¡Servidor detenido!")
    except Exception as e:
        print(f"\n❌ Error iniciando servidor: {str(e)}")
        print("\n💡 Soluciones posibles:")
        print("   1. Verifica que el puerto 8000 esté libre")
        print("   2. Instala dependencias: poetry install")
        print("   3. Configura variables de entorno en .env")
        print("   4. Verifica que Poetry esté correctamente instalado")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error fatal: {str(e)}")
        sys.exit(1) 