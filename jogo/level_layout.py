tile_size = 64
vertical_tile_number = 11
screen_width = 1200
screen_height = vertical_tile_number * tile_size

level_0 = {
    'terreno' : './graficos/level0/level 0 layout_terreno.csv',
    'constraint' : './graficos/level0/level 0 layout_constraint.csv',
    'enemy' : './graficos/level0/level 0 layout_enemy.csv',
    'ouro' : './graficos/level0/level 0 layout_ouro.csv',
    'placas' : './graficos/level0/level 0 layout_placas.csv',
    'player' : './graficos/level0/level 0 layout_player.csv'
}

level_1 = {
    'terreno' : './graficos/level1/level 1 layout_terreno.csv',
    'constraint' : './graficos/level1/level 1 layout_constraint.csv',
    'enemy' : './graficos/level1/level 1 layout_enemy.csv',
    'ouro' : './graficos/level1/level 1 layout_ouro.csv',
    'placas' : './graficos/level1/level 1 layout_placas.csv',
    'player' : './graficos/level1/level 1 layout_player.csv'
}

level_2 = {
    'terreno' : './graficos/level2/level 2 layout_terreno.csv',
    'constraint' : './graficos/level2/level 2 layout_constraint.csv',
    'enemy' : './graficos/level2/level 2 layout_enemy.csv',
    'ouro' : './graficos/level2/level 2 layout_ouro.csv',
    'placas' : './graficos/level2/level 2 layout_placas.csv',
    'player' : './graficos/level2/level 2 layout_player.csv'
}


level_00 = {'node_pos':(110,400),'content': 'this is level 0', 'unlock':1}

levels = {
    0: level_1
}