import pandas as pd

def get_momentum_indicators(df: pd.DataFrame) -> dict:
    """
    RSI ve MACD'yi ek kütüphane olmadan pandas ile hesaplar.
    """
    if df is None or df.empty or len(df) < 30:
        return {"error": "Yeterli momentum verisi yok"}
        
    # RSI Hesaplama
    period = 14
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = (-delta).where(delta < 0, 0)
    
    avg_gain = gain.ewm(com=(period - 1), min_periods=period).mean()
    avg_loss = loss.ewm(com=(period - 1), min_periods=period).mean()
    
    rs = avg_gain / avg_loss
    df['RSI_14'] = 100 - (100 / (1 + rs))
    
    # MACD Hesaplama
    fast = 12
    slow = 26
    signal = 9
    
    fast_ema = df['Close'].ewm(span=fast, adjust=False).mean()
    slow_ema = df['Close'].ewm(span=slow, adjust=False).mean()
    df['MACD'] = fast_ema - slow_ema
    df['MACD_Signal'] = df['MACD'].ewm(span=signal, adjust=False).mean()
    df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']
    
    last_row = df.iloc[-1]
    
    rsi = round(last_row['RSI_14'], 2) if not pd.isna(last_row['RSI_14']) else 0
    macd = round(last_row['MACD'], 2) if not pd.isna(last_row['MACD']) else 0
    macd_signal = round(last_row['MACD_Signal'], 2) if not pd.isna(last_row['MACD_Signal']) else 0
    macd_hist = round(last_row['MACD_Hist'], 2) if not pd.isna(last_row['MACD_Hist']) else 0
    
    rsi_durum = "Normal"
    if rsi > 70:
        rsi_durum = "Aşırı Alım"
    elif rsi < 30:
        rsi_durum = "Aşırı Satım"
        
    macd_durum = "Al (MACD > Sinyal)" if macd > macd_signal else "Sat (MACD < Sinyal)"
    
    return {
        "RSI_14": rsi,
        "RSI_Durum": rsi_durum,
        "MACD": macd,
        "MACD_Sinyal": macd_signal,
        "MACD_Histogram": macd_hist,
        "MACD_Durum": macd_durum
    }
