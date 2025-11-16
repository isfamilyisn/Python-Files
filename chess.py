import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Chess Board")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Chess board parameters
board_size = 8  # 8x8 chess board
tile_size = min(screen_width, screen_height) // 10  # Calculate tile size based on screen
board_pixel_size = tile_size * board_size  # Total board size in pixels

# Calculate board position to center it
board_x = (screen_width - board_pixel_size) // 2
board_y = (screen_height - board_pixel_size) // 2

# Initialize pawns
pawns = []

# Pawn class to represent chess pieces
class Pawn:
    def __init__(self, color, row, col):
        self.color = color  # 'white' or 'black'
        self.row = row
        self.col = col
    
    def draw(self, screen, x, y, size):
        # Draw a simple circle for the pawn
        center_x = x + size // 2
        center_y = y + size // 2
        radius = size // 3
        
        # Draw pawn body
        pygame.draw.circle(screen, self.color, (center_x, center_y), radius)
        # Draw outline
        
        # Determine pawn color and outline color
        if self.color == 'white':
            pawn_color = WHITE
            outline_color = BLACK
        else:
            pawn_color = BLACK
            outline_color = WHITE

        # Draw pawn body
        pygame.draw.circle(screen, pawn_color, (center_x, center_y), radius)
        # Draw outline
        pygame.draw.circle(screen, outline_color, (center_x, center_y), radius, 2)

def setupBoard():
    # Create 8 white pawns on row 6 (rank 2 in chess notation)
    for col in range(8):
        pawns.append(Pawn('white', 6, col))

    # Create 8 black pawns on row 1 (rank 7 in chess notation)
    for col in range(8):
        pawns.append(Pawn('black', 1, col))

# Game loop
setupBoard()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill background
    screen.fill((50, 50, 50))  # Dark grey background

    # Draw chess board
    for row in range(board_size):
        for col in range(board_size):
            # Alternate colors: if row + col is even, use white; if odd, use black
            if (row + col) % 2 == 0:
                tile_color = WHITE
            else:
                tile_color = BLACK
            
            # Calculate tile position
            x = board_x + col * tile_size
            y = board_y + row * tile_size
            
            # Draw the tile
            pygame.draw.rect(screen, tile_color, (x, y, tile_size, tile_size))

    # Draw pawns
    for pawn in pawns:
        x = board_x + pawn.col * tile_size
        y = board_y + pawn.row * tile_size
        pawn.draw(screen, x, y, tile_size)

    # Update display
    pygame.display.flip()

pygame.quit()