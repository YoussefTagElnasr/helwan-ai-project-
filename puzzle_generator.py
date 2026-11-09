import random


def apply_operation(operation, values):
    if operation == "":
        return values[0]
    if operation == "+":
        return sum(values)
    if operation == "×":
        product = 1
        for value in values:
            product *= value
        return product
    if operation == "-":
        return abs(values[0] - values[1])
    if operation == "÷":
        big, small = max(values), min(values)
        if big % small == 0:
            return big // small
    return None


def make_solution(size):
    numbers = random.sample(range(1, size + 1), size)
    row_order = random.sample(range(size), size)
    column_order = random.sample(range(size), size)
    return [[numbers[(row_order[row] + column_order[column]) % size] for column in range(size)]
            for row in range(size)]


def neighbors(row, column, size):
    for row_step, column_step in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        if 0 <= row + row_step < size and 0 <= column + column_step < size:
            yield row + row_step, column + column_step


def choose_operation(values):
    if len(values) == 1:
        return ""
    if len(values) == 2:
        if apply_operation("÷", values) and random.random() < 0.5:
            return "÷"
        return random.choice(["+", "×", "-"])
    return random.choice(["+", "×"])


def generate(size):
    solution = make_solution(size)
    used = set()
    cages = []
    cells = [(row, column) for row in range(size) for column in range(size)]
    random.shuffle(cells)

    for start in cells:
        if start in used:
            continue
        cage_size = random.choice([1, 2, 2, 2, 3, 3, 3, 4, 4])
        cage = [start]
        used.add(start)
        while len(cage) < cage_size:
            options = [cell for row, column in cage for cell in neighbors(row, column, size) if cell not in used]
            if not options:
                break
            cell = random.choice(options)
            cage.append(cell)
            used.add(cell)

        values = [solution[row][column] for row, column in cage]
        operation = choose_operation(values)
        cages.append((operation, apply_operation(operation, values), sorted(cage)))

    return cages, solution
