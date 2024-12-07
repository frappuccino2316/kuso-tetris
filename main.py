import pygame
import random

pygame.init()
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE
FPS = 3

SHAPES = [
    [["1", "1", "1", "1"]],  # I
    [["1", "1"], ["1", "1"]],  # O
    [["", "1", ""], ["1", "1", "1"]],  # T
    [["1", "", ""], ["1", "1", "1"]],  # L
    [["", "", "1"], ["1", "1", "1"]],  # J
    [["", "1", "1"], ["1", "1", ""]],  # S
    [["1", "1", ""], ["", "1", "1"]]   # Z
]
PIECE_LABELS = ['K', 'U', 'S', 'O']

class Block:
    def __init__(self):
        index = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[index]
        new_shape = []
        for l in self.shape:
            new_part = []
            for s in l:
                if s == "1":
                    text = random.choice(PIECE_LABELS)
                    new_part.append(text)
                else:
                    new_part.append("")
            new_shape.append(new_part)
        self.shape = new_shape
        self.text = random.choice(PIECE_LABELS)
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

def check_collision(grid, piece, offset):
    off_x, off_y = offset
    for y, row in enumerate(piece):
        for x, cell in enumerate(row):
            if cell:
                if (y + off_y >= len(grid) or
                    x + off_x < 0 or
                    x + off_x >= len(grid[0]) or
                    (y + off_y >= 0 and grid[y + off_y][x + off_x])):
                    return True
    return False

def merge_grid(grid, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                grid[y + off_y][x + off_x] = cell

def clear(original_grid):
    new_grid = original_grid
    for row_index in range(len(original_grid) - 1, 2, -1):
        for i, cell in enumerate(original_grid[row_index]):
            # 縦列の判定
            if original_grid[row_index][i] == "K" and original_grid[row_index - 1][i] == "U" and original_grid[row_index - 2][i] == "S" and original_grid[row_index - 3][i] == "O":
                new_grid[row_index][i] = ""
                new_grid[row_index - 1][i] = ""
                new_grid[row_index - 2][i] = ""
                new_grid[row_index - 3][i] = ""
            elif original_grid[row_index][i] == "O" and original_grid[row_index - 1][i] == "S" and original_grid[row_index - 2][i] == "U" and original_grid[row_index - 3][i] == "K":
                new_grid[row_index][i] = ""
                new_grid[row_index - 1][i] = ""
                new_grid[row_index - 2][i] = ""
                new_grid[row_index - 3][i] = ""

            # 横列の判定
            elif i > len(original_grid[row_index]) - 4:
                break
            elif original_grid[row_index][i] == "K" and original_grid[row_index][i + 1] == "U" and original_grid[row_index][i + 2] == "S" and original_grid[row_index][i + 3] == "O":
                new_grid[row_index][i] = ""
                new_grid[row_index][i + 1] = ""
                new_grid[row_index][i + 2] = ""
                new_grid[row_index][i + 3] = ""
            elif original_grid[row_index][i] == "O" and original_grid[row_index][i + 1] == "S" and original_grid[row_index][i + 2] == "U" and original_grid[row_index][i + 3] == "K":
                new_grid[row_index][i] = ""
                new_grid[row_index][i + 1] = ""
                new_grid[row_index][i + 2] = ""
                new_grid[row_index][i + 3] = ""

    # 消えた分を下に詰める
    dropped_grid = [[""] * len(original_grid[0]) for _ in range(len(original_grid))]
    for i, _ in enumerate(original_grid[0]):
        # 縦列の空白じゃない値を全て集める
        columns = []
        for j in range(len(original_grid) - 1, -1, -1):
            if new_grid[j][i] != "":
                columns.append(new_grid[j][i])
        
        for index, t in enumerate(columns):
            dropped_grid[len(new_grid) - 1 - index][i] = t

    return dropped_grid

def draw_grid(screen, grid, offset=(0, 0)):
    off_x, off_y = offset
    font = pygame.font.Font(None, BLOCK_SIZE) 
    
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                text_surface = font.render(str(cell), True, (255, 255, 255))  # 白色の文字
                text_rect = text_surface.get_rect(
                    center=((x + off_x) * BLOCK_SIZE + BLOCK_SIZE // 2, 
                            (y + off_y) * BLOCK_SIZE + BLOCK_SIZE // 2)
                )
                screen.blit(text_surface, text_rect)


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    grid = [[""] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    current_piece = Block()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not check_collision(grid, current_piece.shape, (current_piece.x - 1, current_piece.y)):
                        current_piece.x -= 1
                elif event.key == pygame.K_RIGHT:
                    if not check_collision(grid, current_piece.shape, (current_piece.x + 1, current_piece.y)):
                        current_piece.x += 1
                elif event.key == pygame.K_DOWN:
                    if not check_collision(grid, current_piece.shape, (current_piece.x, current_piece.y + 1)):
                        current_piece.y += 1
                elif event.key == pygame.K_UP:
                    rotated = [list(row) for row in zip(*current_piece.shape[::-1])]
                    if not check_collision(grid, rotated, (current_piece.x, current_piece.y)):
                        current_piece.rotate()

        if not check_collision(grid, current_piece.shape, (current_piece.x, current_piece.y + 1)):
            current_piece.y += 1
        else:
            merge_grid(grid, current_piece.shape, (current_piece.x, current_piece.y))
            grid = clear(grid)
            draw_grid(screen, grid)
            current_piece = Block()
            if check_collision(grid, current_piece.shape, (current_piece.x, current_piece.y)):
                running = False

        screen.fill((0, 0, 0))
        draw_grid(screen, grid)
        draw_grid(screen, [[cell for cell in row] for row in current_piece.shape], (current_piece.x, current_piece.y))
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
