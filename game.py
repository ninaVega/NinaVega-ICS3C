import random
import pygame 

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
BLUE = (51, 153, 255) # For the snake
RED = (153, 0, 0) # For the apple
DARK_GREEN = (0, 102, 51)
YELLOW = (255, 220, 0)
BLACK = (0, 0, 0)

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 25)

"""# Music
pygame.mixer.music.load("")
pygame.mixer.music.play(-1)"""

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
    return random.randint(o, 19) * CELL_SIZE

# Function 2 ; Reset the game
def new_position():
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

while running:
    # 1. Handling events and keyboard input
    # Check for events 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
      
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
               running = False
            if game_state == "menu" and event.key == pygame.K_SPACE
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
   

    if check_collision():
        snake_segments = [[300, 200], [280, 200], [260, 200]]
        velocity_x = CELL_SIZE
        velocity_y = 0 
        apple_x, apple_y = generate_apple_position()
        continue
       # 3. Handling the collision with the apple


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
"""# To be able to eat properly, the apple aligns with the grid. 
apple_x = random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE # The square is random
apple_y = random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
"""