"use client"

import { useState } from "react"
import { ArrowLeft, TrendingUp, TrendingDown, Shield, AlertTriangle, Star, PiggyBank, Clock } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import Link from "next/link"

// Datos simulados de acciones argentinas para principiantes
const stocksData = [
  {
    symbol: "CEDEAR AAPL",
    name: "Apple Inc.",
    price: 12500.5,
    change: 125.3,
    changePercent: 1.01,
    recommendation: "COMPRAR",
    confidence: 92,
    sector: "Tecnología",
    risk: "Bajo",
    targetPrice: 13200.0,
    monthlyInvestment: "$1,000",
  },
  {
    symbol: "CEDEAR MSFT",
    name: "Microsoft Corporation",
    price: 11250.0,
    change: 85.5,
    changePercent: 0.76,
    recommendation: "COMPRAR",
    confidence: 90,
    sector: "Tecnología",
    risk: "Bajo",
    targetPrice: 12000.0,
    monthlyInvestment: "$1,000",
  },
  {
    symbol: "CEDEAR KO",
    name: "Coca-Cola Company",
    price: 6890.75,
    change: 45.25,
    changePercent: 0.66,
    recommendation: "COMPRAR",
    confidence: 85,
    sector: "Consumo",
    risk: "Bajo",
    targetPrice: 7200.0,
    monthlyInvestment: "$800",
  },
  {
    symbol: "CEDEAR PG",
    name: "Procter & Gamble",
    price: 8425.3,
    change: 28.7,
    changePercent: 0.34,
    recommendation: "MANTENER",
    confidence: 78,
    sector: "Consumo",
    risk: "Bajo",
    targetPrice: 8600.0,
    monthlyInvestment: "$800",
  },
  {
    symbol: "CEDEAR JNJ",
    name: "Johnson & Johnson",
    price: 7150.0,
    change: -25.0,
    changePercent: -0.35,
    recommendation: "MANTENER",
    confidence: 75,
    sector: "Salud",
    risk: "Bajo",
    targetPrice: 7300.0,
    monthlyInvestment: "$700",
  },
]

// Datos simulados de bonos argentinos para principiantes
const bondsData = [
  {
    symbol: "TX26",
    name: "Bono del Tesoro 2026",
    price: 98.25,
    change: 0.15,
    changePercent: 0.15,
    recommendation: "COMPRAR",
    confidence: 88,
    yield: 8.5,
    duration: 2.5,
    risk: "Medio-Bajo",
    monthlyInvestment: "$1,500",
  },
  {
    symbol: "TO23",
    name: "Bono del Tesoro 2023",
    price: 99.8,
    change: 0.05,
    changePercent: 0.05,
    recommendation: "COMPRAR",
    confidence: 92,
    yield: 7.2,
    duration: 0.8,
    risk: "Bajo",
    monthlyInvestment: "$2,000",
  },
  {
    symbol: "LECAP",
    name: "Letras Capitalizables",
    price: 99.9,
    change: 0.02,
    changePercent: 0.02,
    recommendation: "COMPRAR",
    confidence: 95,
    yield: 6.8,
    duration: 0.5,
    risk: "Muy Bajo",
    monthlyInvestment: "$2,500",
  },
]

