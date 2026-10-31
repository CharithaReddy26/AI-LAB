
import random
import math

def calculate_cost(board):
    n = len(board)
    conflicts = 0

    for i in range(n):
        for j in range(i + 1, n):
            if abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1

    return conflicts


def simulated_annealing(board):
    n = len(board)
    temperature = 100.0
    cooling_rate = 0.99
    min_temperature = 0.01
    max_iterations = 100000

    board = board.copy()
    current_cost = calculate_cost(board)

    for iteration in range(max_iterations):
        print("Current state:", board, "Cost:", current_cost)

        if current_cost == 0:
            return board

        if temperature < min_temperature:
            break

        new_board = board.copy()

        col1, col2 = random.sample(range(n), 2)
        new_board[col1], new_board[col2] = (
            new_board[col2], new_board[col1]
        )

        new_cost = calculate_cost(new_board)
        delta = new_cost - current_cost

        if delta < 0 or random.random() < math.exp(-delta / temperature):
            board = new_board
            current_cost = new_cost

        temperature *= cooling_rate

    if current_cost == 0:
        return board

    print("Solution not found. Try again.")
    return None


n = 8

initial_state = list(map(int, input(
    "Enter initial state for 8 queens (8 row numbers from 0 to 7): "
).split()))

if len(initial_state) != 8 or sorted(initial_state) != list(range(8)):
    print("Invalid input. Enter each number from 0 to 7 exactly once.")
else:
    solution = simulated_annealing(initial_state)

    if solution is not None:
        print("Goal state:", solution)
        print("Final cost:", calculate_cost(solution))

        for row in range(8):
            print(" ".join(
                "Q" if solution[col] == row else "."
                for col in range(8)
            ))

print("Name: charitha reddy")
print("USN: 1WA24CS091")