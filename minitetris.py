from settings import *
import random


class Block(pg.sprite.Sprite):
    def __init__(self, miniTetris, pos):
        self.miniTetris = miniTetris
        self.pos = vec(pos) + INIT_POS_OFFSET
        self.next_pos = vec(pos) + NEXT_POS_OFFSET
        self.alive = True

        super().__init__(miniTetris.tetris.sprite_group)
        self.image = miniTetris.image
        # self.image = pg.Surface([TILE_SIZE,TILE_SIZE])
        # pg.draw.rect(self.image, 'orange', (1, 1, TILE_SIZE - 2, TILE_SIZE - 2), border_radius=8)
        self.rect = self.image.get_rect()

        self.sfx_image = self.image.copy()
        self.sfx_image.set_alpha(110)
        self.sfx_speed = random.uniform(0.2, 0.6)
        self.sfx_cycles = random.randrange(4, 8)
        self.cycle_cnt = 0

    def sfx_end_time(self):
        if self.miniTetris.tetris.app.anim_trigger:
            self.cycle_cnt += 1
            if self.cycle_cnt > self.sfx_cycles:
                self.cycle_cnt = 0
                return True

    def sfx_run(self):
        self.image = self.sfx_image
        self.pos.y -= self.sfx_speed
        self.image = pg.transform.rotate(self.image, pg.time.get_ticks() * self.sfx_speed)

    def is_alive(self):
        if not self.alive:
            if not self.sfx_end_time():
                self.sfx_run()
            else:
                self.kill()

    def rotate(self, pivot_pos):
        translated = self.pos - pivot_pos
        rotated = translated.rotate(90)
        return rotated + pivot_pos

    def set_rect_pos(self):
        pos = [self.next_pos, self.pos][self.miniTetris.current]
        self.rect.topleft = pos * TILE_SIZE

    def update(self):
        self.is_alive()
        self.set_rect_pos()

    def is_collide(self, pos):
        x, y = int(pos.x), int(pos.y)
        if 0 <= x < WIDTH and y < HEIGHT and (y < 0 or not self.miniTetris.tetris.field_array[y][x]):
            return False
        return True


class miniTetris:
    def __init__(self, tetris, current=True):
        self.tetris = tetris
        self.shape = random.choice(list(BLOCKS.keys()))
        self.image = random.choice(tetris.app.images)
        self.blocks = [Block(self, pos) for pos in BLOCKS[self.shape]]
        self.landing = False
        self.current = current

    def rotate(self):
        pivot_pos = self.blocks[0].pos
        new_block_pos = [block.rotate(pivot_pos) for block in self.blocks]

        if not self.is_collide(new_block_pos):
            for i, block in enumerate(self.blocks):
                block.pos = new_block_pos[i]

    def is_collide(self, block_positions):
        return any(map(Block.is_collide, self.blocks, block_positions))

    def move(self, direction):
        move_direction = MOVE_DIRECTIONS[direction]
        new_block_positions = [block.pos + move_direction for block in self.blocks]
        is_collide = self.is_collide(new_block_positions)

        if not is_collide:
            for block in self.blocks:
                block.pos += move_direction
        elif direction == 'down':
            self.landing = True

    def update(self):
        self.move(direction='down')