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

while running:
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