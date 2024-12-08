import os

SHAPES = [
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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

MUSIC_PATH = os.path.join(ASSETS_DIR, 'disfigure.mp3')
CLEAR_SOUND_PATH = os.path.join(ASSETS_DIR, 'clear.mp3')

NEON_COLORS = [
    (57, 255, 20),
    (255, 20, 147),
    (0, 191, 255),
    (255, 165, 0),
    (148, 0, 211),
    (255, 0, 255),
    (173, 255, 47),
    (255, 69, 0),
    (75, 0, 130),
    (0, 255, 255),
    (255, 255, 0)
]
