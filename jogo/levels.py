import pygame
from classes import Player
from classes import Tile, StaticTile, AnimatesTile, Enemy, Fundo
from level_layout import tile_size, screen_width, screen_height
from animations import import_csv_layout, import_cut_graphics

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.world_shift = 0

        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)
        
        terrain_layout = import_csv_layout(level_data['terreno'])
        self.terrain_sprites = self.create_tile_group(terrain_layout,'terreno')

        sign_layout = import_csv_layout(level_data['placas'])
        self.sign_sprites = self.create_tile_group(sign_layout,'placas')

        gold_layout = import_csv_layout(level_data['ouro'])
        self.gold_sprites = self.create_tile_group(gold_layout,'ouro')

        enemy_layout = import_csv_layout(level_data['enemy'])
        self.enemy_sprites = self.create_tile_group(enemy_layout,'enemy')

        constraint_layout = import_csv_layout(level_data['constraint'])
        self.constraint_sprites = self.create_tile_group(constraint_layout,'constraint')

        self.fundo = Fundo(8)

    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()

        for row_index,row in enumerate(layout):
            for col_index,val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terreno':
                        terrain_tile_list = import_cut_graphics('./graficos/tiles/terreno.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)

                    if type == 'placas':
                        sign_tile_list = import_cut_graphics('./graficos/tiles/seta.png')
                        tile_surface = sign_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)      

                    if type == 'ouro':
                        sprite = AnimatesTile(tile_size,x,y,'./graficos/tiles/ouro')
                        
                    if type == 'enemy':
                        sprite = Enemy(tile_size,x,y)

                    if type == 'constraint':
                        sprite = Tile(tile_size,x,y)

                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                
                if cell == '0':
                    sprite = Player((x,y),self.display_surface)
                    self.player.add(sprite)
                if cell == '1':
                    bigode = pygame.image.load('./graficos/win.png').convert_alpha()
                    sprite = StaticTile(tile_size,x,y,bigode)
                    self.goal.add(sprite)

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy,self.constraint_sprites,False):
                enemy.reverse()

    def movimento_horizontal_colisao(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    self.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    self.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def movimento_vertical_colisao(self):
        player = self.player.sprite
        player.gravidade()

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_celling = True
                elif player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_celling and player.direction.y > 0:
            player.on_celling = False

    def scroll_x(self):

        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 2 and direction_x < 0:
            self.world_shift = 4
            player.speed = 0
        elif player_x > screen_width / 2 and direction_x > 0:
            self.world_shift = -4
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 3

    def check_death(self):
        if self.player.sprite.rect.top > screen_height:
            print('you lose')
    
    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite,self.goal,False):
            print('you win!')

    def run(self):

        #self.fundo.draw(self.display_surface)

        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

        #self.sign_sprites.update(self.world_shift)
        #self.sign_sprites.draw(self.display_surface)

        #self.gold_sprites.update(self.world_shift)
        #self.gold_sprites.draw(self.display_surface)

        self.player.update()
        self.movimento_horizontal_colisao()
        self.movimento_vertical_colisao()
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        #self.enemy_sprites.update(self.world_shift)
        #self.enemy_sprites.draw(self.display_surface)

        self.check_death()
        self.check_win()

        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()

'''
    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                
                if cell == '0':
                    sprite = Player(pos, surface)
                
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        if player_x < screen_width / 2 and direction_x < 0:
            self.world_shift = 4
            player.speed = 0
        elif player_x > screen_width / 2 and direction_x > 0:
            self.world_shift = -4
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 3
    def movimento_horizontal_colisao(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    self.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    self.on_right = True
                    self.current_x = player.rect.right
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False
    def movimento_vertical_colisao(self):
        player = self.player.sprite
        player.gravidade()
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_celling = True
                elif player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_celling and player.direction.y > 0:
            player.on_celling = False
    def run(self):
        # blocos do level
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()
        # jogador
        self.player.update()
        self.movimento_horizontal_colisao()
        self.movimento_vertical_colisao()
        self.player.draw(self.display_surface)
        '''