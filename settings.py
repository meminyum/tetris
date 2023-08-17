import pygame as pg

vec = pg.math.Vector2

BLOCK_PATH = 'assets/sprites'
FONT_PATH = 'assets/font/font.ttf'

FPS = 60
FIELD_COLOR = (48, 39, 32)
BG_COLOR = (24, 89, 117)

DROP_TIME = 150
FAST_DROP_TIME = 15

TILE_SIZE = 40
FIELD_SIZE = WIDTH, HEIGHT = 10, 20
FIELD_RES = WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE

FIELD_WIDTH, FIELD_HEIGHT = 1.7, 1.0
WIN_RES = WIN_W, WIN_H = FIELD_RES[0] * FIELD_WIDTH, FIELD_RES[1] * FIELD_HEIGHT

INIT_POS_OFFSET = vec(WIDTH // 2 - 1, 0)
NEXT_POS_OFFSET = vec(WIDTH * 1.3, HEIGHT * 0.45)
MOVE_DIRECTIONS = {'left': vec(-1, 0), 'right': vec(1, 0), 'down': vec(0, 1)}

BLOCKS = {
    'T': [(0, 0), (-1, 0), (1, 0), (0, -1)],
    'O': [(0, 0), (0, -1), (1, 0), (1, -1)],
    'J': [(0, 0), (-1, 0), (0, -1), (0, -2)],
    'L': [(0, 0), (1, 0), (0, -1), (0, -2)],
    'I': [(0, 0), (0, 1), (0, -1), (0, -2)],
    'S': [(0, 0), (-1, 0), (0, -1), (1, -1)],
    'Z': [(0, 0), (1, 0), (0, -1), (-1, -1)]
}