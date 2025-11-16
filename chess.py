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
GREEN = (0, 255, 0)  # Valid move highlight
RED = (255, 0, 0)    # Blocked move highlight
PURPLE = (128, 0, 128)  # Capture move highlight
HIGHLIGHT_ALPHA = 128  # Semi-transparent highlight

# Chess board parameters
board_size = 8  # 8x8 chess board
tile_size = min(screen_width, screen_height) // 10  # Calculate tile size based on screen
board_pixel_size = tile_size * board_size  # Total board size in pixels

# Calculate board position to center it
board_x = (screen_width - board_pixel_size) // 2
board_y = (screen_height - board_pixel_size) // 2

# Initialize pawns
pawns = []
selected_piece = None  # Currently selected piece
valid_moves = []       # List of (row, col) tuples for valid moves
blocked_moves = []     # List of (row, col) tuples for blocked moves
capture_moves = []     # List of (row, col) tuples for capture moves

# Pawn class to represent chess pieces
class Pawn:
    def __init__(self, color, row, col):
        self.color = color  # 'white' or 'black'
        self.row = row
        self.col = col
        self.has_moved = False
    
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

def get_piece_at(row, col):
    """Get the piece at a specific board position"""
    for pawn in pawns:
        if pawn.row == row and pawn.col == col:
            return pawn
    return None

def is_valid_board_position(row, col):
    """Check if a position is within board boundaries"""
    return 0 <= row < board_size and 0 <= col < board_size

def get_pawn_possible_moves(pawn):
    """Calculate all possible moves for a pawn (without checking if blocked)"""
    moves = []
    direction = -1 if pawn.color == 'white' else 1  # White moves up, black moves down
    
    # Move 1 square forward
    new_row = pawn.row + direction
    if is_valid_board_position(new_row, pawn.col):
        moves.append((new_row, pawn.col))
    
    # Move 2 squares forward on first move
    if not pawn.has_moved:
        new_row = pawn.row + (2 * direction)
        if is_valid_board_position(new_row, pawn.col):
            moves.append((new_row, pawn.col))
    
    return moves

def get_pawn_capture_moves(pawn):
    """Calculate all possible capture moves for a pawn (diagonal)"""
    moves = []
    direction = -1 if pawn.color == 'white' else 1  # White moves up, black moves down
    
    # Diagonal captures: left and right
    for col_offset in [-1, 1]:
        new_row = pawn.row + direction
        new_col = pawn.col + col_offset
        if is_valid_board_position(new_row, new_col):
            moves.append((new_row, new_col))
    
    return moves

def check_moves(pawn):
    """Check all possible moves and categorize them as valid, blocked, or capture"""
    global valid_moves, blocked_moves, capture_moves
    valid_moves = []
    blocked_moves = []
    capture_moves = []
    
    # Check forward moves
    possible_moves = get_pawn_possible_moves(pawn)
    direction = -1 if pawn.color == 'white' else 1
    
    for move_row, move_col in possible_moves:
        # Check if move is within board boundaries
        if not is_valid_board_position(move_row, move_col):
            blocked_moves.append((move_row, move_col))
            continue
        
        # Check if there's a piece blocking the path
        # For 2-square move, check both squares
        if abs(move_row - pawn.row) == 2:
            # Check intermediate square
            intermediate_row = pawn.row + direction
            if get_piece_at(intermediate_row, move_col) is not None:
                blocked_moves.append((move_row, move_col))
                continue
        
        # Check destination square
        piece_at_dest = get_piece_at(move_row, move_col)
        if piece_at_dest is not None:
            blocked_moves.append((move_row, move_col))
        else:
            valid_moves.append((move_row, move_col))
    
    # Check capture moves (diagonal)
    capture_positions = get_pawn_capture_moves(pawn)
    for move_row, move_col in capture_positions:
        piece_at_dest = get_piece_at(move_row, move_col)
        if piece_at_dest is not None and piece_at_dest.color != pawn.color:
            # There's an opponent piece that can be captured
            capture_moves.append((move_row, move_col))
        # If no piece or same color piece, don't highlight (not a valid capture)


