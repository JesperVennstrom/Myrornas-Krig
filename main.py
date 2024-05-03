import pygame
from config import *
from sprites import *
import sys

class Game: 
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Blancos Vs Negro")
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.running = True
        self.start_time = pygame.time.get_ticks()  # Record the start time
        self.total_time = 10000  # Total time in milliseconds (10 seconds)

    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.black = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates() #kanske inte behövs om vi har pvp
        self.attacks = pygame.sprite.LayeredUpdates()
        self.player = Player(self, 1, 2)
        self.world = pygame.sprite.LayeredUpdates()

        self.generateTilemap()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False
    
    def generateTilemap(self):
        for i, row in enumerate(TILEMAP):
            for j, column in enumerate(row):
                if column == 0:
                    World(self, j, i)

    def draw_time(self, time_left_seconds):
        pygame.draw.rect(self.screen, GREEN, pygame.Rect(30 + (11*time_left_seconds), 30, 10, 20))

    def start_timer(self):
        keys = pygame.key.get_pressed()
        self.time_left_seconds = None
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(30, 30, 110, 20))

        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP]:
            time_left = self.total_time - (pygame.time.get_ticks() - self.start_time)  # Calculate time left
            time_left = max(0, time_left)  # Ensure time doesn't go below 0
            self.time_left_seconds = time_left // 1000  # Convert milliseconds to seconds
        if self.time_left_seconds:
            self.draw_time(self.time_left_seconds)

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        self.start_timer()
        pygame.display.update()

    def update(self):
        self.all_sprites.update()

    def endScreen(self):
        pass

    def introScreen(self):
        pass

g = Game()
g.introScreen()
g.new()
while g.running:
    g.main()
    g.endScreen()

pygame.quit()
sys.exit()
