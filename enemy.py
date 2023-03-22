import pygame
import random 
from shape import Shape
class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.Surface((30,30))
        self.image.fill((155,60,30))
        self.rect=self.image.get_rect(center=(x,y))
        self.time=0
        self.direction=pygame.Vector2(0,0)
        self.position=pygame.Vector2(x,y)
        self.randtime=0

    def update(self,player_pos,ctime ,space):
        counter=0
        ppos=player_pos.rect
        x_dis=ppos[0]-self.rect.x
        y_dis=ppos[1]-self.rect.y
        vect=pygame.Vector2(x_dis,y_dis)
        velocity=pygame.Vector2(0,0)
        if vect.length()<250 and self.time+3000<ctime:
            self.direction=vect.normalize()
            self.time=ctime
        elif vect.length()>250:
            self.direction=vect.normalize()
            velocity=self.direction
        if self.time+1>ctime:
            self.randtime=random.randint(-100,300)
        if self.time+600+self.randtime>ctime:
            velocity=self.direction*(7+random.randint(-3,5))

        #while velocity isnt 0/negligible for a frame
        while velocity.magnitude_squared() > 1 and counter <= 5:
            #range of object which the square can physically interact/collide with 
            broad=Shape(
                self.rect.left+min(velocity.x, 0),
                self.rect.right+max(velocity.x, 0),
                self.rect.top+min(velocity.y, 0),
                self.rect.bottom+max(velocity.y, 0),
            )

            nx, ny = 0, 0
            #variable showing for when the earlient colision time is as a percentage of a 100% travel
            earliest = 1.0
            for other in space:
                if broad.collides_with(other):
                    timex = Shape.collision_time(self.rect.left, self.rect.right, velocity.x, other.left, other.right)
                    timey = Shape.collision_time(self.rect.top, self.rect.bottom, velocity.y, other.top, other.bottom)
                    min_time = min(timex, timey)
                    #checks for all colisions within the broad, checks for which collision happens first 
                    if min_time < earliest:
                        earliest = min_time
                        #either a right colision happens first or a left colision, one or the other
                        if timex < timey:
                            nx = velocity.x / abs(velocity.x)
                            ny = 0
                        elif timey < timex:
                            nx = 0
                            ny = velocity.y / abs(velocity.y)        

            #moves the player by the velocity plus earliest (which is a percentage of which it can move without passing wall)
            self.position+=velocity*earliest
            #slip and slide, look into this more in the future 
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
        self.position+=velocity
        self.rect.center=self.position
            
    def check_death(self, bullet_xy):
        if bullet_xy.rect[0]>self.rect.left and bullet_xy.rect[0]<self.rect.right and bullet_xy.rect[1]>self.rect.top and bullet_xy.rect[1]<self.rect.bottom:
            self.kill()
            return True