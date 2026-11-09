# Function Reference

## backtracking.py

### `check(grid, cages)`
- **Input:** a filled `grid` and the puzzle's `cages`.
- **Output:** `True` or `False`.
- Checks that every row and column holds 1..size once and every cage hits its target.

### `cage_allows(state, cages, row, column, value)`
- **Input:** the current grid `state`, the puzzle's `cages`, a cell's `row` and `column`, and a `value` to place there.
- **Output:** `True` or `False`.
- Checks the cell's cage: if placing `value` fills the cage, it must hit the target; a cage with empty cells left is allowed.

### `legal_values(state, row, column, cages)`
- **Input:** the current grid `state`, a cell's `row` and `column`, and the puzzle's `cages`.
- **Output:** list of digits that can go in that cell.
- Finds digits not already in the row or column that `cage_allows` accepts.

### `actions(state, cages)`
- **Input:** the current grid `state` and the puzzle's `cages`.
- **Output:** list of moves `(row, column, value)`; empty if the state is a dead end.
- Returns the moves for the empty cell with the fewest legal digits.

### `result(state, action)`
- **Input:** the current grid `state` and an `action` `(row, column, value)`.
- **Output:** a new grid with the digit placed.
- Applies one move without changing the original state.

### `is_goal(state, cages)`
- **Input:** a grid `state` and the puzzle's `cages`.
- **Output:** `True` or `False`.
- Checks whether the grid is full and correct.

### `backtracking(size, cages, stats)`
- **Input:** `size`, `cages`, and a `stats` dictionary with `nodes`, `backtracks`, `solution` and `path`.
- **Output:** the solved grid, or `None`; also fills `stats`.
- Solves the puzzle with a loop-based breadth-first search using a queue, calling `actions`, `result` and `is_goal`.

### `evaluate(size, cages)`
- **Input:** `size` and `cages`.
- **Output:** dictionary with `time`, `nodes`, `backtracks`, `solution`, `path` and `correct`.
- Runs the backtracking solver, times it, and checks the answer.
