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
from map import Map

class State(Enum):
    menu = auto() 
    game = auto()
    new_load = auto()
    wait_level=auto()
    next_level=auto()
    buff_choose=auto()



state = State.menu

pygame.init()
clock = pygame.time.Clock()
info=pygame.display.Info()
display = pygame.display.set_mode((info.current_w*2,info.current_h*2), pygame.FULLSCREEN)
screen_width, screen_height = display.get_size()
screen_height*=2
screen_width*=2
draw_surface = pygame.Surface((2000, 2000))
draw_surface.fill((160, 160, 160))
pygame.display.set_caption('Hello World!')
player = Gunner()
bullet_group = pygame.sprite.Group()
back = pygame.sprite.Group()
wall = pygame.sprite.Group()
text = Text()
enemy_bullets = pygame.sprite.Group()
lsquareg=pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
space = []
buffs_chosen=[]
cols,rows=(7,7)
arr = [["o" for i in range(cols)] for j in range(rows)]
arr[round(cols/2)-1][round(rows/2)-1]="s"
current_space=[3,3]
map=Map(arr,current_space)
room_options=["e","s"]



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

array_class_buffs=[
    [
        ["player.bullet_counter+=1","increase bullet count by 1"],
        ["player.fire_rate=round(player.fire_rate/3*2)","decrease fire rate by a third"],
        ["player.bullet_speed+=2","increase bullet speed"],
        ["player.knockback+=1","increase knockback"],
        ["player.damage+=1","increase damage"]
    ],
    [
        ["player.arrow_speed+=2","increase arrow speed"],
        ["player.damage+=2","increase arrow damage"],
        ["player.knockback+=1","increase arrow knockback"],
        ["player.charge_time=round(player.charge_time/4*3)","decrease charge time by 25%"]
    ],
    [
        ["player.damage+=2","increase swing damage"],
        ["player.knockback+=1","increase knockback"],
        ["player.sword_length+=10","increase sword length"],
        ["player.swing_distance+=0.1","increase swing distance"],
        ["player.swing_timer_max=player.swing_timer_max/7*6","increase swing speed"]

    ]
]

array_of_buffs=[
    ["player.hp_bar.current_hp+=round(player.hp_bar.hp_max/5)","player restores 20%"+ "of hp"],
    ["player.hp_bar.current_hp+=round(player.hp_bar.hp_max*2/5)","player restores 40%"+ "of hp"],
    ["player.hp_bar.hp_max+=30","increase max hp for 30"],
    ["player.hp_bar.hp_max+=50","increase max hp for 50"],
    ["player.invincibility_time+=750","after being hit gain 0.75 of additional invincibility"],
    ["player.dash_reactivation_cd=round(player.dash_reactivation_cd/2)","half the cooldown of dashing"],
    ["player.kill_heal+=3","after killing an enemy heal for 3 hp (stacks)"]

                ]

def make_array(rooms,arr):
    for i in range(rooms):
        around=[(0,1),(0,-1),(1,0),(-1,0)]
        while True:    
            room_count=0
            for i in arr:
                for j in i:
                    if j=="s":
                        room_count+=1
            count=random.randint(1,room_count)
            x,y=0,0
            stored_num=[x,y]
            for i in arr:
                y+=1
                for j in i:
                    x+=1
                    if j=="s":
                        count-=1
                    if count==0 and j=="s":
                        stored_num=[x-1,y-1]
                x=0
            count=0
            for i in around:
                try:
                    if arr[stored_num[1]+i[1]][stored_num[0]+i[0]]=="s":
                        count+=1
                except:
                    pass
            if count<3:
                try:
                    adj=[(0,1),(0,-1),(1,0),(-1,0)]
                    ran_d=adj[random.randint(0,3)]
                    arr[stored_num[1]+ran_d[0]][stored_num[0]+ran_d[1]]="s"
                    break
                except:
                    pass
    return arr
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

def terminal():
    screenchange(display)
    terminal=Terminal()
    terminal.run(display)
    screenchange(display)
    choice1=get_random_buff()
    choice2=get_random_buff()
    choice3=get_random_buff()
    return "buff_choose"

def buff_choose(buffs_chosen):
    choice1=buffs_chosen[0] 
    choice2=buffs_chosen[1] 
    choice3=buffs_chosen[2] 
    text.render(display, "press 1 for: "+choice1[1], screen_width/
                2, screen_height/2-50, 20, (255, 255, 255))
    text.render(display, "press 2 for: "+choice2[1], screen_width/
                2, screen_height/2, 20, (255, 255, 255))
    text.render(display, "press 3 for:  "+choice3[1], screen_width/
                2, screen_height/2+50, 20, (255, 255, 255))
    if button_press == pygame.K_1:
        exec(choice1[0])
        return "finished"
    if button_press == pygame.K_2:
        exec(choice2[0])
        return "finished" 
    if button_press == pygame.K_3:
        exec(choice3[0])
        return "finished"


