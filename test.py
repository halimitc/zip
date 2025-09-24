import os
import requests

# Ambil env dari Railway
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

print("DEBUG TOKEN:", TELEGRAM_BOT_TOKEN)
print("DEBUG CHAT ID:", TELEGRAM_CHAT_ID)

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    try:
        r = requests.post(url, data=data, timeout=5)
        print("Response:", r.text)
    except Exception as e:
        print("Telegram Error:", e)

if __name__ == "__main__":
    send_telegram("✅ Hello from Railway! Test bot berhasil kirim pesan.")
