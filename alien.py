import pygame


class Alien(pygame.sprite.Sprite):
    def __init__(self, colour, x, y):
        super().__init__()
        file_path = "assets/textures/" + colour + "_enemy.png"
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, direction):
        self.rect.x += direction


class ExtraAlien(pygame.sprite.Sprite):
    def __init__(self, side, screen_width):
        super().__init__()
        self.image = pygame.image.load("assets/textures/extra_enemy.png").convert_alpha()

        if side == "right":
            x = screen_width + 50
            self.velocity = -3
        else:
            x = -50
            self.velocity = 3

        self.rect = self.image.get_rect(topleft=(x, 80))

    def update(self):
        self.rect.x += self.velocity
