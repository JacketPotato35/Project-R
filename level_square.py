import pygame
from text import Text

class Level_square(pygame.sprite.Sprite):
    def __init__(self,x,y,direction):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((90, 255, 90))
        #935 810
        self.rect=self.image.get_rect(center=(935+x,810+y))
        self.direction=direction
        self.text=Text()
        self.room=""
        if direction==[1,0]:
            self.room="down"
        if direction==[-1,0]:
            self.room="up"
        if direction==[0,1]:
            self.room="right"
        if direction==[0,-1]:
            self.room="left"
            
    def player_in(self,player,display,button_press):
        if self.rect.right>player.rect.centerx>self.rect.left :
            if self.rect.bottom>player.rect.centery>self.rect.top:
                display_xy=display.get_size()
                self.text.render(display,(f"press space to move a room {self.room}"),display_xy[0],display_xy[1]/8,20,(30,30,30))
                if button_press==pygame.K_SPACE:
                    return True