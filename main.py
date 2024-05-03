import pygame
from config import *
from sprites import *
import sys
from PIL import Image

class Game: 
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Blancos Vs Niggers")
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.toggle_fullscreen()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.running = True

    def new(self):
        self.playing = True

        self.turn = 0

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.black = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates() #kanske inte behövs om vi har pvp
        self.attacks = pygame.sprite.LayeredUpdates()
        self.world = pygame.sprite.LayeredUpdates()

        
        self.players = []
        self.players.append(BlackPlayer(self, 1, 2))
        self.players.append(WhitePlayer(self, 2, 1))
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

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
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
