import numpy as np

#Initialization of the board
class Board:
    def __init__(self, n):
        self.n = n
        self.board = [[' ' for j in range(n)] for i in range(n)]

# This part prints the board
    def print_board(self):
            print()
            for row in self.board:
                print('|', end=' ')
                for col in row:
                    print(col, '|', end=' ')
                print()
                print('-' * (n * 4 - 1))

# This part checks if the board is full
    def is_full(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] == ' ':
                    return False
        return True
    
# This part dertermins if the different moves are valid or not
    def is_valid_move(self, i, j):
        if i < 0 or i >= self.n or j < 0 or j >= self.n:
            return False
        return self.board[i][j] == ' '
    
# Whenever a move is done, this part insert the chip on the board
    def place_chip(self, i, j, player):
        self.board[i][j] = player

# The different winnings that can occur during the game
    def has_winner(self, i, j):
        player = self.board[i][j]

        # It checks if there is a horizontal win
        if all(self.board[i][j] == player for j in range(self.n)):
            return True
        
        # It checks if there is a vertical win
        if all(self.board[i][j] == player for i in range(self.n)):
            return True
        
        # It checks if there is a diagonal win
        if i == j and all(self.board[i][i] == player for i in range(self.n)):
            return True
        
        # It checks if there is an anti-diagonal win
        if i + j == self.n - 1 and all(self.board[i][j] == player for i in range(self.n)):
            return True
        return False

#Initialization of the brain of the game starting with the class intitialization
class Game:
    def __init__(self, n, players, depth):
        self.n = n
        self.players = players
        self.current_player = players[0]
        self.board = Board(n)
        self.depth = depth

    # ALPHA-BETA PRUNING AND SEARCH ALGORITHM implementation using Minimax

    # Alpha-Beta pruning
    def minimax(self, depth, player, alpha, beta):
        if depth == self.depth or self.board.is_full():
            return self.evaluate(), None

        # Minimax ==> This part maximizes the player's move
        if player == self.players[0]:  
            value = float("-inf")
            best_move = None
            for i in range(self.n):
                for j in range(self.n):

                    # If the move is valid and is the best move, it places the chip on the board
                    if self.board.is_valid_move(i, j):
                        self.board.place_chip(i, j, player)
                        new_value, _ = self.minimax(depth + 1, self.players[1], alpha, beta)
                        self.board.place_chip(i, j, ' ')
                        if new_value > value:
                            value = new_value
                            best_move = (i, j)
                        alpha = max(alpha, value)
                        if alpha >= beta:
                            break
            return value, best_move

        # Minimax==> This part maximizing function of the algorithm
        else:  
            value = float("inf")
            best_move = None
            for i in range(self.n):
                for j in range(self.n):
                    if self.board.is_valid_move(i, j):
                        self.board.place_chip(i, j, player)
                        new_value, _ = self.minimax(depth + 1, self.players[0], alpha, beta)
                        self.board.place_chip(i, j, ' ')
                        if new_value < value:
                            value = new_value
                            best_move = (i, j)
                        beta = min(beta, value)
                        if alpha >= beta:
                            break
            return value, best_move
        
    # Dtermonation of the human move
    def get_human_move(self):
        while True:

            # It allows the player to  enter the row and column number in the board using the strip() function
            move = input("Enter move (row, col): ")
            row, col = move.split(",")
            row = int(row.strip())
            col = int(col.strip())
            if self.board.is_valid_move(row, col):
                self.board.place_chip(row, col, self.players[0])
                break
            else:
                print("Invalid move.")

    # This part determines the move that will be by the computer using the minimax function
    def get_computer_move(self):
        _, move = self.minimax(0, self.current_player, float("-inf"), float("inf"))
        self.board.place_chip(move[0], move[1], self.current_player)

    # This part allows the switch from the current player to the next player using indexes
    def get_next_player(self):
        index = self.players.index(self.current_player)
        next_index = (index + 1) % len(self.players)
        return self.players[next_index]

# Using the has_winner() function implemented in the board class, we check if the current player is a winner
    def check_for_winner(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.board.board[i][j] != ' ':
                    if self.board.has_winner(i, j):
                        return self.current_player
        return None

    # This part will output the different situations that will happen when playing the game
    def play(self):

        # We start the game with the human player first
        print("Starting game...")
        print(f"{self.current_player}'s turn.")
        while True:

            #This part checks for a winner before allowing the next player to make a move
            self.board.print_board()
            winner = self.check_for_winner()

            # If there is a winner, it outputs who won the game
            if winner is not None:
                print(f"{winner} wins!")
                break

            # If there was a tie, it tells there was a tie
            if self.board.is_full():
                print("Game over. It's a tie!")
                break

            # It determines whose turn it is using the get_next_player function declare above
            if self.current_player == self.players[0]:
                self.get_human_move()
            else:
                self.get_computer_move()
            self.current_player = self.get_next_player()
            print(f"{self.current_player}'s turn.")


# Here, we now evaluate if either the human(X) player or computer(O) is a winner using
    def evaluate(self):
        if self.board.has_winner('X'):
            return 1
        elif self.board.has_winner('O'):
            return -1
        else:
            return 0


# Let's start the game!
if __name__ == "__main__":

    # We now assaign X as the human and O as the computer
    players = ['X', 'O']
    depth = int(input("Please enter the size of your NxN board: "))
    n = depth

    # Create a new instance of the Game class
    game = Game(n, players, depth)

    # Start playing the game
    game.play()  # Start playing the game