import pandas as pd

def get_trend_indicators(df: pd.DataFrame) -> dict:
    """
    Pandas yerleşik fonksiyonları ile Trend indikatörlerini hesaplar.
    Hata payı risklerini (numba vb) tamamen siler.
    """
    if df is None or df.empty or len(df) < 50:
        return {"error": "Yeterli veri yok"}
        
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()
    
    # ADX Basit Yaklaşım
    period = 14
    plus_dm = df['High'].diff()
    minus_dm = df['Low'].diff()
    plus_dm = plus_dm.where(plus_dm > 0, 0)
    minus_dm = (-minus_dm).where(minus_dm > 0, 0)
    
    tr1 = df['High'] - df['Low']
    tr2 = (df['High'] - df['Close'].shift()).abs()
    tr3 = (df['Low'] - df['Close'].shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    atr = tr.ewm(span=period, adjust=False).mean()
    plus_di = 100 * (plus_dm.ewm(span=period, adjust=False).mean() / atr)
    minus_di = 100 * (minus_dm.ewm(span=period, adjust=False).mean() / atr)
    
    dx = (abs(plus_di - minus_di) / abs(plus_di + minus_di)) * 100
    df['ADX_14'] = dx.ewm(span=period, adjust=False).mean()
    
    last_row = df.iloc[-1]
    
    # Basit bir trend yorumu
    trend_durumu = "Yatay"
    if last_row['SMA_20'] > last_row['SMA_50'] and last_row['Close'] > last_row['SMA_20']:
        trend_durumu = "Güçlü Yükseliş"
    elif last_row['SMA_20'] < last_row['SMA_50'] and last_row['Close'] < last_row['SMA_20']:
        trend_durumu = "Güçlü Düşüş"
        
    return {
        "SMA_20": round(last_row['SMA_20'], 2) if not pd.isna(last_row['SMA_20']) else 0,
        "SMA_50": round(last_row['SMA_50'], 2) if not pd.isna(last_row['SMA_50']) else 0,
        "EMA_200": round(last_row['EMA_200'], 2) if not pd.isna(last_row['EMA_200']) else 0,
        "ADX_14": round(last_row['ADX_14'], 2) if not pd.isna(last_row['ADX_14']) else 0,
        "Trend_Yorumu": trend_durumu
    }
