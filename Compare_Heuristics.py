import time
import random
from Puzzle import a_star, is_solvable

def compare_heuristics(num_tests=5):
    """
    Runs multiple random solvable 8-puzzle tests to compare Hamming and Manhattan heuristics.

    Input:
        num_tests (int): number of random puzzles to test.
    Output:
        Prints average time and expanded nodes for both heuristics.
    """

    total_time_hamming = 0
    total_nodes_hamming = 0
    total_time_manhattan = 0
    total_nodes_manhattan = 0

    for i in range(num_tests):
        start = list(range(9))
        random.shuffle(start)
        while not is_solvable(start):
            random.shuffle(start)

        print(f"\nRunning test {i+1}/{num_tests}...")

        # Hamming
        t0 = time.time()
        _, nodes_h = a_star(start, "hamming")
        total_time_hamming += time.time() - t0
        total_nodes_hamming += nodes_h

        # Manhattan
        t0 = time.time()
        _, nodes_m = a_star(start, "manhattan")
        total_time_manhattan += time.time() - t0
        total_nodes_manhattan += nodes_m

    print("\n📊 Average Results (over", num_tests, "runs):")
    print("Hamming  → Avg Time: {:.4f}s | Avg Nodes: {:.1f}".format(
        total_time_hamming / num_tests, total_nodes_hamming / num_tests))
    print("Manhattan → Avg Time: {:.4f}s | Avg Nodes: {:.1f}".format(
        total_time_manhattan / num_tests, total_nodes_manhattan / num_tests))


compare_heuristics()