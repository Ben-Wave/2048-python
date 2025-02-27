import pygame
from module.Gamemodule import Game2048
from module.const import GameConfig

class GameMain(GameConfig):
    def __init__(self):
        super().__init__()  # Initialisiere GameConfig
        pygame.init()
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption("2048")
        self.game = Game2048()
        self.clock = pygame.time.Clock()
        self.running = True
        self.autoplay = False  # Autoplay standardmäßig deaktiviert

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.game.move(0)
                elif event.key == pygame.K_RIGHT:
                    self.game.move(1)
                elif event.key == pygame.K_DOWN:
                    self.game.move(2)
                elif event.key == pygame.K_LEFT:
                    self.game.move(3)
                elif event.key == pygame.K_r:
                    self.game.reset_game()
                elif event.key == pygame.K_c and self.game.game_won:
                    self.game.continue_game()
                elif event.key == pygame.K_a:
                    self.autoplay = not self.autoplay

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000  
            self.handle_events()
            
            if self.autoplay and not self.game.game_over:
                self.game.auto_move()

            self.game.update(dt)
            self.game.draw(self.screen)
            # Zeichne den Hinweis für Autoplay
            autoplay_text = self.game.config.font['extra_small'].render("Drücke 'A' für Autoplay", True, self.game.config.TEXT_COLOR_BRIGHT)
            self.screen.blit(autoplay_text, (10, self.game.config.WINDOW_HEIGHT - 70))  # Positioniere den Text unterhalb der Statistik

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    GameMain().run()
