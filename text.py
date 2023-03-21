import pygame 
class Text():

    def __init__(self):
        self.font = pygame.font.SysFont("Verdana", 20)
        self.text = self.font.render(("hello"), True, (155, 155, 155))

    def render(self, display, text,locx, locy,font_size):
        self.font = pygame.font.SysFont("Verdana", font_size)
        self.text = self.font.render((text), True, (155, 155, 155))
        size=self.font.size(text)
        display.blit(self.text, (locx-(size[0]*0.5), locy))