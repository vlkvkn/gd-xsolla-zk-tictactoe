import sys
import json
from tictactoe import w3, get_account, get_contract, sign_and_send

acct = get_account()

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
contract = get_contract(abi)

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
tx_hash = sign_and_send(tx)

# ⏳ Output result
print(json.dumps({
    "tx_hash": tx_hash.hex(),
    "from": acct.address,
    "move": {"row": row, "col": col}
}))
