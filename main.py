import sys

import pygame


class Game:
    def __init__(self):
        pass

    def run(self):
        pass


# --- Main Game Loop ---
def main(screen):
    clock = pygame.time.Clock()
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BACKGROUND_COLOUR)
        game.run()

        pygame.display.flip()
        clock.tick(FPS)


# --- Script Entry Point ---
if __name__ == "__main__":
    # --- Game Constants ---
    SCREEN_WIDTH = 600  # Window width
    SCREEN_HEIGHT = 600  # Window height
    FPS = 60  # Frames per second

    DARK_GREY = (30, 30, 30)

    BACKGROUND_COLOUR = (30, 30, 30)

    # --- Pygame Setup ---
    pygame.init()
    GAME_WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    main(GAME_WINDOW)
