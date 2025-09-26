# stock_monitor.py
import yfinance as yf
from newsapi import NewsApiClient
import openai
import datetime

portfolio = ['AAPL', 'MSFT', 'NVDA', 'TSLA', 'GOOGL']
newsapi = NewsApiClient(api_key='YOUR_NEWSAPI_KEY')
openai.api_key = 'YOUR_OPENAI_KEY'

def get_price_change(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="2d")
    if len(hist) < 2:
        return None
    prev_close = hist['Close'].iloc[0]
    latest_close = hist['Close'].iloc[1]
    change_pct = ((latest_close - prev_close) / prev_close) * 100
    return round(change_pct, 2), latest_close

def get_news(ticker):
    company_name = yf.Ticker(ticker).info['shortName']
    articles = newsapi.get_everything(q=company_name, language='en', sort_by='relevancy', page_size=3)
    return [article['title'] for article in articles['articles']]

def summarize_news(headlines):
    prompt = "Summarize the following news headlines:\n" + "\n".join(headlines)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

def generate_report():
    print(f"\n📈 Stock Report for {datetime.date.today()}")
    flagged = []
    for ticker in portfolio:
        result = get_price_change(ticker)
        if result:
            change, price = result
            if abs(change) >= 5:
                print(f"\n{ticker} moved {change}% to ${price}")
                headlines = get_news(ticker)
                summary = summarize_news(headlines)
                print("📰 Commentary:", summary)

generate_report()
