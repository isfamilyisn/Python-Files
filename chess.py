import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Grid Example")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRID_COLOR = (100, 100, 100) # A darker grey for grid lines

# Grid parameters
tile_size = 40

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill background
    screen.fill(BLACK)

    # Draw grid lines
    for x in range(0, screen_width, tile_size):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, screen_height))
    for y in range(0, screen_height, tile_size):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (screen_width, y))

    # Update display
    pygame.display.flip()

pygame.quit()