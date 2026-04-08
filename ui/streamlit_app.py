import streamlit as st
import os
import sys

# Proje ana dizinini sistem yoluna ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.oracle_brain import brain
from data.price_fetcher import fetch_stock_basic_data, fetch_historical_data
from data.macro_fetcher import fetch_macro_indicators
from data.news_aggregator import fetch_latest_news
from anomaly.anomaly_scorer import detect_anomalies
from analysis.technical_analyzer import analyze_stock_technicals
from db.database import SessionLocal, engine, Base
from learning.performance_tracker import record_recommendation
from config import settings

# Veritabanını hazırla
Base.metadata.create_all(bind=engine)

st.set_page_config(page_title="BIST ORACLE AI", page_icon="🔮", layout="wide")

st.title("🔮 BIST ORACLE — Ultimate Trading Intelligence")
st.markdown("Borsa İstanbul yatırımcıları için *kurumsal seviyede* analiz ve yapay zeka asistanı.")

# API Key Uyarısı
if not settings.gemini_api_key or settings.gemini_api_key == "buraya_google_gemini_api_key_giriniz":
    st.error("⚠️ GEMINI_API_KEY .env dosyasında yapılandırılmamış. Lütfen 'bist-oracle/.env' dosyasını düzenleyin ve sunucuyu yeniden başlatın.")
    st.stop()

# Sekmeler
tab1, tab2, tab3 = st.tabs(["📊 Günlük Piyasa Raporu", "🔬 Derin Hisse Analizi", "💬 Oracle ile Konuş"])

with tab1:
    st.header("Günlük İstihbarat Raporu")
    if st.button("🚀 Raporu Üret (AI Piyasayı Analiz Etsin)"):
        with st.spinner("Makro Veriler ve BIST Verileri Çekiliyor..."):
            macro = fetch_macro_indicators()
            bist = fetch_stock_basic_data("XU100")
            
            st.write("Veriler toplandı! Gemini AI Raporu yazıyor...")
            
            market_data = {"macro": macro, "bist100": bist}
            
            # AI Yanıtı
            rapor = brain.generate_daily_report(market_data)
            st.success("Analiz Tamamlandı!")
            st.markdown(rapor)

with tab2:
    st.header("Hisse Röntgeni & Anomali Tespiti")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        hisse = st.text_input("Hisse Sembolü (Örn: THYAO, ASELS)", value="THYAO")
        analiz_btn = st.button("Röntgen Çek")
        
    if analiz_btn:
        with st.spinner(f"{hisse} için Derin Analiz Yapılıyor..."):
            hisse = hisse.upper()
            
            # 1. Teknik Analiz
            st.subheader("1. Teknik Göstergeler")
            tech_data = analyze_stock_technicals(hisse)
            st.json(tech_data)
            
            # 2. Anomali Tespiti
            st.subheader("2. Anomali & Manipülasyon Skoru")
            df = fetch_historical_data(hisse, period="3mo")
            anomaly_data = detect_anomalies(df, hisse)
            
            if anomaly_data.get('anomali_skoru', 0) > 50:
                st.error(f"Risk: {anomaly_data['risk_durumu']} (Skor: {anomaly_data['anomali_skoru']})")
            elif anomaly_data.get('anomali_skoru', 0) > 30:
                st.warning(f"Risk: {anomaly_data['risk_durumu']} (Skor: {anomaly_data['anomali_skoru']})")
            else:
                st.success(f"Risk: {anomaly_data['risk_durumu']} (Skor: {anomaly_data['anomali_skoru']})")
                
            st.write("**Bulgular:**", anomaly_data.get('tespitler', []))
            
            # 3. Haber Akışı
            st.subheader("3. Son Uluslararası / Yerel Haberler")
            haberler = fetch_latest_news(hisse)
            for h in haberler:
                st.markdown(f"- [{h['title']}]({h['link']}) *(Kaynak: {h.get('publisher', '')})*")

with tab3:
    st.header("BIST ORACLE'a Danış")
    soru = st.text_area("Hisse stratejisi, piyasa yönü veya teknik analiz hakkında ne sormak istersin?", value="THYAO'nun son takas durumunu ve makro etkilerini değerlendirir misin?")
    
    if st.button("Sor"):
        with st.spinner("Zihin Düşünüyor..."):
            cevap = brain.model.generate_content(soru).text
            st.markdown(cevap)
