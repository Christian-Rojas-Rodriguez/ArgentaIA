#!/usr/bin/env python3
"""
Script para configurar API Keys de ArgentaIA
"""

import os
from pathlib import Path


def print_banner():
    print("🔑 ArgentaIA - Configuración de API Keys")
    print("=" * 50)


def check_existing_env():
    """Verifica si ya existe .env"""
    env_file = Path(".env")
    if env_file.exists():
        print("✅ Archivo .env existente encontrado")
        with open(env_file, 'r') as f:
            content = f.read()
            if "FMP_API_KEY" in content:
                print("   - FMP_API_KEY: Configurada")
            else:
                print("   - FMP_API_KEY: ❌ NO configurada")
            
            if "GNEWS_API_KEY" in content:
                print("   - GNEWS_API_KEY: Configurada")
            else:
                print("   - GNEWS_API_KEY: ❌ NO configurada")
        return True
    return False


def show_api_instructions():
    """Muestra instrucciones para obtener API keys"""
    print("\n📋 INSTRUCCIONES PARA OBTENER API KEYS:")
    print("-" * 50)
    
    print("\n🏦 1. FINANCIAL MODELING PREP (FMP)")
    print("   ├─ URL: https://financialmodelingprep.com/developer/docs")
    print("   ├─ Plan: Gratuito (250 requests/día)")
    print("   ├─ Pasos:")
    print("   │  1. Crear cuenta gratis")
    print("   │  2. Verificar email")
    print("   │  3. Copiar API key del dashboard")
    print("   └─ Necesaria para: Análisis fundamental (ratios)")
    
    print("\n📰 2. GNEWS.IO")
    print("   ├─ URL: https://gnews.io/")
    print("   ├─ Plan: Gratuito (100 requests/día)")
    print("   ├─ Pasos:")
    print("   │  1. Crear cuenta gratis")
    print("   │  2. Verificar email")
    print("   │  3. Copiar API key del dashboard")
    print("   └─ Necesaria para: Análisis de sentimiento")
    
    print("\n✅ 3. APIs PÚBLICAS (No requieren key)")
    print("   ├─ Yahoo Finance: Análisis técnico")
    print("   └─ BCRA: Datos macro argentinos")


def configure_keys():
    """Configura las API keys interactivamente"""
    print("\n🔧 CONFIGURACIÓN DE API KEYS")
    print("-" * 30)
    
    env_content = []
    
    # Leer .env existente si existe
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if not line.strip().startswith(('FMP_API_KEY', 'GNEWS_API_KEY')):
                    env_content.append(line.rstrip())
    else:
        # Contenido base si no existe .env
        env_content = [
            "# ArgentaIA - Configuración",
            "DEBUG=true",
            "LOG_LEVEL=INFO",
            "",
            "# URLs de APIs (no cambiar a menos que sea necesario)",
            "FMP_BASE_URL=https://financialmodelingprep.com/api/v3",
            "GNEWS_BASE_URL=https://gnews.io/api/v4",
            "BCRA_BASE_URL=https://api.bcra.gob.ar",
            ""
        ]
    
    # FMP API Key
    print("\n1️⃣ Financial Modeling Prep (FMP)")
    fmp_key = input("   Ingresa tu FMP API Key (o Enter para omitir): ").strip()
    if fmp_key:
        env_content.append(f"FMP_API_KEY={fmp_key}")
        print("   ✅ FMP API Key configurada")
    else:
        env_content.append("# FMP_API_KEY=tu_key_aqui")
        print("   ⚠️  FMP API Key omitida - análisis fundamental será limitado")
    
    # GNews API Key  
    print("\n2️⃣ GNews.io")
    gnews_key = input("   Ingresa tu GNews API Key (o Enter para omitir): ").strip()
    if gnews_key:
        env_content.append(f"GNEWS_API_KEY={gnews_key}")
        print("   ✅ GNews API Key configurada")
    else:
        env_content.append("# GNEWS_API_KEY=tu_key_aqui")
        print("   ⚠️  GNews API Key omitida - análisis de sentimiento será limitado")
    
    # Escribir .env
    with open(".env", 'w') as f:
        f.write('\n'.join(env_content))
    
    print(f"\n✅ Configuración guardada en {env_file.absolute()}")


def test_keys():
    """Prueba las API keys configuradas"""
    print("\n🧪 PROBANDO API KEYS...")
    print("-" * 25)
    
    # Cargar variables
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ No se encontró archivo .env")
        return
    
    import subprocess
    import sys
    
    try:
        # Test básico de importaciones
        result = subprocess.run([
            sys.executable, "-c", 
            "from services.fundamental_analysis import FundamentalAnalyzer; "
            "from services.sentiment_analysis import SentimentAnalyzer; "
            "print('✅ Importaciones exitosas')"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Servicios importados correctamente")
        else:
            print("❌ Error importando servicios:")
            print(f"   {result.stderr}")
            
    except Exception as e:
        print(f"⚠️  No se pudo probar servicios: {str(e)}")
        print("   Ejecuta 'make health' una vez que el servidor esté corriendo")


def show_next_steps():
    """Muestra próximos pasos"""
    print("\n🚀 PRÓXIMOS PASOS:")
    print("-" * 20)
    print("1. Ejecutar servidor: make run")
    print("2. Verificar salud: make health") 
    print("3. Probar recomendaciones: make daily-recs")
    print("4. Ver documentación: http://localhost:8000/docs")
    print("\n💡 TIPS:")
    print("- Las APIs gratuitas tienen límites diarios")
    print("- El sistema funciona con fallbacks si alguna API falla")
    print("- Puedes agregar más keys después editando .env")


def main():
    print_banner()
    
    # Verificar estado actual
    has_env = check_existing_env()
    
    # Mostrar instrucciones
    show_api_instructions()
    
    # Preguntar si quiere configurar
    print(f"\n{'🔄 RECONFIGURAR' if has_env else '⚙️ CONFIGURAR'} API KEYS")
    configure = input("¿Quieres configurar las API keys ahora? (y/N): ").strip().lower()
    
    if configure in ['y', 'yes', 's', 'si']:
        configure_keys()
        test_keys()
        show_next_steps()
    else:
        print("\n💭 Puedes configurar las keys más tarde editando el archivo .env")
        print("   O ejecutando nuevamente: python setup_api_keys.py")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Configuración cancelada")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("💡 Puedes configurar manualmente editando .env") 