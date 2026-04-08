import pandas as pd

def detect_anomalies(df: pd.DataFrame, ticker: str) -> dict:
    """
    1-3 aylık geçmiş fiyat/hacim verisi üzerinden anomali skoru hesaplar.
    Bu skor 0-100 aralığındadır. Ortalama üzeri ise "Yüksek Manipülasyon Riski" üretilir.
    """
    if df is None or df.empty or len(df) < 20:
        return {"error": "Veri yetersiz", "skor": 0}
        
    skor = 0
    hedefler = []
    
    # 20 günlük hacim ortalaması
    df['Vol_SMA_20'] = df['Volume'].rolling(window=20).mean()
    son_gun = df.iloc[-1]
    
    # 1. Hacim Sıçraması (Hacim > 3x ortalama ise = +20 Puan)
    if son_gun.get('Volume') > son_gun.get('Vol_SMA_20', 0) * 3:
        skor += 20
        hedefler.append("Anormal Hacim Sıçraması (>3x)")
        
    # 2. Şüpheli Volatilite (Tek günde %10+ fiyat hareketi = +15 Puan)
    fiyat_degisimi = abs((son_gun.get('Close') - son_gun.get('Open')) / son_gun.get('Open')) * 100
    if fiyat_degisimi >= 10:
        skor += 15
        hedefler.append("Tek Günde >%10 Fiyat Dalgalanması")
        
    # 3. Yüksek Gölge (Wick) Tespiti (Sahte kırılım vs. = +10 Puan)
    yüksek_gölge = son_gun.get('High') - max(son_gun.get('Close'), son_gun.get('Open'))
    govde_uzunlugu = abs(son_gun.get('Close') - son_gun.get('Open'))
    if govde_uzunlugu > 0 and (yüksek_gölge / govde_uzunlugu) > 2:
        skor += 10
        hedefler.append("Anormal Mum İğnesi (Wick) - Likidite Avı Şüphesi")

    # Risk Seviyesi Belirleme
    durum = "Normal"
    if skor > 30: durum = "Dikkat ⚠️"
    if skor > 50: durum = "Şüpheli 🔴"
    if skor > 70: durum = "Yüksek Manipülasyon Riski ⛔"
    
    return {
        "hisse": ticker,
        "anomali_skoru": skor,
        "risk_durumu": durum,
        "tespitler": hedefler if hedefler else ["Şüpheli bir aktivite bulunamadı."]
    }
