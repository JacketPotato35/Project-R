import pygame
from bullet import Bullet
from shape import Shape
from text import Text

class BasePlayer(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(935, 810))
        self.bullet_xy = self.rect.center
        self.dash_cd = 0
        self.dash_time = 0
        self.hp_bar=self.Hp_bar(100000)
        self.livecd = -1000
        self.blink_duration = 0
        self.blink_time = -100
        self.blink_state = True
        self.score=0
        self.player_class="base"
        self.invincibility_time=500
        self.dash_reactivation_cd=3000
        self.damage=5
        self.knockback=5
        self.kill_heal=0
    # returns vector direction
    class Hp_bar():
        def __init__(self,hp):
            self.hp_bar_size=400
            self.image = pygame.Surface((self.hp_bar_size, 25))
            self.image.fill((0, 255, 0))
            self.hp_max=hp
            self.current_hp=hp

        def update_hp(self,hp_change):
            self.current_hp=self.current_hp+hp_change
            if self.current_hp<=0:
                return
            self.image=pygame.Surface((round(self.current_hp/self.hp_max*self.hp_bar_size),25))
            self.image.fill((0,255,0))

    def get_direction(self) -> pygame.math.Vector2:
        direction = pygame.math.Vector2(0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            direction.y -= 1
        if keys[pygame.K_s]:
            direction.y += 1
        if keys[pygame.K_a]:
            direction.x -= 1
        if keys[pygame.K_d]:
            direction.x += 1
        return direction

    def blink(self, current_time):
        if self.blink_duration > 0:
            self.blink_duration -= 1
            if self.blink_time+100 < current_time:
                self.blink_time = current_time
                if self.blink_state == True:
                    self.image.fill((180, 160, 160))
                    self.blink_state = False
                elif self.blink_state == False:
                    self.image.fill((255, 255, 255))
                    self.blink_state = True
        else:
            if self.blink_state == False:
                self.image.fill((255, 255, 255))
                self.blink_state = True

    def dash(self, velocity, current_time):
        keys = pygame.key.get_pressed()
        self.dash_cd += 1
        if keys[pygame.K_SPACE] and self.dash_cd < current_time and velocity.magnitude_squared() != 0:
            self.dash_direction = self.get_direction()
            self.dash_time = 10
            self.dash_cd += self.dash_reactivation_cd
        if self.dash_time > 0:
            velocity = self.dash_direction*9+velocity*1
            self.dash_time -= 1
            return velocity
        return velocity

    def check_death(self, enemy_rect: pygame.Rect, current_time):
        if self.rect.right > enemy_rect.centerx > self.rect.left and self.rect.bottom > enemy_rect.centery > self.rect.top and self.livecd+self.invincibility_time < current_time:
            self.hp_bar.update_hp(-15)
            self.livecd = current_time
            self.blink_duration += 50
        if self.hp_bar.current_hp <= 0:
            return True

    def update(self, space, current_time, draw_surface):

        counter = 0
        velocity = self.dash(self.get_direction()*3, current_time)
        # while velocity isnt 0/negligible for a frame
        while velocity.magnitude_squared() > 1 and counter <= 5:
            # range of object which the square can physically interact/collide with
            broad = Shape(
                self.rect.left+min(velocity.x, 0),
                self.rect.right+max(velocity.x, 0),
                self.rect.top+min(velocity.y, 0),
                self.rect.bottom+max(velocity.y, 0),
            )

            nx, ny = 0, 0
            # variable showing for when the earlient colision time is as a percentage of a 100% travel
            earliest = 1.0
            for other in space:
                if broad.collides_with(other):
                    timex = Shape.collision_time(
                        self.rect.left, self.rect.right, velocity.x, other.left, other.right)
                    timey = Shape.collision_time(
                        self.rect.top, self.rect.bottom, velocity.y, other.top, other.bottom)
                    min_time = min(timex, timey)
                    # checks for all colisions within the broad, checks for which collision happens first
                    if min_time < earliest:
                        earliest = min_time
                        # either a right colision happens first or a left colision, one or the other
                        if timex < timey:
                            nx = velocity.x / abs(velocity.x)
                            ny = 0
                        elif timey < timex:
                            nx = 0
                            ny = velocity.y / abs(velocity.y)

            # moves the player by the velocity plus earliest (which is a percentage of which it can move without passing wall)
            self.rect.center += velocity*earliest
            self.bullet_xy = self.rect.center+velocity*earliest

            # slip and slide, look into this more in the future
            dot_product = (
                velocity.x * ny
                + velocity.y * nx
            ) * (1-earliest)

            # Determine new velocity
            velocity = pygame.math.Vector2(
                dot_product * ny,
                dot_product * nx
            )
            counter += 0

        self.blink(current_time)
        self.draw_to_surface(draw_surface)

    def draw_to_surface(self,draw_surface):
            draw_surface.blit(self.image,(self.rect.x,self.rect.y))


class Gunner(BasePlayer):

    def __init__(self):
        super().__init__()
        self.bullet_time = -300
        self.bullet_counter = 4
        self.reloading = False
        self.reload_time = -0
        self.player_class="gunner"
        self.knockback=3
        self.damage=5
        self.bullet_speed=6
        self.fire_rate=800
    def update(self, space, current_time, draw_surface):
        super().update(space, current_time, draw_surface)
        self.reload_text(draw_surface,current_time)

    def create_bullet(self, screen_height, screen_width):
        return (Bullet(self.bullet_xy[0], self.bullet_xy[1], screen_height, screen_width, self.bullet_xy,self.bullet_speed,self.knockback,self.damage))

    def bullet_timer(self, ctime):

        if self.bullet_counter > 0:
            if self.bullet_time+self.fire_rate < ctime:
                self.bullet_time = ctime
                self.bullet_counter -= 1
                return True
            else:
                return False

    def reload_text(self, display : pygame.display, ctime):
        screen_width, screen_height = display.get_size()
        if self.bullet_counter == 0:
            if self.reloading == False:
                self.reload_time = ctime
            self.reloading = True

        if self.reloading:
            if self.reload_time+2200 < ctime: 
                self.reloading = False
                self.bullet_counter = 6
        text = Text()
        if self.reloading == True:
            text.render(display, "reloading", self.rect.x+(screen_width/2), self.rect.y+100, 20, (45, 50, 30))
        elif self.reloading == False:
            text.render(display, ("bullets: "+str(self.bullet_counter)),
                        self.rect.x+(screen_width/2), self.rect.y+100, 20, (45, 50, 30))

    def reload(self,display,ctime):
        screen_width, screen_height = display.get_size()
        if self.reloading == False:
            self.reload_time = ctime
        self.reloading = True

        if self.reloading:
            if self.reload_time+2200 < ctime: 
                self.reloading = False
                self.bullet_counter = 6
        text = Text()
        if self.reloading == True:
            text.render(display, "reloading", self.rect.x+(screen_width/2), self.rect.y+100, 20, (45, 50, 30))
        elif self.reloading == False:
            text.render(display, ("bullets: "+str(self.bullet_counter)),
                        screen_width/2, screen_height/2+40, 20, (45, 50, 30)) 

class Empty_player(BasePlayer):
    def __init__(self):
        super().__init__()

class Knight(BasePlayer):
    def __init__(self):
        super().__init__()
        self.player_class="knight"
        self.marker_group=pygame.sprite.Group()
        self.swing=False
        self.swing_timer_max=64
        self.swing_timer=1
        self.swing_current_cooldown=self.swing_timer_max
        self.swing_cooldown=self.swing_timer_max
        self.knockback=10
        self.damage=100
        self.sword_length=20
        self.swing_distance=1.2
    def draw_marker(self,draw_surface,swing_timer,swing_timer_max):
        for x in self.marker_group:
            x.draw_2_surface(self.rect,draw_surface,swing_timer,swing_timer_max)

    def update_marker(self,mouse_pos,screen_width,screen_height):
        if self.swing_current_cooldown>self.swing_cooldown:
            self.swing=True
            self.marker_group.add(self.Marker(mouse_pos,screen_width,screen_height,self.sword_length,self.swing_distance))
            self.swing_current_cooldown=0

    def update(self, space, current_time,draw_surface):
        super().update( space, current_time,draw_surface)
        self.swing_current_cooldown+=1
        if self.swing==True and self.swing_timer<self.swing_timer_max:
            self.swing_timer+=1
        else:
            for x in self.marker_group:
                x.kill()
            self.swing=False
            self.swing_timer=1
        self.draw_marker(draw_surface,self.swing_timer,self.swing_timer_max)
        

    class Marker(pygame.sprite.Sprite):
        def __init__(self,mouse_pos,screen_width,screen_height,length,swing_dis):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((18, 18))
            self.image.fill((255, 0, 0))
            self.rect1 =self.image.get_rect(center=(0, 0))
            self.rect2 = self.image.get_rect(center=(0,0))
            self.rect3 = self.image.get_rect(center=(0,0))
            self.rect4 = self.image.get_rect(center=(0,0))
            self.mouse_pos=mouse_pos
            center_screen=pygame.Vector2(screen_width,screen_height)
            pointer=center_screen-mouse_pos
            self.pointer=pygame.math.Vector2.normalize(-pointer)
            self.screen_width=screen_width
            self.screen_height=screen_height
            self.sword_length=length
            self.swing_distance=swing_dis
        def draw_2_surface(self,player_rect, draw_surface,swing_timer,swing_timer_max):

            if self.pointer.x==0:
                self.pointer.x=0.1
            normal_gradient=(self.pointer[1]/self.pointer[0])
            if normal_gradient==0:
                normal_gradient=0.1
            if self.screen_height<=self.mouse_pos[1]:
                normal=pygame.Vector2(-1,(normal_gradient**-1))
            elif self.screen_height>self.mouse_pos[1]:
                normal=pygame.Vector2(1,-(normal_gradient**-1))
            right_pointer=pygame.math.Vector2.normalize(normal)
            left_pointer=pygame.math.Vector2.normalize(-normal)
            if swing_timer<swing_timer_max/2:
                pointer=pygame.math.Vector2.normalize(self.pointer+(right_pointer*self.swing_distance*(1-(swing_timer/(swing_timer_max/2)))))
            elif swing_timer<=swing_timer_max:
                pointer=pygame.math.Vector2.normalize(self.pointer+(left_pointer*self.swing_distance*((swing_timer-(swing_timer_max/2))/(swing_timer_max/2))))
            else:
                pointer=self.pointer
            self.draw_and_rect(draw_surface,player_rect,pointer,self.rect1,1)
            self.draw_and_rect(draw_surface,player_rect,pointer,self.rect2,2)
            self.draw_and_rect(draw_surface,player_rect,pointer,self.rect3,3)
            self.draw_and_rect(draw_surface,player_rect,pointer,self.rect4,4)
        
        def draw_and_rect(self,draw_surface,player_rect,pointer,rect,num):
            draw_surface.blit(self.image,(player_rect.x+pointer.x*self.sword_length*num,player_rect.y+pointer.y*self.sword_length*num))
            rect.center=(player_rect.x+pointer.x*self.sword_length*num,player_rect.y+pointer.y*self.sword_length*num)

class Archer(BasePlayer):
    def __init__(self):
        super().__init__()
        self.charging=False
        self.charging_time=0
        self.player_class="archer"
        self.charge_bar=self.ChargeBar(self.rect)
        self.damage=5
        self.knockback=5
        self.arrow_speed=0
        self.charge_time=120

    def update(self, space, current_time,draw_surface):
        super().update( space, current_time,draw_surface)
        if self.charging_time>self.charge_time:
            self.charging_time=self.charge_time
        self.charge_bar.update(self.rect,self.charging_time)
        self.charge_bar.draw_to_screen(draw_surface,self.rect,self.charging_time)
        if self.charging==True:
            self.charging_time+=1


    def create_arrow(self, screen_height, screen_width):
        self.charge_bar.update_charge_time(self.charge_time)
        if self.charging_time>self.charge_time:
            self.charging_time=self.charge_time
        bullet_ratio=round(((self.charging_time/self.charge_time)**2)*2,2)
        self.charging_time=0
        self.charging=False
        return (Bullet(self.bullet_xy[0], self.bullet_xy[1], screen_height, screen_width, self.bullet_xy,round(self.arrow_speed+3+4*bullet_ratio),round(self.knockback*bullet_ratio),round(self.damage*bullet_ratio)))


    class ChargeBar():
        def __init__(self,player_rect):
            self.image = pygame.Surface((5, 30))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(center=(player_rect.x, player_rect.y))
            self.charge_time=120
        def update_charge_time(self,charge_time):
            self.charge_time=charge_time
        def update(self,player_rect,charging_time):
            self.image=pygame.Surface((5,round(15*((charging_time/self.charge_time)**2)*2)))
            self.rect=self.image.get_rect(center=(player_rect.x,player_rect.y))
        def draw_to_screen(self,draw_surface,player_rect,charging_time):

            draw_surface.blit(self.image,(player_rect.x+player_rect.width+5,player_rect.y+player_rect.height-(round(15*((charging_time/self.charge_time)**2)*2))))

            