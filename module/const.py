import pygame
class GameConfig:
    def __init__(self):
        pygame.init()
        
        # Farben
        self.BACKGROUND_COLOR = (187, 173, 160)
        self.EMPTY_CELL_COLOR = (205, 193, 180)
        self.FONT_COLOR = (119, 110, 101)
        self.TEXT_COLOR_BRIGHT = (249, 246, 242)

        # Farben für verschiedene Zahlen
        self.TILE_COLORS = {
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
            4096: (114, 177, 237),
            8192: (97, 204, 237),
            16384: (80, 200, 237),
            32768: (63, 197, 237),
            65536: (46, 194, 237),
        }

        # Spielkonstanten
        self.GRID_SIZE = 4
        self.CELL_SIZE = 100
        self.CELL_MARGIN = 10
        self.GRID_PADDING = 10
        self.WINDOW_WIDTH = self.GRID_SIZE * (self.CELL_SIZE + self.CELL_MARGIN) + self.GRID_PADDING * 2
        self.WINDOW_HEIGHT = self.WINDOW_WIDTH + 50
        self.WINDOW_SIZE = (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        # Animationen
        self.MOVE_ANIMATION_DURATION = 0.1  # Dauer der Bewegungsanimation in Sekunden
        self.MERGE_ANIMATION_DURATION = 0.2  # Dauer der Merge-Animation in Sekunden
        self.SPAWN_ANIMATION_DURATION = 0.15  # Dauer der Spawn-Animation in Sekunden

        # Fonts
        self.font = {
            'small': pygame.font.SysFont('Arial', 36),
            'medium': pygame.font.SysFont('Arial', 48),
            'large': pygame.font.SysFont('Arial', 60),
            'extra_small': pygame.font.SysFont('Arial', 24),
        }
        #Text_fonts
        self.TEXT_COLORS = {
            2: (119, 110, 101),
            4: (119, 110, 101),
            8: (249, 246, 242),
            16: (249, 246, 242),
            32: (249, 246, 242),
            64: (249, 246, 242),
            128: (249, 246, 242),
            256: (249, 246, 242),
            512: (249, 246, 242),
            1024: (249, 246, 242),
            2048: (249, 246, 242),
            4096: (249, 246, 242),
            8192: (249, 246, 242),
            16384: (249, 246, 242),
            32768: (249, 246, 242),
            65536: (249, 246, 242),
        }