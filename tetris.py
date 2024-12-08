import pygame
import random

pygame.init()
W, H, S = 400, 800, 40
window = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
pygame.display.set_caption("Tetris")
font = pygame.font.Font(None, 36)
score = 0

shapes = [
    [[1, 1, 1, 1]],
    [[0, 1, 1],
     [1, 1, 0]],
    [[1, 1, 0],
     [0, 1, 1]],
    [[0, 1, 0],
     [1, 1, 1]],
    [[1, 1, 1],
     [0, 0, 1]],
    [[1, 1, 1],
     [1, 0, 0]],
    [[1, 1],
     [1, 1]]
]


def random_color():
    return [random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)]


def new_piece():
    return [random.choice(shapes), [W//S//2-2, 1], random_color()]


piece = new_piece()
board = [[0] * (W//S) for _ in range(H//S)]


def collides(piece, board):
    shape, (x, y), color = piece

    for r, row in enumerate(shape):
        for c, cell in enumerate(row):
            if cell:
                invalid_x = x + c < 0 or len(board[0]) <= x + c
                invalid_y = y + r < 0 or len(board) <= y + r
                if invalid_x or invalid_y:
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


def handle_drop(board):
    global piece, run, score
    piece[1][1] += 1
    if collides(piece, board):
        piece[1][1] -= 1
        place(piece, board)
        cleared = clear(board)
        if cleared:
            score += cleared * 100
        piece = new_piece()
        if collides(piece, board):
            run = False


drop = pygame.USEREVENT + 1
pygame.time.set_timer(drop, 500)
run = True

while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        elif (e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN) or e.type == drop:
            handle_drop(board)

        elif e.type == pygame.KEYDOWN:
            shape, (x, y), color = piece
            orig_x, orig_shape = x, [row[:] for row in shape]

            if e.key == pygame.K_LEFT:
                piece[1][0] -= 1
            elif e.key == pygame.K_RIGHT:
                piece[1][0] += 1
            elif e.key == pygame.K_UP:
                rotated_shape = list(zip(*shape[::-1]))
                piece[0] = [list(row) for row in rotated_shape]

            if collides(piece, board):
                piece[1][0] = orig_x
                shape = orig_shape

    window.fill((0, 0, 0))

    for r, row in enumerate(board):
        for c, val in enumerate(row):
            if val:
                pygame.draw.rect(window, val, (c*S, r*S, S, S), 0)

    shape, (x, y), color = piece
    for rr, row in enumerate(shape):
        for cc, val in enumerate(row):
            if val:
                pygame.draw.rect(window, color, ((x+cc)*S, (y+rr)*S, S, S), 0)

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    score_x = (W - score_text.get_width()) // 2
    window.blit(score_text, (score_x, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
