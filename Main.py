import random

# Initialisiere das 4x4-Raster
def initialize_grid():
    grid = [[0] * 4 for _ in range(4)]
    add_random_tile(grid)
    add_random_tile(grid)
    return grid

# Füge eine zufällige Kachel (2 oder 4) hinzu
def add_random_tile(grid):
    empty_cells = [(i, j) for i in range(4) for j in range(4) if grid[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        grid[i][j] = random.choice([2, 4])

# Drucke das Raster
def print_grid(grid):
    for row in grid:
        print(" ".join(f"{num:4}" if num != 0 else "    " for num in row))
    print()

# Verschiebe die Kacheln nach links
def move_left(grid):
    new_grid = []
    for row in grid:
        # Entferne Nullen und kombiniere gleiche Kacheln
        new_row = [num for num in row if num != 0]
        new_row = combine_tiles(new_row)
        new_row += [0] * (4 - len(new_row))
        new_grid.append(new_row)
    return new_grid

# Kombiniere benachbarte gleiche Kacheln
def combine_tiles(row):
    for i in range(len(row) - 1):
        if row[i] == row[i + 1]:
            row[i] *= 2
            row[i + 1] = 0
    row = [num for num in row if num != 0]
    return row

# Drehe das Raster für andere Bewegungen
def rotate_grid(grid):
    return [list(row) for row in zip(*grid[::-1])]

# Hauptspielschleife
def main():
    grid = initialize_grid()
    print("Willkommen bei 2048!")
    print("Benutze W (hoch), A (links), S (runter), D (rechts), Q (beenden)")
    while True:
        print_grid(grid)
        move = input("Dein Zug: ").upper()
        if move == 'Q':
            print("Spiel beendet.")
            break
        elif move in ['W', 'A', 'S', 'D']:
            # Raster drehen, um die Bewegung zu vereinfachen
            if move == 'W':  # Hoch
                grid = rotate_grid(grid)
                grid = move_left(grid)
                grid = rotate_grid(grid)
                grid = rotate_grid(grid)
                grid = rotate_grid(grid)
            elif move == 'A':  # Links
                grid = move_left(grid)
            elif move == 'S':  # Runter
                grid = rotate_grid(grid)
                grid = rotate_grid(grid)
                grid = move_left(grid)
                grid = rotate_grid(grid)
                grid = rotate_grid(grid)
            elif move == 'D':  # Rechts
                grid = rotate_grid(grid)
                grid = rotate_grid(grid)
                grid = rotate_grid(grid)
                grid = move_left(grid)
                grid = rotate_grid(grid)
            add_random_tile(grid)
        else:
            print("Ungültige Eingabe! Benutze W, A, S, D oder Q.")

if __name__ == "__main__":
    main()
