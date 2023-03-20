import pygame
import random 
class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.Surface((30,30))
        self.image.fill((155,60,30))
        self.rect=self.image.get_rect(center=(x,y))
        self.time=0
        self.direction=pygame.Vector2(0,0)
        self.position=pygame.Vector2(x,y)
        self.randtime=0
    def update(self,player_pos, ctime):
        ppos=player_pos.rect
        x_dis=ppos[0]-self.rect.x
        y_dis=ppos[1]-self.rect.y
        vect=pygame.Vector2(x_dis,y_dis)
        if vect.length()<250 and self.time+3000<ctime:
            self.direction=vect.normalize()
            self.time=ctime
        elif vect.length()>250:
            self.direction=vect.normalize()
            self.position+=self.direction*0.5
        if self.time+1>ctime:
            self.randtime=random.randint(-100,300)
            print(self.randtime)
        if self.time+600+self.randtime>ctime:
            self.position+=self.direction*(7+random.randint(-3,5))
        self.rect.center=self.position
            
    def check_death(self, bullet_xy):
        if bullet_xy.rect[0]>self.rect.left and bullet_xy.rect[0]<self.rect.right and bullet_xy.rect[1]>self.rect.top and bullet_xy.rect[1]<self.rect.bottom:
            self.kill()