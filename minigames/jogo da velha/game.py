import pygame, sys 

pygame.init()

c = 600
h = 600
c_linha = 15

vermelho = (255,0,0)
fundo = (28,170,156)
linha = (23,145,135)

tela = pygame.display.set_mode((c,h))
pygame.display.set_caption('Jogo da Velha')
tela.fill(fundo)

pygame.draw.line(tela,vermelho,(10,10),(300,300),10)

def draw_line():
    pygame.draw.line()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    pygame.display.update()