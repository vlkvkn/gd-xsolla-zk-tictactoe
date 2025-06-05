// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

contract TicTacToeVsAI {
    address public winner;

    enum Cell { Empty, X, O }
    Cell[3][3] public board;
    bool public gameStarted;
    bool public gameEnded;

    function startGame() external {
        require(!gameStarted || gameEnded, "Game in progress");
        resetBoard();
        gameStarted = true;
        gameEnded = false;
        winner = address(0);
    }

    function move(uint8 row, uint8 col) external {
        require(gameStarted && !gameEnded, "Invalid game state");
        require(row < 3 && col < 3, "Out of bounds");
        require(board[row][col] == Cell.Empty, "Cell already taken");

        // Player move (X)
        board[row][col] = Cell.X;
        if (checkWin(Cell.X)) {
            winner = msg.sender;
            gameEnded = true;
            return;
        }

        // If not over and board not full, let AI move
        if (!isBoardFull()) {
            aiMove(); // internal move
            if (checkWin(Cell.O)) {
                winner = address(this); // AI is contract
                gameEnded = true;
            }
        }

        // End game if board is full
        if (isBoardFull()) {
            gameEnded = true;
        }
    }

    function aiMove() internal {
        // Simple AI: first empty cell
        for (uint8 i = 0; i < 3; i++) {
            for (uint8 j = 0; j < 3; j++) {
                if (board[i][j] == Cell.Empty) {
                    board[i][j] = Cell.O;
                    return;
                }
            }
        }
    }

    function isBoardFull() internal view returns (bool) {
        for (uint8 i = 0; i < 3; i++) {
            for (uint8 j = 0; j < 3; j++) {
                if (board[i][j] == Cell.Empty) return false;
            }
        }
        return true;
    }

    function checkWin(Cell symbol) internal view returns (bool) {
        for (uint8 i = 0; i < 3; i++) {
            if (
                board[i][0] == symbol &&
                board[i][1] == symbol &&
                board[i][2] == symbol
            ) return true;

            if (
                board[0][i] == symbol &&
                board[1][i] == symbol &&
                board[2][i] == symbol
            ) return true;
        }

        if (
            board[0][0] == symbol &&
            board[1][1] == symbol &&
            board[2][2] == symbol
        ) return true;

        if (
            board[0][2] == symbol &&
            board[1][1] == symbol &&
            board[2][0] == symbol
        ) return true;

        return false;
    }

    function getBoard() external view returns (Cell[3][3] memory) {
        return board;
    }

    function resetBoard() internal {
        for (uint8 i = 0; i < 3; i++) {
            for (uint8 j = 0; j < 3; j++) {
                board[i][j] = Cell.Empty;
            }
        }
    }
}
