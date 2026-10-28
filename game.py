import random
import pygame 

# Set screen resolution
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

CELL_SIZE = 30  # Each grid square will be 30x30 pixels

# Set up colours
WHITE = (255, 255, 255)
BLUE = (51, 153, 255) # For the snake
RED = (153, 0, 0) # For the apple
DARK_GREEN = (0, 102, 51)
LIGHT_GREEN = (204, 255, 204)
BLACK = (0, 0, 0)

# The snake starts with 3 segments: head, body part 1, body part 2
snake_segments = [[300, 300], [270, 300], [240, 300]]

# Game takes place on a grid, the snake must move forward by one full square
velocity_x = CELL_SIZE 
velocity_y = 0

# To be able to eat properly, the apple aligns with the grid. 
apple_x = random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE # The square is random
apple_y = random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE

# Set up the game
clock = pygame.time.Clock()
running = True


while running:
    # 1. Handling events and keyboard input
    # Check for events 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Get the keys being pressed
    keys = pygame.key.get_pressed()
    
    # Change directions + no sucide 
    if keys[pygame.K_LEFT] and velocity_x == 0:
        velocity_x = -CELL_SIZE
        velocity_y = 0
    elif keys[pygame.K_RIGHT] and velocity_x == 0:
        velocity_x = CELL_SIZE
        velocity_y = 0
    elif keys[pygame.K_UP] and velocity_y == 0:
        velocity_x = 0
        velocity_y = -CELL_SIZE
    elif keys[pygame.K_DOWN] and velocity_y == 0:
        velocity_x = 0
        velocity_y = CELL_SIZE

    # 2. Calculating the new position of the head 
    new_head = [snake_segments[0][0] + velocity_x, snake_segments[0][1] + velocity_y]
    
   # Insert the new head at the beginning of the list
    snake_segments.insert(0, new_head)
   
   # 3. Handling the collision with the apple
    if snake_segments[0][0] == apple_x and snake_segments[0][1] == apple_y:
        # The snake eats the apple: we generate new position for apple
        apple_x = random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        apple_y = random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        # We don't delete the last segment, it's what make the snake grow
    else:
        # The snake goes on normally, we just delete the last segment
        snake_segments.pop()
   

    # 4. Affichage (Dessin)
    screen.fill(BLACK)  # Fond noir

    # Dessiner la pomme
    pygame.draw.rect(screen, RED, pygame.Rect(apple_x, apple_y, CELL_SIZE, CELL_SIZE))

    # Dessiner le serpent
    for segment in snake_segments:
        pygame.draw.rect(screen, BLUE, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))

    # Mettre à jour l'écran (indispensable pour afficher les dessins)
    pygame.display.flip()

pygame.quit()