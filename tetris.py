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
     [0, 1, 1]]
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
            invalid_x = x + c < 0 or len(board[0]) <= x + c
            invalid_y = y + r < 0 or len(board) <= y + r
            if invalid_x or invalid_y or cell:
                return True

    return False


def place(piece, board):
    shape, (x, y), color = piece

    for r, row in enumerate(shape):
        for c, cell in enumerate(row):
            if cell:
                board[y + r][x + c] = color


def clear(board):
