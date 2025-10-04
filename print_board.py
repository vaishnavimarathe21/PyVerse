import random
def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)
def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False
def is_full(board):
    return all(cell != " " for row in board for cell in row)
def player_move(board):
    move = input("Enter row and column (0,1,2): ").split()
    r, c = int(move[0]), int(move[1])
    if board[r][c] == " ":
        board[r][c] = "X"
    else:
        print("Invalid move")
        player_move(board)
def ai_move(board):
    empty = [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]
    move = random.choice(empty)
    board[move[0]][move[1]] = "O"
board = [[" "]*3 for _ in range(3)]
while True:
    print_board(board)
    player_move(board)
    if check_winner(board, "X"):
        print_board(board)
        print("You win!")
        break
    if is_full(board):
        print("Draw")
        break
    ai_move(board)
    if check_winner(board, "O"):
        print_board(board)
        print("AI wins!")
        break
