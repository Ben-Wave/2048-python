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
        self.autoplay = False      # Autoplay standardmäßig deaktiviert
        self.ai_play = False       # KI-Modus deaktiviert
        self.show_stats = False    # Debug-Overlay standardmäßig ausgeblendet

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
                elif event.key == pygame.K_i:
                    self.ai_play = not self.ai_play
                elif event.key == pygame.K_d:
                    self.show_stats = not self.show_stats  # Toggle Debug-Informationen

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000  
            self.handle_events()

            dt_effective = dt * 3 if not self.autoplay and not self.ai_play else dt

            if self.autoplay and not self.game.game_over:
                self.game.auto_move()
            if self.ai_play and not self.game.game_over:
                self.game.auto_ai_move()

            if self.game.game_over:
                if self.ai_play:  # Nur wenn AI aktiv ist, soll das Spiel neu starten
                    self.game.ai.games_played += 1
                    if self.game.score > self.game.ai.best_score:
                        self.game.ai.best_score = self.game.score
                    if self.game.best_tile > self.game.ai.best_tile:
                        self.game.ai.best_tile = self.game.best_tile

                    self.game.ai.save_model()  # Nur einmal speichern
                    self.game.reset_game()  # Nur hier resetten!

            self.game.update(dt_effective)
            self.game.draw(self.screen)

            font_small = self.game.config.font['extra_small']
            text_color = self.game.config.TEXT_COLOR_BRIGHT
            autoplay_text = font_small.render("'A' für Autoplay", True, text_color)
            ai_text = font_small.render("'I' für Intelligent Mode", True, text_color)
            self.screen.blit(autoplay_text, (10, self.game.config.WINDOW_HEIGHT - 70))
            self.screen.blit(ai_text, (270, self.game.config.WINDOW_HEIGHT - 70))

            if self.show_stats:
                overlay_rect = pygame.Rect(10, 10, 250, 80)
                overlay = pygame.Surface((overlay_rect.width, overlay_rect.height))
                overlay.set_alpha(150)
                overlay.fill((0, 0, 0))
                self.screen.blit(overlay, (overlay_rect.x, overlay_rect.y))

                version_text = font_small.render(f"Modell-Version: {self.game.ai.version}", True, text_color)
                best_score_text = font_small.render(f"Best Score: {self.game.ai.best_score}", True, text_color)
                games_played_text = font_small.render(f"Spiele: {self.game.ai.games_played}", True, text_color)
                self.screen.blit(version_text, (overlay_rect.x + 5, overlay_rect.y + 5))
                self.screen.blit(best_score_text, (overlay_rect.x + 5, overlay_rect.y + 30))
                self.screen.blit(games_played_text, (overlay_rect.x + 5, overlay_rect.y + 55))

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    GameMain().run()
