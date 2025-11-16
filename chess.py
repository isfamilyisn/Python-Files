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

# Initialize all pieces
pieces = []  # Changed from pawns to pieces to hold all piece types
selected_piece = None  # Currently selected piece
valid_moves = []       # List of (row, col) tuples for valid moves
blocked_moves = []     # List of (row, col) tuples for blocked moves
capture_moves = []     # List of (row, col) tuples for capture moves

# Base Piece class
class Piece:
    def __init__(self, color, row, col, piece_type):
        self.color = color  # 'white' or 'black'
        self.row = row
        self.col = col
        self.piece_type = piece_type  # 'pawn', 'rook', 'knight', 'bishop', 'queen', 'king'
        self.has_moved = False
    
    def draw(self, screen, x, y, size):
        center_x = x + size // 2
        center_y = y + size // 2
        
        # Determine piece color and outline color
        if self.color == 'white':
            piece_color = WHITE
            outline_color = BLACK
        else:
            piece_color = BLACK
            outline_color = WHITE
        
        # Draw different shapes for different pieces
        if self.piece_type == 'pawn':
            radius = size // 3
            pygame.draw.circle(screen, piece_color, (center_x, center_y), radius)
            pygame.draw.circle(screen, outline_color, (center_x, center_y), radius, 2)
        elif self.piece_type == 'rook':
            # Draw a rectangle
            rect_size = size // 2
            pygame.draw.rect(screen, piece_color, (center_x - rect_size//2, center_y - rect_size//2, rect_size, rect_size))
            pygame.draw.rect(screen, outline_color, (center_x - rect_size//2, center_y - rect_size//2, rect_size, rect_size), 2)
        elif self.piece_type == 'knight':
            # Draw a triangle
            points = [(center_x, center_y - size//3), (center_x - size//3, center_y + size//3), (center_x + size//3, center_y + size//3)]
            pygame.draw.polygon(screen, piece_color, points)
            pygame.draw.polygon(screen, outline_color, points, 2)
        elif self.piece_type == 'bishop':
            # Draw a diamond
            points = [(center_x, center_y - size//3), (center_x + size//3, center_y), (center_x, center_y + size//3), (center_x - size//3, center_y)]
            pygame.draw.polygon(screen, piece_color, points)
            pygame.draw.polygon(screen, outline_color, points, 2)
        elif self.piece_type == 'queen':
            # Draw a circle with a smaller circle on top
            radius = size // 3
            pygame.draw.circle(screen, piece_color, (center_x, center_y), radius)
            pygame.draw.circle(screen, outline_color, (center_x, center_y), radius, 2)
            # Crown
            small_radius = size // 6
            pygame.draw.circle(screen, piece_color, (center_x, center_y - size//4), small_radius)
            pygame.draw.circle(screen, outline_color, (center_x, center_y - size//4), small_radius, 2)
        elif self.piece_type == 'king':
            # Draw a circle with a cross on top
            radius = size // 3
            pygame.draw.circle(screen, piece_color, (center_x, center_y), radius)
            pygame.draw.circle(screen, outline_color, (center_x, center_y), radius, 2)
            # Cross
            cross_size = size // 4
            pygame.draw.line(screen, outline_color, (center_x, center_y - radius), (center_x, center_y - radius - cross_size), 2)
            pygame.draw.line(screen, outline_color, (center_x - cross_size//2, center_y - radius - cross_size//2), (center_x + cross_size//2, center_y - radius - cross_size//2), 2)

def get_piece_at(row, col):
    """Get the piece at a specific board position"""
    for piece in pieces:
        if piece.row == row and piece.col == col:
            return piece
    return None

def is_valid_board_position(row, col):
    """Check if a position is within board boundaries"""
    return 0 <= row < board_size and 0 <= col < board_size

def get_pawn_moves(piece):
    """Calculate all possible moves for a pawn"""
    moves = []
    direction = -1 if piece.color == 'white' else 1
    
    # Move 1 square forward
    new_row = piece.row + direction
    if is_valid_board_position(new_row, piece.col):
        moves.append((new_row, piece.col))
    
    # Move 2 squares forward on first move
    if not piece.has_moved:
        new_row = piece.row + (2 * direction)
        if is_valid_board_position(new_row, piece.col):
            moves.append((new_row, piece.col))
    
    return moves

def get_pawn_capture_moves(piece):
    """Calculate capture moves for a pawn (diagonal)"""
    moves = []
    direction = -1 if piece.color == 'white' else 1
    
    for col_offset in [-1, 1]:
        new_row = piece.row + direction
        new_col = piece.col + col_offset
        if is_valid_board_position(new_row, new_col):
            moves.append((new_row, new_col))
    
    return moves

def get_rook_moves(piece):
    """Calculate all possible moves for a rook (horizontal and vertical)"""
    moves = []
    # Horizontal moves
    for col_offset in [-1, 1]:
        for i in range(1, board_size):
            new_col = piece.col + (col_offset * i)
            if not is_valid_board_position(piece.row, new_col):
                break
            moves.append((piece.row, new_col))
            if get_piece_at(piece.row, new_col) is not None:
                break
    
    # Vertical moves
    for row_offset in [-1, 1]:
        for i in range(1, board_size):
            new_row = piece.row + (row_offset * i)
            if not is_valid_board_position(new_row, piece.col):
                break
            moves.append((new_row, piece.col))
            if get_piece_at(new_row, piece.col) is not None:
                break
    
    return moves

def get_knight_moves(piece):
    """Calculate all possible moves for a knight (L-shaped)"""
    moves = []
    knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    
    for row_offset, col_offset in knight_moves:
        new_row = piece.row + row_offset
        new_col = piece.col + col_offset
        if is_valid_board_position(new_row, new_col):
            moves.append((new_row, new_col))
    
    return moves

def get_bishop_moves(piece):
    """Calculate all possible moves for a bishop (diagonal)"""
    moves = []
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    for row_offset, col_offset in directions:
        for i in range(1, board_size):
            new_row = piece.row + (row_offset * i)
            new_col = piece.col + (col_offset * i)
            if not is_valid_board_position(new_row, new_col):
                break
            moves.append((new_row, new_col))
            if get_piece_at(new_row, new_col) is not None:
                break
    
    return moves

def get_queen_moves(piece):
    """Calculate all possible moves for a queen (rook + bishop)"""
    moves = []
    moves.extend(get_rook_moves(piece))
    moves.extend(get_bishop_moves(piece))
    return moves

def get_king_moves(piece):
    """Calculate all possible moves for a king (one square in any direction)"""
    moves = []
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    for row_offset, col_offset in directions:
        new_row = piece.row + row_offset
        new_col = piece.col + col_offset
        if is_valid_board_position(new_row, new_col):
            moves.append((new_row, new_col))
    
    return moves

def check_moves(piece):
    """Check all possible moves and categorize them as valid, blocked, or capture"""
    global valid_moves, blocked_moves, capture_moves
    valid_moves = []
    blocked_moves = []
    capture_moves = []
    
    # Get possible moves based on piece type
    if piece.piece_type == 'pawn':
        possible_moves = get_pawn_moves(piece)
        direction = -1 if piece.color == 'white' else 1
        
        for move_row, move_col in possible_moves:
            if not is_valid_board_position(move_row, move_col):
                blocked_moves.append((move_row, move_col))
                continue
            
            # Check if there's a piece blocking the path (for 2-square move)
            if abs(move_row - piece.row) == 2:
                intermediate_row = piece.row + direction
                if get_piece_at(intermediate_row, move_col) is not None:
                    blocked_moves.append((move_row, move_col))
                    continue
            
            piece_at_dest = get_piece_at(move_row, move_col)
            if piece_at_dest is not None:
                blocked_moves.append((move_row, move_col))
            else:
                valid_moves.append((move_row, move_col))
        
        # Check capture moves for pawn
        capture_positions = get_pawn_capture_moves(piece)
        for move_row, move_col in capture_positions:
            piece_at_dest = get_piece_at(move_row, move_col)
            if piece_at_dest is not None and piece_at_dest.color != piece.color:
                capture_moves.append((move_row, move_col))
    
    else:
        # For other pieces, get their moves
        if piece.piece_type == 'rook':
            possible_moves = get_rook_moves(piece)
        elif piece.piece_type == 'knight':
            possible_moves = get_knight_moves(piece)
        elif piece.piece_type == 'bishop':
            possible_moves = get_bishop_moves(piece)
        elif piece.piece_type == 'queen':
            possible_moves = get_queen_moves(piece)
        elif piece.piece_type == 'king':
            possible_moves = get_king_moves(piece)
        else:
            possible_moves = []
        
        for move_row, move_col in possible_moves:
            if not is_valid_board_position(move_row, move_col):
                blocked_moves.append((move_row, move_col))
                continue
            
            piece_at_dest = get_piece_at(move_row, move_col)
            if piece_at_dest is None:
                valid_moves.append((move_row, move_col))
            elif piece_at_dest.color != piece.color:
                capture_moves.append((move_row, move_col))
            else:
                blocked_moves.append((move_row, move_col))

def get_board_position_from_mouse(mouse_x, mouse_y):
    """Convert mouse coordinates to board row and column"""
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
        if selected_piece is not None:
            if (row, col) in valid_moves:
                move_piece(selected_piece, row, col)
                selected_piece = None
                valid_moves = []
                blocked_moves = []
                capture_moves = []
                return
            elif (row, col) in capture_moves:
                captured_piece = get_piece_at(row, col)
                if captured_piece is not None:
                    pieces.remove(captured_piece)
                move_piece(selected_piece, row, col)
                selected_piece = None
                valid_moves = []
                blocked_moves = []
                capture_moves = []
                return
        
        piece = get_piece_at(row, col)
        if piece is not None:
            selected_piece = piece
            check_moves(selected_piece)
        else:
            selected_piece = None
            valid_moves = []
            blocked_moves = []
            capture_moves = []

def draw_highlights(screen):
    """Draw green highlights for valid moves, red for blocked moves, and purple for capture moves"""
    for row, col in valid_moves:
        x = board_x + col * tile_size
        y = board_y + row * tile_size
        highlight = pygame.Surface((tile_size, tile_size))
        highlight.set_alpha(HIGHLIGHT_ALPHA)
        highlight.fill(GREEN)
        screen.blit(highlight, (x, y))
    
    for row, col in blocked_moves:
        x = board_x + col * tile_size
        y = board_y + row * tile_size
        highlight = pygame.Surface((tile_size, tile_size))
        highlight.set_alpha(HIGHLIGHT_ALPHA)
        highlight.fill(RED)
        screen.blit(highlight, (x, y))
    
    for row, col in capture_moves:
        x = board_x + col * tile_size
        y = board_y + row * tile_size
        highlight = pygame.Surface((tile_size, tile_size))
        highlight.set_alpha(HIGHLIGHT_ALPHA)
        highlight.fill(PURPLE)
        screen.blit(highlight, (x, y))

def setupBoard():
    """Setup the board with all pieces in starting positions"""
    pieces.clear()
    
    # White pieces (bottom, rows 6-7)
    # Pawns (row 6)
    for col in range(8):
        pieces.append(Piece('white', 6, col, 'pawn'))
    
    # Back row (row 7)
    pieces.append(Piece('white', 7, 0, 'rook'))
    pieces.append(Piece('white', 7, 1, 'knight'))
    pieces.append(Piece('white', 7, 2, 'bishop'))
    pieces.append(Piece('white', 7, 3, 'queen'))
    pieces.append(Piece('white', 7, 4, 'king'))
    pieces.append(Piece('white', 7, 5, 'bishop'))
    pieces.append(Piece('white', 7, 6, 'knight'))
    pieces.append(Piece('white', 7, 7, 'rook'))
    
    # Black pieces (top, rows 0-1)
    # Pawns (row 1)
    for col in range(8):
        pieces.append(Piece('black', 1, col, 'pawn'))
    
    # Back row (row 0)
    pieces.append(Piece('black', 0, 0, 'rook'))
    pieces.append(Piece('black', 0, 1, 'knight'))
    pieces.append(Piece('black', 0, 2, 'bishop'))
    pieces.append(Piece('black', 0, 3, 'queen'))
    pieces.append(Piece('black', 0, 4, 'king'))
    pieces.append(Piece('black', 0, 5, 'bishop'))
    pieces.append(Piece('black', 0, 6, 'knight'))
    pieces.append(Piece('black', 0, 7, 'rook'))

def draw_all_pieces(screen, pieces_list, board_x, board_y, tile_size):
    """Draw all pieces on the board"""
    for piece in pieces_list:
        x = board_x + piece.col * tile_size
        y = board_y + piece.row * tile_size
        piece.draw(screen, x, y, tile_size)

# Game loop
setupBoard()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                handle_piece_selection(mouse_x, mouse_y)

    screen.fill((50, 50, 50))

    # Draw chess board
    for row in range(board_size):
        for col in range(board_size):
            if (row + col) % 2 == 0:
                tile_color = WHITE
            else:
                tile_color = BLACK
            
            x = board_x + col * tile_size
            y = board_y + row * tile_size
            pygame.draw.rect(screen, tile_color, (x, y, tile_size, tile_size))

    # Draw highlights
    if selected_piece is not None:
        draw_highlights(screen)

    # Draw all pieces
    draw_all_pieces(screen, pieces, board_x, board_y, tile_size)

    pygame.display.flip()

pygame.quit()