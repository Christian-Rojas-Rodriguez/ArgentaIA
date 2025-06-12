"use client"

import { useState } from "react"
import { ArrowLeft, TrendingUp, TrendingDown, Shield, AlertTriangle, Star } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import Link from "next/link"

// Datos simulados de acciones argentinas
const stocksData = [
  {
    symbol: "GGAL",
    name: "Grupo Financiero Galicia",
    price: 285.5,
    change: 12.3,
    changePercent: 4.51,
    recommendation: "COMPRAR",
    confidence: 89,
    sector: "Financiero",
    risk: "Medio",
    targetPrice: 320.0,
  },
  {
    symbol: "YPFD",
    name: "YPF S.A.",
    price: 1250.0,
    change: -25.5,
    changePercent: -2.0,
    recommendation: "MANTENER",
    confidence: 72,
    sector: "Energía",
    risk: "Alto",
    targetPrice: 1300.0,
  },
  {
    symbol: "PAMP",
    name: "Pampa Energía",
    price: 890.75,
    change: 45.25,
    changePercent: 5.35,
    recommendation: "COMPRAR",
    confidence: 85,
    sector: "Energía",
    risk: "Medio",
    targetPrice: 980.0,
  },
  {
    symbol: "TECO2",
    name: "Telecom Argentina",
    price: 425.3,
    change: 8.7,
    changePercent: 2.09,
    recommendation: "COMPRAR",
    confidence: 78,
    sector: "Telecomunicaciones",
    risk: "Bajo",
    targetPrice: 465.0,
  },
  {
    symbol: "MIRG",
    name: "Mirgor S.A.C.I.F.I.A.",
    price: 2150.0,
    change: -85.0,
    changePercent: -3.8,
    recommendation: "VENDER",
    confidence: 82,
    sector: "Tecnología",
    risk: "Alto",
    targetPrice: 1950.0,
  },
]

// Datos simulados de bonos argentinos
const bondsData = [
  {
    symbol: "AL30",
    name: "Bonos República Argentina USD 2030",
    price: 45.25,
    change: 1.15,
    changePercent: 2.61,
    recommendation: "COMPRAR",
    confidence: 75,
    yield: 18.5,
    duration: 6.2,
    risk: "Alto",
  },
  {
    symbol: "GD30",
    name: "Bonos República Argentina USD 2030",
    price: 44.8,
    change: 0.95,
    changePercent: 2.17,
    recommendation: "COMPRAR",
    confidence: 73,
    yield: 18.8,
    duration: 6.2,
    risk: "Alto",
  },
  {
    symbol: "AL35",
    name: "Bonos República Argentina USD 2035",
    price: 38.9,
    change: -0.45,
    changePercent: -1.14,
    recommendation: "MANTENER",
    confidence: 68,
    yield: 21.2,
    duration: 8.5,
    risk: "Muy Alto",
  },
]

