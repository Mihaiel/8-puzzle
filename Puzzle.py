import random
import time

# Start state of the board (randomly shuffle 9 integers 0-8, 0 being blank)
start_state = list(range(9))
random.shuffle(start_state)

# Our goal state
goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
goal_positions = {
  1: (0,1),     # tile 1 should be row 0, col 1
  2: (0,2),     # tile 2 should be row 0, col 2
  3: (1,0),
  4: (1,1),
  5: (1,2),
  6: (2,0),
  7: (2,1),
  8: (2,2)
}

# Instead of writing everything in a line, we want to prettify it
def prettify(board):
    board_printed = ""
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

# Checks if the board has a solution (not all randomly generated boards have one)
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
    new_boards = []
    i0 = board.index(0)  # where is the blank?
    row, col = divmod(i0, 3)

    # check each direction if we can move there
    if row > 0:  # move up
        new = board.copy()
        new[i0], new[i0 - 3] = new[i0 - 3], new[i0]
        new_boards.append(new)

    if row < 2:  # move down
        new = board.copy()
        new[i0], new[i0 + 3] = new[i0 + 3], new[i0]
        new_boards.append(new)

    if col > 0:  # move left
        new = board.copy()
        new[i0], new[i0 - 1] = new[i0 - 1], new[i0]
        new_boards.append(new)

    if col < 2:  # move right
        new = board.copy()
        new[i0], new[i0 + 1] = new[i0 + 1], new[i0]
        new_boards.append(new)

    return new_boards

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def a_star(start, heuristic_func):
    # f(n) = g(n) + h(n)
    # |      |      ->  h(n) = our heuristic (manhattan or hamming)
    # |       ->        g(n) = our moves so far
    #  ->               f(n) = total cost (A* Algorithm)

    # Convert to tuple so we can use it in dictionaries
    start = tuple(start)
    goal = tuple(goal_state)

    # Decide which heuristic to use
    if heuristic_func == "manhattan":
        print("Using manhattan as heuristic.")
        heuristic = lambda b: manhattan(list(b))
    elif heuristic_func == "hamming":
        print("Using hamming as heuristic.")
        heuristic = lambda b: hamming(list(b))
    else:
        print("Wrong heuristic name! Use either 'manhattan' or 'hamming'.")
        return None

    # Keep track of where we came from (used to rebuild path)
    came_from = {}

    # g[n] = cost (moves) to reach this board, saved as a tuple -> key value pair
    g_score = {start: 0}

    # f[n] = g + h, saved as a tuple -> key value pair
    f_score = {start: heuristic(start)}

    # Boards we still need to explore and expanded nodes (for memory measure)
    to_explore = [start]
    expanded_nodes = 0

    while to_explore:
            # Look at each board b in to_explore, calculate f_score of each, pick the lowest one
            # (min function)
            current = min(to_explore, key=lambda b: f_score[b])
            expanded_nodes += 1

            # If we reached the goal → stop
            if current == goal:
                print("✅ Goal reached!")
                return reconstruct_path(came_from, current), expanded_nodes

            # Remove from open list
            to_explore.remove(current)

            # Explore all neighbors (possible moves of the blank)
            for neighbor in neighbors(list(current)):
                neighbor = tuple(neighbor)
                tentative_g = g_score[current] + 1  # one more move

                # If we haven't seen this board before or found a better path to it
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor)
                    if neighbor not in to_explore:
                        to_explore.append(neighbor)

    print("No solution found (shouldn't happen if solvable).")
    return None


### MAIN CODE ###
# Wrap (Run this code only if this file is being executed directly, not when it’s imported)
if __name__ == "__main__":
    # Keep generating until we get a solvable start
    while not is_solvable(start_state):
        print("Current board not solvable, generating another one...")
        random.shuffle(start_state)

    # Starting state of the puzzle
    print("\nSolvable board generated!")
    prettify(start_state)

    # Choose heuristic
    while True:
        print("\nChoose a heuristic:")
        print("(1) Hamming")
        print("(2) Manhattan")
        choice = input("> ").strip()
        if choice == "1":
            heuristic_name = "hamming"
            break
        elif choice == "2":
            heuristic_name = "manhattan"
            break
        else:
            print("Wrong input, try again (1 or 2).")

    print("\nStarting A* Search...\n")
    # Start the A* Algorithm and measure the time
    start_time = time.time()
    solution_path, expanded = a_star(start_state, heuristic_name)
    elapsed_time = time.time() - start_time

    # --- show result ---
    if solution_path:
        print("\nSolution found!")
        print("Number of moves:", len(solution_path) - 1)
        print("Time taken: " + str(elapsed_time) + "s")
        print("Memory used: " + str(expanded))
        for i, board in enumerate(solution_path):
            print(f"\nStep {i}:")
            prettify(list(board))
    else:
        print("No solution could be found.")