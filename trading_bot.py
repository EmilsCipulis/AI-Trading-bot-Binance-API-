import ccxt
import time

# Binance API keys
api_key = "YOUR_API_KEY"
api_secret = "YOUR_API_SECRET"

exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
    'options': {'adjustForTimeDifference': True}
})

# Trading settings
symbol = "BTC/USDT"
lot_size = 0.001  # Adjust according to your balance
POLL_INTERVAL_SECONDS = 5

def get_price():
    ticker = exchange.fetch_ticker(symbol)
    return ticker['last']

while True:
    try:
        price = get_price()
    except ccxt.RequestTimeout:
        print(f"Timed out fetching {symbol} price. Retrying in {POLL_INTERVAL_SECONDS} seconds.")
    else:
        print(f"Current {symbol} Price: {price}")
    time.sleep(POLL_INTERVAL_SECONDS)
