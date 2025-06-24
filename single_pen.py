import pygame
import sys
import numpy as np
import math

# Initiera Pygame
pygame.init()

# Skapa fönsterstorlek och öppna ett fönster
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Matematisk pendel")

# Färger 
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0,0,0)
GREY = (100, 100, 100)

# Klocka för att kontrollera bildfrekvens (FPS)
clock = pygame.time.Clock()
FPS = 60

# Parametrar pendel
g = 9.82 
L = 100
mass = 1.0     # kg
k_drag = 0.05  # luftmotståndskoefficient (testa olika värden)


# Initialvillkor
theta = -np.pi / 2
omega = 0.0


my_font = pygame.font.SysFont(None, 30, False, False)
my_font2 = pygame.font.SysFont(None, 20, False, False)


# Till graf
omega_history = []  # Samlar historik
max_history = 300   # Antal punkter att spara (ca 5 sekunder vid 60 fps)
GRAPH_HEIGHT = 100
GRAPH_WIDTH = 300 

pen_rect_pos = [GRAPH_WIDTH + 10, 10, WIDTH - GRAPH_WIDTH - 30, HEIGHT-GRAPH_HEIGHT-20]

pendulum_base = [pen_rect_pos[0] + pen_rect_pos[3] / 2, pen_rect_pos[1]/2 + pen_rect_pos[3]/2 ]
ball_pos = [pendulum_base[0] + L*np.sin(theta) ,pendulum_base[1] + L*np.cos(theta)]

def derivatives(theta, omega):
    dtheta_dt = omega
    drag_torque = - k_drag * omega * abs(omega)
    domega_dt = - (g / L) * np.sin(theta) + drag_torque / (mass * (L/100)**2)
    return dtheta_dt, domega_dt

pygame.draw.line(screen, WHITE, pendulum_base, ball_pos, 5)
pygame.draw.circle(screen, RED, ball_pos, 15, 0)


pygame.display.update()

def draw_omega_graph(surface, omega_history, graph_height = GRAPH_HEIGHT, graph_width = GRAPH_WIDTH):
    graph_top = HEIGHT - graph_height - 10
    graph_left = 10

    pygame.draw.rect(surface, WHITE, (graph_left - 1, graph_top - 1, graph_width + 2, graph_height + 2), 1)

    if len(omega_history) < 2:
        return

    # Normalisera värden för att passa i grafen
    max_val = max(max(omega_history), abs(min(omega_history)), 1)
    scale = graph_height / (2 * max_val)

    for i in range(len(omega_history) - 1):
        x1 = graph_left + i
        y1 = graph_top + graph_height // 2 - int(omega_history[i] * scale)
        x2 = graph_left + i + 1
        y2 = graph_top + graph_height // 2 - int(omega_history[i + 1] * scale)
        pygame.draw.line(surface, GREEN, (x1, y1), (x2, y2), 1)


def update_ball_pos(theta, L = L):
    theta = float(theta)
    ball_pos = [pendulum_base[0] + L*np.sin(theta) ,pendulum_base[1] + L*np.cos(theta)]

    return ball_pos
    

def rungeKutta(theta: float, omega: float, dt = 0.1):

    k1_theta, k1_omega = derivatives(theta, omega)
    k2_theta, k2_omega = derivatives(theta + 0.5*dt*k1_theta, omega + 0.5*dt*k1_omega)
    k3_theta, k3_omega = derivatives(theta + 0.5*dt*k2_theta, omega + 0.5*dt*k2_omega)
    k4_theta, k4_omega = derivatives(theta + dt*k3_theta, omega + dt*k3_omega)
    
    theta += (dt/6) * (k1_theta + 2*k2_theta + 2*k3_theta + k4_theta)
    omega += (dt/6) * (k1_omega + 2*k2_omega + 2*k3_omega + k4_omega)

    return theta, omega


param_sel = None
drag_activated = False

