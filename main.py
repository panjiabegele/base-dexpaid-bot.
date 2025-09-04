import requests
import time

# === TOKEN BOT TELEGRAM KAMU ===
BOT_TOKEN = "7603272223:AAFHin7cU3QmfhHj6AoYRiuB5Sr3X1T97nk"
CHAT_ID = "6739323643"

DEX_API = "https://api.dexscreener.com/latest/dex/pairs/base"
sudah_dikirim = set()

def kirim_tele(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Gagal kirim ke Telegram:", e)

def cek_token_base():
    try:
        r = requests.get(DEX_API).json()
        if "pairs" not in r:
            return []
        
        hasil = []
        for pair in r["pairs"]:
            token_info = pair.get("info", {})
            socials = token_info.get("socials", [])
            logo = token_info.get("imageUrl", "")
            ca = pair.get("baseToken", {}).get("address")

            # Filter: Paid (punya logo atau social)
            if logo or socials:
                if ca not in sudah_dikirim:
                    hasil.append({
                        "name": pair.get("baseToken", {}).get("name"),
                        "symbol": pair.get("baseToken", {}).get("symbol"),
                        "ca": ca,
                        "dex": pair.get("dexId"),
                        "url": pair.get("url"),
                    })
                    sudah_dikirim.add(ca)
        return hasil
    except Exception as e:
        print("Error API:", e)
        return []

def main():
    while True:
        tokens = cek_token_base()
        for token in tokens:
            msg = (
                f"🚨 <b>Token Baru Paid</b> 🚨\n\n"
                f"Nama: {token['name']} ({token['symbol']})\n"
                f"CA: <code>{token['ca']}</code>\n"
                f"DEX: {token['dex']}\n"
                f"🔗 <a href='{token['url']}'>Link Dexscreener</a>\n"
            )
            kirim_tele(msg)
            print("Kirim alert untuk:", token['ca'])
        
        time.sleep(60)  # cek tiap 1 menit

if __name__ == "__main__":
    main()
