import pandas as pd

def get_volatility_indicators(df: pd.DataFrame) -> dict:
    """
    Saf pandas ile Bollinger Bantları ve ATR oynaklık metrikleri
    """
    if df is None or df.empty or len(df) < 20:
        return {"error": "Yeterli volatilite verisi yok"}
        
    # Bollinger Bantları
    period = 20
    std_dev = 2
    
    df['BB_M'] = df['Close'].rolling(window=period).mean()
    rstd = df['Close'].rolling(window=period).std()
    
    df['BB_U'] = df['BB_M'] + (rstd * std_dev)
    df['BB_L'] = df['BB_M'] - (rstd * std_dev)
    
    # ATR
    atr_period = 14
    tr1 = df['High'] - df['Low']
    tr2 = (df['High'] - df['Close'].shift()).abs()
    tr3 = (df['Low'] - df['Close'].shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    df['ATR'] = tr.rolling(window=atr_period).mean()
    
    last_row = df.iloc[-1]
    close_price = last_row.get('Close', 0)
    
    bb_alt = round(last_row['BB_L'], 2) if not pd.isna(last_row['BB_L']) else 0
    bb_orta = round(last_row['BB_M'], 2) if not pd.isna(last_row['BB_M']) else 0
    bb_ust = round(last_row['BB_U'], 2) if not pd.isna(last_row['BB_U']) else 0
    atr = round(last_row['ATR'], 2) if not pd.isna(last_row['ATR']) else 0
    
    durum = "BB Bandı İçinde"
    if close_price > bb_ust:
        durum = "BB Üst Bandını Kırdı (Yüksek oynaklık / Aşırı alım)"
    elif close_price < bb_alt:
        durum = "BB Alt Bandını Kırdı (Aşırı satım)"
        
    return {
        "BB_Ust": bb_ust,
        "BB_Orta": bb_orta,
        "BB_Alt": bb_alt,
        "Fiyat_BB_Konumu": durum,
        "ATR_14": atr
    }
