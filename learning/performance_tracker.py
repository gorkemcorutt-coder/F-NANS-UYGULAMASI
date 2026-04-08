from sqlalchemy.orm import Session
from db.models import TradeRecommendation
import uuid
import json

def record_recommendation(db: Session, rec_data: dict) -> TradeRecommendation:
    """Yapay Zeka'nın ürettiği yeni tavsiyeyi DB'ye yazar"""
    new_rec = TradeRecommendation(
        öneri_id=str(uuid.uuid4()),
        hisse=rec_data.get("hisse"),
        giriş_fiyatı=rec_data.get("giriş_fiyatı"),
        hedef=rec_data.get("hedef"),
        stop=rec_data.get("stop"),
        rr_oranı=rec_data.get("rr_oranı"),
        beklenen_süre=rec_data.get("beklenen_süre"),
        piyasa_rejimi=rec_data.get("piyasa_rejimi"),
        kullanılan_sinyal=rec_data.get("kullanılan_sinyal", []),
        makro_ortam=rec_data.get("makro_ortam")
    )
    db.add(new_rec)
    db.commit()
    db.refresh(new_rec)
    return new_rec

def close_recommendation(db: Session, oneri_id: str, sonuc_fiyati: float, ogrenilen: str = None) -> TradeRecommendation:
    """Tavsiye edilen işlemin sonucunu kapatır ve karlılığı hesaplar"""
    rec = db.query(TradeRecommendation).filter(TradeRecommendation.öneri_id == oneri_id).first()
    
    if not rec:
        return None
    
    if rec.is_closed:
        return rec
        
    rec.is_closed = True
    rec.sonuç_fiyatı = sonuc_fiyati
    
    # Başarı Hesabı
    kar_zarar_farki = sonuc_fiyati - rec.giriş_fiyatı
    
    if rec.hedef > rec.giriş_fiyatı: # Long pozisyon
        rec.kazanç_yüzdesi = (kar_zarar_farki / rec.giriş_fiyatı) * 100
    else: # Short pozisyon (Opsiyonel)
        rec.kazanç_yüzdesi = (-kar_zarar_farki / rec.giriş_fiyatı) * 100
        
    rec.başarı = True if rec.kazanç_yüzdesi > 0 else False
    
    # Süre
    rec.süre_gün = (rec.tarih.now() - rec.tarih).days
    
    rec.öğrenilen = ogrenilen
    
    db.commit()
    db.refresh(rec)
    return rec
