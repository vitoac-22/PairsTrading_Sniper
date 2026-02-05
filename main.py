"""
Entry point for the Pairs Trading Bot.
Orquestador principal.
"""
from src.data_loader import DataLoader
from src.stat_engine import StatEngine
from src.backtester import Backtester # <--- NUEVO IMPORT
import matplotlib.pyplot as plt

if __name__ == "__main__":
    print("--- System Online. Ready to hunt inefficiencies. ---\n")
    
    # 1. Configuración (Prueba GOOG vs GOOGL para ver ganancias casi seguras)
    TICKER_X = 'GOOGL' 
    TICKER_Y = 'GOOG' 
    START = '2022-01-01'
    END = '2024-01-01'
    
    # 2. Cargar Datos
    loader = DataLoader([TICKER_X, TICKER_Y], START, END)
    df = loader.get_aligned_pairs()
    
    # 3. Análisis Estadístico
    engine = StatEngine(df, TICKER_X, TICKER_Y)
    p_value, is_coint = engine.check_cointegration()
    
    if is_coint:
        print("\n>>> ¡ALERTA! Par Cointegrado encontrado. Iniciando Backtest...")
        
        # Calcular Spread y Z-Score
        spread, z_score = engine.compute_spread_and_zscore(window=30)
        
        # 4. Simulación (Backtest)
        bot = Backtester(initial_capital=10000, transaction_cost=0.0005) # 0.05% comisión
        results = bot.run_backtest(spread, z_score)
        
        final_value = results['Portfolio_Value'].iloc[-1]
        roi = ((final_value - 10000) / 10000) * 100
        
        print(f"\nResultados Finales:")
        print(f"Capital Inicial: $10,000")
        print(f"Capital Final:   ${final_value:.2f}")
        print(f"Retorno Total:   {roi:.2f}%")
        
        # Visualización
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
        
        # Gráfico 1: El Spread y las entradas
        spread.plot(ax=ax1, color='blue', alpha=0.6, label='Spread')
        ax1.set_title(f"Spread de Precios: {TICKER_Y} - ({engine.hedge_ratio:.2f} * {TICKER_X})")
        ax1.legend()
        
        # Gráfico 2: Crecimiento del dinero
        results['Portfolio_Value'].plot(ax=ax2, color='green', label='Equity Curve')
        ax2.set_title("Evolución del Capital (Equity Curve)")
        ax2.legend()
        
        plt.tight_layout()
        plt.show()
        
    else:
        print("\n>>> Este par no sirve. La estadística dice que es ruido. Busca otros.")