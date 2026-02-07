import random

# Constants
EMPTY = "🌊"
DOG = "🐶"
HIT = "💥"
MISS = "❌"

ROWS = 10
COLS = 10
NUM_DOGS = 5  # number of Scotty Dogs

def empty_board():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board, hide_dogs=False):
    print("   " + " ".join(f"{c:2}" for c in range(COLS)))
    for r in range(ROWS):
        row_display = []
        for c in range(COLS):
            cell = board[r][c]
            if hide_dogs and cell == DOG:
                row_display.append(EMPTY)
            else:
                row_display.append(cell)
        print(f"{r:2} " + " ".join(row_display))
    print()

def create_dog(row, col, orientation):
    """Create 3-cell dog starting at (row, col). orientation='H' or 'V'"""
    dog = []
    try:
        if orientation.upper() == "H":
            dog = [[row, col-1], [row, col], [row, col+1]]
        else:
            dog = [[row-1, col], [row, col], [row+1, col]]
    except IndexError:
        return None
    for r, c in dog:
        if not (0 <= r < ROWS and 0 <= c < COLS):
            return None
    return dog

def check_dog(board, dog):
    for r, c in dog:
        if board[r][c] != EMPTY:
            return False
    return True

def add_dog(board, dog):
    for r, c in dog:
        board[r][c] = DOG

def user_place_dogs():
    board = empty_board()
    placed = 0
    print(f"\nPlace your {NUM_DOGS} Scotty Dogs on the board!")
    while placed < NUM_DOGS:
        print_board(board)
        try:
            row = int(input(f"Dog {placed+1} - Enter row of center (0-{ROWS-1}): "))
            col = int(input(f"Dog {placed+1} - Enter col of center (0-{COLS-1}): "))
            orientation = input("Orientation? (H for horizontal, V for vertical): ").upper()
            dog = create_dog(row, col, orientation)
            if dog and check_dog(board, dog):
                add_dog(board, dog)
                placed += 1
            else:
                print("Invalid placement. Try again.")
        except ValueError:
            print("Enter valid numbers!")
    return board

def add_computer_dogs(board):
    added = 0
    while added < NUM_DOGS:
        row = random.randint(1, ROWS-2)
        col = random.randint(1, COLS-2)
        orientation = random.choice(["H", "V"])
        dog = create_dog(row, col, orientation)
        if dog and check_dog(board, dog):
            add_dog(board, dog)
            added += 1
    return board

def is_game_over(board):
    for row in board:
        if DOG in row:
            return False
    return True

def user_guess(board):
    while True:
        try:
            row = int(input("Enter row to guess: "))
            col = int(input("Enter col to guess: "))
            if not (0 <= row < ROWS and 0 <= col < COLS):
                print("Coordinates out of bounds.")
                continue
            if board[row][col] == DOG:
                board[row][col] = HIT
                print("Woof! You hit a Scotty Dog!")
            elif board[row][col] == EMPTY:
                board[row][col] = MISS
                print("Splash! Just water.")
            else:
                print("You already guessed that!")
                continue
            break
        except ValueError:
            print("Enter valid numbers!")

def computer_guess(board):
    while True:
        r = random.randint(0, ROWS-1)
        c = random.randint(0, COLS-1)
        if board[r][c] in [EMPTY, DOG]:
            if board[r][c] == DOG:
                board[r][c] = HIT
                print(f"Computer hit your Scotty Dog at ({r}, {c})!")
            else:
                board[r][c] = MISS
                print(f"Computer missed at ({r}, {c}).")
            break

def main():
    print("🐾 Welcome to CMU Scotty Dog Battleship! 🐾")
    user_board = user_place_dogs()
    comp_board = add_computer_dogs(empty_board())
    
    turn = 1
    while True:
        print(f"\nTurn {turn}!")
        print("\nYour Board:")
        print_board(user_board)
        print("Computer Board:")
        print_board(comp_board, hide_dogs=True)

        print("\nYour turn!")
        user_guess(comp_board)
        if is_game_over(comp_board):
            print("\n🎉 Congratulations! You found all the Scotty Dogs! You win! 🎉")
            break

        print("\nComputer's turn!")
        computer_guess(user_board)
        if is_game_over(user_board):
            print("\n😢 Oh no! The computer found all your Scotty Dogs. You lose! 😢")
            break

        turn += 1

if __name__ == "__main__":
    main()



