/**
 * Configuración de la aplicación
 */

// Configuración de la API
export const API_CONFIG = {
  // URL base de la API de FastAPI
  baseUrl: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",

  // Tiempo de espera para las peticiones en milisegundos
  timeout: 10000,

  // Endpoints principales
  endpoints: {
    recommendations: {
      stocks: "/api/recommendations/stocks",
      bonds: "/api/recommendations/bonds",
    },
    auth: {
      login: "/api/auth/login",
      register: "/api/auth/register",
    },
  },
}

// Configuración de la aplicación
export const APP_CONFIG = {
  // Nombre de la aplicación
  appName: "ArgentaAI",

  // Descripción de la aplicación
  appDescription: "Recomendaciones inteligentes de acciones y bonos argentinos",

  // Versión de la aplicación
  version: "1.0.0",
}

/**
 * Ejemplo de cómo configurar FastAPI en Python:
 *
 * ```python
 * from fastapi import FastAPI
 * from fastapi.middleware.cors import CORSMiddleware
 *
 * app = FastAPI(
 *     title="ArgentaAI API",
 *     description="API para recomendaciones de inversiones",
 *     version="1.0.0"
 * )
 *
 * # Configurar CORS para permitir peticiones desde el frontend
 * app.add_middleware(
 *     CORSMiddleware,
 *     allow_origins=["http://localhost:3000"],  # URL del frontend
 *     allow_credentials=True,
 *     allow_methods=["*"],
 *     allow_headers=["*"],
 * )
 *
 * @app.get("/api/recommendations/stocks")
 * async def get_stock_recommendations():
 *     # Lógica para obtener recomendaciones de acciones
 *     return [...]
 *
 * @app.get("/api/recommendations/bonds")
 * async def get_bond_recommendations():
 *     # Lógica para obtener recomendaciones de bonos
 *     return [...]
 * ```
 */
