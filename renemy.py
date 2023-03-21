import pygame
import random
class Renemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.Surface((30,30))
        self.image.fill((30,60,155))
        self.rect=self.image.get_rect(center=(x,y))
        self.direction=pygame.Vector2(0,0)
        self.position=pygame.Vector2(x,y)
        self.randx=random.randint(-1,1)
        self.randy=random.randint(-1,0) 
        self.time_move=0
    def pdirection(self,player):
        sx=self.rect.centerx
        sy=self.rect.centery
        px=player.rect.centerx
        py=player.rect.centery
        if sx<px and sy<py:
            return pygame.Vector2(random.randint(0,1),random.randint(0,1))
        elif sx>px and sy<py:
            return pygame.Vector2(random.randint(-1,0),random.randint(0,1))
        elif sx<px and sy>py:
            return pygame.Vector2(random.randint(0,1),random.randint(-1,0))
        elif sx>px and sy>py:
            return pygame.Vector2(random.randint(-1,0),random.randint(-1,0))

    def update(self,player, ctime, space):
        if self.time_move+1500<ctime:
            self.time_move=ctime 
            self.direction=self.pdirection(player)
        if self.time_move+750>ctime:
            self.position+=self.direction*3
        self.rect.center=self.position 
    def check_death(self, bullet_xy):
        if bullet_xy.rect[0]>self.rect.left and bullet_xy.rect[0]<self.rect.right and bullet_xy.rect[1]>self.rect.top and bullet_xy.rect[1]<self.rect.bottom:
            self.kill()
            return True