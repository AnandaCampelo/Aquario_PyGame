import pygame
import random
from palavras import dic

window = pygame.display.set_mode((1000,600))

pygame.font.init()
font = pygame.font.SysFont('Courier New', 50)
font_dica = pygame.font.SysFont('Courier New', 30)

dicas = []
for dica in dic.keys():
    dicas.append(dica)
dica_escolhida = random.choice(dicas)
for dica,lista in dic.items():
         if dica == dica_escolhida:
            palavra = random.choice(lista)
            break

tentativas = []
palavra_escolhida = []
palavra_escondida = []
end_game = True
chances = 0
letra = ''

def desenho(window, chances):
    pygame.draw.rect(window, (255,255,255), (0,0,1000,600))
    pygame.draw.line(window, (0,0,0), (100,500), (100,100), 10)
    pygame.draw.line(window, (0,0,0), (50,500), (150,500), 10)
    pygame.draw.line(window, (0,0,0), (100,100), (300,100), 10)
    pygame.draw.line(window, (0,0,0), (300,100), (300,150), 10)

    if chances >= 1:
        pygame.draw.circle(window, (0,0,0), (300,200), 50, 10)
    if chances >= 2:
        pygame.draw.line(window, (0,0,0), (300,250), (300,350), 10)
    if chances >= 3:
        pygame.draw.line(window, (0,0,0), (300,265), (250,315), 10)
    if chances >= 4:
        pygame.draw.line(window, (0,0,0), (300,265), (350,315), 10)
    if chances >= 5:
        pygame.draw.line(window, (0,0,0), (300,340), (225,415), 10)
    if chances >= 6:
        pygame.draw.line(window, (0,0,0), (300,340), (375,415), 10)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            letra = str(pygame.key.name(event.key)).upper()

    desenho(window,chances)

    pygame.display.update()