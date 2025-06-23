import pygame
import sys

# Initiera Pygame
pygame.init()

# Skapa fönsterstorlek och öppna ett fönster
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grundläggande Pygame-spel")

# Definiera färger (RGB-format)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Skapa en spelare (rektangel)
player_pos = [WIDTH // 2, HEIGHT // 2]
player_size = 50
player_speed = 5

# Klocka för att kontrollera bildfrekvens (FPS)
clock = pygame.time.Clock()
FPS = 60

# Spelloopen
running = True
while running:
    # Begränsa hastigheten till FPS bilder per sekund
    clock.tick(FPS)

    # --- Händelsehantering ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Uppdatera spelobjekt ---
    keys = pygame.key.get_pressed()  # Kontrollera vilka tangenter som hålls nere
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    if keys[pygame.K_UP]:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += player_speed

    # --- Rita om skärmen ---
    screen.fill(WHITE)  # Fyll skärmen med vitt
    pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], player_size, player_size))  # Rita spelaren
    pygame.display.flip()  # Uppdatera hela skärmen

# Avsluta Pygame och programmet
pygame.quit()
sys.exit()
