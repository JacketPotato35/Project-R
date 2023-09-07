import pygame
import sys
import random
from test2 import Terminal 
from pygame.locals import QUIT
from dataclasses import dataclass
from player import Gunner,Archer,Knight,Empty_player
from wall import Wall
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
player = Gunner()
bullet_group = pygame.sprite.Group()
back = pygame.sprite.Group()
wall = pygame.sprite.Group()
text = Text()
enemy_bullets = pygame.sprite.Group()
level_square= Level_square()
lsquareg=pygame.sprite.Group()
lsquareg.add(level_square)
enemy_group = pygame.sprite.Group()
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
    bullet_group.draw(draw_surface)
    enemy_bullets.draw(draw_surface)
    


        

def load_new(ctime):
    player.score=0
    player.rect.center=(935,810)
    player.lives=3
    player.bullet_counter=6

    enemy_group.empty()
    enemy_bullets.empty()
    bullet_group.empty()

    while len(enemy_group.sprites())==0:
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
            enemy_group.add(Renemy(enemyx,enemyy,ctime))

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
    draw_surface.fill((160, 160, 160))
    if button_press==pygame.K_r:
        player.reload(display,current_time)
    for i in bullet_group:
        for x in enemy_group:
            if x.check_bullet_collision(i):
                x.apply_knockback(i.knockback,i.pointer)
                x.hp_bar.update_hp(-i.damage)
                x.check_death()
                terminal(random.randint(1,20))
                i.kill()
    if player.player_class=="knight":
        for x in enemy_group:
            for y in player.marker_group:
                if x.check_hit_collision(y.rect1) or x.check_hit_collision(y.rect2):
                    x.apply_knockback(player.knockback,y.pointer)
                    x.hp_bar.update_hp(-player.damage)
                    x.check_death()
    for i in enemy_group:
        i.update(player, current_time, space)
        i.draw_to_surface(draw_surface)
        player.check_death(i.rect, current_time)
    for i in enemy_bullets:
        if player.check_death(i.rect, current_time):
            return "dead"
    for i in enemy_group:
        if type(i).__name__=="Renemy":
            if i.enemyb_timer(current_time):
                enemy_bullets.add(i.create_ebullet(player))


    player.update(space, current_time,draw_surface)
    bullet_group.update(screen_height, screen_width, space)
    enemy_bullets.update(space)
    draw_to_surface()
    display.blit(draw_surface, (-player.rect.x-15 +
                 (screen_width/2), -player.rect.y+(screen_height/2)))
    text.render(display, ("lives:"+str(player.lives)),
                screen_width/12,screen_height/20, 30, (30, 30, 30))
    text.render(display, ("score:"+str(player.score)),
                screen_width/12*11,screen_height/20, 30, (30, 30, 30))
    if len(enemy_group.sprites())==0:
        return "next level"


def menu(player):
    text.render(display, "press 1 to play as gunner", screen_width/
                2, screen_height/2, 20, (255, 255, 255))
    text.render(display, "press 2 to play as archer", screen_width/
                2, screen_height/2+25, 20, (255, 255, 255))
    if button_press == pygame.K_1:
        game_loop()
        return "gunner"
    if button_press== pygame.K_2:
        game_loop()
        return "archer"
    if button_press== pygame.K_3:
        game_loop()
        return "knight"

def wait_level(button_press):

    draw_surface.fill((160, 160, 160))
    player.update(space, current_time, draw_surface)
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
    if level_square.player_in(player,display,button_press):
        return "next level"
        
def next_level(ctime):
    player.rect.center=(935,810)
    player.bullet_counter=6
    player.score+=1

    enemy_group.empty()
    enemy_bullets.empty()
    bullet_group.empty()

    while len(enemy_group.sprites())==0:
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
            enemy_group.add(Renemy(enemyx,enemyy,ctime))

while True:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP:
            button_press = event.key
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player.player_class=="gunner":
                if player.bullet_timer(current_time):
                    bullet_group.add(player.create_bullet(
                        screen_height, screen_width))
            if player.player_class=="archer":
                if player.charging==False:
                    player.charging=True
            if player.player_class=="knight":
                mouse_pos=pygame.mouse.get_pos()
                player.update_marker(mouse_pos,screen_width/2,screen_height/2)
        if event.type==pygame.MOUSEBUTTONUP:
            if player.player_class=="archer":
                if player.charging==True:
                    bullet_group.add(player.create_arrow(screen_height,screen_width))
                    
    if state == State.menu:
        if menu(player)=="gunner":
            player=Gunner()
            state = State.new_load
        elif menu(player)=="archer":
            player=Archer()
            state = State.new_load
        elif menu(player)=="knight":
            player=Knight()
            state=State.new_load
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
