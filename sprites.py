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
        self.collide()
        self.gravity()

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

        self.image = pygame.Surface([self.width, self.hight])
        self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        if self.game.blue_turn == 1:
            self.movment()
            self.jump()
        self.gravity()

    def movment(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= VEL

        if keys[pygame.K_RIGHT]:
            self.rect.x += VEL

        if keys[pygame.K_UP] and self.vel_up < 0.1:
            self.vel_up = 20
    
    def gravity(self):
        hits = pygame.sprite.spritecollide(self, self.game.world, False)
        if not hits:
            self.rect.y += GRAVITY
        else:
            self.rect.y = hits[0].rect.y - self.hight + 1
            self.vel_up = 0
            


    def jump(self):
        if self.vel_up > 0.1:
            self.rect.y -= self.vel_up
            self.vel_up = self.vel_up * 0.95

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
