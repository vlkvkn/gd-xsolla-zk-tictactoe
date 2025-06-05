from web3 import Web3
import os
import json
from dotenv import load_dotenv

# 🌍 Load environment variables
load_dotenv()
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
if not PRIVATE_KEY:
    print("Error: PRIVATE_KEY not set in .env")
    exit(1)

# 🛠 Config
RPC_URL = "https://zkrpc.xsollazk.com"
CONTRACT_ADDRESS = "0xC43e8965367D53b83C97E65203EdaB272dFe98CE"

# 📡 Initialize Web3
w3 = Web3(Web3.HTTPProvider(RPC_URL))
acct = w3.eth.account.from_key(PRIVATE_KEY)
contract_address = Web3.to_checksum_address(CONTRACT_ADDRESS)

# 🔗 ABI for startGame()
abi = [
    {
        "inputs": [],
        "name": "startGame",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# 📲 Contract
contract = w3.eth.contract(address=contract_address, abi=abi)

# 🧾 Build transaction
nonce = w3.eth.get_transaction_count(acct.address)
tx = contract.functions.startGame().build_transaction({
    "from": acct.address,
    "nonce": nonce,
    "gas": 300_000,
    "gasPrice": w3.to_wei("0.25", "gwei"),
})

# ✍️ Sign and send
signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

# ⏳ Output result
print(json.dumps({
    "tx_hash": tx_hash.hex(),
    "from": acct.address,
    "action": "startGame"
}, indent=2))
