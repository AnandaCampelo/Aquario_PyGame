import pygame
from animations import import_folder

#classe para os blocos
class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,size):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, x_shift):
        self.rect.x += x_shift

#classe para o jogador
class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        self.import_character_animation()
        self.frame_index = 0
        self.animation_speed = 0.15
        super().__init__()
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        # movimento do player
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 3
        self.gravity = 0.8
        self.jump_speed = -10

    def import_character_animation(self):
        character_path = r'../graficos/player/'
        self.animations = {'idle': [], 'andar': [], 'pulo': [], 'cair': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations['idle']
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        self.image = animation[int(self.frame_index)]

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            self.pulo()
    
    def gravidade(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def pulo(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.animate()