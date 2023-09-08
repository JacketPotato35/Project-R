import pygame
import random
from shape import Shape


class BaseEnemy(pygame.sprite.Sprite):
    # have methods here that each enemy would have
    # for example, drawing health, setting health, etc.
    def __init__(self, x, y,ctime):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill((70, 70, 70))
        self.rect = self.image.get_rect(center=(x, y))
        self.hp_bar = self.HP(11,30)
        self.direction = pygame.Vector2(0, 0)
        self.position = pygame.Vector2(x, y)
        self.is_hit_timer=0
        self.knockback=pygame.Vector2(0,0)
        if random.randint(4,5)==4:
            self.hacked=True
        else:
            self.hacked=False
        self.particle_group=pygame.sprite.Group()
        self.random_particle_add=random.randint(1,10)

    class HP(pygame.sprite.Sprite):
        def __init__(self, hp_amount, hp_bar_size):
            super().__init__()
            self.image=pygame.Surface((hp_bar_size,5))
            self.image.fill((0,255,0))
            self.hp_max=hp_amount
            self.hp=hp_amount
            self.hp_bar_size=hp_bar_size
        def update_hp(self,hp_change):
            self.hp=self.hp+hp_change
            if self.hp<=0:
                return
            self.image=pygame.Surface((round(self.hp/self.hp_max*self.hp_bar_size),5))
            self.image.fill((0,255,0))


    def draw_to_surface(self,draw_surface):
        draw_surface.blit(self.image,(self.rect.x,self.rect.y))
        draw_surface.blit(self.hp_bar.image,(self.rect.x,self.rect.y))
    

    def check_bullet_collision(self, bullet_xy):
        if self.is_hit_timer>0:
            return False
        if bullet_xy.rect[0] > self.rect.left and bullet_xy.rect[0] < self.rect.right and bullet_xy.rect[1] > self.rect.top and bullet_xy.rect[1] < self.rect.bottom:
            self.is_hit_timer=10
            return True
        
    def check_hit_collision(self,rect):
        if self.is_hit_timer>0:
            return False
        corners=[rect.topleft , rect.topright, rect.bottomleft, rect.bottomright]
        for corner in corners:
            if corner[0] > self.rect.left and corner[0] < self.rect.right and corner[1] > self.rect.top and corner[1] < self.rect.bottom:
                self.is_hit_timer=13
                return True
        
    def check_death(self):
        if self.hp_bar.hp<=0:
            self.kill()
            return "dead"
    
    def apply_knockback(self, knockback,bullet_direction):
            self.knockback=bullet_direction*knockback

    class Hacked_effect(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((random.randint(20,30), random.randint(1,3)))
            self.image.fill((255, 255, 255))
            self.time_to_live=random.randint(1,10)
            self.off_set=[random.randint(-10,10),random.randint(-2,32)]
        def update(self):
            self.time_to_live-=1
            if self.time_to_live<=0:
                self.kill()

    
class Enemy(BaseEnemy):
    def __init__(self,x,y,ctime):
        super().__init__(x,y,ctime)
        self.image.fill((155, 60, 30))
        self.time = ctime-500
        self.randtime=0
    def update(self, player_pos, ctime, space):
            self.particle_group.update()
            if self.hacked==True:
                if self.random_particle_add<=0:
                    for i in range(random.randint(0,3)):
                        self.particle_group.add(self.Hacked_effect())
                self.random_particle_add-=1
            
            if self.is_hit_timer>0:
                self.is_hit_timer-=1
                velocity=self.knockback
            else: 
                ppos = player_pos.rect
                x_dis = ppos[0]-self.rect.x
                y_dis = ppos[1]-self.rect.y
                vect = pygame.Vector2(x_dis, y_dis)
                velocity = pygame.Vector2(0, 0)
                if vect.length() < 250 and self.time+3000 < ctime:
                    self.direction = vect.normalize()
                    self.time = ctime
                elif vect.length() > 250:
                    self.direction = vect.normalize()
                    velocity = self.direction
                if self.time+1 > ctime:
                    self.randtime = random.randint(-100, 300)
                if self.time+600+self.randtime > ctime:
                    velocity = self.direction*(7+random.randint(-3, 5))

            counter=0
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
                self.position += velocity*earliest
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
            self.position += velocity
            self.rect.center = self.position
    