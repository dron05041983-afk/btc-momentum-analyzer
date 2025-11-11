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

def calculate_rsi(prices, period=14):
    """Расчёт RSI"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def analyze_momentum():
    """Основная логика анализа"""
    df = get_klines()
    df['RSI'] = calculate_rsi(df['Close'])
    last_rsi = df['RSI'].iloc[-1]
    last_close = df['Close'].iloc[-1]

    if last_rsi > 70:
        signal = "⚠️ RSI перегрет — возможен откат вниз"
    elif last_rsi < 30:
        signal = "✅ RSI перепродан — возможен импульс вверх"
    else:
        signal = "ℹ️ Нейтральная зона"

    print(f"\n=== BTC Momentum Analyzer ===")
    print(f"Цена: {last_close:.2f} USDT")
    print(f"RSI: {last_rsi:.2f}")
    print(f"Сигнал: {signal}\n")

if __name__ == "__main__":
    while True:
        analyze_momentum()
        time.sleep(300)
