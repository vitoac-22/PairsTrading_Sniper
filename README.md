# 🎯 Pairs Trading Sniper: Statistical Arbitrage Bot

> *"In the short run, the market is a voting machine but in the long run, it is a weighing machine."* — Benjamin Graham (and this bot exploits the noise in between).

Este repositorio contiene un framework de **Arbitraje Estadístico** automatizado diseñado para identificar y explotar ineficiencias de precios a corto plazo entre dos activos cointegrados.

No se trata de predecir el futuro ni de análisis técnico subjetivo. Se trata de **Reversión a la Media** pura y dura, respaldada por tests de hipótesis robustos.

## 🧠 La Lógica Matemática (The Quant Approach)

El core del proyecto se basa en la hipótesis de que ciertos pares de activos tienen una relación de equilibrio a largo plazo, aunque diverjan a corto plazo.

### 1. Cointegración (No confundir con Correlación)

Usamos el **Test de Engle-Granger** para verificar si la combinación lineal de dos series de tiempo no estacionarias () resulta en una serie estacionaria ().

Donde:

* : Precio del activo dependiente.
* : Precio del activo benchmark.
* : *Hedge Ratio* (calculado vía OLS).
* : El residuo (Spread), que **debe** ser estacionario ().

Si el p-value del test ADF sobre  es , asumimos cointegración.

### 2. Generación de Señales (Z-Score)

Para normalizar la volatilidad, transformamos el Spread en un Z-Score usando una ventana móvil (*Rolling Window*) para evitar el sesgo de anticipación (*Look-ahead bias*):

Reglas de Trading:

* **Short Spread ():** El activo  está caro relativo a . Vendemos , Compramos .
* **Long Spread ():** El activo  está barato relativo a . Compramos , Vendemos .
* **Exit ():** Cerramos posiciones cuando la ineficiencia desaparece.

## 🚀 Arquitectura del Proyecto

El código está estructurado bajo principios de **Programación Orientada a Objetos (OOP)** para garantizar modularidad y escalabilidad.

```text
PairsTrading_Sniper/
├── src/
│   ├── data_loader.py    # Ingesta y limpieza de datos (Yahoo Finance API)
│   ├── stat_engine.py    # Cálculo de Cointegración, Hedge Ratio y Z-Scores
│   ├── backtester.py     # Motor de simulación con gestión de posiciones y PnL
│   └── utils.py          # Utilidades auxiliares
├── main.py               # Orquestador principal del flujo
└── requirements.txt      # Dependencias (pandas, numpy, statsmodels, etc.)

```

## 🛠 Instalación y Uso

1. **Clonar el repositorio:**
```bash
git clone https://github.com/vitoac-22/PairsTrading_Sniper.git
cd PairsTrading_Sniper

```


2. **Instalar dependencias:**
```bash
pip install -r requirements.txt

```


3. **Ejecutar el Backtest:**
Edita `main.py` para seleccionar tus tickers y rango de fechas, luego ejecuta:
```bash
python main.py

```



## 📊 Resultados Esperados

El script generará:

1. **Test de Hipótesis:** Confirmación de si el par seleccionado es estadísticamente viable.
2. **Backtest Report:** Retorno sobre la inversión (ROI) considerando costos de transacción.
3. **Visualización:** Gráficos del comportamiento del Spread y la Curva de Capital (Equity Curve).

---

**Disclaimer:** *Este software es para fines educativos y de investigación. El trading algorítmico conlleva riesgos financieros significativos. No me culpes si el mercado permanece irracional más tiempo del que tú puedes permanecer solvente.*

---
