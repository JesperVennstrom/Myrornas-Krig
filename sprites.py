import pygame
from config import *
import math
import random

class BlackPlayer(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.hight = TILESIZE
        self.vel_up = 0

        self.health = 1
        self.exp_direction = 0
        self.push_vel = 0

        self.first_click = True

        self.x_facing = None
        self.y_facing = "down"
        self.has_hit = False

        self.image = pygame.Surface([self.width, self.hight])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        if self.game.red_turn:
            self.movment()
            self.jump()
            self.bazooka()
        self.collide()
        self.gravity()

        self.damage()

    def damage(self):
        hits = pygame.sprite.spritecollide(self, self.game.explosion, False)
        if hits:
            self.health -= 0.01
            self.push_vel = 10
            self.exp_direction = hits[0].rect.centerx - self.rect.centerx
            if self.exp_direction > 0:
                self.exp_direction = -1
            elif self.exp_direction < 0:
                self.exp_direction = 1

        self.push(self.exp_direction)
        self.death()
    
    def push(self, direction):
        if self.push_vel > 0.1:
            self.rect.y -= self.push_vel
            self.rect.x += self.push_vel * direction
            self.push_vel = self.push_vel * 0.95

    def death(self):
        if self.health <= 0:
            self.kill()


    def movment(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.vel_up < 0.1:
            self.x_facing = "left"

        if keys[pygame.K_RIGHT] and self.vel_up < 0.1:
            self.x_facing = "right"

        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and self.vel_up < 0.1:
            self.x_facing = None

        if keys[pygame.K_UP] and self.vel_up < 0.1:
            self.vel_up = 20
        
        if self.x_facing == "left":
            self.rect.x -= VEL
        if self.x_facing == "right":
            self.rect.x += VEL
        
    
    def gravity(self):
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, self.game.world, False)
        if not hits:
            self.rect.y += GRAVITY
            self.y_facing = "down"
        self.rect.y -= 1
            
    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.world, False)
        if hits and self.y_facing == "down" and self.x_facing == None: 
            self.rect.y = hits[0].rect.y - self.hight
            self.vel_up = 0	
            self.has_hit = True
        elif not hits and self.y_facing == "down" and self.has_hit:
            self.y_facing = None
            self.has_hit = False

        if hits and self.x_facing == "right" and not self.y_facing == "down":
            self.rect.x = hits[0].rect.x - self.width
        elif hits and self.x_facing == "left" and not self.y_facing == "down":
            self.rect.x = hits[0].rect.x + hits[0].width

        if hits and self.x_facing == "right" and self.y_facing == "down":
            self.rect.x = hits[0].rect.x - self.width
            self.x_facing = None
        elif hits and self.x_facing == "left" and self.y_facing == "down":
            self.rect.x = hits[0].rect.x + hits[0].width
            self.x_facing = None
    def jump(self):
        if self.vel_up > 0.1:
            self.rect.y -= self.vel_up
            self.vel_up = self.vel_up * 0.95
    
    def bazooka(self):
        pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if pressed[0] and self.first_click:
            self.first_click = False
        elif pressed[0] and not self.first_click:
            mouse_end = mouse_pos
            self.shoot_angle = math.degrees(math.atan2(mouse_end[1]-self.rect.y, mouse_end[0]-self.rect.x))
        
        if not pressed[0] and not self.first_click:
            self.first_click = True
            if self.shoot_angle:
                Rocket(self.game, self.rect.x, self.rect.y, self.shoot_angle)


