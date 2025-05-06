import sys

import pygame

import obstacle
from player import Player


class Game:
    def __init__(self):
        # Player setup
        player_sprite = Player((SCREEN_WIDTH / 2, SCREEN_HEIGHT), SCREEN_WIDTH, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Obstacle setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (SCREEN_WIDTH / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start=SCREEN_WIDTH / 15, y_start=480)

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == "x":
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size, RED, x, y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def run(self):
        self.player.update()

        self.player.sprite.lasers.draw(GAME_WINDOW)
        self.player.draw(GAME_WINDOW)

        self.blocks.draw(GAME_WINDOW)


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
    RED = (241, 79, 80)

    BACKGROUND_COLOUR = (30, 30, 30)

    # --- Pygame Setup ---
    pygame.init()
    GAME_WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    main(GAME_WINDOW)
