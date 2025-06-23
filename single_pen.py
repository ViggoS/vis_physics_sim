import pygame
import sys
import numpy as np
import math

# Initiera Pygame
pygame.init()

# Skapa fönsterstorlek och öppna ett fönster
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Double pendumum")

# Färger 
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0,0,0)

# Klocka för att kontrollera bildfrekvens (FPS)
clock = pygame.time.Clock()
FPS = 60

ball_pos = [WIDTH/2 ,HEIGHT/2]

# Vinkel theta

pygame.draw.line(screen, WHITE, ball_pos,[WIDTH/2,HEIGHT/2 - 100], 5)
pygame.draw.circle(screen, RED, ball_pos, 15, 0)

pygame.display.update()
theta = 0

def update_ball_pos(ball_pos):
    x_dis = ball_pos[0]-(WIDTH/2)
    y_dis = ball_pos[1]-(HEIGHT/2-100)
    if y_dis != 0: 
        theta = np.arctan(x_dis/y_dis)
        theta = np.degrees(theta)
    else: 
        theta = 0
    if np.abs(theta) < 45:
        ball_pos[0] += 1
        #ball_pos[1] += 0.5
    else:
        ball_pos[0] -= 1
        #ball_pos[1] -= 0.5

    #print(theta)


running = True
while running:
    # Begränsa hastigheten till FPS bilder per sekund
    clock.tick(FPS)

    # --- Händelsehantering ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    update_ball_pos(ball_pos) 
    screen.fill(BLACK)  # Fyll skärmen med svart
    pygame.draw.line(screen, WHITE, ball_pos,[WIDTH/2,HEIGHT/2 - 100], 5)
    pygame.draw.circle(screen, RED, ball_pos, 15, 0)
    pygame.display.update()
    

pygame.display.update()


# Avsluta Pygame och programmet
pygame.quit()
sys.exit()
