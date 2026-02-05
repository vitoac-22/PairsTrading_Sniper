# 🎯 Pairs Trading Sniper: Statistical Arbitrage Bot

> *"In the short run, the market is a voting machine but in the long run, it is a weighing machine."* — Benjamin Graham (and this bot exploits the noise in between).

Este repositorio contiene un framework de **Arbitraje Estadístico** automatizado diseñado para identificar y explotar ineficiencias de precios a corto plazo entre dos activos cointegrados.

No se trata de predecir el futuro ni de análisis técnico subjetivo. Se trata de **Reversión a la Media** pura y dura, respaldada por tests de hipótesis robustos.

## 🧠 La Lógica Matemática (The Quant Approach)

El core del proyecto se basa en la hipótesis de que ciertos pares de activos tienen una relación de equilibrio a largo plazo, aunque diverjan a corto plazo.

### 1. Cointegración (No confundir con Correlación)

Usamos el Test de Engle-Granger para verificar si la combinación lineal de dos series de tiempo no estacionarias ($X_t, Y_t$) resulta en una serie estacionaria ($\epsilon_t$). $$Y_t = \beta X_t + \epsilon_t$$
Donde:

* $Y_t$: Precio del activo dependiente.
* $X_t$: Precio del activo benchmark.
* $\beta$: Hedge Ratio (calculado vía OLS).
* $\epsilon_t$: El residuo (Spread), que debe ser estacionario ($I(0)$).

Si el p-value del test ADF sobre $\epsilon_t$ es $< 0.05$, asumimos cointegración.

### 2. Generación de Señales (Z-Score)

$$Z_t = \frac{S_t - \mu_{rolling}}{\sigma_{rolling}}$$

Para normalizar la volatilidad, transformamos el Spread en un Z-Score usando una ventana móvil (*Rolling Window*) para evitar el sesgo de anticipación (*Look-ahead bias*):

Reglas de Trading:

* **Short Spread ($Z > 2.0$):** El activo $Y$ está caro relativo a $X$. Vendemos $Y$, Compramos $\beta \times X$.
* **Long Spread ($Z < -2.0$):** El activo $Y$ está barato relativo a $X$. Compramos $Y$, Vendemos $\beta \times X$.
* **Exit ($Z \approx 0$):** Cerramos posiciones cuando la ineficiencia desaparece.

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
