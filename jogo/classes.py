import pygame

class Tile(pygame.sprit.Sprite):
    def __init__(self,pos,size):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = pos)