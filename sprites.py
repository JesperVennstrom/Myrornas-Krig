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

        self.image = pygame.Surface([self.width, self.hight])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.x_change = 0

    def update(self):
        if self.game.red_turn:
            self.movment()
            self.bazooka()
        self.damage()
        self.x_change += self.push_vel
        self.rect.x += self.x_change
        self.collideX(self.x_facing)
        self.jump()
        self.collideY("up")
        self.gravity()
        self.offMap()

        self.healthbar()
        
        self.x_change = 0


    def damage(self):
        hits = pygame.sprite.spritecollide(self, self.game.explosion, False)
        self.push_vel = self.push_vel * 0.95
        if hits:
            self.health -= 0.01
            self.push_vel = 0
            self.vel_up = 10
            self.exp_direction = hits[0].rect.centerx - self.rect.centerx
            print(self.exp_direction)
            if self.exp_direction > 0:
                self.push_vel = -10
                self.x_facing = "left"
            elif self.exp_direction < 0:
                self.push_vel = 10
                self.x_facing = "right"

        self.death()

    def death(self):
        if self.health <= 0:
            self.kill()

    def healthbar(self):
        health_bar = pygame.Surface([self.width, 5])
        health = pygame.Surface([self.width * self.health, 5])
        health_bar.fill(RED)
        health.fill(GREEN)
        self.image.blit(health_bar, (0,0))
        self.image.blit(health, (0,0))

    def offMap(self):
        if self.rect.x > WIN_WIDTH - TILESIZE:
            self.rect.x = WIN_WIDTH - TILESIZE
        elif self.rect.x < 0:
            self.rect.x = 0
        if self.rect.y > WIN_HEIGHT:
            self.kill()
        elif self.rect.y < 0:
            self.rect.y = 0



    def movment(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x_facing = "left"
            self.x_change = -VEL

        if keys[pygame.K_RIGHT]:
            self.x_facing = "right"
            self.x_change = VEL

        if keys[pygame.K_UP] and self.vel_up < 0.1:
            self.vel_up = 20
        
    
    def gravity(self):
        self.rect.y += GRAVITY
        self.collideY("down")

    def collideX(self, direction):
        hits = pygame.sprite.spritecollide(self, self.game.world, False)
        if hits and direction == "right":
            while hits:
                self.rect.x = hits[0].rect.x - self.width
                hits = pygame.sprite.spritecollide(self, self.game.world, False)
        elif hits and direction == "left":
            while hits:
                self.rect.x = hits[0].rect.x + hits[0].width
                hits = pygame.sprite.spritecollide(self, self.game.world, False)
            
    def collideY(self, direction):
        hits = pygame.sprite.spritecollide(self, self.game.world, False)
        if hits and direction == "down":
            self.rect.y = hits[0].rect.y - self.hight
            self.vel_up = 0
            self.has_hit = True
        if hits and direction == "up": 
            while hits:
                self.rect.y = hits[0].rect.y + hits[0].hight
                hits = pygame.sprite.spritecollide(self, self.game.world, False)

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

        self.x_change = 0

    def update(self):
        if self.game.blue_turn:
            self.movment()
            self.bazooka()
        self.rect.x += self.x_change
        self.collideX(self.x_facing)
        self.jump()
        self.collideY("up")
        self.gravity()
        self.offMap()

        self.damage()
        self.healthbar()


    def healthbar(self):
        health_bar = pygame.Surface([self.width, 5])
        health = pygame.Surface([self.width * self.health, 5])
        health_bar.fill(RED)
        health.fill(GREEN)
        self.image.blit(health_bar, (0,0))
        self.image.blit(health, (0,0))

    def offMap(self):
        if self.rect.x > WIN_WIDTH - TILESIZE:
            self.rect.x = WIN_WIDTH - TILESIZE
        elif self.rect.x < 0:
            self.rect.x = 0
        if self.rect.y > WIN_HEIGHT:
            self.kill()
        elif self.rect.y < 0:
            self.rect.y = 0

    def damage(self):
        hits = pygame.sprite.spritecollide(self, self.game.explosion, False)
        if hits:
            self.health -= 0.01
            self.push_vel = 10
            self.vel_up = 10
            self.exp_direction = hits[0].rect.centerx - self.rect.centerx
            if self.exp_direction > 0:
                self.x_facing = "left"
                self.x_change = -VEL
            elif self.exp_direction < 0:
                self.x_facing = "right"
                self.x_change = VEL

        self.death()

        self.x_change = 0
    
    
    def death(self):
        if self.health <= 0:
            self.kill()


    def movment(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x_facing = "left"
            self.x_change = -VEL

        if keys[pygame.K_RIGHT]:
            self.x_facing = "right"
            self.x_change = VEL

        if keys[pygame.K_UP] and self.vel_up < 0.1:
            self.vel_up = 20
        
    
    def gravity(self):
        self.rect.y += GRAVITY
        self.collideY("down")

    def collideX(self, direction):
        hits = pygame.sprite.spritecollide(self, self.game.world, False)
        if hits and direction == "right":
            self.rect.x = hits[0].rect.x - self.width
        elif hits and direction == "left":
            self.rect.x = hits[0].rect.x + hits[0].width
            
    def collideY(self, direction):
        hits = pygame.sprite.spritecollide(self, self.game.world, False)
        if hits and direction == "down":
            self.rect.y = hits[0].rect.y - self.hight
            self.vel_up = 0
            self.has_hit = True
        if hits and direction == "up": 
            while hits:
                self.rect.y = hits[0].rect.y + hits[0].hight
                hits = pygame.sprite.spritecollide(self, self.game.world, False)

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
        self.offMap()

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

    def offMap(self):
        if self.rect.x > WIN_WIDTH or self.rect.x < 0 or self.rect.y > WIN_HEIGHT or self.rect.y < 0:
            self.kill()

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
