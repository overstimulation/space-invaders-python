import sys
from random import choice, randint

import pygame

import obstacle
from alien import Alien, ExtraAlien
from laser import Laser
from player import Player


class Game:
    def __init__(self):
        # Player setup
        player_sprite = Player((SCREEN_WIDTH / 2, SCREEN_HEIGHT), SCREEN_WIDTH, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Health and score setup
        self.lives = 3
        self.life_surface = pygame.image.load("assets/textures/player.png").convert_alpha()
        self.life_x_start_position = SCREEN_WIDTH - (self.life_surface.get_size()[0] * 2 + 20)
        self.score = 0
        try:
            self.font = pygame.font.Font("assets/fonts/Pixeled.ttf", FONT_SIZE)
        except pygame.error:
            self.font = pygame.font.SysFont(None, FONT_SIZE)

        # Obstacle setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (SCREEN_WIDTH / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start=SCREEN_WIDTH / 15, y_start=480)

        # Alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows=6, cols=8)
        self.alien_direction = 1

        # Extra alien setup
        self.extra_alien = pygame.sprite.GroupSingle()
        self.extra_alien_spawn_time = randint(400, 800)

        # Audio setup
        music = pygame.mixer.Sound("assets/sounds/background_music.wav")
        music.set_volume(0.2)
        music.play(loops=-1)
        self.laser_sound = pygame.mixer.Sound("assets/sounds/laser.wav")
        self.laser_sound.set_volume(0.5)
        self.explosion_sound = pygame.mixer.Sound("assets/sounds/explosion.wav")
        self.explosion_sound.set_volume(0.3)

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

    def alien_setup(self, rows, cols, x_distance=60, y_distance=48, x_offset=70, y_offset=100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0:
                    alien_sprite = Alien("yellow", x, y)
                elif 1 <= row_index <= 2:
                    alien_sprite = Alien("green", x, y)
                else:
                    alien_sprite = Alien("red", x, y)

                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= SCREEN_WIDTH:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 6, SCREEN_HEIGHT)
            self.alien_lasers.add(laser_sprite)
            self.laser_sound.play()

    def extra_alien_timer(self):
        self.extra_alien_spawn_time -= 1
        if self.extra_alien_spawn_time <= 0:
            self.extra_alien.add(ExtraAlien(choice(["right", "left"]), SCREEN_WIDTH))
            self.extra_alien_spawn_time = randint(400, 800)

    def collision_checks(self):
        # Player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # Obstacle collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                # Alien collisions
                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()
                    self.explosion_sound.play()

                # Extra alien collision
                if pygame.sprite.spritecollide(laser, self.extra_alien, True):
                    self.score += 500
                    laser.kill()

        # Alien lasers
        if self.alien_lasers:
            for laser in self.alien_lasers:
                # Obstacle collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                # Player collision
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

        # Aliens
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)

                if pygame.sprite.spritecollide(alien, self.player, False):
                    pygame.quit()
                    sys.exit()

    def display_lives(self):
        for life in range(self.lives - 1):
            x = self.life_x_start_position + (life * (self.life_surface.get_size()[0] + 10))
            GAME_WINDOW.blit(self.life_surface, (x, 8))

    def display_score(self):
        score_surface = self.font.render(f"score: {self.score}", False, "white")
        score_rect = score_surface.get_rect(topleft=(10, -10))
        GAME_WINDOW.blit(score_surface, score_rect)

    def run(self):
        self.player.update()
        self.aliens.update(self.alien_direction)
        self.extra_alien.update()
        self.alien_lasers.update()

        self.alien_position_checker()
        self.extra_alien_timer()
        self.collision_checks()

        self.player.sprite.lasers.draw(GAME_WINDOW)
        self.player.draw(GAME_WINDOW)
        self.blocks.draw(GAME_WINDOW)
        self.aliens.draw(GAME_WINDOW)
        self.alien_lasers.draw(GAME_WINDOW)
        self.extra_alien.draw(GAME_WINDOW)
        self.display_lives()
        self.display_score()


class CRT:
    def __init__(self):
        self.tv = pygame.image.load("assets/textures/tv_effect.png").convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def create_crt_lines(self):
        line_height = 3
        line_amount = int(SCREEN_HEIGHT / line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv, "black", (0, y_pos), (SCREEN_WIDTH, y_pos), 1)

    def draw(self):
        self.tv.set_alpha(randint(75, 90))
        self.create_crt_lines()
        GAME_WINDOW.blit(self.tv, (0, 0))


# --- Main Game Loop ---
def main(screen):
    clock = pygame.time.Clock()
    game = Game()
    crt = CRT()

    ALIEN_LASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIEN_LASER, 600)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIEN_LASER:
                game.alien_shoot()

        screen.fill(BACKGROUND_COLOUR)
        game.run()
        crt.draw()

        pygame.display.flip()
        clock.tick(FPS)


# --- Script Entry Point ---
if __name__ == "__main__":
    # --- Game Constants ---
    SCREEN_WIDTH = 600  # Window width
    SCREEN_HEIGHT = 600  # Window height
    FPS = 60  # Frames per second
    FONT_SIZE = 20

    DARK_GREY = (30, 30, 30)
    RED = (241, 79, 80)

    BACKGROUND_COLOUR = DARK_GREY

    # --- Pygame Setup ---
    pygame.init()
    GAME_WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    main(GAME_WINDOW)
