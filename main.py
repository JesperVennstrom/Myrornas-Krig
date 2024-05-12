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
        self.players.append(BlackPlayer(self, 30, 0))
        self.players.append(WhitePlayer(self, 10, 0))
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


    # Beskrivning: Startar och ritar en timer. Om timern går ner till 0 byter det tur. Detta är en funktion utan nån input eller return.
    # Den har dock med variabler som är utanför funktionen, såsom, total_time, start_time och pygame.time.get_ticks()

    # Argument 1:          Boolean - Om det är röds tur (red_turn == true) börjar timern för röd. Detta görs genom att ta tidskillnaden från att funktionen startar tills att timern går ut.
    # Tiden kvar är då den angivna totala tiden minus tidsskillnaden. Vi sätter också ett minimum värde på 0.
    # Vi konveterar milisekunder till sekunder och ritar rektanglar vid värdet av sekunden (gånger 11)

    # Argument 2:          Integer - Om timern når noll ska det byta tur och starta om start tiden
    # Argument 3 och 4:    Boolean och Integer - Samma sak som arg1 och 2 bara för blåa spelaren (funktionen körs om blue_turn == True). 
    # Return: Inget
    # Exempel:         
    # print(time_left, time_left_seconds) =>  10039 10
                                            # 10023 10
                                            # 10006 10
                                            # 9990 9
                                            # 9973 9
                                            # 9957 9
                                            # 9941 9
                                            # 9925 9
    # Datum: 2024-05-06
    # Namn: Arvid Mårild, Jesper Vennström
    def start_timer(self):
        keys = pygame.key.get_pressed()
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(30, 30, 155, 20))
        pygame.draw.rect(self.screen, WHITE, pygame.Rect((WIN_WIDTH - 180), 30, 155, 20))

        if self.red_turn:
            time_left = self.total_time - (pygame.time.get_ticks() - self.start_time)  # Calculate time left
            time_left = max(0, time_left)  # Ensure time doesn't go below 0
            time_left_seconds = time_left // 1000  # Convert milliseconds to seconds
            pygame.draw.rect(self.screen, GREEN, pygame.Rect(30, 30, (time_left_seconds*11), 20))
            if time_left <= 0:
                self.red_turn = False
                self.blue_turn = True
                self.start_time = pygame.time.get_ticks()

        if self.blue_turn:
            time_left = self.total_time - (pygame.time.get_ticks() - self.start_time)  # Calculate time left
            time_left = max(0, time_left)  # Ensure time doesn't go below 0
            time_left_seconds = time_left // 1000  # Convert milliseconds to seconds
            pygame.draw.rect(self.screen, GREEN, pygame.Rect((WIN_WIDTH - 180), 30, (time_left_seconds*11), 20))
            if time_left <= 0:
                self.red_turn = True
                self.blue_turn = False
                self.start_time = pygame.time.get_ticks()
    
    def ui(self):
        if self.red_turn:
            self.screen.blit(self.font.render('Red Turn', True, (WHITE)), ((WIN_WIDTH/2), 30))
        if self.blue_turn:
            self.screen.blit(self.font.render('Blue Turn', True, (WHITE)), ((WIN_WIDTH/2), 30))

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        self.start_timer()
        self.ui()
        pygame.display.update()

    def update(self):
        self.all_sprites.update()

g = Game()
g.new()
while g.running:
    g.main()

pygame.quit()
sys.exit()