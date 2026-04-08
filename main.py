from fastapi import FastAPI, HTTPException
from core.oracle_brain import brain
from data.price_fetcher import fetch_bist100_summary, fetch_stock_basic_data
from data.macro_fetcher import fetch_macro_indicators
from analysis.technical_analyzer import analyze_stock_technicals
from db.database import engine, Base, get_db
from db.models import TradeRecommendation
from learning.performance_tracker import record_recommendation, close_recommendation
from sqlalchemy.orm import Session
from fastapi import Depends
import uvicorn
import os

# Veritabanı tablolarını oluştur
Base.metadata.create_all(bind=engine)


app = FastAPI(title="BIST ORACLE AI", version="1.0.0")

@app.get("/health")
def read_health():
    return {"status": "Sistem aktif, zihin devrede."}

@app.get("/gunluk")
def get_daily_report():
    """
    Sistemin ana `/gunluk` endpointi.
    1. Makro verileri okur
    2. BIST100 genel durumunu okur
    3. Örnek bir hisse (THYAO) için verileri okur
    4. Tüm veriyi OracleBrain'e iletir ve analiz ister
    """
    macro_data = fetch_macro_indicators()
    bist100_data = fetch_bist100_summary()
    thyao_data = fetch_stock_basic_data("THYAO")
    
    market_data_summary = {
        "macro": macro_data,
        "bist100": bist100_data,
        "sample_stock_thyao": thyao_data
    }
    
    # Gemini AI'a istek at
    report = brain.generate_daily_report(market_data_summary)
    
    return {"rapor": report}

@app.post("/oneri")
def create_recommendation(rec_data: dict, db: Session = Depends(get_db)):
    """
    AI tarafından üretilen hisse önerisini veritabanına kaydeder.
    JSON Örneği: 
    {
      "hisse": "THYAO", "giriş_fiyatı": 245.5, "hedef": 270.0, "stop": 225.0, 
      "rr_oranı": 2.8, "beklenen_süre": "2 hafta", "piyasa_rejimi": "Trend",
      "kullanılan_sinyal": ["Ichimoku"], "makro_ortam": "Normal"
    }
    """
    new_rec = record_recommendation(db, rec_data)
    return {"mesaj": "Öneri başarıyla sisteme kaydedildi.", "öneri_id": new_rec.öneri_id}

@app.put("/oneri/{oneri_id}/kapat")
def finalize_recommendation(oneri_id: str, sonuc_fiyati: float, ogrenilen: str = None, db: Session = Depends(get_db)):
    """
    Kapanan bir işlemin sonucunu ve öğrenilenleri veritabanına yazar.
    """
    closed_rec = close_recommendation(db, oneri_id, sonuc_fiyati, ogrenilen)
    if not closed_rec:
        raise HTTPException(status_code=404, detail="Öneri bulunamadı.")
        
    return {
        "mesaj": "Öneri kapatıldı ve hafızaya işlendi.",
        "başarı": closed_rec.başarı,
        "kazanç_yüzdesi": f"%{closed_rec.kazanç_yüzdesi:.2f}",
        "hisse": closed_rec.hisse
    }

@app.get("/analiz/{hisse_kodu}")
def get_technical_analysis(hisse_kodu: str):
    """
    Belirtilen hisse senedi için teknik analiz indikatör röntgeni çeker.
    """
    analysis_result = analyze_stock_technicals(hisse_kodu)
    
    if "error" in analysis_result:
        raise HTTPException(status_code=400, detail=analysis_result["error"])
        
    return analysis_result

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
