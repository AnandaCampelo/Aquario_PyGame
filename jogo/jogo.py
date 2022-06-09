import pygame, sys
from level_layout import *
from classes import Tile,Overworld, UI
from levels import Level


class Game:
    def __init__(self):
        self.max_level = 0
        self.coins = 0
        
        self.overworld = Overworld(0,self.max_level,screen,self.create_level)
        self.status = 'overworld'

        self.ui = UI
    
    def create_level(self, current_level):
        self.level = Level(current_level,screen,self.create_overworld)
        self.status = 'level'

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.new_level = new_max_level
        self.overworld = Overworld(current_level,self.max_level,screen,self.create_level)
        self.status = 'overworld'

    def change_coins(self,amount):
        self.coins += amount

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_coins(0,12)

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill('grey')
    game.run()

    pygame.display.update()
    clock.tick(60)