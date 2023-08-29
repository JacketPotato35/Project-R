import pygame
import sys
import random
from test2 import Terminal 
from pygame.locals import QUIT
from dataclasses import dataclass
from player import Player
from wall import Wall
from background_tile import Background
from shape import Shape
from enemy import Enemy
from renemy import Renemy
from rooms import room
from enum import Enum, auto
from text import Text
from level_square import Level_square

class State(Enum):
    menu = auto()
    game = auto()
    new_load = auto()
    wait_level=auto()
    next_level=auto()



state = State.menu

pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = display.get_size()
draw_surface = pygame.Surface((2000, 2000))
draw_surface.fill((160, 160, 160))
pygame.display.set_caption('Hello World!')
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)
bullet_group = pygame.sprite.Group()
back = pygame.sprite.Group()
wall = pygame.sprite.Group()
text = Text()
enemy_bullets = pygame.sprite.Group()
level_square= Level_square()
lsquareg=pygame.sprite.Group()
lsquareg.add(level_square)
enemy_group = pygame.sprite.Group()
renemy_group = pygame.sprite.Group()

space = []

roomy = 8
for y in room:
    roomy += 1
    roomx = 8
    for x in y:
        roomx += 1
        if x == "w":
            walls = Wall(roomx*50, roomy*50)
            wall.add(walls)
            # uses a shape dataclass
            space.append(Shape(walls.rect.left, walls.rect.right,
                         walls.rect.top, walls.rect.bottom))

current_time = 0
button_press = pygame.key

def draw_to_surface():
    back.draw(draw_surface)
    wall.draw(draw_surface)
    player_group.draw(draw_surface)
    bullet_group.draw(draw_surface)
    enemy_group.draw(draw_surface)
    hp=pygame.Surface((10,5))
    for sprite in enemy_group:
        draw_surface.blit(sprite.hp_bar.image,(sprite.rect.x,sprite.rect.y))
    enemy_bullets.draw(draw_surface)
    renemy_group.draw(draw_surface)
    


        

def load_new(ctime):
    player.score=0
    player.rect.center=(935,810)
    player.lives=3
    player.bullet_counter=6

    enemy_group.empty()
    renemy_group.empty()
    enemy_bullets.empty()
    bullet_group.empty()

    while len(enemy_group.sprites())+len(renemy_group.sprites())==0:
        for i in range(0,random.randint(0,3)):
            enemyx=random.randint(535,1300) #935
            enemyy=random.randint(410,1110) ##810
            while 1035>enemyx>835 and 910>enemyy>710:
                enemyx=random.randint(535,1335) #935
                enemyy=random.randint(410,1110) ##810
            enemy_group.add(Enemy(enemyx,enemyy,ctime,))
            
        for i in range(0,random.randint(0,3)):
            enemyx=random.randint(535,1300) #935
            enemyy=random.randint(410,1110) ##810
            while 1035>enemyx>835 and 910>enemyy>710:
                enemyx=random.randint(535,1335) #935
                enemyy=random.randint(410,1110) ##810
            renemy_group.add(Renemy(enemyx,enemyy,ctime))

def terminal(random):
    if random==1:
        screenchange(display)
        terminal=Terminal()
        terminal.run(display)

def screenchange(display_return : pygame.surface):
    display_xy=display_return.get_size()
    line=pygame.Surface((display_xy[0],3))
    line.fill((63, 63, 63))
    for y in range(0,int(round(display_xy[1]/2,0)),3):
        display.blit(line,(0,int(round(display_xy[1]/2,0))+y))
        display.blit(line,(0,int(round(display_xy[1]/2,0))-y))
        pygame.display.update()
        pygame.time.delay(1)
    pygame.display.update()
    pygame.time.delay(400)


