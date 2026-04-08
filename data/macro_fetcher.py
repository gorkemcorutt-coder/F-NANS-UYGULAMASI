import yfinance as yf

def fetch_macro_indicators() -> dict:
    """
    Fetches global macro indicators like VIX, DXY, US10Y.
    Using yahoo finance tickers: 
    ^VIX (Volatility S&P 500)
    DX-Y.NYB (US Dollar Index)
    ^TNX (Treasury Yield 10 Years)
    TRY=X (USD/TRY)
    """
    tickers = {
        "VIX": "^VIX",
        "DXY": "DX-Y.NYB",
        "US10Y": "^TNX",
        "USDTRY": "TRY=X"
    }
    
    results = {}
    
    for name, ticker_symbol in tickers.items():
        try:
            stock = yf.Ticker(ticker_symbol)
            hist = stock.history(period="1d")
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                results[name] = round(current_price, 3)
            else:
                results[name] = "Data Unavailable"
        except Exception as e:
            results[name] = f"Error: {str(e)}"
            
    return results