export default function RecomendacionesPage() {
  const [activeTab, setActiveTab] = useState<"acciones" | "bonos">("acciones")

  const getRecommendationColor = (rec: string) => {
    switch (rec) {
      case "COMPRAR":
        return "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400 border-green-200 dark:border-green-800"
      case "MANTENER":
        return "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400 border-yellow-200 dark:border-yellow-800"
      case "VENDER":
        return "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400 border-red-200 dark:border-red-800"
      default:
        return "bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-400 border-gray-200 dark:border-gray-700"
    }
  }

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case "Muy Bajo":
        return "text-green-600 dark:text-green-400"
      case "Bajo":
        return "text-green-600 dark:text-green-400"
      case "Medio-Bajo":
        return "text-yellow-600 dark:text-yellow-400"
      case "Medio":
        return "text-yellow-600 dark:text-yellow-400"
      case "Alto":
        return "text-orange-600 dark:text-orange-400"
      case "Muy Alto":
        return "text-red-600 dark:text-red-400"
      default:
        return "text-gray-600 dark:text-gray-400"
    }
  }

  return (
    <div className="min-h-screen bg-white dark:bg-gray-950">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-white dark:bg-gray-950 border-b border-gray-200 dark:border-gray-800">
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Link href="/">
              <Button
                variant="ghost"
                size="sm"
                className="text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800"
              >
                <ArrowLeft className="w-4 h-4 mr-2" />
                Volver
              </Button>
            </Link>
            <div className="flex items-center space-x-2">
              <PiggyBank className="w-6 h-6 text-blue-600" />
              <span className="text-xl font-semibold text-gray-900 dark:text-white">ArgentaAI</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="pt-24 pb-12 px-6">
        <div className="container mx-auto max-w-7xl">
          {/* Page Header */}
          <div className="text-center mb-12">
            <h1 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Recomendaciones para principiantes
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Opciones simples y seguras para comenzar a invertir con montos pequeños cada mes
            </p>
          </div>

          {/* Tabs */}
          <div className="flex justify-center mb-8">
            <div className="bg-gray-100 dark:bg-gray-800 p-1 rounded-lg flex space-x-1">
              <Button
                variant={activeTab === "acciones" ? "default" : "ghost"}
                onClick={() => setActiveTab("acciones")}
                className={`px-6 py-2 ${
                  activeTab === "acciones"
                    ? "bg-blue-600 text-white"
                    : "text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700"
                }`}
              >
                <TrendingUp className="w-4 h-4 mr-2" />
                CEDEARs
              </Button>
              <Button
                variant={activeTab === "bonos" ? "default" : "ghost"}
                onClick={() => setActiveTab("bonos")}
                className={`px-6 py-2 ${
                  activeTab === "bonos"
                    ? "bg-blue-600 text-white"
                    : "text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700"
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
                  <div
                    key={stock.symbol}
                    className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm p-6 hover:shadow-md transition-shadow"
                  >
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h3 className="text-xl font-semibold text-gray-900 dark:text-white">{stock.symbol}</h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400">{stock.name}</p>
                        <p className="text-xs text-gray-500 dark:text-gray-500">{stock.sector}</p>
                      </div>
                      <Badge className={getRecommendationColor(stock.recommendation)}>{stock.recommendation}</Badge>
                    </div>

                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-2xl font-bold text-gray-900 dark:text-white">
                          ${stock.price.toLocaleString("es-AR")}
                        </span>
                        <div
                          className={`flex items-center ${stock.change >= 0 ? "text-green-600 dark:text-green-400" : "text-red-600 dark:text-red-400"}`}
                        >
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
                          <span className="text-gray-500 dark:text-gray-400">Inversión mensual:</span>
                          <p className="font-medium text-gray-900 dark:text-white">{stock.monthlyInvestment}</p>
                        </div>
                        <div>
                          <span className="text-gray-500 dark:text-gray-400">Confianza:</span>
                          <div className="flex items-center">
                            <Star className="w-3 h-3 text-yellow-500 mr-1" />
                            <span className="font-medium text-gray-900 dark:text-white">{stock.confidence}%</span>
                          </div>
                        </div>
                        <div>
                          <span className="text-gray-500 dark:text-gray-400">Riesgo:</span>
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
                  <div
                    key={bond.symbol}
                    className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm p-6 hover:shadow-md transition-shadow"
                  >
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h3 className="text-xl font-semibold text-gray-900 dark:text-white">{bond.symbol}</h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400">{bond.name}</p>
                      </div>
                      <Badge className={getRecommendationColor(bond.recommendation)}>{bond.recommendation}</Badge>
                    </div>

                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-2xl font-bold text-gray-900 dark:text-white">
                          ${bond.price.toFixed(2)}
                        </span>
                        <div
                          className={`flex items-center ${bond.change >= 0 ? "text-green-600 dark:text-green-400" : "text-red-600 dark:text-red-400"}`}
                        >
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
                          <span className="text-gray-500 dark:text-gray-400">Rendimiento:</span>
                          <p className="font-medium text-blue-600">{bond.yield.toFixed(1)}%</p>
                        </div>
                        <div>
                          <span className="text-gray-500 dark:text-gray-400">Duración:</span>
                          <p className="font-medium text-gray-900 dark:text-white">{bond.duration} años</p>
                        </div>
                        <div>
                          <span className="text-gray-500 dark:text-gray-400">Inversión mensual:</span>
                          <p className="font-medium text-gray-900 dark:text-white">{bond.monthlyInvestment}</p>
                        </div>
                        <div>
                          <span className="text-gray-500 dark:text-gray-400">Riesgo:</span>
                          <p className={`font-medium ${getRiskColor(bond.risk)}`}>{bond.risk}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Beginner's Guide */}
          <div className="mt-16 bg-blue-50 dark:bg-blue-900/20 rounded-xl p-8">
            <div className="flex flex-col md:flex-row items-start md:items-center gap-6">
              <div className="bg-blue-100 dark:bg-blue-800/30 p-4 rounded-full">
                <Clock className="w-8 h-8 text-blue-600 dark:text-blue-400" />
              </div>
              <div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Guía para principiantes</h3>
                <p className="text-gray-700 dark:text-gray-300 mb-4">
                  Recomendamos comenzar con inversiones pequeñas y regulares. Invertir una cantidad fija cada mes te
                  ayuda a promediar el costo de tus inversiones y reducir el impacto de la volatilidad del mercado.
                </p>
                <Button
                  variant="outline"
                  className="border-blue-600 text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/20"
                >
                  Ver tutorial completo
                </Button>
              </div>
            </div>
          </div>

          {/* Disclaimer */}
          <div className="mt-12 p-6 bg-gray-50 dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800">
            <div className="flex items-start space-x-3">
              <AlertTriangle className="w-5 h-5 text-yellow-500 mt-0.5 flex-shrink-0" />
              <div className="text-sm text-gray-600 dark:text-gray-400">
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
