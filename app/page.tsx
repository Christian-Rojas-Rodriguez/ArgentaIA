"use client"

import { useState, useEffect } from "react"
import { ArrowRight, Clock, Shield, BarChart3, PiggyBank } from "lucide-react"
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
    <div className="min-h-screen bg-white dark:bg-gray-950">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-white dark:bg-gray-950 border-b border-gray-200 dark:border-gray-800">
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <PiggyBank className="w-8 h-8 text-blue-600" />
            <span className="text-xl font-semibold text-gray-900 dark:text-white">ArgentaAI</span>
          </div>
          <div className="flex items-center space-x-3">
            <ThemeToggle />
            <Button
              variant="outline"
              className="border-blue-600 text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/20"
            >
              Probar demo
            </Button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="pt-32 pb-16 px-6">
        <div className="container mx-auto text-center max-w-3xl">
          <div className="mb-6 text-blue-600 font-medium">Invierte a tu manera</div>
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-6">
            Beneficios de invertir con ArgentaAI
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-2xl mx-auto">
            Herramientas simples, inversiones confiables y cero complicaciones — todo lo que necesitas para invertir con
            confianza mes a mes.
          </p>
          <Link href="/recomendaciones">
            <Button className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-6 text-lg font-medium rounded-xl">
              Ver recomendaciones
              <ArrowRight className="ml-2 w-5 h-5" />
            </Button>
          </Link>
        </div>
      </section>

      {/* Benefits Grid */}
      <section className="py-12 px-6">
        <div className="container mx-auto max-w-6xl">
          <div className="grid md:grid-cols-12 gap-8">
            {/* Left Panel */}
            <div className="md:col-span-5 bg-blue-600 text-white rounded-xl p-10 flex flex-col justify-between">
              <div className="space-y-16">
                <div>
                  <h2 className="text-3xl font-bold mb-2">&gt; 5 Minutos</h2>
                  <p className="text-blue-100">
                    Te toma menos de 5 minutos encontrar la inversión perfecta para tu perfil de riesgo.
                  </p>
                </div>

                <div>
                  <h2 className="text-3xl font-bold mb-2">0 Complicaciones</h2>
                  <p className="text-blue-100">
                    Sin jerga financiera ni procesos complejos. Todo está explicado en lenguaje simple.
                  </p>
                </div>

                <div>
                  <h2 className="text-3xl font-bold mb-2">Libertad Total</h2>
                  <p className="text-blue-100">
                    Elige la inversión que se sienta correcta para ti — sin presiones, solo tu decisión.
                  </p>
                </div>
              </div>
            </div>

            {/* Right Panel */}
            <div className="md:col-span-7 grid grid-cols-1 md:grid-cols-2 gap-8">
              {/* Card 1 */}
              <div className="bg-gray-50 dark:bg-gray-900 p-6 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm">
                <div className="mb-4 bg-blue-100 dark:bg-blue-900/30 w-10 h-10 rounded-full flex items-center justify-center">
                  <PiggyBank className="w-5 h-5 text-blue-600" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Ahorra $1.200 Anualmente</h3>
                <p className="text-gray-600 dark:text-gray-300">
                  Obtén inversiones personalizadas con comisiones mínimas — sin gastos ocultos.
                </p>
              </div>

              {/* Card 2 */}
              <div className="bg-gray-50 dark:bg-gray-900 p-6 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm">
                <div className="mb-4 bg-blue-100 dark:bg-blue-900/30 w-10 h-10 rounded-full flex items-center justify-center">
                  <Clock className="w-5 h-5 text-blue-600" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Inversión Automática</h3>
                <p className="text-gray-600 dark:text-gray-300">
                  Configura una vez y olvídate. Invierte automáticamente cada mes sin esfuerzo.
                </p>
              </div>

              {/* Card 3 */}
              <div className="bg-gray-50 dark:bg-gray-900 p-6 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm">
                <div className="mb-4 bg-blue-100 dark:bg-blue-900/30 w-10 h-10 rounded-full flex items-center justify-center">
                  <BarChart3 className="w-5 h-5 text-blue-600" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Compara 15+ Opciones</h3>
                <p className="text-gray-600 dark:text-gray-300">
                  Analizamos las mejores opciones del mercado argentino para pequeños inversores.
                </p>
              </div>

              {/* Card 4 */}
              <div className="bg-gray-50 dark:bg-gray-900 p-6 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm">
                <div className="mb-4 bg-blue-100 dark:bg-blue-900/30 w-10 h-10 rounded-full flex items-center justify-center">
                  <Shield className="w-5 h-5 text-blue-600" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Riesgo Controlado</h3>
                <p className="text-gray-600 dark:text-gray-300">
                  Tu dinero está protegido — seleccionamos solo opciones de bajo riesgo para principiantes.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Why Trust Section */}
      <section className="py-16 px-6">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">¿Por qué confiar en nosotros?</h2>
            <p className="text-xl text-gray-600 dark:text-gray-300">
              Resultados que respaldan nuestras recomendaciones
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-8 bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm">
              <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center mx-auto mb-6">
                <BarChart3 className="w-8 h-8 text-blue-600" />
              </div>
              <div className="text-4xl font-bold text-blue-600 mb-2">8.5%</div>
              <div className="text-lg font-medium text-gray-900 dark:text-white mb-2">Rendimiento Promedio</div>
              <p className="text-gray-600 dark:text-gray-400">Retorno anual promedio para inversores principiantes</p>
            </div>

            <div className="text-center p-8 bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm">
              <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center mx-auto mb-6">
                <Shield className="w-8 h-8 text-blue-600" />
              </div>
              <div className="text-4xl font-bold text-blue-600 mb-2">-5.2%</div>
              <div className="text-lg font-medium text-gray-900 dark:text-white mb-2">Máxima Caída</div>
              <p className="text-gray-600 dark:text-gray-400">Pérdida máxima histórica en nuestras recomendaciones</p>
            </div>

            <div className="text-center p-8 bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm">
              <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center mx-auto mb-6">
                <PiggyBank className="w-8 h-8 text-blue-600" />
              </div>
              <div className="text-4xl font-bold text-blue-600 mb-2">$500</div>
              <div className="text-lg font-medium text-gray-900 dark:text-white mb-2">Inversión Mínima</div>
              <p className="text-gray-600 dark:text-gray-400">Comienza con poco y aumenta cuando te sientas cómodo</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-6 border-t border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-950">
        <div className="container mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <PiggyBank className="w-6 h-6 text-blue-600" />
              <span className="text-lg font-medium text-gray-900 dark:text-white">ArgentaAI</span>
            </div>

            <div className="flex space-x-6 mb-4 md:mb-0">
              <a href="#" className="text-gray-600 dark:text-gray-400 hover:text-blue-600 transition-colors">
                Términos
              </a>
              <a href="#" className="text-gray-600 dark:text-gray-400 hover:text-blue-600 transition-colors">
                Privacidad
              </a>
              <a href="#" className="text-gray-600 dark:text-gray-400 hover:text-blue-600 transition-colors">
                Contacto
              </a>
            </div>
          </div>

          <div className="mt-8 pt-8 border-t border-gray-200 dark:border-gray-800 text-center">
            <p className="text-sm text-gray-500 dark:text-gray-400">
              <strong>Disclaimer CNV:</strong> Las recomendaciones no constituyen asesoramiento financiero. Consulte con
              un profesional antes de invertir. Riesgo de pérdida de capital.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
