from data.price_fetcher import fetch_historical_data
from indicators.trend import get_trend_indicators
from indicators.momentum import get_momentum_indicators
from indicators.volatility import get_volatility_indicators

def analyze_stock_technicals(ticker: str) -> dict:
    """
    Belirli bir hissenin teknik analiz röntgenini çeker.
    Tüm indikatörleri çalıştırır ve ortak bir sonuç döner.
    """
    # Veri çek (Son 1 yıllık günlük veri, SMA200 hesabı için yeterli)
    df = fetch_historical_data(ticker, period="1y", interval="1d")
    
    if df is None or df.empty:
        return {"error": f"{ticker} için geçmiş veri alınamadı."}
        
    trend_results = get_trend_indicators(df)
    momentum_results = get_momentum_indicators(df)
    volatility_results = get_volatility_indicators(df)
    
    close_price = round(df.iloc[-1].get('Close', 0), 2)
    
    # Tüm sonuçları birleştir
    technical_summary = {
        "hisse": ticker.upper(),
        "kapanis_fiyati": close_price,
        "Trend": trend_results,
        "Momentum": momentum_results,
        "Volatilite": volatility_results
    }
    
    return technical_summary
