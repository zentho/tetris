import pygame
import random
from constants import SHAPES, NEON_COLORS, MUSIC_PATH, CLEAR_SOUND_PATH

pygame.init()
W, H, S = 400, 800, 40
window = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
score = 0

pygame.display.set_caption("Tetris")
font = pygame.font.Font(None, 36)

pygame.mixer.music.load(MUSIC_PATH)
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
CLEAR_SOUND = pygame.mixer.Sound(CLEAR_SOUND_PATH)


def new_piece():
    return [random.choice(SHAPES), [W//S//2-2, 1], random.choice(NEON_COLORS)]


piece = new_piece()
board = [[0] * (W//S) for _ in range(H//S)]


def collides(piece, board):
    shape, (x, y), color = piece
    for r, row in enumerate(shape):
        for c, cell in enumerate(row):
            if cell:
                invalid_x = x + c < 0 or len(board[0]) <= x + c
                invalid_y = y + r < 0 or len(board) <= y + r
                if invalid_x or invalid_y or board[y + r][x + c]:
                    return True
    return False


def place(piece, board):
    shape, (x, y), color = piece
    for r, row in enumerate(shape):
        for c, cell in enumerate(row):
            if cell:
                board[y + r][x + c] = color


def clear(board):
    full_rows = [i for i, row in enumerate(board) if all(row)]
    for i in reversed(full_rows):
        del board[i]
    for _ in full_rows:
        board.insert(0, [0] * len(board[0]))
    return len(full_rows)


NORMAL_DROP = 500
FAST_DROP = 50

drop = pygame.USEREVENT + 1
pygame.time.set_timer(drop, NORMAL_DROP)
run = True

while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
        elif e.type == pygame.KEYDOWN:
            shape, (x, y), color = piece
            orig_x, orig_shape = x, [row[:] for row in shape]

            if e.key == pygame.K_DOWN:
                pygame.time.set_timer(drop, FAST_DROP)
            elif e.key == pygame.K_LEFT:
                piece[1][0] -= 1
                if collides(piece, board):
                    piece[1][0] = orig_x
            elif e.key == pygame.K_RIGHT:
                piece[1][0] += 1
                if collides(piece, board):
                    piece[1][0] = orig_x
            elif e.key == pygame.K_UP:
                rotated_shape = list(zip(*shape[::-1]))
                piece[0] = [list(row) for row in rotated_shape]
                if collides(piece, board):
                    piece[0] = orig_shape

        elif e.type == pygame.KEYUP:
            if e.key == pygame.K_DOWN:
                pygame.time.set_timer(drop, NORMAL_DROP)

        elif e.type == drop:
            piece[1][1] += 1
            if collides(piece, board):
                piece[1][1] -= 1
                place(piece, board)
                cleared = clear(board)
                if cleared:
                    CLEAR_SOUND.play()
                    score += cleared * 100
                piece = new_piece()
                if collides(piece, board):
                    run = False

    window.fill((0, 0, 0))
    grid_color = (50, 50, 50)

    for x_line in range(0, W, S):
        pygame.draw.line(window, grid_color, (x_line, 0), (x_line, H))

    for y_line in range(0, H, S):
        pygame.draw.line(window, grid_color, (0, y_line), (W, y_line))

    for r, row in enumerate(board):
        for c, val in enumerate(row):
            if val:
                dimensions = (c*S, r*S, S, S)
                pygame.draw.rect(window, val, dimensions, 0)
                pygame.draw.rect(window, (0, 0, 0), dimensions, 1)

    shape, (x, y), color = piece
    for rr, row in enumerate(shape):
        for cc, val in enumerate(row):
            if val:
                dimensions = ((x+cc)*S, (y+rr)*S, S, S)
                pygame.draw.rect(window, color, dimensions, 0)
                pygame.draw.rect(window, (0, 0, 0), dimensions, 1)

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    score_x = (W - score_text.get_width()) // 2
    window.blit(score_text, (score_x, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.mixer.music.fadeout(1000)
window.fill((0, 0, 0))
game_over_text = font.render("Game Over", True, (255, 0, 0))
score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
window.blit(game_over_text, ((W - game_over_text.get_width()) // 2, H//2 - 50))
window.blit(score_text, ((W - score_text.get_width()) // 2, H//2))
pygame.display.flip()
pygame.time.delay(3000)
pygame.quit()
