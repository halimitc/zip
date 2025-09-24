import os
import time
import requests
from web3 import Web3

# ===== CONFIG =====
RPC_WS = os.getenv("RPC_WS")  # WebSocket RPC Somnia, contoh: wss://ws.infra.mainnet.somnia.network
JADU_ADDRESS = Web3.to_checksum_address(os.getenv("JADU_ADDRESS"))  # alamat token JADU
FACTORY_ADDRESS = Web3.to_checksum_address(os.getenv("FACTORY_ADDRESS"))  # alamat factory

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

DELAY = 10  # Delay notif average buy

# ===== SETUP WEB3 =====
w3 = Web3(Web3.WebsocketProvider(RPC_WS))
if not w3.is_connected():
    print("❌ Gagal connect ke WebSocket RPC")
    exit()

# ===== ERC20 Transfer ABI =====
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
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML"}
    try:
        requests.post(url, data=data, timeout=5)
    except Exception as e:
        print("Telegram Error:", e)

# ===== HANDLE BUY/SELL =====
def handle_event(event):
    try:
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
    except Exception as e:
        print("Handle Event Error:", e)

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
