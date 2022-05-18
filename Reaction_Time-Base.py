import pygame, sys
import random

pygame.init()

screen = pygame.display.set_mode((800,400)) #main display surface object
clock = pygame.time.Clock() #measure time

font = pygame.font.SysFont(None, 30)
img = font.render('precione qualquer tecla para começar.', True, (255,255,255))
screen.blit(img, (20, 20))

current_time = 0
button_pressed_time = 0

reaction_time = 0

k = True
a = True
b = False
c = False

#game loop
while k:

    #check for input if the player press the escape button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and a == True:
            button_pressed_time = pygame.time.get_ticks()
            screen.fill((0,255,100))
            a = False
        elif event.type == pygame.KEYDOWN and a == False and b == True:
            screen.fill((0,0,0))
            reaction_time = pygame.time.get_ticks()
            print('\n' + f'tempo de reação: {reaction_time}' + '\n')
            font = pygame.font.SysFont(None, 30)
            img = font.render(f'tempo de reação: {reaction_time}', True, (255,255,255))
            screen.blit(img, (20, 20))
            a = True
            b = False
            c = True
        elif event.type == pygame.KEYDOWN and a == False and b == False:
            screen.fill((0,0,0))
            font = pygame.font.SysFont(None, 30)
            img = font.render('Muito Cedo! Clique novamente para recomeçar.', True, (255,255,255))
            screen.blit(img, (20, 20))
            a = True

    lista_tempo = []
    for i in range(2000,10000):
        lista_tempo.append(i)

    random_time = random.choice(lista_tempo)

    #gets what milliseconds it is at the moment
    current_time = pygame.time.get_ticks()  

    if current_time - button_pressed_time > random_time and a == False:
        screen.fill((250,0,50))
        b = True
        
    #draw the frame painted in the while loop:
    pygame.display.flip()

    #meaures the time accurately (60 frames per second)
    clock.tick(60)