import os
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML"}
    r = requests.post(url, data=data)
    print("Status Code:", r.status_code)
    print("Response:", r.text)

if __name__ == "__main__":
    send_telegram("✅ Bot JADU sudah online dan terhubung ke Telegram!")
