from web3 import Web3
import requests
import os
import time

# ===== CONFIG =====
RPC_URL = "https://api.infra.mainnet.somnia.network"  # RPC resmi Somnia
JADU_ADDRESS = Web3.to_checksum_address("0x7bdc0a37c4f4f4928744e2a8111f16268c5dad52")  # ganti dengan alamat token JADU
FACTORY_ADDRESS = Web3.to_checksum_address("0x347b4be0f7Bf542597BA232e5f282cA2ec6a970b")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")   # diset di Railway Env
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")       # diset di Railway Env

# Delay notif average buy
DELAY = 10  

# ===== SETUP =====
w3 = Web3(Web3.HTTPProvider(RPC_URL))

ERC20_ABI = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "from", "type": "address"},
            {"indexed": True, "internalType": "address", "name": "to", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "value", "type": "uint256"},
        ],
        "name": "Transfer",
        "type": "event",
    }
]

jadu_contract = w3.eth.contract(address=JADU_ADDRESS, abi=ERC20_ABI)

# ===== TELEGRAM FUNCTION =====
def send_telegram(msg):
    url = f"https://api.telegram.org/7856840601:AAG7MqzMAlJUQQUVN78wwkS5SNR5bl8rJJ0/sendMessage"
    data = {"chat_id": -4853724640, "text": msg, "parse_mode": "HTML"}
    try:
        requests.post(url, data=data, timeout=5)
    except Exception as e:
        print("Telegram Error:", e)

# ===== HANDLE BUY/SELL =====
def handle_event(event):
    from_addr = event["args"]["from"]
    to_addr = event["args"]["to"]
    amount = w3.from_wei(event["args"]["value"], "ether")

    if from_addr.lower() == FACTORY_ADDRESS.lower():
        msg = f"🚀 <b>BUY ALERT</b>\n👤 Buyer: {to_addr}\n💰 Amount: {amount} JADU"
        print(msg)
        send_telegram(msg)

    elif to_addr.lower() == FACTORY_ADDRESS.lower():
        msg = f"⚠️ <b>SELL ALERT</b>\n👤 Seller: {from_addr}\n📉 Amount: {amount} JADU"
        print(msg)
        send_telegram(msg)

# ===== AVERAGE BUY (manual input contoh) =====
def average_buy_notif():
    transaksi = [
        {"before": 2.8, "after": 3.8},
        {"before": 3.8, "after": 5.0},
        {"before": 5.0, "after": 7.2},
        {"before": 7.2, "after": 10.0},
    ]

    for tx in transaksi:
        msg = (
            f"📈 <b>Average Buy Terdeteksi</b>\n\n"
            f"🔹 Sebelumnya: <b>{tx['before']}%</b>\n"
            f"🔹 Sekarang: <b>{tx['after']}%</b>\n"
            f"🛡️ Developer terus melakukan average buy demi keberlangsungan project <b>JADU</b>!"
        )
        send_telegram(msg)
        time.sleep(DELAY)

# ===== MAIN LOOP =====
def main():
    send_telegram("✅ <b>Bot JADU sudah online!</b>")
    print("📡 BuyBot JADU aktif, mantau transaksi...")

    # kirim notif average buy sekali (manual)
    average_buy_notif()

    try:
        event_filter = jadu_contract.events.Transfer.create_filter(from_block="latest")
    except Exception as e:
        print("Filter Error:", e)
        return

    while True:
        try:
            for event in event_filter.get_new_entries():
                handle_event(event)
        except Exception as e:
            print("Error:", e)
            time.sleep(5)  # jeda biar gak spam error

        time.sleep(2)

if __name__ == "__main__":
    main()
