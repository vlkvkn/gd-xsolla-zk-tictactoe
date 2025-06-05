from web3 import Web3
import sys
import json

# URL RPC Xsolla zk testnet
w3 = Web3(Web3.HTTPProvider("https://zkrpc.xsollazk.com"))

# Вводим аргументами: адрес контракта и адрес пользователя (необязательно)
contract_address = Web3.to_checksum_address("0xC43e8965367D53b83C97E65203EdaB272dFe98CE")

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
contract = w3.eth.contract(address=contract_address, abi=abi)

# Получаем доску
board_raw = contract.functions.getBoard().call()

# Преобразуем числа в символы для удобства
cell_map = {0: "", 1: "X", 2: "O"}
board = [[cell_map.get(cell, "?") for cell in row] for row in board_raw]

# Вывод JSON
print(json.dumps({"board": board}))
