import pygame
from text import Text

class Level_square(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((90, 255, 90))
        self.rect=self.image.get_rect(center=(935, 810))
    def player_in(self,player,display,button_press):
        display_xy=display.get_size()
        prx=player.rect.centerx
        pry=player.rect.centery
        if self.rect.right>prx>self.rect.left and self.rect.bottom>pry>self.rect.top:
            text=Text()
            text.render(display,("press space to go to next level"),display_xy[0]/2,display_xy[1]/11,20,(30,30,30))
            if button_press==pygame.K_SPACE:
                return True