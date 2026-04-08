import yfinance as yf
from datetime import datetime

def fetch_stock_basic_data(ticker: str) -> dict:
    """
    Fetches basic current data for a given BIST ticker.
    Note: yfinance uses TICKER.IS format for Borsa Istanbul (e.g., THYAO.IS)
    """
    try:
        if not ticker.endswith(".IS"):
            ticker = f"{ticker}.IS"
            
        stock = yf.Ticker(ticker)
        # Fetch latest daily data to get current price and volume
        hist = stock.history(period="1d")
        if hist.empty:
            return {"error": f"No data found for {ticker}"}
            
        current_price = hist['Close'].iloc[-1]
        volume = hist['Volume'].iloc[-1]
        
        return {
            "ticker": ticker,
            "current_price": round(current_price, 2),
            "volume": volume,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
    except Exception as e:
        return {"error": str(e)}

def fetch_bist100_summary() -> dict:
    """
    Fetches BIST 100 summary data using XU100.IS
    """
    return fetch_stock_basic_data("XU100")

def fetch_historical_data(ticker: str, period="1y", interval="1d"):
    """
    OHLCV geçmiş verilerini pandas DataFrame olarak döner.
    İndikatör hesaplamaları için gereklidir.
    """
    try:
        if not ticker.endswith(".IS"):
            ticker = f"{ticker}.IS"
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        return df
    except Exception as e:
        print(f"Error fetching historical data for {ticker}: {e}")
        return None

