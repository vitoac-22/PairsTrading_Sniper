"""
Entry point for the Pairs Trading Bot.
Orquestador principal.
"""
from src.data_loader import DataLoader
from src.stat_engine import StatEngine
import matplotlib.pyplot as plt

if __name__ == "__main__":
    print("--- System Online. Ready to hunt inefficiencies. ---\n")
    
    # 1. Configuración
    TICKER_X = 'MSFT' # Benchmark
    TICKER_Y = 'GOOG' # Asset to trade
    START = '2023-01-01'
    END = '2024-01-01'
    
    # 2. Cargar Datos
    loader = DataLoader([TICKER_X, TICKER_Y], START, END)
    df = loader.get_aligned_pairs()
    
    # 3. Análisis Estadístico
    engine = StatEngine(df, TICKER_X, TICKER_Y)
    
    # Verificar si están cointegrados
    p_value, is_coint = engine.check_cointegration()
    
    if is_coint:
        print("\n>>> ¡ALERTA! Par Cointegrado encontrado. Iniciando análisis de señales...")
        
        # Calcular Spread y Z-Score
        spread, z_score = engine.compute_spread_and_zscore(window=20)
        
        # Visualización rápida (Cínica: ver para creer)
        plt.figure(figsize=(12, 6))
        z_score.plot(label='Z-Score (30d Rolling)')
        plt.axhline(2.0, color='red', linestyle='--', label='Venta (Overvalued)')
        plt.axhline(-2.0, color='green', linestyle='--', label='Compra (Undervalued)')
        plt.axhline(0, color='black', alpha=0.5)
        plt.title(f"Z-Score Monitor: {TICKER_Y} vs {TICKER_X}")
        plt.legend()
        plt.show()
        
    else:
        print("\n>>> Este par no sirve. La estadística dice que es ruido. Busca otros.")