# -*- coding: utf-8 -*-
import time
import pandas as pd
from binance.client import Client

# --- Binance Settings ---
API_KEY = "ТВОЙ_API_KEY"
API_SECRET = "ТВОЙ_API_SECRET"
SYMBOL = "BTCUSDT"
INTERVAL = "5m"
LIMIT = 500

client = Client(API_KEY, API_SECRET)

def get_klines():
    """Получаем данные с Binance"""
    candles = client.get_klines(symbol=SYMBOL, interval=INTERVAL, limit=LIMIT)
    df = pd.DataFrame(candles, columns=[
        'Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
        'Close time', 'Quote asset volume', 'Number of trades',
        'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'
    ])
    df['Close'] = df['Close'].astype(float)
    return df

"""RSI calculation"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def analyze_momentum():
    df = get_klines()
    df['RSI'] = calculate_rsi(df['Close'])
    last_rsi = df['RSI'].iloc[-1]
    print(f"Последний RSI: {last_rsi:.2f}")

    if last_rsi > 70:
        print("⚠️ Перекупленность — возможен откат вниз.")
    elif last_rsi < 30:
        print("💡 Перепроданность — возможен импульс вверх.")
    else:
        print("📊 Нейтральная зона — рынок без чёткой фазы.")

if __name__ == "__main__":
    while True:
        analyze_momentum()
        time.sleep(300)  # обновление каждые 5 минут
