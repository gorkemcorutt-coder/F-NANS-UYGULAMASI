import yfinance as yf

def fetch_latest_news(ticker: str) -> list:
    """
    Yahoo Finance üzerinden ilgili BIST hissesi hakkında en son haber başlıklarını çeker.
    (API Key gerektirmez, public veridir. Daha gelişmişi için Haber API'leri eklenebilir)
    """
    try:
        if not ticker.endswith(".IS"):
            ticker = f"{ticker}.IS"
            
        stock = yf.Ticker(ticker)
        news = stock.news
        
        if not news:
            return [{"title": "Hisse ile ilgili uluslararası yakında bir haber bulunamadı.", "link": "#"}]
            
        # Son 5 haberi al
        formatted_news = []
        for n in news[:5]:
            formatted_news.append({
                "title": n.get("title", ""),
                "publisher": n.get("publisher", "Bilinmiyor"),
                "link": n.get("link", "#")
            })
            
        return formatted_news
    except Exception as e:
        return [{"title": f"Haberler çekilirken hata oluştu: {str(e)}", "link": "#"}]
