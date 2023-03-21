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
    def update(self,player, ctime):
        self.direction.x=self.randx
        self.direction.y=self.randy
        if self.time_move+4000>ctime:
            self.time_move=ctime 
        if self.time_move+3000<ctime:
            self.postion+=self.direction*3
        self.rect.center=self.position 
    def check_death(self, bullet_xy):
        if bullet_xy.rect[0]>self.rect.left and bullet_xy.rect[0]<self.rect.right and bullet_xy.rect[1]>self.rect.top and bullet_xy.rect[1]<self.rect.bottom:
            self.kill()
            return True