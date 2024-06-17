import tkinter as tk
import random

class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048")
        self.master.geometry("500x600")  # Increased height to accommodate score label
        self.master.bind("<Key>", self.handle_key)

        self.grid_size = 4
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0

        self.init_ui()
        self.add_tile()
        self.update_grid()

    def init_ui(self):
        self.tiles = []
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                tile = tk.Label(self.master, text="", font=("Helvetica", 32, "bold"), width=4, height=2, relief="raised")
                tile.grid(row=i, column=j, padx=10, pady=10)
                row.append(tile)
            self.tiles.append(row)

        self.score_label = tk.Label(self.master, text=f"Score: {self.score}", font=("Helvetica", 24, "bold"))
        self.score_label.grid(row=self.grid_size, column=0, columnspan=self.grid_size)

    def add_tile(self):
        empty_cells = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def update_grid(self):
        color_map = {
            0: ("#776e65", "lightgray"),
            2: ("#776e65", "#eee4da"),
            4: ("#776e65", "#ede0c8"),
            8: ("#f9f6f2", "#f2b179"),
            16: ("#f9f6f2", "#f59563"),
            32: ("#f9f6f2", "#f67c5f"),
            64: ("#f9f6f2", "#f65e3b"),
            128: ("#f9f6f2", "#edcf72"),
            256: ("#f9f6f2", "#edcc61"),
            512: ("#f9f6f2", "#edc850"),
            1024: ("#f9f6f2", "#edc53f"),
            2048: ("#f9f6f2", "#edc22e"),
            4096: ("#f9f6f2", "#3c3a32"),
        }
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = self.grid[i][j]
                color, bg_color = color_map.get(value, ("#f9f6f2", "#3c3a32"))
                self.tiles[i][j].configure(text=str(value) if value != 0 else "", fg=color, bg=bg_color)
        
        self.score_label.configure(text=f"Score: {self.score}")
        self.master.update_idletasks()

    def handle_key(self, event):
        if event.keysym in ['Up', 'Down', 'Left', 'Right']:
            original_grid = [row[:] for row in self.grid]
            self.move_tiles(event.keysym)
            if self.grid != original_grid:
                self.add_tile()
                self.update_grid()
                if self.check_game_over():
                    self.game_over()

    def move_tiles(self, direction):
        if direction == 'Up':
            self.grid = self.transpose(self.grid)
            self.grid = self.merge_tiles(self.grid)
            self.grid = self.transpose(self.grid)
        elif direction == 'Down':
            self.grid = self.reverse(self.transpose(self.grid))
            self.grid = self.merge_tiles(self.grid)
            self.grid = self.transpose(self.reverse(self.grid))
        elif direction == 'Left':
            self.grid = self.merge_tiles(self.grid)
        elif direction == 'Right':
            self.grid = self.reverse(self.grid)
            self.grid = self.merge_tiles(self.grid)
            self.grid = self.reverse(self.grid)

    def merge_tiles(self, grid):
        new_grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        score = 0
        for i in range(self.grid_size):
            fill_position = 0
            for j in range(self.grid_size):
                if grid[i][j] != 0:
                    if new_grid[i][fill_position] == 0:
                        new_grid[i][fill_position] = grid[i][j]
                    elif new_grid[i][fill_position] == grid[i][j]:
                        new_grid[i][fill_position] *= 2
                        score += new_grid[i][fill_position]
                        fill_position += 1
                    else:
                        fill_position += 1
                        new_grid[i][fill_position] = grid[i][j]
        self.score += score
        return new_grid

    def check_game_over(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 0:
                    return False
                if j < self.grid_size - 1 and self.grid[i][j] == self.grid[i][j + 1]:
                    return False
                if i < self.grid_size - 1 and self.grid[i][j] == self.grid[i + 1][j]:
                    return False
        return True

    def game_over(self):
        game_over_label = tk.Label(self.master, text="Game Over! Score: {}".format(self.score), font=("Helvetica", 24, "bold"), bg="red", fg="white")
        game_over_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    @staticmethod
    def transpose(matrix):
        return [[row[i] for row in matrix] for i in range(len(matrix[0]))]

    @staticmethod
    def reverse(matrix):
        return [row[::-1] for row in matrix]

def main():
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()

if __name__ == "__main__":
    main()
