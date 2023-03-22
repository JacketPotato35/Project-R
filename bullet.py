import pygame 
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x_pos,y_pos, screen_width, screen_height,bullet_xy):
        super().__init__()
        self.player_center=bullet_xy
        self.image=pygame.Surface((10,10))
        self.image.fill((255,0,0))
        self.rect=self.image.get_rect(center=(x_pos,y_pos))
        self.position=pygame.Vector2(x_pos,y_pos)
        mouse_pos=pygame.mouse.get_pos()
        self.pointer=pygame.Vector2((-screen_height/2)+mouse_pos[0],-screen_width/2+mouse_pos[1]).normalize()
    def update(self,screen_width, screen_height,space):
        for i in space:
            if i.right>self.rect.centerx>i.left and i.bottom>self.rect.centery>i.top:
                self.kill()
        self.position.y+=self.pointer.y*5
        self.position.x+=self.pointer.x*5
        self.rect.center=self.position 

        if self.rect.y>self.player_center[1]+screen_height or self.rect.y<0-self.player_center[1] or self.rect.x>screen_width+self.player_center[0] or self.rect.x<0-self.player_center[0]:
            self.kill()