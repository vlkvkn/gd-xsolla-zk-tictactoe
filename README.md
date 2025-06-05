# TicTacToe zk Blockchain Demo

This repository contains a small Godot project that connects to a TicTacToe smart contract on Xsolla's zkEVM network. Moves are sent through Python scripts and recorded on chain.

## Problem Statement

Traditional games rely on local logic and are hard to verify. By moving the game logic to a smart contract, every move is transparent and tamper proof. This project demonstrates how a Godot front end can interact with such a contract, letting players see a decentralised game in action.

## Installation

1. Install **Python 3** and **pip**.
2. Install required packages:

   ```bash
   pip install web3 python-dotenv
   ```
3. Install **Godot 4** to run the project.
4. Clone this repository and create a `.env` file in the root. It must contain your private key:

   ```
   PRIVATE_KEY=<your_private_key>
   ```

   The key is used to sign transactions when interacting with the contract.

## Running the Game

1. Open the project in Godot and press **Play**.
2. When you click a cell, the project calls the Python scripts in `xsolla-zk-lib/` to start the game, make a move and refresh the board.

You can also run the Python helpers directly from the command line if desired:

```bash
python xsolla-zk-lib/tictactoe-startgame.py   # start a new game
python xsolla-zk-lib/tictactoe-move.py <row> <col>  # send a move
python xsolla-zk-lib/tictactoe-getBoard.py    # print board state
```

## Testing Locally

There is no automated test suite. To ensure the scripts work you can run a quick syntax check:

```bash
python -m py_compile xsolla-zk-lib/*.py
```

If you have Godot installed you can also run the game scene directly and confirm that moves are reflected on chain.

