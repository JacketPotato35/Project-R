import pygame


class level_square(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface(40, 40)
        self.image.fill(90, 255, 90)
        self.rect-self.image.get_rect(center=(935, 810))
