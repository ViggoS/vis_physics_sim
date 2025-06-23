import pygame
import sys

# Initiera Pygame
pygame.init()

# Skapa fönsterstorlek och öppna ett fönster
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Double pendumum")

# Klocka för att kontrollera bildfrekvens (FPS)
clock = pygame.time.Clock()
FPS = 60

pygame.draw.line(screen, (255, 255, 255), [WIDTH/2,HEIGHT/2],[WIDTH/2,HEIGHT/2 - 100], 5)

pygame.display.update()


running = True
while running:
    # Begränsa hastigheten till FPS bilder per sekund
    clock.tick(FPS)

    # --- Händelsehantering ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

pygame.display.update()


# Avsluta Pygame och programmet
pygame.quit()
sys.exit()
