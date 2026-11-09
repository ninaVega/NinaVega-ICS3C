import random, pygame, math, os, time

# Set up the screen 
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Initialize Pygame
pygame.init()
pygame.mixer.init() 

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch the apples!")

CELL_SIZE = 30  # Each grid square will be 30x30 pixels

# Set up colours
WHITE = (255, 255, 255)
BLUE = (51, 153, 255) 
RED = (204, 0, 0) 
DARK_GREEN = (34, 139, 34)  # The grass
YELLOW = (255, 220, 0)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)  # The sky
BROWN = (102, 51, 0)

font = pygame.font.Font(None, 36) # Creating font sizes for displaying
small_font = pygame.font.Font(None, 25)

# Set up the player
basket_x = 270
basket_y = 340
basket_width = 90
basket_height = 30
basket_speed = 8

# lists that store the falling apples and power-ups
apples = [] # Stores all falling apples
power_ups = [] # Stoes all falling stars

# Game Variables
score = 0 # Number of apples caught
lives = 3 # Number of chances remaining
level = 1 # Difficulty level, the apples fall faster
game_state = "menu" # To determine which screen is being displayed
frame_count = 0 # Counts how manyframes hasve passed

# Set up the game
clock = pygame.time.Clock() # Control the rate at which frames change
running = True # Keeps the game looping

# Set up the music
pygame.mixer.music.load("mario_basic_sound.mp3") # load the music in the background

power_up_sound = pygame.mixer.Sound("mario_power-up_sound.mp3")
game_over_sound = pygame.mixer.Sound("game_over_sound.mp3")

# Function 1: Choose random position
def new_position(): # the apples and stars appear at random positions, always aligned with the grid
    """Choose a random horizontal position on the grid"""
    return random.randint(0, (SCREEN_WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE

# Function 2 ; Reset the game
def reset_game():
    """Reset the player, score, lives and falling object"""
    global basket_x, apples, power_ups # to change the variables we created out of the function
    global score, lives, level, frame_count, game_state

    basket_x = 270
    apples = [] # list back to not having anything
    power_ups = []
    score = 0
    lives = 3
    level = 1
    frame_count = 0  
    game_state = "playing"

    pygame.mixer.music.play(-1)

# Function 3: Display the text
def draw_text(message, x, y, colour, text_font):
    """Display a message at chosen position"""
    text = text_font.render(message, True, colour) # for the text to be displayed in pygame
    screen.blit(text, (x, y)) # place the text on the screen, x/y determine the position

#  Function 4: Draw a cloud
def draw_cloud(x, y): # Creating a cloud that overlaps 3 cirles
    """Draw a cloud that is 3 cirlcles close together"""
    pygame.draw.circle(screen, WHITE, (x, y), 25)
    pygame.draw.circle(screen, WHITE, (x + 25, y - 5), 35)
    pygame.draw.circle(screen, WHITE, (x + 50, y), 25)

# Function 5:Draw a star for the power-up
def draw_pygame_star(x, y, num_points, outer_radius, inner_radius, color):
    """Draw a star with math propreties in pygame"""
    points = [] # Empty list to store the points of the stars
    for i in range(num_points * 2): #creating both inner and outer points
        radius = outer_radius if i % 2 == 0 else inner_radius
        angle = i * math.pi / num_points - math.pi / 2  # aligns the point facing up
        pt_x = x + math.cos(angle) * radius #horizontal coordinates
        pt_y = y + math.sin(angle) * radius # vertical coordinates
        points.append((pt_x, pt_y)) # adds all the coordinates to the list
    pygame.draw.polygon(screen, color, points)

# MAIN LOOP -
while running: 
    
    # 1. Handling events and keyboard input
    for event in pygame.event.get(): #Checks for events (keys being pressed)
        if event.type == pygame.QUIT: # The game stops when screen in closed
            running = False
      
        if event.type == pygame.KEYDOWN:# Check a key being pressed
            if event.key == pygame.K_ESCAPE: # the escape key closes the game
                running = False
            
            if event.key == pygame.K_SPACE: # the space key starts a new game
                if game_state == "menu" or game_state == "gameover": # From menu or second chance
                    reset_game()

    # Get the keys being pressed
    keys = pygame.key.get_pressed() # check what key is currently being pressed

    if game_state == "playing":
        frame_count += 1

        # Move the basket
        if keys[pygame.K_LEFT]: # left arrow moves backet to left
            basket_x -= basket_speed # subtracts from the position
        if keys[pygame.K_RIGHT]: # right arrow moves the backet to the right
            basket_x += basket_speed # adds to the posiotion

        # Keep basket inside of the screen 
        basket_x = max(0, min(basket_x, SCREEN_WIDTH - basket_width))
                   # max()to not go too far on the lft
                   # min() prevents from going too far to the right
        
        # basket_rect being defined before checking collisions
        basket_rect = pygame.Rect(basket_x, basket_y, basket_width, basket_height)
                   # invisible rectangle around basket as 'shield'
        
        # Apples 
        if frame_count % max(15, 45 - level * 3) == 0: #
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

        # Move power-ups (the stars) and check collisions
        for power_up in power_ups[:]:
            power_up[1] += 3

            power_rect = pygame.Rect(power_up[0], power_up[1], CELL_SIZE, CELL_SIZE)
            

            if basket_rect.colliderect(power_rect):
                power_ups.remove(power_up)
                lives = min(lives + 1, 5)
                power_up_sound.play()
            elif power_up[1] > SCREEN_HEIGHT:
                power_ups.remove(power_up)
    
        # Check game over
        if lives <= 0:
            game_state = "gameover"
            pygame.mixer.music.stop()
            game_over_sound.play()

    
    # 3. Draw everything
    screen.fill(SKY_BLUE)

    # Nuages de fond totalement fixes
    draw_cloud(80, 80)
    draw_cloud(420, 100)

    # grass at the bottom of the screen (hauteur 40 pixels)
    pygame.draw.rect(screen, DARK_GREEN, (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40))

    if game_state == "menu":
        menu_bg = pygame.Surface((400, 180))
        menu_bg.set_alpha(150)
        menu_bg.fill(BLACK)
        screen.blit(menu_bg, (100, 100))

        draw_text("CATCH THE APPLES!", 180, 120, WHITE, font)
        draw_text("Press SPACE to start", 220, 190, YELLOW, small_font)
        draw_text("Use LEFT and RIGHT arrows", 195, 225, WHITE, small_font)

    elif game_state == "playing":
        # Draw the basket
        pygame.draw.rect(screen, BROWN, (basket_x, basket_y, basket_width, basket_height))

        # Draw apples
        for apple in apples:
            pygame.draw.circle(
                screen, RED,
                (apple[0] + CELL_SIZE // 2, apple[1] + CELL_SIZE // 2),
                CELL_SIZE // 2
            )

        # Drawing stars 
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

        draw_text("GAME OVER!", 220, 120, RED, font)
        draw_text("Final score: " + str(score), 235, 170, WHITE, small_font)
        draw_text("Press SPACE to play again", 195, 220, YELLOW, small_font)

    pygame.display.flip()
    clock.tick(40)

pygame.quit()
