import requests

API_URL = "https://api.binance.com/api/v3/ticker/price"
symbol = "BTCUSDT"
threshold = 45000  # Set your alert price

def get_price():
    response = requests.get(API_URL, params={"symbol": symbol})
    price = float(response.json()["price"])
    return price

while True:
    price = get_price()
    if price > threshold:
        print(f"🚨 ALERT! {symbol} is now {price} USD 🚨")
    else:
        print(f"{symbol}: {price} USD")
