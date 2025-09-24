from web3 import Web3
import requests
import os
import time

# ===== CONFIG =====
RPC_URL = "https://api.infra.mainnet.somnia.network"  # RPC resmi Somnia
JADU_ADDRESS = Web3.to_checksum_address("0xYOUR_JADU_TOKEN_ADDRESS")  # ganti dengan alamat token JADU
FACTORY_ADDRESS = Web3.to_checksum_address("0x347b4be0f7Bf542597BA232e5f282cA2ec6a970b")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")   # diset di Railway Env
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")       # diset di Railway Env

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


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    try:
        requests.post(url, data=data, timeout=5)
    except Exception as e:
        print("Telegram Error:", e)


def handle_event(event):
    from_addr = event["args"]["from"]
    to_addr = event["args"]["to"]
    amount = w3.from_wei(event["args"]["value"], "ether")

    if from_addr.lower() == FACTORY_ADDRESS.lower():
        msg = f"🚀 BUY ALERT\n👤 Buyer: {to_addr}\n💰 Amount: {amount} JADU"
        print(msg)
        send_telegram(msg)

    elif to_addr.lower() == FACTORY_ADDRESS.lower():
        msg = f"⚠️ SELL ALERT\n👤 Seller: {from_addr}\n📉 Amount: {amount} JADU"
        print(msg)
        send_telegram(msg)


def main():
    print("📡 BuyBot JADU aktif, mantau transaksi...")
    event_filter = jadu_contract.events.Transfer.create_filter(fromBlock="latest")

    while True:
        try:
            for event in event_filter.get_new_entries():
                handle_event(event)
        except Exception as e:
            print("Error:", e)

        time.sleep(2)  # jeda biar tidak overload RPC


if __name__ == "__main__":
    main()
