import json
from tictactoe import w3, get_account, get_contract, sign_and_send

acct = get_account()

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
contract = get_contract(abi)

# 🧾 Build transaction
nonce = w3.eth.get_transaction_count(acct.address)
tx = contract.functions.startGame().build_transaction({
    "from": acct.address,
    "nonce": nonce,
    "gas": 300_000,
    "gasPrice": w3.to_wei("0.25", "gwei"),
})

# ✍️ Sign and send
tx_hash = sign_and_send(tx)

# ⏳ Output result
print(json.dumps({
    "tx_hash": tx_hash.hex(),
    "from": acct.address,
    "action": "startGame"
}, indent=2))
