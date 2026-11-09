import time
from collections import deque

from puzzle_generator import apply_operation, generate


def check(grid, cages):
    size = len(grid)
    full = set(range(1, size + 1))
    for index in range(size):
        if set(grid[index]) != full:
            return False
        if {grid[row][index] for row in range(size)} != full:
            return False
    for operation, target, cells in cages:
        if apply_operation(operation, [grid[row][column] for row, column in cells]) != target:
            return False
    return True


def cage_allows(state, cages, row, column, value):
    for operation, target, cells in cages:
        if (row, column) in cells:
            values = [value if cell == (row, column) else state[cell[0]][cell[1]] for cell in cells]
            return 0 in values or apply_operation(operation, values) == target


def legal_values(state, row, column, cages):
    column_values = [line[column] for line in state]
    legal = []
    for value in range(1, len(state) + 1):
        if value in state[row] or value in column_values:
            continue
        if cage_allows(state, cages, row, column, value):
            legal.append(value)
    return legal


def actions(state, cages):
    best = None
    for row in range(len(state)):
        for column in range(len(state)):
            if state[row][column] == 0:
                moves = [(row, column, value) for value in legal_values(state, row, column, cages)]
                if not moves:
                    return []
                if best is None or len(moves) < len(best):
                    best = moves
    return best or []


def result(state, action):
    row, column, value = action
    new_state = [line[:] for line in state]
    new_state[row][column] = value
    return new_state


def is_goal(state, cages):
    return all(0 not in line for line in state) and check(state, cages)


def backtracking(size, cages, stats):
    queue = deque([[[0] * size for _ in range(size)]])
    while queue:
        state = queue.popleft()
        stats["path"].append(state)
        moves = actions(state, cages)
        if not moves:
            stats["backtracks"] += 1
        for action in moves:
            stats["nodes"] += 1
            child = result(state, action)
            if is_goal(child, cages):
                stats["path"].append(child)
                stats["solution"] = child
                return child
            queue.append(child)
    return None


def evaluate(size, cages):
    stats = {"nodes": 0, "backtracks": 0, "solution": None, "path": []}
    start = time.perf_counter()
    backtracking(size, cages, stats)
    stats["time"] = time.perf_counter() - start
    stats["correct"] = stats["solution"] is not None and check(stats["solution"], cages)
    return stats


if __name__ == "__main__":
    for size in range(3, 10):
        cages, solution = generate(size)
        assert check(solution, cages)
        report = evaluate(size, cages)
        assert report["correct"]
        print(f"{size}x{size}: {report['time']:.3f}s nodes={report['nodes']} backtracks={report['backtracks']}")
