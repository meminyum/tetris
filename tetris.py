from settings import *
from minitetris import miniTetris
import pygame.freetype as ft
import math

class Text:
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FONT_PATH)

    def draw(self):
        self.font.render_to(self.app.screen, (WIN_W * 0.6, WIN_H * 0.02),
                            text='TETRIS', fgcolor='white', size=TILE_SIZE * 1.65, bgcolor='black')
        self.font.render_to(self.app.screen, (WIN_W * 0.65, WIN_H * 0.22),
                            text='next', fgcolor='orange', size=TILE_SIZE * 1.65, bgcolor='black')
        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.67),
                            text='score', fgcolor='orange', size=TILE_SIZE * 1.65, bgcolor='black')
        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.8),
                            text=f'{self.app.tetris.score}', fgcolor='white', size=TILE_SIZE * 1.65,)

class Tetris:
    def __init__(self, app):
        self.app = app
        self.field_array = self.get_field_array()
        self.sprite_group = pg.sprite.Group( )
        self.minitetris = miniTetris(self)
        self.next_minitetris = miniTetris(self, current=False)
        self.speed_up = False
        self.score = 0
        self.full_lines = 0
        self.points_line = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}
        self.font = ft.Font(FONT_PATH)

    def get_score(self):
        self.score += self.points_line[self.full_lines]
        self.full_lines = 0

    def full_line_check(self):
        row = HEIGHT - 1
        for y in range(HEIGHT - 1, -1, -1):
            for x in range(WIDTH):
                self.field_array[row][x] = self.field_array[y][x]

                if self.field_array[y][x]:
                    self.field_array[row][x].pos = vec(x,y)

            if sum(map(bool, self.field_array[y])) < WIDTH:
                row -= 1
            else:
                for x in range(WIDTH):
                    self.field_array[row][x].alive = False
                    self.field_array[row][x] = 0
                self.full_lines += 1

    def blocks_to_array(self):
        for block in self.minitetris.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block

    def get_field_array(self):
        return [[0 for x in range(WIDTH)] for y in range(HEIGHT)]

    def is_game_over(self):
        if self.minitetris.blocks[0].pos.y == INIT_POS_OFFSET[1]:
            pg.time.wait(250)
            return True

    def check_if_land(self):
        if self.minitetris.landing:
            if self.is_game_over():
                self.__init__(self.app)
            else:
                self.speed_up = False
                self.blocks_to_array()
                self.next_minitetris.current = True
                self.minitetris = self.next_minitetris
                self.next_minitetris = miniTetris(self, current=False)

    def control(self, pressed_key):
        if pressed_key == pg.K_LEFT:
            self.minitetris.move(direction='left')
        elif pressed_key == pg.K_RIGHT:
            self.minitetris.move(direction='right')
        elif pressed_key == pg.K_UP:
            self.minitetris.rotate()
        elif pressed_key == pg.K_DOWN:
            self.speed_up = True

    def draw_grid(self):
        for x in range(WIDTH):
            for y in range(HEIGHT):
                pg.draw.rect(self.app.screen, 'black',
                             (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    def update(self):
        trigger = [self.app.anim_trigger, self.app.fast_anim_trigger][self.speed_up]
        if trigger:
            self.minitetris.update()
            self.check_if_land()
            self.full_line_check()
            self.get_score()
        self.sprite_group.update()

    def draw(self):
        self.draw_grid()
        self.sprite_group.draw(self.app.screen)