running = True
while running:
    # Begränsa hastigheten till FPS bilder per sekund
    clock.tick(FPS)

    ball = pygame.Rect(ball_pos[0], ball_pos[1], 30, 30)
    g_button = pygame.Rect(10, 10, 200, 40)
    l_button = pygame.Rect(10, 60, 200, 40)
    drag_button = pygame.Rect(10, 110, 200, 40)
    activate_drag_button = pygame.Rect(GRAPH_WIDTH+20, HEIGHT - GRAPH_HEIGHT, GRAPH_HEIGHT-10, GRAPH_HEIGHT-10)

    mouseClicked = None


    theta, omega = rungeKutta(theta, omega)

    omega_history.append(omega)
    if len(omega_history) > max_history:
        omega_history.pop(0)

    ev = pygame.event.get()
    mouse = pygame.mouse.get_pos()
    #print(mouse)

    # --- Händelsehantering ---
    for event in ev:
        if event.type == pygame.QUIT:
            running = False
    
    # Tangenter
    keys = pygame.key.get_pressed()  # Kontrollera vilka tangenter som hålls nere
    if param_sel == "l_button":    
        if keys[pygame.K_UP]:
            L += 0.5
        if keys[pygame.K_DOWN]:
            L -= 0.5
    elif param_sel == "g_button":
        if keys[pygame.K_UP]:
            g += 0.1
        if keys[pygame.K_DOWN]:
            g -= 0.1
    elif param_sel == "drag_button":
        if keys[pygame.K_UP]:
            k_drag += 0.01
        if keys[pygame.K_DOWN]:
            k_drag -= 0.01

    if event.type == pygame.MOUSEBUTTONDOWN :
        mouseClicked = True
    if event.type == pygame.MOUSEBUTTONUP :
        mouseClicked = False

    if l_button.collidepoint(mouse) and mouseClicked:
      param_sel = 'l_button'
    elif g_button.collidepoint(mouse) and mouseClicked:
      param_sel = 'g_button'
    elif drag_button.collidepoint(mouse) and mouseClicked and drag_activated == True:
      param_sel = 'drag_button'

    if activate_drag_button.collidepoint(mouse) and mouseClicked:
        drag_activated = not drag_activated


    #print(selected)

    # Bestäm position för pendel

    if mouseClicked and ball.collidepoint(mouse):
        if mouse[1] <= abs(pendulum_base[1]+L): # bättre lösning
            ball_pos = [mouse[0],mouse[1]]
    else:
        ball_pos = update_ball_pos(theta, L) 

    screen.fill(BLACK)  # Fyll skärmen med svart
    


    # Visa pendel
    pygame.draw.rect(screen, WHITE, pen_rect_pos, 1) # (x, y, width, height)
    pygame.draw.line(screen, WHITE, pendulum_base, ball_pos, 5)
    pygame.draw.circle(screen, RED, ball_pos, 15, 0)
    pygame.draw.rect(screen, GREY, l_button)
    pygame.draw.rect(screen, GREY, g_button)
    pygame.draw.rect(screen, WHITE, activate_drag_button, 1)

    if drag_activated == True:
        pygame.draw.rect(screen, GREY, activate_drag_button)
        pygame.draw.rect(screen, GREY, drag_button)
        text_drag = my_font.render(f'k_drag =  {round(k_drag,2)}, [N]', False, WHITE)
        screen.blit(text_drag, (drag_button[0]+10, drag_button[1]+10))

    if param_sel == "l_button":    
        pygame.draw.rect(screen, WHITE, l_button, 1)
    elif param_sel == "g_button":
        pygame.draw.rect(screen, WHITE, g_button, 1)
    elif param_sel == "drag_button" and drag_activated == True:
        pygame.draw.rect(screen, WHITE, drag_button, 1)

    

    # Visa text
    text_vinkelhastighet = my_font.render(f'Vinkelhastighet: {round(omega, 2)} ', False, GREEN)
    screen.blit(text_vinkelhastighet, (10,HEIGHT-GRAPH_HEIGHT-30))
    text_L = my_font.render(f'L =  {round(L/100,2)} [m]', False, WHITE)
    screen.blit(text_L, (l_button[0]+10, l_button[1]+10))
    text_g = my_font.render(f'g =  {round(g,2)} [m/s^2]', False, WHITE)
    screen.blit(text_g, (g_button[0]+10, g_button[1]+10))
    
    text_g = my_font2.render('luftmotstånd', False, WHITE)
    screen.blit(text_g, (activate_drag_button[0]+5, activate_drag_button[1]+30))
    
    # Visa graf
    draw_omega_graph(screen, omega_history)

    pygame.display.update()
    

#pygame.display.update()


# Avsluta Pygame och programmet
pygame.quit()
sys.exit()
