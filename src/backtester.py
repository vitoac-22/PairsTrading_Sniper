"""
Module: backtester.py
Description: Motor de simulación. Ejecuta las señales históricas y calcula PnL (Ganancias y Pérdidas).
             Incluye lógica de 'Mark-to-Market' diaria.
"""

import pandas as pd
import numpy as np

class Backtester:
    def __init__(self, initial_capital=10000, transaction_cost=0.001):
        """
        :param initial_capital: Dinero inicial (USD).
        :param transaction_cost: Costo por operación (0.1% por defecto).
                                 Sé cínico con esto, las comisiones matan estrategias.
        """
        self.capital = initial_capital
        self.initial_capital = initial_capital
        self.cost = transaction_cost
        self.positions = 0  # 1 = Long Spread, -1 = Short Spread, 0 = Flat
        self.equity_curve = []
        
    def run_backtest(self, spread_series, z_score_series, entry_threshold=2.0, exit_threshold=0.0):
        """
        Simula la estrategia paso a paso.
        Reglas:
            - Si Z > 2.0: Vender el Spread (Short Y, Long X). Esperamos que baje.
            - Si Z < -2.0: Comprar el Spread (Long Y, Short X). Esperamos que suba.
            - Si Z cruza 0: Cerrar posiciones (Take Profit).
        """
        print(f"--- Iniciando Backtest (Capital: ${self.initial_capital}) ---")
        
        # DataFrame para guardar el historial
        history = pd.DataFrame(index=spread_series.index)
        history['Spread'] = spread_series
        history['Z_Score'] = z_score_series
        history['Position'] = 0 # Lo que tenemos
        history['PnL_Daily'] = 0.0
        
        current_pos = 0 # 0 = fuera, 1 = long spread, -1 = short spread
        entry_price = 0
        
        for i in range(len(spread_series)):
            date = spread_series.index[i]
            z = z_score_series.iloc[i]
            price = spread_series.iloc[i]
            
            # 1. Lógica de Salida (Take Profit / Stop Loss implícito al volver a la media)
            if current_pos != 0:
                # Si estábamos Long y el Z subió hasta 0 (o más), vendemos
                if (current_pos == 1 and z >= exit_threshold):
                    pnl = (price - entry_price) - (abs(price) * self.cost)
                    self.capital += pnl
                    current_pos = 0
                    print(f"[{date.date()}] CIERRE LONG. PnL: ${pnl:.2f}")

                # Si estábamos Short y el Z bajó hasta 0 (o menos), compramos
                elif (current_pos == -1 and z <= -exit_threshold):
                    pnl = (entry_price - price) - (abs(price) * self.cost)
                    self.capital += pnl
                    current_pos = 0
                    print(f"[{date.date()}] CIERRE SHORT. PnL: ${pnl:.2f}")
            
            # 2. Lógica de Entrada
            if current_pos == 0:
                # El spread está muy barato (Z < -2), compramos
                if z < -entry_threshold:
                    current_pos = 1
                    entry_price = price
                    # Pagamos comisión al entrar
                    self.capital -= (abs(price) * self.cost)
                    print(f"[{date.date()}] ENTRADA LONG (Spread barato). Z: {z:.2f}")
                
                # El spread está muy caro (Z > 2), vendemos
                elif z > entry_threshold:
                    current_pos = -1
                    entry_price = price
                    self.capital -= (abs(price) * self.cost)
                    print(f"[{date.date()}] ENTRADA SHORT (Spread caro). Z: {z:.2f}")
            
            # Guardar estado
            history.loc[date, 'Position'] = current_pos
            history.loc[date, 'Portfolio_Value'] = self.capital
            
        return history