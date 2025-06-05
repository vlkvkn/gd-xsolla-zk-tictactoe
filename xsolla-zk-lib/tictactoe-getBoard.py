import json
from tictactoe import get_contract

# ABI только для метода getBoard() и enum Cell
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

# Подключение к контракту
contract = get_contract(abi)

# Получаем доску
board_raw = contract.functions.getBoard().call()

# Преобразуем числа в символы для удобства
cell_map = {0: "", 1: "X", 2: "O"}
board = [[cell_map.get(cell, "?") for cell in row] for row in board_raw]

# Вывод JSON
print(json.dumps({"board": board}))
