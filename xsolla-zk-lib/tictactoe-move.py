from web3 import Web3
import sys
import json
import os
from dotenv import load_dotenv

# 🌍 Load environment variables from .env
load_dotenv()
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
#print(PRIVATE_KEY)

if not PRIVATE_KEY:
    print("Error: PRIVATE_KEY not set in .env file.")
    sys.exit(1)

# ⚙️ Configuration
RPC_URL = "https://zkrpc.xsollazk.com"
CONTRACT_ADDRESS = "0xC43e8965367D53b83C97E65203EdaB272dFe98CE"

# 📡 Initialize Web3
w3 = Web3(Web3.HTTPProvider(RPC_URL))
acct = w3.eth.account.from_key(PRIVATE_KEY)
contract_address = Web3.to_checksum_address(CONTRACT_ADDRESS)

# ABI only for the move() function
abi = [
    {
        "inputs": [
            {"internalType": "uint8", "name": "row", "type": "uint8"},
            {"internalType": "uint8", "name": "col", "type": "uint8"}
        ],
        "name": "move",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# 📲 Connect to contract
contract = w3.eth.contract(address=contract_address, abi=abi)

# 🧾 Get parameters from CLI
if len(sys.argv) != 3:
    print("Usage: python send_move.py <row> <col>")
    sys.exit(1)

row = int(sys.argv[1])
col = int(sys.argv[2])

print("Sender:", acct.address)
print("Balance (ETH):", w3.from_wei(w3.eth.get_balance(acct.address), "ether"))

# 🧱 Build transaction
nonce = w3.eth.get_transaction_count(acct.address)
tx = contract.functions.move(row, col).build_transaction({
    "from": acct.address,
    "nonce": nonce,
    "gas": 500_000,
    "gasPrice": w3.to_wei("0.25", "gwei"),
})

# ✍️ Sign and send
signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

# ⏳ Output result
print(json.dumps({
    "tx_hash": tx_hash.hex(),
    "from": acct.address,
    "move": {"row": row, "col": col}
}))
