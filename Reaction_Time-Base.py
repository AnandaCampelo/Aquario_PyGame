import pygame, sys
import random

pygame.init()

screen = pygame.display.set_mode((800,800)) #main display surface object
clock = pygame.time.Clock() #measure time

current_time = 0
button_pressed_time = 0

reaction_time = 0

k = True
a = True

#game loop
while k:

    #check for input if the player press the escape button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and a == True:
            button_pressed_time = pygame.time.get_ticks()
            screen.fill((0,255,0))
            a = False
        elif event.type == pygame.KEYDOWN and a == False:
                reaction_time = pygame.time.get_ticks()
                print(f'reaction time: {reaction_time}')

    lista_tempo = []
    for i in range(2000,10000):
        lista_tempo.append(i)

    random_time = random.choice(lista_tempo)
    print(random_time)

    #gets what milliseconds it is at the moment
    current_time = pygame.time.get_ticks()  

    if  current_time - button_pressed_time > random_time:
        screen.fill((250,0,0))
    
    if reaction_time > 0:
        k = False

    #draw the frame painted in the while loop:
    pygame.display.flip()

    #meaures the time accurately (60 frames per second)
    clock.tick(60)