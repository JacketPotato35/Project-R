import pygame, sys
from pygame.locals import QUIT
from dataclasses import dataclass 
from player import Player
from wall import Wall
from background_tile import Background
from shape import Shape 
from enemy import Enemy 
from rooms import room

print("i just wanna check i downloaded the right stuff")

pygame.init()
clock = pygame.time.Clock()
screen_width, screen_height = 800,700
display = pygame.display.set_mode((screen_width, screen_height))
draw_surface=pygame.Surface((2000,2000))
pygame.display.set_caption('Hello World!')

player = Player(screen_width, screen_height)
player_group = pygame.sprite.Group()
player_group.add(player)
bullet_group=pygame.sprite.Group()
back = pygame.sprite.Group()
wall=pygame.sprite.Group()

enemy=Enemy(600,600)
enemy2=Enemy(700,700)
enemy_group=pygame.sprite.Group()
enemy_group.add(enemy2)
enemy_group.add(enemy)
space=[]

for y in range(0,2000,100):
    for x in range(0, 2000, 100):
        background = Background(x,y)
        back.add(background)

roomy=8
for y in room:
    roomy+=1
    roomx=8
    for x in y:
        roomx+=1
        if x=="w":
            walls = Wall(roomx*50,roomy*50)
            wall.add(walls)
            #uses a shape dataclass
            space.append(Shape(walls.rect.left, walls.rect.right, walls.rect.top, walls.rect.bottom))

current_time=0
while True:
    current_time=pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            if player.bullet_timer(current_time):
                bullet_group.add(player.create_bullet(screen_height, screen_width)) 

    for i in bullet_group: 
        for x in enemy_group:
            if x.check_death(i):
                i.kill()

    for i in enemy_group:
            i.update(player,current_time)    
            player.check_death(i.rect)
    draw_surface.fill((30,30,30))
    player_group.update(space,current_time)
    bullet_group.update(screen_height,screen_width,space)
    back.draw(draw_surface)
    wall.draw(draw_surface)
    player_group.draw(draw_surface)
    bullet_group.draw(draw_surface)
    enemy_group.draw(draw_surface)
    display.blit(draw_surface, (-player.rect.x+(screen_width/2), -player.rect.y+(screen_height/2)))
    pygame.display.update()
    clock.tick(60)
