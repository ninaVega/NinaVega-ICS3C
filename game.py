import random
import pygame 
import math

# Set up the screen 
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch the apples!")

CELL_SIZE = 30  # Each grid square will be 30x30 pixels

# Set up colours
WHITE = (255, 255, 255)
BLUE = (51, 153, 255) 
RED = (153, 0, 0) 
DARK_GREEN = (34, 139, 34)  # The grass
YELLOW = (255, 220, 0)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)  # The sky

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 25)

# Set up the player
basket_x = 270
basket_y = 340
basket_width = 90
basket_height = 30
basket_speed = 8

# lists that store the falling apples and power-ups
apples = []
power_ups = []

# Game Variables
score = 0
lives = 3
level = 1
game_state = "menu"
frame_count = 0

# Set up the game
clock = pygame.time.Clock()
running = True

# Function 1: Choose random position
def new_position():
    """Choose a random horizontal position on the grid"""
    return random.randint(0, (SCREEN_WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE

# Function 2 ; Reset the game
def reset_game():
    """Reset the player, score, lives and falling object"""
    global basket_x, apples, power_ups
    global score, lives, level, frame_count, game_state

    basket_x = 270
    apples = []
    power_ups = []
    score = 0
    lives = 3
    level = 1
    frame_count = 0  
    game_state = "playing"


# Function 3: Display the text
def draw_text(message, x, y, colour, text_font):
    """Display a message at chosen position"""
    text = text_font.render(message, True, colour)
    screen.blit(text, (x, y))

# Fonction pour dessiner un nuage statique
def draw_cloud(x, y):
    """Dessine un nuage fait de 3 cercles blancs imbriqués"""
    pygame.draw.circle(screen, WHITE, (x, y), 25)
    pygame.draw.circle(screen, WHITE, (x + 25, y - 5), 35)
    pygame.draw.circle(screen, WHITE, (x + 50, y), 25)

# Fonction Pygame pour générer la géométrie d'une étoile
def draw_pygame_star(x, y, num_points, outer_radius, inner_radius, color):
    """Dessine une étoile polygonale directement dans la fenêtre Pygame"""
    points = []
    for i in range(num_points * 2):
        radius = outer_radius if i % 2 == 0 else inner_radius
        angle = i * math.pi / num_points - math.pi / 2  # Aligne la pointe vers le haut
        pt_x = x + math.cos(angle) * radius
        pt_y = y + math.sin(angle) * radius
        points.append((pt_x, pt_y))
    pygame.draw.polygon(screen, color, points)

while running:
    # 1. Handling events and keyboard input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
      
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            
            if event.key == pygame.K_SPACE:
                if game_state == "menu" or game_state == "gameover":
                    reset_game()

    # Get the keys being pressed
    keys = pygame.key.get_pressed()

    if game_state == "playing":
        frame_count += 1

        # Move the basket
        if keys[pygame.K_LEFT]:
            basket_x -= basket_speed
        if keys[pygame.K_RIGHT]:
            basket_x += basket_speed

        # Keep basket inside of the screen 
        basket_x = max(0, min(basket_x, SCREEN_WIDTH - basket_width))

        # IMPORTANT: basket_rect must be defined before checking collisions
        basket_rect = pygame.Rect(basket_x, basket_y, basket_width, basket_height)

        # Apples 
        if frame_count % max(15, 45 - level * 3) == 0:
            apples.append([new_position(), 0])

        # occasional power-up
        if frame_count % 300 == 0:
            power_ups.append([new_position(), 0])

        # Move apples and check collisions
        for apple in apples[:]:
            apple[1] += 4 + level

            apple_rect = pygame.Rect(apple[0], apple[1], CELL_SIZE, CELL_SIZE)

            if basket_rect.colliderect(apple_rect):
                apples.remove(apple)
                score += 1
                level = score // 10 + 1

            elif apple[1] > SCREEN_HEIGHT:
                apples.remove(apple)
                lives -= 1

        # Move power-ups (les étoiles) et vérifier les collisions
        for power_up in power_ups[:]:
            power_up[1] += 3

            power_rect = pygame.Rect(power_up[0], power_up[1], CELL_SIZE, CELL_SIZE)

            if basket_rect.colliderect(power_rect):
                power_ups.remove(power_up)
                lives = min(lives + 1, 5)

            elif power_up[1] > SCREEN_HEIGHT:
                power_ups.remove(power_up)
    
        # Check game over
        if lives <= 0:
            game_state = "gameover"
    
    # 3. Draw everything
    screen.fill(SKY_BLUE)

    # Nuages de fond totalement fixes
    draw_cloud(80, 80)
    draw_cloud(420, 100)

    # Bande de pelouse verte fixe tout en bas (hauteur 40 pixels)
    pygame.draw.rect(screen, DARK_GREEN, (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40))

    if game_state == "menu":
        menu_bg = pygame.Surface((400, 180))
        menu_bg.set_alpha(150)
        menu_bg.fill(BLACK)
        screen.blit(menu_bg, (100, 100))

        draw_text("CATCH THE APPLES!", 155, 120, WHITE, font)
        draw_text("Press SPACE to start", 175, 190, YELLOW, small_font)
        draw_text("Use LEFT and RIGHT arrows", 155, 225, WHITE, small_font)

    elif game_state == "playing":
        # Draw the basket
        pygame.draw.rect(screen, BLUE, (basket_x, basket_y, basket_width, basket_height))

        # Draw apples
        for apple in apples:
            pygame.draw.circle(
                screen, RED,
                (apple[0] + CELL_SIZE // 2, apple[1] + CELL_SIZE // 2),
                CELL_SIZE // 2
            )

        # CORRECTION : Dessiner les bonus sous forme d'étoiles jaunes au lieu de carrés !
        for power_up in power_ups:
            center_x = power_up[0] + CELL_SIZE // 2
            center_y = power_up[1] + CELL_SIZE // 2
            draw_pygame_star(center_x, center_y, num_points=5, outer_radius=15, inner_radius=7, color=YELLOW)

        # Display score, lives and level
        draw_text("Score: " + str(score), 10, 10, BLACK, small_font)
        draw_text("Lives: " + str(lives), 230, 10, BLACK, small_font)
        draw_text("Level: " + str(level), 440, 10, BLACK, small_font)

    elif game_state == "gameover":
        go_bg = pygame.Surface((400, 180))
        go_bg.set_alpha(150)
        go_bg.fill(BLACK)
        screen.blit(go_bg, (100, 100))

        draw_text("GAME OVER!", 205, 120, RED, font)
        draw_text("Final score: " + str(score), 210, 170, WHITE, small_font)
        draw_text("Press SPACE to play again", 145, 220, YELLOW, small_font)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
