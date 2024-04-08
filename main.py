import pygame
from config import *
from sprites import *
import sys 

class Game: 
    def __init__(self):
        pygame.init()
        pygame.displat.set_caption("Blancos Vs Niggers")
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("freesansbold.ttf", 32)

    def new(self):
        self.playing = True

    def main(self):
        pass
    
    def generateTilemap(self):
        pass

    def draw(self):
        pass

    def update(self):
        pass

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