export default function RecomendacionesPage() {
  const [activeTab, setActiveTab] = useState<"acciones" | "bonos">("acciones")

  const getRecommendationColor = (rec: string) => {
    switch (rec) {
      case "COMPRAR":
        return "bg-green-500/20 text-green-400 border-green-500/30"
      case "MANTENER":
        return "bg-yellow-500/20 text-yellow-400 border-yellow-500/30"
      case "VENDER":
        return "bg-red-500/20 text-red-400 border-red-500/30"
      default:
        return "bg-gray-500/20 text-gray-400 border-gray-500/30"
    }
  }

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case "Bajo":
        return "text-green-400"
      case "Medio":
        return "text-yellow-400"
      case "Alto":
        return "text-orange-400"
      case "Muy Alto":
        return "text-red-400"
      default:
        return "text-gray-400"
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-night via-teal/20 to-soft-white dark:from-night dark:via-night/90 dark:to-night/70 relative overflow-hidden">
      {/* Background Effects */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute -top-1/2 -left-1/4 w-96 h-96 bg-gradient-radial from-teal/20 via-teal/5 to-transparent rounded-full blur-3xl" />
        <div className="absolute top-1/4 -right-1/4 w-80 h-80 bg-gradient-radial from-orange/15 via-orange/3 to-transparent rounded-full blur-3xl" />
      </div>

      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 backdrop-blur-md bg-white/10 dark:bg-black/20 border-b border-white/20 dark:border-white/10">
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Link href="/">
              <Button
                variant="ghost"
                size="sm"
                className="text-night dark:text-white hover:bg-white/10 dark:hover:bg-black/20"
              >
                <ArrowLeft className="w-4 h-4 mr-2" />
                Volver
              </Button>
            </Link>
            <div className="flex items-center space-x-2">
              <TrendingUp className="w-8 h-8 text-teal" />
              <span className="text-xl font-semibold text-night dark:text-white">ArgentaAI</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="pt-24 pb-12 px-6">
        <div className="container mx-auto max-w-7xl">
          {/* Page Header */}
          <div className="text-center mb-12">
            <h1 className="text-4xl md:text-5xl font-semibold text-night dark:text-white mb-4">
              Recomendaciones <span className="text-teal">IA</span>
            </h1>
            <p className="text-xl text-night/70 dark:text-white/70 max-w-3xl mx-auto">
              Análisis en tiempo real de los mejores activos argentinos con inteligencia artificial explicable
            </p>
          </div>

          {/* Tabs */}
          <div className="flex justify-center mb-8">
            <div className="glass-card p-2 flex space-x-2">
              <Button
                variant={activeTab === "acciones" ? "default" : "ghost"}
                onClick={() => setActiveTab("acciones")}
                className={`px-6 py-2 ${
                  activeTab === "acciones"
                    ? "bg-teal text-white"
                    : "text-night dark:text-white hover:bg-white/10 dark:hover:bg-black/20"
                }`}
              >
                <TrendingUp className="w-4 h-4 mr-2" />
                Acciones
              </Button>
              <Button
                variant={activeTab === "bonos" ? "default" : "ghost"}
                onClick={() => setActiveTab("bonos")}
                className={`px-6 py-2 ${
                  activeTab === "bonos"
                    ? "bg-teal text-white"
                    : "text-night dark:text-white hover:bg-white/10 dark:hover:bg-black/20"
                }`}
              >
                <Shield className="w-4 h-4 mr-2" />
                Bonos
              </Button>
            </div>
          </div>

          {/* Acciones Tab */}
          {activeTab === "acciones" && (
            <div className="grid gap-6">
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {stocksData.map((stock) => (
                  <div key={stock.symbol} className="recommendation-card">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h3 className="text-xl font-semibold text-night dark:text-white">{stock.symbol}</h3>
                        <p className="text-sm text-night/60 dark:text-white/60">{stock.name}</p>
                        <p className="text-xs text-night/50 dark:text-white/50">{stock.sector}</p>
                      </div>
                      <Badge className={getRecommendationColor(stock.recommendation)}>{stock.recommendation}</Badge>
                    </div>

                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-2xl font-bold text-night dark:text-white">${stock.price.toFixed(2)}</span>
                        <div className={`flex items-center ${stock.change >= 0 ? "text-green-400" : "text-red-400"}`}>
                          {stock.change >= 0 ? (
                            <TrendingUp className="w-4 h-4 mr-1" />
                          ) : (
                            <TrendingDown className="w-4 h-4 mr-1" />
                          )}
                          <span className="font-medium">
                            {stock.change >= 0 ? "+" : ""}
                            {stock.changePercent.toFixed(2)}%
                          </span>
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <span className="text-night/60 dark:text-white/60">Precio objetivo:</span>
                          <p className="font-medium text-night dark:text-white">${stock.targetPrice.toFixed(2)}</p>
                        </div>
                        <div>
                          <span className="text-night/60 dark:text-white/60">Confianza:</span>
                          <div className="flex items-center">
                            <Star className="w-3 h-3 text-yellow-400 mr-1" />
                            <span className="font-medium text-night dark:text-white">{stock.confidence}%</span>
                          </div>
                        </div>
                        <div>
                          <span className="text-night/60 dark:text-white/60">Riesgo:</span>
                          <p className={`font-medium ${getRiskColor(stock.risk)}`}>{stock.risk}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Bonos Tab */}
          {activeTab === "bonos" && (
            <div className="grid gap-6">
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {bondsData.map((bond) => (
                  <div key={bond.symbol} className="recommendation-card">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h3 className="text-xl font-semibold text-night dark:text-white">{bond.symbol}</h3>
                        <p className="text-sm text-night/60 dark:text-white/60">{bond.name}</p>
                      </div>
                      <Badge className={getRecommendationColor(bond.recommendation)}>{bond.recommendation}</Badge>
                    </div>

                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-2xl font-bold text-night dark:text-white">${bond.price.toFixed(2)}</span>
                        <div className={`flex items-center ${bond.change >= 0 ? "text-green-400" : "text-red-400"}`}>
                          {bond.change >= 0 ? (
                            <TrendingUp className="w-4 h-4 mr-1" />
                          ) : (
                            <TrendingDown className="w-4 h-4 mr-1" />
                          )}
                          <span className="font-medium">
                            {bond.change >= 0 ? "+" : ""}
                            {bond.changePercent.toFixed(2)}%
                          </span>
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <span className="text-night/60 dark:text-white/60">Rendimiento:</span>
                          <p className="font-medium text-teal">{bond.yield.toFixed(1)}%</p>
                        </div>
                        <div>
                          <span className="text-night/60 dark:text-white/60">Duración:</span>
                          <p className="font-medium text-night dark:text-white">{bond.duration} años</p>
                        </div>
                        <div>
                          <span className="text-night/60 dark:text-white/60">Confianza:</span>
                          <div className="flex items-center">
                            <Star className="w-3 h-3 text-yellow-400 mr-1" />
                            <span className="font-medium text-night dark:text-white">{bond.confidence}%</span>
                          </div>
                        </div>
                        <div>
                          <span className="text-night/60 dark:text-white/60">Riesgo:</span>
                          <p className={`font-medium ${getRiskColor(bond.risk)}`}>{bond.risk}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Disclaimer */}
          <div className="mt-12 p-6 glass-card">
            <div className="flex items-start space-x-3">
              <AlertTriangle className="w-5 h-5 text-orange-400 mt-0.5 flex-shrink-0" />
              <div className="text-sm text-night/70 dark:text-white/70">
                <p className="font-medium mb-2">Aviso Importante - CNV</p>
                <p>
                  Las recomendaciones presentadas son generadas por inteligencia artificial y no constituyen
                  asesoramiento financiero personalizado. Los precios y análisis son simulados con fines demostrativos.
                  Consulte con un asesor financiero profesional antes de tomar decisiones de inversión. Existe riesgo de
                  pérdida de capital.
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
