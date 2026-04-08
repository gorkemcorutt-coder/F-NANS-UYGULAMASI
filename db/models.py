from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON
from db.database import Base
from datetime import datetime

class TradeRecommendation(Base):
    __tablename__ = "trade_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    öneri_id = Column(String, unique=True, index=True) # UUID
    
    tarih = Column(DateTime, default=datetime.utcnow)
    hisse = Column(String, index=True)
    giriş_fiyatı = Column(Float)
    hedef = Column(Float)
    stop = Column(Float)
    rr_oranı = Column(Float)
    beklenen_süre = Column(String)
    
    piyasa_rejimi = Column(String)
    kullanılan_sinyal = Column(JSON) # Liste olarak sinyaller
    makro_ortam = Column(String)
    
    # Sonuç Alanları (İşlem kapandığında doldurulacak)
    is_closed = Column(Boolean, default=False)
    sonuç_fiyatı = Column(Float, nullable=True)
    başarı = Column(Boolean, nullable=True) # True = Hedef, False = Stop/Başarısız
    kazanç_yüzdesi = Column(Float, nullable=True)
    süre_gün = Column(Integer, nullable=True)
    hata_analizi = Column(String, nullable=True)
    öğrenilen = Column(String, nullable=True)
