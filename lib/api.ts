/**
 * Utilidades para conectar con el backend de FastAPI
 */

// URL base de la API - cambiar según el entorno
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

/**
 * Cliente HTTP para realizar peticiones a la API de FastAPI
 */
export async function fetchFromAPI<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`

  const defaultHeaders = {
    "Content-Type": "application/json",
    Accept: "application/json",
  }

  const response = await fetch(url, {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  })

  if (!response.ok) {
    // Manejar errores de la API
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.detail || `Error en la petición: ${response.status}`)
  }

  return response.json()
}

/**
 * Tipos de datos que se esperan de la API
 */
export interface StockRecommendation {
  symbol: string
  name: string
  price: number
  change: number
  changePercent: number
  recommendation: string
  confidence: number
  sector: string
  risk: string
  targetPrice: number
  monthlyInvestment: string
}

export interface BondRecommendation {
  symbol: string
  name: string
  price: number
  change: number
  changePercent: number
  recommendation: string
  confidence: number
  yield: number
  duration: number
  risk: string
  monthlyInvestment: string
}

/**
 * Funciones para obtener datos de la API
 */
export async function getStockRecommendations(): Promise<StockRecommendation[]> {
  return fetchFromAPI<StockRecommendation[]>("/api/recommendations/stocks")
}

export async function getBondRecommendations(): Promise<BondRecommendation[]> {
  return fetchFromAPI<BondRecommendation[]>("/api/recommendations/bonds")
}
