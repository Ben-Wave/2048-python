import pygame
from module.Gamemodule import Game2048
from module.const import *

def main():
    pygame.init()
    
    # Fenster erstellen
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("2048")

    # Spiel-Objekt erstellen
    game = Game2048()
    
    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(60) / 1000  # Delta Time für Animationen
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.move(0)
                elif event.key == pygame.K_RIGHT:
                    game.move(1)
                elif event.key == pygame.K_DOWN:
                    game.move(2)
                elif event.key == pygame.K_LEFT:
                    game.move(3)
                elif event.key == pygame.K_r:
                    game.reset_game()
                elif event.key == pygame.K_c and game.game_won:
                    game.continue_game()

        game.update(dt)
        game.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
