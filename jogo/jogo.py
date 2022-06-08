import pygame, sys
from level_layout import *
from classes import Tile  #, Overworld
from levels import Level

'''
class Game:
    def __init__(self):
        self.max_level = 3
        self.overworld = Overworld(0, self.max_level, screen)
    
    def run(self):
        self.overworld.run()
'''

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
#game = Game()
level = Level(level_2, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill('grey')
    #game.run()
    level.run()

    pygame.display.update()
    clock.tick(60)