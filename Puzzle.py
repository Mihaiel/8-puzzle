import random

# Start state of the board (randomly shuffle 9 integers 0-8, 0 being blank)
start_state = list(range(9))
random.shuffle(start_state)

# Our goal state
goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
goal_positions = {tile: divmod(i, 3)
                  for i, tile in enumerate(goal_state) if tile != 0}

# We define our possible moves
moves = {
    'U': -3,  # Move up
    'D': 3,   # Move down
    'L': -1,  # Move left
    'R': 1    # Move rightxq
}

# Instead of writing everything in a line, we want to prettify it
def prettify(board):
    board_printed = "START STATE OF THE BOARD:"
    for i, x in enumerate(board):       # i = index, x = value
        if i % 3 == 0:
            board_printed += "\n"       # new row every 3 tiles
        else:
            board_printed += " "

        if x == 0:
            board_printed += "_"
        else:
            board_printed += str(x)

    print(board_printed)

def is_solvable(board) -> bool:
    summe = 0
    for k in range(9):
        for i, value in enumerate(board[k:], start=k):
            if board[k] != 0 and board[k] <= value:
                summe += 1
    return summe % 2 == 0


# Return Hamming distance - count of tiles that are not in their position (excluding empty)
def hamming(board) -> int:
    distance = 0
    for i, x in enumerate(board):
        if x != 0 and board[i] != goal_state[i]:
            distance += 1
    return distance

# Return Manhattan distance
def manhattan(board) -> int:
    distance = 0
    for i, value in enumerate(board):
        if value == 0:  # skip the blank
            continue
        r, c = divmod(i, 3)  # current row, col
        gr, gc = goal_positions[value]  # goal row, col
        distance += abs(r - gr) + abs(c - gc)
    return distance

def neighbors(board):

while not is_solvable(start_state):
    print("Current board not solvable, generating another one...")
    random.shuffle(start_state)
else:
    print("Solvable board generated!")
    prettify(start_state)

print("\nHamming distance of the board: " + str(hamming(start_state)))
print("Manhattan distance of the board: " + str(manhattan(start_state)))