class WhitePlayer(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.hight = TILESIZE
        self.vel_up = 0

        self.health = 1

        self.exp_direction = 0
        self.push_vel = 0

        self.first_click = True

        self.x_facing = None
        self.y_facing = "down"
        self.has_hit = False

        self.image = pygame.Surface([self.width, self.hight])
        self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        if self.game.blue_turn:
            self.movment()
            self.jump()
            self.bazooka()
        self.collide()
        self.gravity()

        self.damage()

    def damage(self):
        hits = pygame.sprite.spritecollide(self, self.game.explosion, False)
        if hits:
            self.health -= 0.01
            self.push_vel = 10
            self.vel_up = 10
            self.exp_direction = hits[0].rect.centerx - self.rect.centerx
            if self.exp_direction > 0:
                self.exp_direction = -1
                self.x_facing = "left"
            elif self.exp_direction < 0:
                self.exp_direction = 1
                self.x_facing = "right"

        self.push(self.exp_direction)
        self.death()
    
    def push(self, direction):
        if self.push_vel > 0.1:
            self.rect.x += self.push_vel * direction
            self.push_vel = self.push_vel * 0.95
            self.y_facing = "down"
    
    def death(self):
        if self.health <= 0:
            self.kill()


    def movment(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.vel_up < 0.1:
            self.x_facing = "left"

        if keys[pygame.K_RIGHT] and self.vel_up < 0.1:
            self.x_facing = "right"

        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and self.vel_up < 0.1:
            self.x_facing = None

        if keys[pygame.K_UP] and self.vel_up < 0.1:
            self.vel_up = 20
        
        if self.x_facing == "left":
            self.rect.x -= VEL
        if self.x_facing == "right":
            self.rect.x += VEL
        
    
    def gravity(self):
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, self.game.world, False)
        if not hits:
            self.rect.y += GRAVITY
            self.y_facing = "down"
        self.rect.y -= 1
            
    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.world, False)
        if hits and self.y_facing == "down" and self.x_facing == None: 
            self.rect.y = hits[0].rect.y - self.hight
            self.vel_up = 0	
            self.has_hit = True
        elif not hits and self.y_facing == "down" and self.has_hit:
            self.y_facing = None
            self.has_hit = False

        if hits and self.x_facing == "right" and not self.y_facing == "down":
            self.rect.x = hits[0].rect.x - self.width
        elif hits and self.x_facing == "left" and not self.y_facing == "down":
            self.rect.x = hits[0].rect.x + hits[0].width

        if hits and self.x_facing == "right" and self.y_facing == "down":
            self.rect.x = hits[0].rect.x - self.width
            self.x_facing = None
        elif hits and self.x_facing == "left" and self.y_facing == "down":
            self.rect.x = hits[0].rect.x + hits[0].width
            self.x_facing = None
    def jump(self):
        if self.vel_up > 0.1:
            self.rect.y -= self.vel_up
            self.vel_up = self.vel_up * 0.95
    
    def bazooka(self):
        pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if pressed[0] and self.first_click:
            self.first_click = False
        elif pressed[0] and not self.first_click:
            mouse_end = mouse_pos
            self.shoot_angle = math.degrees(math.atan2(mouse_end[1]-self.rect.y, mouse_end[0]-self.rect.x))
        
        if not pressed[0] and not self.first_click:
            self.first_click = True
            if self.shoot_angle:
                Rocket(self.game, self.rect.x, self.rect.y, self.shoot_angle)
class World(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = WORLD_LAYER
        self.groups = self.game.all_sprites, self.game.world
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * 10
        self.y = y * 10
        self.width = 10
        self.hight = 10

        self.image = pygame.Surface([self.width, self.hight])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Rocket(pygame.sprite.Sprite):
    def __init__(self, game, x, y, angle):
        self.game = game
        self._layer = BULLET_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = 5
        self.hight = 5
        self.vel_x = 10
        self.vel_y = 5
        self.angle = angle

        self.gravity = 0.1

        self.image = pygame.Surface([self.width, self.hight])
        self.image.fill(GREEN)

        self.rect = pygame.draw.circle(self.image, GREEN, (self.width // 2, self.hight // 2), self.width // 2)
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.collide()

    def movement(self):
        self.rect.x += self.vel_x * math.cos(math.radians(self.angle))
        self.rect.y += (self.vel_x + GRAVITY) * math.sin(math.radians(self.angle))

        self.rect.y += self.gravity
        self.gravity = self.gravity + 0.45
    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.world, False)
        if hits:
            self.kill()
            Explosion(self.game, self.rect.x-TILESIZE//2, self.rect.centery-TILESIZE//2)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BULLET_LAYER
        self.groups = self.game.all_sprites, self.game.explosion
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = 50
        self.hight = 50

        self.image = pygame.Surface([self.width, self.hight], pygame.SRCALPHA)

        self.rect = pygame.draw.circle(self.image, ORANGE, (self.width // 2, self.hight // 2), self.width // 2)
        self.rect.x = self.x
        self.rect.y = self.y

        self.start_time = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.start_time > 1000:
            self.game.blue_turn = not self.game.blue_turn
            self.game.red_turn = not self.game.red_turn
            self.game.start_time = pygame.time.get_ticks()
            self.kill()
        self.collide()
    
    def collide(self):
        for sprite in self.game.world:
            if pygame.sprite.collide_circle(self, sprite):
                sprite.kill()
