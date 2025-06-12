"use client"

import { useState, useEffect } from "react"
import { ArrowRight, TrendingUp, Shield, BarChart3, Newspaper, Target, Activity } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ThemeToggle } from "@/components/theme-toggle"
import Link from "next/link"

export default function LandingPage() {
  const [scrollY, setScrollY] = useState(0)

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY)
    window.addEventListener("scroll", handleScroll)
    return () => window.removeEventListener("scroll", handleScroll)
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-night via-teal/20 to-soft-white dark:from-night dark:via-night/90 dark:to-night/70 relative overflow-hidden">
      {/* Animated Background Arcs */}
      <div className="fixed inset-0 pointer-events-none">
        <div
          className="absolute -top-1/2 -left-1/4 w-96 h-96 bg-gradient-radial from-teal/30 via-teal/10 to-transparent rounded-full blur-3xl"
          style={{ transform: `translateY(${scrollY * 0.1}px)` }}
        />
        <div
          className="absolute top-1/4 -right-1/4 w-80 h-80 bg-gradient-radial from-orange/20 via-orange/5 to-transparent rounded-full blur-3xl"
          style={{ transform: `translateY(${scrollY * -0.05}px)` }}
        />
        <div
          className="absolute -bottom-1/4 left-1/3 w-72 h-72 bg-gradient-radial from-night/20 via-night/5 to-transparent rounded-full blur-3xl"
          style={{ transform: `translateY(${scrollY * 0.08}px)` }}
        />
      </div>

      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 backdrop-blur-md bg-white/10 dark:bg-black/20 border-b border-white/20 dark:border-white/10">
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <TrendingUp className="w-8 h-8 text-teal" />
            <span className="text-xl font-semibold text-night dark:text-white">ArgentaAI</span>
          </div>
          <div className="flex items-center space-x-3">
            <ThemeToggle />
            <Button
              variant="outline"
              className="glass-button text-night dark:text-white border-white/30 hover:bg-white/20"
            >
              Probar demo
            </Button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-6">
        <div className="container mx-auto text-center max-w-4xl">
          <div className="animate-fade-in">
            <h1 className="text-5xl md:text-6xl font-semibold text-night dark:text-white mb-6 leading-tight">
              Top 10 activos argentinos
              <br />
              <span className="text-teal">IA explicable</span>
            </h1>
            <p className="text-xl text-night/80 dark:text-white/80 mb-8 max-w-2xl mx-auto">
              Recomendaciones inteligentes de acciones y bonos con análisis transparente y métricas de riesgo en tiempo
              real.
            </p>
            <Link href="/recomendaciones">
              <Button className="bg-gradient-to-r from-teal to-teal/80 hover:from-teal/90 hover:to-teal/70 text-white px-8 py-3 text-lg font-medium rounded-xl shadow-lg hover:shadow-xl transition-all duration-300">
                Ver recomendaciones
                <ArrowRight className="ml-2 w-5 h-5" />
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Cards Mosaic */}
      <section className="py-20 px-6">
        <div className="container mx-auto">
          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            <div className="glass-card group">
              <div className="p-8">
                <div className="w-12 h-12 bg-gradient-to-br from-teal to-teal/70 rounded-xl flex items-center justify-center mb-6">
                  <TrendingUp className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-2xl font-semibold text-night dark:text-white mb-4">Acciones</h3>
                <p className="text-night/70 dark:text-white/70 mb-6">
                  Análisis técnico y fundamental de las principales acciones del MERVAL con predicciones basadas en IA.
                </p>
                <div className="flex items-center text-teal font-medium">
                  Ver análisis <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </div>
              </div>
            </div>

            <div className="glass-card group">
              <div className="p-8">
                <div className="w-12 h-12 bg-gradient-to-br from-orange to-orange/70 rounded-xl flex items-center justify-center mb-6">
                  <Shield className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-2xl font-semibold text-night dark:text-white mb-4">Bonos</h3>
                <p className="text-night/70 dark:text-white/70 mb-6">
                  Evaluación de riesgo país y oportunidades en bonos soberanos y corporativos argentinos.
                </p>
                <div className="flex items-center text-orange font-medium">
                  Explorar bonos <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </div>
              </div>
            </div>

            <div className="glass-card group">
              <div className="p-8">
                <div className="w-12 h-12 bg-gradient-to-br from-night to-night/70 rounded-xl flex items-center justify-center mb-6">
                  <Newspaper className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-2xl font-semibold text-night dark:text-white mb-4">Noticias</h3>
                <p className="text-night/70 dark:text-white/70 mb-6">
                  Análisis de sentimiento en tiempo real de noticias que impactan el mercado argentino.
                </p>
                <div className="flex items-center text-night dark:text-white font-medium">
                  Leer insights <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Why Trust Section */}
      <section className="py-20 px-6">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-semibold text-night dark:text-white mb-4">¿Por qué confiar?</h2>
            <p className="text-xl text-night/70 dark:text-white/70">Métricas que respaldan nuestras recomendaciones</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center neuro-card">
              <div className="w-16 h-16 bg-gradient-to-br from-teal to-teal/70 rounded-2xl flex items-center justify-center mx-auto mb-6">
                <BarChart3 className="w-8 h-8 text-white" />
              </div>
              <div className="text-4xl font-bold text-teal mb-2">89.2%</div>
              <div className="text-lg font-medium text-night dark:text-white mb-2">Precisión Back-test</div>
              <p className="text-night/60 dark:text-white/60">Últimos 24 meses de predicciones validadas</p>
            </div>

            <div className="text-center neuro-card">
              <div className="w-16 h-16 bg-gradient-to-br from-orange to-orange/70 rounded-2xl flex items-center justify-center mx-auto mb-6">
                <Target className="w-8 h-8 text-white" />
              </div>
              <div className="text-4xl font-bold text-orange mb-2">2.34</div>
              <div className="text-lg font-medium text-night dark:text-white mb-2">Ratio Sharpe</div>
              <p className="text-night/60 dark:text-white/60">Retorno ajustado por riesgo superior al mercado</p>
            </div>

            <div className="text-center neuro-card">
              <div className="w-16 h-16 bg-gradient-to-br from-night to-night/70 rounded-2xl flex items-center justify-center mx-auto mb-6">
                <Activity className="w-8 h-8 text-white" />
              </div>
              <div className="text-4xl font-bold text-night dark:text-white mb-2">-12.5%</div>
              <div className="text-lg font-medium text-night dark:text-white mb-2">Max Draw-down</div>
              <p className="text-night/60 dark:text-white/60">Pérdida máxima controlada en períodos adversos</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-6 border-t border-white/20 backdrop-blur-sm bg-white/5">
        <div className="container mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <TrendingUp className="w-6 h-6 text-teal" />
              <span className="text-lg font-medium text-night dark:text-white">ArgentaAI</span>
            </div>

            <div className="flex space-x-6 mb-4 md:mb-0">
              <a href="#" className="text-night/70 dark:text-white/70 hover:text-teal transition-colors">
                Términos
              </a>
              <a href="#" className="text-night/70 dark:text-white/70 hover:text-teal transition-colors">
                Privacidad
              </a>
              <a href="#" className="text-night/70 dark:text-white/70 hover:text-teal transition-colors">
                Contacto
              </a>
            </div>
          </div>

          <div className="mt-8 pt-8 border-t border-white/10 text-center">
            <p className="text-sm text-night/60 dark:text-white/60">
              <strong>Disclaimer CNV:</strong> Las recomendaciones no constituyen asesoramiento financiero. Consulte con
              un profesional antes de invertir. Riesgo de pérdida de capital.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
