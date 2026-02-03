"""
Module: stat_engine.py
Description: Núcleo matemático. Calcula cointegración, Hedge Ratio y Z-Scores.
             Aquí es donde se valida si la estrategia tiene sentido estadístico.
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint

class StatEngine:
    def __init__(self, dataframe, ticker_x, ticker_y):
        """
        :param dataframe: DF con columnas alineadas de precios.
        :param ticker_x: El activo independiente (Benchmark)
        :param ticker_y: El activo dependiente (El que tradeamos)
        """
        self.df = dataframe
        self.x_name = ticker_x
        self.y_name = ticker_y
        self.hedge_ratio = None
        self.spread = None

    def check_cointegration(self):
        """
        Ejecuta el test de Engle-Granger.
        H0: No hay cointegración.
        Si p-value < 0.05, rechazamos H0 -> ¡Hay dinero aquí!
        """
        x = self.df[self.x_name]
        y = self.df[self.y_name]
        
        # El test retorna: t-stat, p-value, critical_values
        score, pvalue, _ = coint(y, x)
        
        is_cointegrated = pvalue < 0.05
        print(f"Resultados Cointegración ({self.y_name} vs {self.x_name}):")
        print(f"   P-Value: {pvalue:.5f} [{'✅ APROBADO' if is_cointegrated else '❌ FALLIDO'}]")
        
        return pvalue, is_cointegrated

    def calculate_hedge_ratio(self):
        """
        Calcula beta (pendiente) usando regresión lineal (OLS).
        Y = beta * X + alpha
        """
        x = self.df[self.x_name]
        y = self.df[self.y_name]
        
        # Añadir constante para el intercepto (alpha)
        x_with_const = sm.add_constant(x)
        
        model = sm.OLS(y, x_with_const).fit()
        
        # La pendiente es el segundo parámetro (el primero es la constante)
        self.hedge_ratio = model.params.iloc[1]
        print(f"Hedge Ratio calculado: {self.hedge_ratio:.4f}")
        return self.hedge_ratio

    def compute_spread_and_zscore(self, window=30):
        """
        1. Calcula el Spread (Diferencia de precios ajustada).
        2. Calcula el Z-Score ROLLING (Ventana móvil).
           No usamos media histórica total para evitar 'look-ahead bias'.
        """
        if self.hedge_ratio is None:
            self.calculate_hedge_ratio()
            
        x = self.df[self.x_name]
        y = self.df[self.y_name]
        
        # Cálculo del Spread
        self.spread = y - (self.hedge_ratio * x)
        
        # Cálculo del Z-Score Móvil
        # (Spread - Media_Movil) / Desviacion_Movil
        rolling_mean = self.spread.rolling(window=window).mean()
        rolling_std = self.spread.rolling(window=window).std()
        
        z_score = (self.spread - rolling_mean) / rolling_std
        
        return self.spread, z_score