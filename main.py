board = [[" "] * 6 for _ in range(6)]


def print_board():
    print("  0    1    2    3    4    5")
    for row in board:
        print(row)
    print("  0    1    2    3    4    5")


def drop(checker, column_id):
    for row in reversed(board):
        if row[column_id] == " ":
            row[column_id] = checker
            return True
    return False


def win_check():
    # Check rows for four consecutive discs
    for row in board:
        for col in range(len(row) - 3):
            if row[col] != " " and row[col] == row[col+1] == row[col+2] == row[col+3]:
                return True

    # Check columns for four consecutive discs
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if board[row][col] != " " and board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col]:
                return True

    # Check diagonals (top-left to bottom-right) for four consecutive discs
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] != " " and board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3]:
                return True

    # Check diagonals (bottom-left to top-right) for four consecutive discs
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] != " " and board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3]:
                return True

    return False


def play(player):
    print(f"{player} turn")
    while True:
        try:
            column = int(input("type in column id: "))
            if drop(player, column):
                break
            else:
                print("-Column is full-")
        except ValueError:
            print("-Invalid column id-")
        except IndexError:
            print("-Column id out of range-")

    print_board()
    if win_check():
        print(f"{player} wins")
        return
    play("x" if player == "o" else "o")


print_board()
play("x")
