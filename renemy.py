import pygame
import random
from shape import Shape
from enemy_bullet import Enemy_bullet
from enemy import BaseEnemy

class Renemy(BaseEnemy):
    def __init__(self,x,y,ctime):
        super().__init__(x,y,ctime)
        self.image.fill((30, 60, 155))
        self.randx = random.randint(-1, 1)
        self.randy = random.randint(-1, 0)
        self.time_move = 0
        self.bullet_time = ctime+400+random.randint(0,2800)

    def update(self, player, ctime, space):
        self.particle_group.update()
        if self.invincibility_timer>0:
            self.invincibility_timer-=1
        if self.hacked==True:
                if self.random_particle_add<=0:
                    for i in range(random.randint(0,3)):
                        self.particle_group.add(self.Hacked_effect())
                self.random_particle_add-=1
        if self.is_hit_timer>0:
            self.is_hit_timer-=1
            velocity=self.knockback
        else:
            self.hp_bar.update(self.rect.centerx,self.rect.centery)
            velocity = pygame.Vector2(0, 0)
            
            if self.time_move+1500 < ctime:
                self.time_move = ctime
                self.direction = self.pdirection(player)
            if self.time_move+750 > ctime:
                velocity = self.direction*3
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
        self.hp_bar.center=((self.rect.centerx,self.rect.centery+25))
        

    def pdirection(self, player):
        sx = self.rect.centerx
        sy = self.rect.centery
        px = player.rect.centerx
        py = player.rect.centery
        if sx <= px and sy <= py:
            return pygame.Vector2(random.randint(0, 1), random.randint(0, 1))
        elif sx >= px and sy <= py:
            return pygame.Vector2(random.randint(-1, 0), random.randint(0, 1))
        elif sx <= px and sy >= py:
            return pygame.Vector2(random.randint(0, 1), random.randint(-1, 0))
        elif sx >= px and sy >= py:
            return pygame.Vector2(random.randint(-1, 0), random.randint(-1, 0))
        
    def enemyb_timer(self, ctime):
        if self.bullet_time+2800 < ctime:
            self.bullet_time = ctime
            return True

    def create_ebullet(self, player):
        ppos = player.rect
        x_dis = ppos[0]-self.rect.x
        y_dis = ppos[1]-self.rect.y
        pointer = pygame.Vector2(x_dis, y_dis)
        pointer = pointer.normalize()
        return (Enemy_bullet(self.rect.centerx, self.rect.centery, pointer))
        

