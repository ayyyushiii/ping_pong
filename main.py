import pygame
from game.game_engine import GameEngine

pygame.init()
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Replay Version")

clock = pygame.time.Clock()
FPS = 60

def main():
    engine = GameEngine(WIDTH, HEIGHT)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Key events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                # Handle replay choices after Game Over
                if engine.game_over and engine.waiting_for_replay_choice:
                    if event.key == pygame.K_3:
                        engine.start_new_match(3)
                    elif event.key == pygame.K_5:
                        engine.start_new_match(5)
                    elif event.key == pygame.K_7:
                        engine.start_new_match(7)

        # Only update game if not over
        if not engine.game_over:
            keys = pygame.key.get_pressed()
            engine.handle_input(keys)
            engine.update()

        # Always render
        engine.render(SCREEN)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
