import pygame
from bullet import Bullet
from shape import Shape
from text import Text


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(935, 810))
        self.bullet_xy = self.rect.center
        self.dash_cd = 0
        self.dash_time = 0
        self.bullet_time = -300
        self.lives = 3
        self.livecd = -1000
        self.blink_duration = 0
        self.blink_time = -100
        self.blink_state = True
        self.bullet_counter = 6
        self.reloading = False
        self.reload_time = -0
        self.score=0
    # returns vector direction

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
            self.dash_cd += 1500
        if self.dash_time > 0:
            velocity = self.dash_direction*9+velocity*1
            self.dash_time -= 1
            return velocity
        return velocity

    def check_death(self, enemy_rect: pygame.Rect, current_time):
        if self.rect.right > enemy_rect.centerx > self.rect.left and self.rect.bottom > enemy_rect.centery > self.rect.top and self.livecd+500 < current_time:
            self.lives -= 1
            self.livecd = current_time
            self.blink_duration += 50
        if self.lives <= 0:
            return True

    def update(self, space, current_time):

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

    def create_bullet(self, screen_height, screen_width):
        return (Bullet(self.bullet_xy[0], self.bullet_xy[1], screen_height, screen_width, self.bullet_xy))

    def bullet_timer(self, ctime):

        if self.bullet_counter > 0:
            if self.bullet_time+700 < ctime:
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
                self.bullet_counter += 6
        text = Text()
        if self.reloading == True:
            text.render(display, "reloading", screen_width/2, screen_height/2+40, 20, (45, 50, 30))
        elif self.reloading == False:
            text.render(display, ("bullets: "+str(self.bullet_counter)),
                        screen_width/2, screen_height/2+40, 20, (45, 50, 30))
