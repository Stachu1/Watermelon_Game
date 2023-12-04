import pygame, sys, time
from fruit import Fruit

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Watermelon Game")

# Clock to control the frame rate
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)


fruits = [Fruit(WIDTH/2, 0, 1)]
frame_time = 1/60
can_spawn = True

# Game loop
running = True
while running:
    frame_start_time = pygame.time.get_ticks()
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    mouse_x, mouse_y = pygame.mouse.get_pos()
    left_button, _, right_button = pygame.mouse.get_pressed()
    
    
    # Update game state
    
    if left_button and can_spawn:
        fruits[-1].is_held = False
        fruits.append(Fruit(WIDTH/2, 0, 1))
        can_spawn = False
        
    elif not left_button and not can_spawn:
        can_spawn = True
    
    
    fruits[-1].pos.x = mouse_x
    
    
    for fruit in fruits:
        if not fruit.is_held:
            fruit.update_box_collision(WIDTH, HEIGHT)
    
    
    ft_s = frame_time/1000
    for fruit in fruits:
        if not fruit.is_held:
            fruit.update_free_fall(ft_s)


    for index_f1, fruit_1 in enumerate(fruits):
        for index_f2, fruit_2 in enumerate(fruits):
            if fruit_1 == fruit_2:
                continue
            
            if fruit_1.is_held or fruit_2.is_held:
                continue
            
            result = fruit_1.update_fruit_fruit_collision(fruit_2)
            if result is not None:
                fruits.remove(fruit_1)
                fruits.remove(fruit_2)
                fruits.insert(0, result)
                break


    # Draw everything
    screen.fill(BLACK)
    
    
    for fruit in fruits:
        fruit.draw(screen)
        
    # Render the frame time
    screen.blit(font.render(f"{frame_time} ms", True, WHITE), (10, 10))

    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    # clock.tick(FPS)
    
    # Calculate the frame time
    frame_time = (pygame.time.get_ticks() - frame_start_time)
    
    

# Quit the game
pygame.quit()
sys.exit()