def get_random_buff():
    type=random.randint(0,1)
    if type==0:
        return array_of_buffs[random.randint(0,len(array_of_buffs)-1)]
    elif type==1:
        if player.player_class=="gunner":
            pclass=0
        elif player.player_class=="archer":
            pclass=1
        elif player.player_class=="knight":
            pclass=2
        return array_class_buffs[pclass][random.randint(0,len(array_class_buffs[pclass])-1)]
    
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
                if x.check_death():
                    player.hp_bar.current_hp+=player.kill_heal
                    if x.hacked==True:
                        return terminal()
    if player.player_class=="knight":
        for x in enemy_group:
            for y in player.marker_group:
                if x.check_hit_collision(y.rect1) or x.check_hit_collision(y.rect2) or x.check_hit_collision(y.rect3) or x.check_hit_collision(y.rect4):
                    x.apply_knockback(player.knockback,y.pointer)
                    x.hp_bar.update_hp(-player.damage)
                if x.check_death():
                    player.hp_bar.current_hp+=player.kill_heal
                    if x.hacked==True:
                        return terminal()
    for i in enemy_group:
        i.update(player, current_time, space)
        i.draw_to_surface(draw_surface)
        if player.check_death(i.rect, current_time):
            return "dead"
        for x in i.particle_group:
            draw_surface.blit(x.image,(i.rect.x+x.off_set[0],i.rect.y+x.off_set[1]))
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
    display.blit(draw_surface, (-player.rect.x +
                 (screen_width/4), -player.rect.y+(screen_height/4)))
    display.blit(player.hp_bar.image,((15),(15)))
    text.render(display, (str(player.hp_bar.current_hp)+"/"+str(player.hp_bar.hp_max)),
                150,30, 30, (30, 30, 30))
    text.render(display, ("score:"+str(player.score)),
                screen_width/12*11.2,15, 30, (30, 30, 30))
    if len(enemy_group.sprites())==0:
        return "next level"


def menu(player):
    text.render(display, "press 1 to play as gunner", screen_width/
                2, screen_height/2, 20, (255, 255, 255))
    text.render(display, "press 2 to play as archer", screen_width/
                2, screen_height/2+50, 20, (255, 255, 255))
    text.render(display, "press 3 to play as knight", screen_width/
                2, screen_height/2+100, 20, (255, 255, 255))
    if button_press == pygame.K_1:
        game_loop()
        return "gunner"
    if button_press== pygame.K_2:
        game_loop()
        return "archer"
    if button_press== pygame.K_3:
        game_loop()
        return "knight"

def wait_level(button_press,current_space,arr):
    draw_surface.fill((160, 160, 160))
    player.update(space, current_time, draw_surface)
    bullet_group.update(screen_height, screen_width, space)
    enemy_bullets.update(space)
    lsquareg.draw(draw_surface)
    draw_to_surface()
    display.blit(draw_surface, (-player.rect.x +
                 (screen_width/4), -player.rect.y+(screen_height/4)))
    display.blit(player.hp_bar.image,((15),(15)))
    text.render(display, (str(player.hp_bar.current_hp)+"/"+str(player.hp_bar.hp_max)),
                screen_width/10,40, 30, (30, 30, 30))
    text.render(display, ("score:"+str(player.score)),
                screen_width/12*11,screen_height/20, 30, (30, 30, 30))
    map.draw_grid(display)
    for lsquare in lsquareg:

        if lsquare.player_in(player,display,button_press):
            current_space[0]+=lsquare.direction[1]
            current_space[1]+=lsquare.direction[0]
            temp_arr=arr
            temp_arr[current_space[0]][current_space[1]]="c"
            #print(f"""{temp_arr[current_space[0]+1][current_space[1]]}\n
          #{arr[current_space[0]-1][current_space[1]]}\n
          #{arr[current_space[0]][current_space[1]+1]}\n
          #{arr[current_space[0]][current_space[1]-1]}""")
            #for i in temp_arr: 
            #    print (i)
            #print("///////")
            for i in lsquareg:
                i.kill()
            map.update(arr,current_space)
            return "next level"
            
        
def next_level(ctime,arr,current_space):
    player.rect.center=(935,810)
    player.bullet_counter=6
    player.score+=1

    enemy_group.empty()
    enemy_bullets.empty()
    bullet_group.empty()
    if arr[current_space[1]][current_space[0]]=="s":
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
arr=make_array(15,arr)
for i in arr:
    print(i)
print("///////")
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
                        screen_height/2, screen_width/2))
            if player.player_class=="archer":
                if player.charging==False:
                    player.charging=True
            if player.player_class=="knight":
                mouse_pos=pygame.mouse.get_pos()
                mouse_pos=(mouse_pos[0]*2,mouse_pos[1]*2)
                player.update_marker(mouse_pos,screen_width/2,screen_height/2)
        if event.type==pygame.MOUSEBUTTONUP:
            if player.player_class=="archer":
                if player.charging==True:
                    bullet_group.add(player.create_arrow(screen_height/2,screen_width/2))
                    
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
            if arr[current_space[1]+1%7][current_space[0]%7] in room_options:
                level_square= Level_square(0,100,[1,0])
                lsquareg.add(level_square)
            if arr[current_space[1]-1%7][current_space[0]%7] in room_options:
                level_square= Level_square(0,-100,[-1,0])
                lsquareg.add(level_square)
            if arr[current_space[1]%7][current_space[0]+1%7] in room_options:
                level_square= Level_square(100,0,[0,1])
                lsquareg.add(level_square)
            if arr[current_space[1]%7][current_space[0]-1%7] in room_options:
                level_square= Level_square(-100,0,[0,-1])
                lsquareg.add(level_square)
            for i in arr:
                print(i)
        if game_loop_return== "buff_choose":
            state=State.buff_choose
            buffs_chosen=[get_random_buff(),get_random_buff(),get_random_buff()]
    elif state== State.buff_choose:
        if buff_choose(buffs_chosen)=="finished":
            state=State.game
    elif state== State.new_load:
        load_new(current_time)
        state=State.game
    elif state==State.wait_level:
        wait=wait_status=wait_level(button_press,current_space,arr)
        button_press=""
        if wait=="next level":
            state=State.next_level
    elif state==State.next_level:
        next_level(current_time,arr,current_space)
        arr[current_space[1]][current_space[0]]="e"
        state=State.game
    pygame.display.update()
    clock.tick(60)
