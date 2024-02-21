import pygame
class Map(pygame.sprite.Sprite):
    def __init__(self, arr,current_pos):
        pygame.sprite.Sprite.__init__(self)
        self.grid_size=10
        self.image = pygame.Surface((self.grid_size-1,self.grid_size-1))
        self.image.fill((250, 10, 10))
        self.arr=arr
        self.current_pos=current_pos
    def update(self,arr,current_pos):
        self.arr=arr
        self.current_pos=current_pos
    def draw_grid(self,display):
         x=0
         y=0
         for row in self.arr:
                for element in row:
                  if element=="s":
                      self.image.fill((250,10,10))
                  if element=="e":
                      self.image.fill((12,12,12))
                  if element=="o":
                      self.image.fill((10,250,250))
                  if self.current_pos==[x/self.grid_size,y/self.grid_size]:
                      self.image.fill((10,10,250))
                  display.blit(self.image,(x+100,y+100))
                  x+=self.grid_size
                x=0
                y+=self.grid_size
