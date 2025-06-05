import json
from tictactoe import get_contract

# ABI only for the getBoard() method and the Cell enum
abi = [
    {
        "inputs": [],
        "name": "getBoard",
        "outputs": [
            {
                "internalType": "enum TicTacToeVsAI.Cell[3][3]",
                "name": "",
                "type": "uint8[3][3]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# Connect to the contract
contract = get_contract(abi)

# Retrieve the board
board_raw = contract.functions.getBoard().call()

# Convert numbers to symbols for convenience
cell_map = {0: "", 1: "X", 2: "O"}
board = [[cell_map.get(cell, "?") for cell in row] for row in board_raw]

# Output JSON
print(json.dumps({"board": board}))
