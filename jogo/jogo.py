import pygame, sys
from level_layout import *
from classes import Tile,Overworld, UI
from levels import Level


class Game:
    def __init__(self):
        self.max_level = 2
        self.coins = 0
        
        self.overworld = Overworld(0,self.max_level,screen,self.create_level)
        self.status = 'overworld'

        self.ui = UI(screen)
    
    def create_level(self, current_level):
        self.level = Level(current_level,screen,self.create_overworld, self.change_coins)
        self.status = 'level'

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.new_level = new_max_level
        self.overworld = Overworld(current_level,self.max_level,screen,self.create_level)
        self.status = 'overworld'

    def change_coins(self,amount):
        self.coins += amount

    def change_level(self):
        if self.coins == 23 and self.max_level == 0:
            self.coins = 0
            self.max_level = 1
            self.overworld = Overworld(0,self.max_level,screen,self.create_level)
            self.status = 'overworld'
        elif self.coins == 17 and self.max_level == 1:
            self.coins = 0
            self.max_level = 2
            self.overworld = Overworld(0,self.max_level,screen,self.create_level)
            self.status = 'overworld'
        elif self.coins == 15 and self.max_level == 2:
            print('Você Ganhou!!!')

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_coins(self.coins)
            self.change_level()

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