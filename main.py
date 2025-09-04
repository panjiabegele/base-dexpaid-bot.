import requests
import time
import telebot

# Token & Chat ID langsung dari kamu
TOKEN = "7603272223:AAFHin7cU3QmfhHj6AoYRiuB5Sr3X1T97nk"
CHAT_ID = "6739323643"

bot = telebot.TeleBot(TOKEN)

# Simpan token yang sudah dikirim agar tidak dobel alert
sudah_kirim = set()

def cek_token_base():
    url = "https://api.dexscreener.com/latest/dex/search?q=base"
    data = requests.get(url).json()

    for pair in data.get("pairs", []):
        name = pair["baseToken"]["name"]
        symbol = pair["baseToken"]["symbol"]
        price = pair.get("priceUsd", "N/A")
        liquidity = pair.get("liquidity", {}).get("usd", 0)
        url_pair = pair["url"]

        # ID unik tiap token
        token_id = pair["pairAddress"]

        # Filter sederhana: hanya token baru dengan liquidity > 20k
        if token_id not in sudah_kirim and liquidity > 20000:
            alert = f"""
🚨 Token Baru di Base 🚨
Nama: {name} ({symbol})
Harga: ${price}
Liquidity: ${liquidity}
Link: {url_pair}
"""
            bot.send_message(CHAT_ID, alert)
            sudah_kirim.add(token_id)

def run_bot():
    while True:
        try:
            cek_token_base()
        except Exception as e:
            print("Error:", e)
        time.sleep(60)  # cek tiap 1 menit

if __name__ == "__main__":
    run_bot()
