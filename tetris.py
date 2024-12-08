import pygame
import random

pygame.init()

W, H, S = 400, 800, 40

window = pygame.window.set_mode((W, H))
clock = pygame.time.Clock()
pygame.display.set_caption("Tetris")
