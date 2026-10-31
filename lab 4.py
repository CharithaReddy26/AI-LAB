
def cost(board):
    n = len(board)
    conflicts = 0

    for i in range(n):
        for j in range(i + 1, n):
            if abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1

    return conflicts


def hill_climbing(board):
    n = len(board)

    while True:
        current_cost = cost(board)
        print("Current state:", board, "Cost:", current_cost)

        if current_cost == 0:
            return board

        best_board = None
        best_cost = current_cost

        for i in range(n):
            for j in range(i + 1, n):
                neighbor = board.copy()
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                neighbor_cost = cost(neighbor)

                if neighbor_cost < best_cost:
                    best_cost = neighbor_cost
                    best_board = neighbor

        if best_board is None:
            print("Hill climbing stuck at local minimum.")
            return None

        board = best_board


n = int(input("Enter number of queens: "))
initial_state = list(map(int, input(
    "Enter initial state (space-separated row numbers): "
).split()))

if len(initial_state) != n or sorted(initial_state) != list(range(n)):
    print("Invalid initial state. Enter each row number from 0 to n-1 once.")
else:
    solution = hill_climbing(initial_state)

    if solution is not None:
        print("Goal state:", solution)
        print("Final cost:", cost(solution))

        for row in range(n):
            print(" ".join(
                "Q" if solution[col] == row else "."
                for col in range(n)
            ))

print("Name: Charitha reddy")
print("USN: 1WA24CS091")