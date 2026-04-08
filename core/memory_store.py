import json
from sqlalchemy.orm import Session
from sqlalchemy import func
from db.models import TradeRecommendation

def get_learning_summary(db: Session) -> str:
    """
    Geçmiş kapalı işlemlerin başarı istatistiklerini hesaplar.
    AI motoruna "Öz-Değerlendirme" ve "Rejim Hafızası" katar.
    """
    closed_trades = db.query(TradeRecommendation).filter(TradeRecommendation.is_closed == True).all()
    
    if not closed_trades:
        return "Henüz kapanmış işlem veya geçmiş hafıza kaydı bulunmuyor."
        
    total_trades = len(closed_trades)
    successful_trades = sum(1 for t in closed_trades if t.başarı)
    failed_trades = total_trades - successful_trades
    
    win_rate = (successful_trades / total_trades) * 100 if total_trades > 0 else 0
    
    # En başarılı sinyaller analizi
    # Gerçek uygulamada JSON objesi expand edilerek daha karmaşık sayım yapılır
    # Burada basit tutuyoruz
    
    summary = f"Geçmiş İşlem Hafızası: Toplam İşlem: {total_trades}, Başarılı: {successful_trades}, Başarısız: {failed_trades}. Kazanma Oranı: %{win_rate:.1f}. \n"
    summary += "Kapanan İşlemlerden Öğrenilenler:\n"
    
    for trade in closed_trades[-5:]: # Son 5 işlemi ekle
        summary += f"- {trade.hisse} (B: {trade.başarı}, %{trade.kazanç_yüzdesi}): {trade.öğrenilen or 'Öğrenilen not girilmemiş.'}\n"
        
    return summary