def game_loop():
    for i in bullet_group:
        for x in enemy_group:
            if x.check_death(i):
                x.hp_bar.update_hp(-5)
                terminal(random.randint(1,5))
                i.kill()
        for x in renemy_group:
            if x.check_death(i):
                i.kill()
                terminal(random.randint(1,8))
    for i in enemy_group:
        i.update(player, current_time, space)
        player.check_death(i.rect, current_time)
    for i in enemy_bullets:
        if player.check_death(i.rect, current_time):
            return "dead"
    for i in renemy_group:
        i.update(player, current_time, space)
        player.check_death(i.rect, current_time)
        if i.enemyb_timer(current_time):
            enemy_bullets.add(i.create_ebullet(player))

    draw_surface.fill((160, 160, 160))
    player_group.update(space, current_time)
    bullet_group.update(screen_height, screen_width, space)
    enemy_bullets.update(space)
    draw_to_surface()
    display.blit(draw_surface, (-player.rect.x-15 +
                 (screen_width/2), -player.rect.y+(screen_height/2)))
    text.render(display, ("lives:"+str(player.lives)),
                screen_width/12,screen_height/20, 30, (30, 30, 30))
    text.render(display, ("score:"+str(player.score)),
                screen_width/12*11,screen_height/20, 30, (30, 30, 30))
    player.reload_text(display, current_time)
    if len(enemy_group.sprites())+len(renemy_group.sprites())==0:
        return "next level"


def menu():
    text.render(display, "press space to play", screen_width/
                2, screen_height/2, 20, (255, 255, 255))
    if button_press == pygame.K_SPACE:
        return (True)

def wait_level(button_press):

    draw_surface.fill((160, 160, 160))
    player_group.update(space, current_time)
    bullet_group.update(screen_height, screen_width, space)
    enemy_bullets.update(space)
    lsquareg.draw(draw_surface)
    draw_to_surface()
    display.blit(draw_surface, (-player.rect.x +
                 (screen_width/2), -player.rect.y+(screen_height/2)))
    text.render(display, ("lives:"+str(player.lives)),
                screen_width/12,screen_height/20, 30, (30, 30, 30))
    text.render(display, ("score:"+str(player.score)),
                screen_width/12*11,screen_height/20, 30, (30, 30, 30))
    player.reload_text(display, current_time)
    if level_square.player_in(player,display,button_press):
        return "next level"
        
def next_level(ctime):
    player.rect.center=(935,810)
    player.bullet_counter=6
    player.score+=1

    enemy_group.empty()
    renemy_group.empty()
    enemy_bullets.empty()
    bullet_group.empty()

    while len(enemy_group.sprites())+len(renemy_group.sprites())==0:
        for i in range(0,random.randint(0,3)):
            enemyx=random.randint(535,1300) #935
            enemyy=random.randint(410,1160) ##810
            while 1035>enemyx>835 and 910>enemyy>710:
                enemyx=random.randint(535,1300) #935
                enemyy=random.randint(410,1110) ##810
            enemy_group.add(Enemy(enemyx,enemyy,ctime))
            
        for i in range(0,random.randint(0,3)):
            enemyx=random.randint(535,1300) #935
            enemyy=random.randint(410,1160) ##810
            while 1035>enemyx>835 and 910>enemyy>710:
                enemyx=random.randint(535,1300) #935
                enemyy=random.randint(410,1110) ##810
            renemy_group.add(Renemy(enemyx,enemyy,ctime))

while True:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP:
            button_press = event.key
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player.bullet_timer(current_time):
                bullet_group.add(player.create_bullet(
                    screen_height, screen_width))
    if state == State.menu:
        if menu():
            button_press=""
            state = State.new_load
    elif state == State.game:
        game_loop_return=game_loop()
        if game_loop_return== "dead":
            state = State.menu
        if game_loop_return== "next level":
            state=State.wait_level
    elif state== State.new_load:
        load_new(current_time)
        state=State.game
    elif state==State.wait_level:
        wait=wait_status=wait_level(button_press)
        button_press=""
        if wait=="next level":
            state=State.next_level
    elif state==State.next_level:
        next_level(current_time)
        state=State.game
    pygame.display.update()
    clock.tick(60)
