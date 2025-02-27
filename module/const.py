import pygame

# Initialisierung
pygame.init()

# Farben
BACKGROUND_COLOR = (187, 173, 160)
EMPTY_CELL_COLOR = (205, 193, 180)
FONT_COLOR = (119, 110, 101)
TEXT_COLOR_BRIGHT = (249, 246, 242)

# Farben für verschiedene Zahlen
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    # Zusätzliche Farben für höhere Werte
    4096: (114, 177, 237),
    8192: (97, 204, 237),
    16384: (80, 200, 237),
    32768: (63, 197, 237),
    65536: (46, 194, 237)
}

# Textfarben (hell für dunkle Kacheln, dunkel für helle Kacheln)
TEXT_COLORS = {
    0: FONT_COLOR,
    2: FONT_COLOR,
    4: FONT_COLOR,
    8: TEXT_COLOR_BRIGHT,
    16: TEXT_COLOR_BRIGHT,
    32: TEXT_COLOR_BRIGHT,
    64: TEXT_COLOR_BRIGHT,
    128: TEXT_COLOR_BRIGHT,
    256: TEXT_COLOR_BRIGHT,
    512: TEXT_COLOR_BRIGHT,
    1024: TEXT_COLOR_BRIGHT,
    2048: TEXT_COLOR_BRIGHT,
    4096: TEXT_COLOR_BRIGHT,
    8192: TEXT_COLOR_BRIGHT,
    16384: TEXT_COLOR_BRIGHT,
    32768: TEXT_COLOR_BRIGHT,
    65536: TEXT_COLOR_BRIGHT
}

# Spielkonstanten
GRID_SIZE = 4
CELL_SIZE = 100
CELL_MARGIN = 10
GRID_PADDING = 10

# Animationskonstanten
SPAWN_ANIMATION_DURATION = 0.2  # Sekunden für den Spawn-Effekt
MOVE_ANIMATION_DURATION = 0.15  # Sekunden für Bewegungsanimationen
MERGE_ANIMATION_DURATION = 0.1  # Sekunden für Merge-Effekt

# Fenstergröße
WINDOW_WIDTH = GRID_SIZE * (CELL_SIZE + CELL_MARGIN) + GRID_PADDING * 2
WINDOW_HEIGHT = WINDOW_WIDTH + 50  # Extra Platz für Punktestand und Highscore
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Fonts
font = {
    'small': pygame.font.SysFont('Arial', 36),
    'medium': pygame.font.SysFont('Arial', 48),
    'large': pygame.font.SysFont('Arial', 60),
    'extra_small': pygame.font.SysFont('Arial', 24)  # Für sehr große Zahlen
}