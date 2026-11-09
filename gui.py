import tkinter as tk
from tkinter import messagebox, ttk

import backtracking
import puzzle_generator

SOLVERS = {
    "Backtracking (BFS)": backtracking.backtracking,
    "Genetic Algorithm": None,
    "Memetic Algorithm": None,
}
CELL = 60
PAD = 10


def position(index):
    return PAD + index * CELL


class App:
    def __init__(self, root):
        self.root = root
        root.title("KenKen Solver")

        top = ttk.Frame(root, padding=8)
        top.pack(fill="x")
        self.size_choice = tk.IntVar(value=4)
        self.algorithm = tk.StringVar(value="Backtracking (BFS)")
        self.animate = tk.BooleanVar(value=True)

        ttk.Label(top, text="Size:").pack(side="left")
        ttk.Spinbox(top, from_=3, to=9, width=3, textvariable=self.size_choice, state="readonly").pack(side="left", padx=5)
        ttk.Label(top, text="Algorithm:").pack(side="left")
        ttk.Combobox(top, textvariable=self.algorithm, values=list(SOLVERS), state="readonly", width=20).pack(side="left", padx=5)
        ttk.Checkbutton(top, text="Animate", variable=self.animate).pack(side="left")

        buttons = ttk.Frame(root, padding=(8, 0))
        buttons.pack(fill="x")
        ttk.Button(buttons, text="New Puzzle", command=self.new_puzzle).pack(side="left")
        ttk.Button(buttons, text="Solve", command=self.solve).pack(side="left", padx=5)
        ttk.Button(buttons, text="Clear", command=self.clear).pack(side="left")

        self.canvas = tk.Canvas(root, bg="white", highlightthickness=0)
        self.canvas.pack(padx=8, pady=8)
        self.metrics = ttk.Label(root, padding=8, font=("Consolas", 10))
        self.metrics.pack(fill="x")

        self.running = None
        self.new_puzzle()

    def new_puzzle(self):
        self.running = None
        self.size = self.size_choice.get()
        self.cages, _ = puzzle_generator.generate(self.size)
        self.draw()
        self.metrics.config(text="New puzzle generated. Choose an algorithm and press Solve.")

    def draw(self):
        size = self.size
        canvas = self.canvas
        canvas.delete("all")
        canvas.config(width=size * CELL + 2 * PAD, height=size * CELL + 2 * PAD)

        cage_of = {}
        for cage_index, (_, _, cells) in enumerate(self.cages):
            for cell in cells:
                cage_of[cell] = cage_index

        for row in range(size):
            for column in range(size):
                canvas.create_rectangle(position(column), position(row), position(column + 1), position(row + 1),
                                        outline="#ccc")

        for (row, column), cage_index in cage_of.items():
            left, right = position(column), position(column + 1)
            top, bottom = position(row), position(row + 1)
            if cage_of.get((row - 1, column)) != cage_index:
                canvas.create_line(left, top, right, top, width=3)
            if cage_of.get((row + 1, column)) != cage_index:
                canvas.create_line(left, bottom, right, bottom, width=3)
            if cage_of.get((row, column - 1)) != cage_index:
                canvas.create_line(left, top, left, bottom, width=3)
            if cage_of.get((row, column + 1)) != cage_index:
                canvas.create_line(right, top, right, bottom, width=3)

        for operation, target, cells in self.cages:
            row, column = cells[0]
            canvas.create_text(position(column) + 4, position(row) + 3, text=f"{target}{operation}", anchor="nw",
                               font=("Arial", 10, "bold"))

        self.texts = []
        for row in range(size):
            line = []
            for column in range(size):
                line.append(canvas.create_text(position(column) + CELL / 2, position(row) + CELL / 2 + 6,
                                               font=("Arial", 20)))
            self.texts.append(line)

    def set_cell(self, row, column, value):
        self.canvas.itemconfig(self.texts[row][column], text=value, fill="#1a7f37")

    def clear(self):
        self.running = None
        for row in range(self.size):
            for column in range(self.size):
                self.set_cell(row, column, "")

    def solve(self):
        name = self.algorithm.get()
        solver = SOLVERS[name]
        if solver is None:
            messagebox.showinfo("Not implemented", f"{name} is not implemented yet.")
            return

        self.clear()
        result = backtracking.evaluate(self.size, self.cages)
        self.metrics.config(
            text=f"{name} | {self.size}x{self.size} | time: {result['time'] * 1000:.1f} ms | "
                 f"nodes: {result['nodes']} | backtracks: {result['backtracks']} | "
                 f"correct: {'YES' if result['correct'] else 'NO'}"
        )

        if self.animate.get():
            self.running = result["path"]
            self.step(self.running, 0)
        elif result["solution"]:
            self.show_grid(result["solution"])

    def show_grid(self, grid):
        for row in range(self.size):
            for column in range(self.size):
                value = grid[row][column]
                self.set_cell(row, column, value if value else "")

    def step(self, path, index):
        if path is not self.running or index >= len(path):
            return
        self.show_grid(path[index])
        self.root.after(30, self.step, path, index + 1)


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
