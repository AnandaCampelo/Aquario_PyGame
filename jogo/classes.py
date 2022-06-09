import pygame
from animations import import_folder
from level_layout import screen_height,screen_width,tile_size,vertical_tile_number, levels

#classe para os blocos
class Tile(pygame.sprite.Sprite):
    def __init__(self,size,x,y):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect(topleft = (x,y))
    
    def update(self,shift):
        self.rect.x += shift


    def update(self, x_shift):
        self.rect.x += x_shift
    
#classe para o jogador
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface):
        self.import_character_animation()
        self.frame_index = 0
        self.animation_speed = 0.15
        super().__init__()
        idle = self.animations['idle']
        self.image = idle[self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        # movimento do player
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 4
        self.gravity = 0.8
        self.jump_speed = -20

        # estado do jogador
        self.status = 'idle'
        self.olhando_frente = True
        self.on_ground = False
        self.on_celling = False
        self.on_right = False
        self.on_left = False

    def import_character_animation(self):
        character_path = r'./graficos/player/'
        self.animations = {'idle': [], 'andar': [], 'pulo': [], 'cair': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        image = animation[int(self.frame_index)]
        if self.olhando_frente:
            self.image = image
        else:
            virar_jogador = pygame.transform.flip(image,True,False)
            self.image = virar_jogador

        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_celling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_celling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_celling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.olhando_frente = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.olhando_frente = False
        else:
            self.direction.x = 0

        if (keys[pygame.K_UP] or keys[pygame.K_SPACE])  and self.on_ground:
            self.pulo()
    
    def get_status(self):
        if self.direction.y < 0:
            self.status = 'pulo'
        elif self.direction.y > 1:
            self.status = 'cair'
        else:
            if self.direction.x != 0:
                self.status = 'andar'
            else:
                self.status = 'idle'

    def gravidade(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def pulo(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()


class StaticTile(Tile):
    def __init__(self,size,x,y,surface):
        super().__init__(size,x,y)
        self.image = surface

class AnimatesTile(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self,shift):
        self.animate()
        self.rect.x += shift

class Enemy(AnimatesTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, './graficos/tiles/enemy')
        self.speed = 3

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image,True,False)
    
    def reverse(self):
        self.speed *= -1

    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()

class Fundo:
    def __init__(self,horizon):
        self.horizon = horizon

        self.fundo = pygame.image.load('./graficos/background.png').convert()
        self.fundo = pygame.transform.scale(self.fundo,(screen_width,tile_size))

    def draw(self,surface):
        for row in range(vertical_tile_number):
            y = row * tile_size
            surface.blit(self.fundo,(0,y))

class Node(pygame.sprite.Sprite):
    def __init__(self,pos,status,icon_speed):
        super().__init__()
        self.image = pygame.Surface((100,80))
        if status == 'available':
            self.image = pygame.image.load('./graficos/open.png').convert_alpha()
            self.rect = self.image.get_rect(center = pos)
        else:
            self.image = pygame.image.load('./graficos/closed.png').convert_alpha()
            self.rect = self.image.get_rect(center = pos)
        self.rect = self.image.get_rect(center = pos)

        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_speed / 2),self.rect.centery - (icon_speed / 2),icon_speed,icon_speed)

class Icon(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load('./graficos/fox.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)

    def update(self):
        self.rect.center = self.pos

class Overworld:
    def __init__(self,start_level,max_level,surface,create_level):

        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level

        self.moving = False
        self.move_direction = pygame.math.Vector2(0,0)
        self.speed = 8

        self.setup_nodes()
        self.setup_icon()

    def setup_nodes(self):
        
        self.nodes = pygame.sprite.Group()

        for index,node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'],'available',self.speed)
            else:
                node_sprite = Node(node_data['node_pos'],'locked',self.speed)
            self.nodes.add(node_sprite)
    
    # def draw_paths(self):
    #     points = [node['node_pos'] for index,node in enumerate(levels.values()) if index <= self.max_level]
    #     pygame.draw.lines(self.display_surface,'red',False,points,6)

    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.moving:
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data('next')
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_LEFT] and self.current_level > 0:
                self.move_direction = self.get_movement_data('previous')
                self.current_level -=1
                self.moving = True
            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)

    def get_movement_data(self,target):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        
        if target == 'next':
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)

        return (end - start).normalize()

    def update_icon_pos(self):
        # self.icon.sprite.rect.center = self.nodes.sprites()[self.current_level].rect.center
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0,0)

    def run(self):
        self.input()
        self.update_icon_pos()
        self.icon.update()
        #self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)


class UI:
    def __init__(self,surface):
        self.display_surface = surface

        #self.coin = pygame.image.load('/graficos/tiles/moeda/pixil-frame-0 (33).png')
        #self.coin_rect = self.coin.get_rect(topleft = (20,10))
        self.font = pygame.font.SysFont('Courier New', 30)

    def show_coins(self,amount):
        #self.display_surface.blit(self.coin,self.coin_rect)
        coin_amount_surf = self.font.render(str(amount),False,'#33323d')
        coin_amount_rect = coin_amount_surf.get_rect(midleft = (30,10))