def get_board_position_from_mouse(mouse_x, mouse_y):
    """Convert mouse coordinates to board row and column"""
    # Check if click is within board boundaries
    if (board_x <= mouse_x < board_x + board_pixel_size and
        board_y <= mouse_y < board_y + board_pixel_size):
        col = (mouse_x - board_x) // tile_size
        row = (mouse_y - board_y) // tile_size
        return row, col
    return None, None

def move_piece(piece, new_row, new_col):
    """Move a piece to a new position"""
    piece.row = new_row
    piece.col = new_col
    if not piece.has_moved:
        piece.has_moved = True

def handle_piece_selection(mouse_x, mouse_y):
    """Handle clicking on a piece to select it, or moving to a valid square"""
    global selected_piece, valid_moves, blocked_moves, capture_moves
    row, col = get_board_position_from_mouse(mouse_x, mouse_y)
    
    if row is not None and col is not None:
        # If a piece is already selected, check if clicking on a valid move
        if selected_piece is not None:
            # Check if clicking on a valid move (green highlight)
            if (row, col) in valid_moves:
                move_piece(selected_piece, row, col)
                selected_piece = None
                valid_moves = []
                blocked_moves = []
                capture_moves = []
                return
            # Check if clicking on a capture move (purple highlight)
            elif (row, col) in capture_moves:
                # Remove the captured piece
                captured_piece = get_piece_at(row, col)
                if captured_piece is not None:
                    pawns.remove(captured_piece)
                move_piece(selected_piece, row, col)
                selected_piece = None
                valid_moves = []
                blocked_moves = []
                capture_moves = []
                return
        
        # Handle piece selection or deselection
        piece = get_piece_at(row, col)
        if piece is not None:
            selected_piece = piece
            check_moves(selected_piece)
        else:
            # Clicked on empty square - deselect
            selected_piece = None
            valid_moves = []
            blocked_moves = []
            capture_moves = []

def draw_highlights(screen):
    """Draw green highlights for valid moves, red for blocked moves, and purple for capture moves"""
    # Draw valid moves in green
    for row, col in valid_moves:
        x = board_x + col * tile_size
        y = board_y + row * tile_size
        # Create a semi-transparent green surface
        highlight = pygame.Surface((tile_size, tile_size))
        highlight.set_alpha(HIGHLIGHT_ALPHA)
        highlight.fill(GREEN)
        screen.blit(highlight, (x, y))
    
    # Draw blocked moves in red
    for row, col in blocked_moves:
        x = board_x + col * tile_size
        y = board_y + row * tile_size
        # Create a semi-transparent red surface
        highlight = pygame.Surface((tile_size, tile_size))
        highlight.set_alpha(HIGHLIGHT_ALPHA)
        highlight.fill(RED)
        screen.blit(highlight, (x, y))
    
    # Draw capture moves in purple
    for row, col in capture_moves:
        x = board_x + col * tile_size
        y = board_y + row * tile_size
        # Create a semi-transparent purple surface
        highlight = pygame.Surface((tile_size, tile_size))
        highlight.set_alpha(HIGHLIGHT_ALPHA)
        highlight.fill(PURPLE)
        screen.blit(highlight, (x, y))

def setupBoard():
    """setup the board"""
    # Create 8 white pawns on row 6 (rank 2 in chess notation)
    for col in range(8):
        pawns.append(Pawn('white', 4, col))

    # Create 8 black pawns on row 1 (rank 7 in chess notation)
    for col in range(8):
        pawns.append(Pawn('black', 1, col))

def draw_all_pawns(screen, pawns_list, board_x, board_y, tile_size):
    """Draw all pawns on the board"""
    for pawn in pawns_list:
        x = board_x + pawn.col * tile_size
        y = board_y + pawn.row * tile_size
        pawn.draw(screen, x, y, tile_size)

# Game loop
setupBoard()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = event.pos
                handle_piece_selection(mouse_x, mouse_y)

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

    # Draw highlights for selected piece
    if selected_piece is not None:
        draw_highlights(screen)

    # Draw pawns
    draw_all_pawns(screen, pawns, board_x, board_y, tile_size)

    # Update display
    pygame.display.flip()

pygame.quit()