import pygame


class Enemy_bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, pointer):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((20, 50, 175))
        self.rect = self.image.get_rect(center=(x, y))
        self.pointer = pointer*7
        self.position = pygame.Vector2(x, y)

    def update(self, space):
        for i in space:
            if i.right > self.rect.centerx > i.left and i.bottom > self.rect.centery > i.top:
                self.kill()
        self.position += self.pointer
        self.rect.center = self.position
