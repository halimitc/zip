import os
import time
import requests
from web3 import Web3

# =========================
# CONFIG dari Environment Variables
# =========================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
RPC_URL = os.getenv("RPC_URL")
TOKEN_CONTRACT = os.getenv("TOKEN_CONTRACT")
FACTORY_ADDRESS = os.getenv("FACTORY_ADDRESS")

# =========================
# Telegram function
# =========================
def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML"}
    try:
        r = requests.post(url, data=data)
        print("Telegram Status:", r.status_code)
    except Exception as e:
        print("❌ Gagal kirim Telegram:", e)

# =========================
# Web3 setup
# =========================
w3 = Web3(Web3.HTTPProvider(RPC_URL))
if not w3.isConnected():
    raise Exception("❌ Gagal koneksi ke Somnia RPC")

# =========================
# Minimal ABI untuk Transfer event
# =========================
TOKEN_ABI = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "from", "type": "address"},
            {"indexed": True, "name": "to", "type": "address"},
            {"indexed": False, "name": "value", "type": "uint256"},
        ],
        "name": "Transfer",
        "type": "event",
    }
]

token_contract = w3.eth.contract(address=TOKEN_CONTRACT, abi=TOKEN_ABI)

# =========================
# Track latest block
# =========================
latest_block = w3.eth.block_number
send_telegram("✅ Bot JADU sudah online dan memantau transaksi!")

# =========================
# Main loop
# =========================
while True:
    try:
        current_block = w3.eth.block_number
        if current_block > latest_block:
            for block in range(latest_block + 1, current_block + 1):
                events = token_contract.events.Transfer.createFilter(
                    fromBlock=block, toBlock=block
                ).get_all_entries()
                
                for e in events:
                    from_addr = e['args']['from']
                    to_addr = e['args']['to']
                    value = e['args']['value'] / (10 ** 18)  # asumsi token 18 decimals

                    # Tentukan Buy/Sell berdasarkan Factory Address
                    if from_addr.lower() == FACTORY_ADDRESS.lower():
                        # Buy
                        msg = f"🟢 Buy Token JADU\nUser: {to_addr}\nAmount: {value} JADU"
                        send_telegram(msg)
                    elif to_addr.lower() == FACTORY_ADDRESS.lower():
                        # Sell
                        msg = f"🔴 Sell Token JADU\nUser: {from_addr}\nAmount: {value} JADU"
                        send_telegram(msg)
            
            latest_block = current_block
        time.sleep(5)  # cek setiap 5 detik

    except Exception as ex:
        print("Error:", ex)
        time.sleep(10)
