import pygame
pygame.init()

background_colour = (234, 212, 252)
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption('Geeksforgeeks')
screen.fill(background_colour)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()

pygame.quit()