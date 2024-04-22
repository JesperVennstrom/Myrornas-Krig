import pygame
from config import *
import math
import random

class Player(pygame.sprite.Sprite):
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
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
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
        if not pygame.sprite.spritecollide(self, self.game.world, False):
            self.rect.y += GRAVITY
        else:
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

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.hight = TILESIZE

        self.image = pygame.Surface([self.width, self.hight])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Time(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = WORLD_LAYER
        self.groups = self.game.all_sprites, self.game.world
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.hight = TILESIZE

        self.image = pygame.Surface([self.width, self.hight])
        self.image.fill(GRAY)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y