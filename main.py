import pygame
from config import *
from sprites import *
import sys
from PIL import Image

class Game: 
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Blancos Vs Negro")
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.toggle_fullscreen()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.running = True
        self.start_time = pygame.time.get_ticks()  # Record the start time
        self.total_time = 15000  # Total time in milliseconds (10 seconds)
        self.red_turn = True
        self.blue_turn = False

    def new(self):
        self.playing = True

        self.turn = 0

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.black = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates() #kanske inte behövs om vi har pvp
        self.attacks = pygame.sprite.LayeredUpdates()
        self.world = pygame.sprite.LayeredUpdates()
        self.explosion = pygame.sprite.LayeredUpdates()

        
        self.players = []
        self.players.append(BlackPlayer(self, 1, 20))
        self.players.append(WhitePlayer(self, 10, 20))
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

    def convertBitmap(self):
        # Open the image
        img = Image.open("img/map.ppm")
        
        # Convert the image to grayscale
        img = img.convert('L') # 'L' mode means grayscale
        
        # Get image dimensions
        height, width = img.size
        print(width, height)
        
        # Create an empty list to store the tilemap

        self.map = []
        
        # Iterate through the image and extract tiles
        for y in range(width):
            row = []
            for x in range(height):
                # Crop the tile from the image
                tile = img.crop((x, y, (x + 1), (y + 1)))
                # Convert the tile to a list of RGB values
                tile_colors = list(tile.getdata())
                # Append the tile colors to the row
                row.append(tile_colors)
            # Append the row to the tilemap
            self.map.append(row)    
        
    
    def generateTilemap(self):
        self.convertBitmap()
        i = 0
        j = 0
        while i < len(self.map):
            while j < len(self.map[i]):
                if self.map[i][j] == [0]:
                    World(self, j, i)
                j += 1
            i += 1
            j = 0


    def start_timer(self):
        keys = pygame.key.get_pressed()
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(30, 30, 155, 20))
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(415, 30, 155, 20))

        if self.red_turn:
            time_left = self.total_time - (pygame.time.get_ticks() - self.start_time)  # Calculate time left
            time_left = max(0, time_left)  # Ensure time doesn't go below 0
            time_left_seconds = time_left // 1000  # Convert milliseconds to seconds
            pygame.draw.rect(self.screen, GREEN, pygame.Rect(30, 30, (time_left_seconds / 10) * 110, 20))
            if time_left <= 0:
                self.red_turn = False
                self.blue_turn = True
                self.start_time = pygame.time.get_ticks()

        if self.blue_turn:
            time_left = self.total_time - (pygame.time.get_ticks() - self.start_time)  # Calculate time left
            time_left = max(0, time_left)  # Ensure time doesn't go below 0
            time_left_seconds = time_left // 1000  # Convert milliseconds to seconds
            pygame.draw.rect(self.screen, GREEN, pygame.Rect(415, 30, (time_left_seconds / 10) * 110, 20))
            if time_left <= 0:
                self.red_turn = True
                self.blue_turn = False
                self.start_time = pygame.time.get_ticks()


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
