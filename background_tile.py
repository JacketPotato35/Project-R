import pygame


class Background(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((155, 155, 0))
        self.rect = self.image.get_rect(center=(x, y))
