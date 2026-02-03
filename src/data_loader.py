"""
Module: data_loader.py
Description: Gestor de descarga y limpieza de datos financieros.
             Se encarga de que las series de tiempo estén alineadas.
"""

import yfinance as yf
import pandas as pd

class DataLoader:
    def __init__(self, tickers, start_date, end_date):
        """
        Inicializa el cargador de datos.
        :param tickers: Lista de strings ['KO', 'PEP']
        :param start_date: String 'YYYY-MM-DD'
        :param end_date: String 'YYYY-MM-DD'
        """
        self.tickers = tickers
        self.start = start_date
        self.end = end_date
        self.data = None

    def fetch_data(self):
        """Descarga datos de Yahoo Finance."""
        print(f"--- Iniciando descarga para: {self.tickers} ---")
        try:
            # auto_adjust=True nos da precios ajustados por dividendos y splits (crucial)
            raw_data = yf.download(self.tickers, start=self.start, end=self.end, auto_adjust=True)
            
            # yfinance a veces devuelve un MultiIndex complejo, simplificamos:
            if 'Close' in raw_data.columns:
                self.data = raw_data['Close']
            else:
                self.data = raw_data # Fallback
            
            print(f"Descarga completada. Filas obtenidas: {len(self.data)}")
            return self.data
        except Exception as e:
            print(f"Error crítico en la descarga: {e}")
            return None
    
    def get_aligned_pairs(self):
        """
        Retorna un DataFrame limpio sin valores nulos (NaN).
        Si un activo no cotizó un día, borramos ese día para ambos.
        """
        if self.data is None:
            self.fetch_data()
            
        # Eliminar cualquier fila que tenga al menos un NaN
        clean_data = self.data.dropna()
        
        # Verificación cínica
        lost_rows = len(self.data) - len(clean_data)
        if lost_rows > 0:
            print(f"Aviso: Se eliminaron {lost_rows} filas por datos faltantes (mercados cerrados/errores).")
            
        return clean_data