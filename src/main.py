from enum import Enum, unique
from keyboard_operation import *
import copy
import random
import time

class KindOfMarker(Enum):
    BLANK_       = 0
    MINO_        = 1
    FALLEN_MINO_ = 2
    WALL_        = 3

class Mino:
    mino_ = [
                # I
                [
                    [0, 0, 0, 0],
                    [1, 1, 1, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]
                ],

                # J
                [
                    [0, 0, 1],
                    [0, 0, 1],
                    [0, 1, 1]
                ],

                # L
                [
                    [1, 0, 0],
                    [1, 0, 0],
                    [1, 1, 0]
                ],

                # O
                [
                    [1, 1],
                    [1, 1]
                ],

                # S
                [
                    [0, 1, 1],
                    [1, 1, 0],
                    [0, 0, 0]
                ],

                # T
                [
                    [1, 1, 1],
                    [0, 1, 0],
                    [0, 0, 0],
                ],

                # Z
                [
                    [1, 1, 0],
                    [0, 1, 1],
                    [0, 0, 0]
                ]
            ]

class Tetris:
    FIELD_HEIGHT_ = 20
    FIELD_WIDTH_  = 10

    DELETE_ROW_POINT_ = 10
    TETRIS_POINT_     = 10

    score_ = 0

    MINO_MERKAR_        = '◻️i'
    FALLEN_MINO_MARKER_ = '◻️i'
    WALL_MARKER_        = '🔳'
    BLANK_MARKER_       = '　'


    def select_marker(self, field_elm):
        if field_elm == KindOfMarker.BLANK_:
            return self.BLANK_MARKER_
        elif field_elm == KindOfMarker.MINO_:
            return self.MINO_MERKAR_
        else:
            return self.FALLEN_MINO_MARKER_

    def print_field(self, field):
        print("\033[22A", end = '')
        for i in field:
            print(self.WALL_MARKER_, end = '')
            for j in i:
                print(self.select_marker(j), end = '')
            print(self.WALL_MARKER_)
        for i in range(self.FIELD_WIDTH_ + 2):
            print(self.WALL_MARKER_, end = '')
        print('')
        print('score:', self.score_)

    def init_field_array(self):
        return [[KindOfMarker.BLANK_
            for i in range(self.FIELD_WIDTH_)] for j in range(self.FIELD_HEIGHT_)]

    def generate_new_mino(self):
        mino = Mino()
        new_mino = mino.mino_[random.randint(0, len(mino.mino_) - 1)]
        ret_mino = []
        for i in new_mino:
            row = []
            for j in i:
                if j == 1:
                    row.append(KindOfMarker.MINO_)
                else:
                    row.append(KindOfMarker.BLANK_)
            ret_mino.append(row)
        return ret_mino

    def set_mino(self, field, mino, left_top_x, left_top_y):
        height = len(mino)
        width  = len(mino[0])
        for i in range(height):
            for j in range(width):
                if mino[i][j] != KindOfMarker.MINO_:
                    continue
                field[left_top_y + i][left_top_x + j] = mino[i][j]

    def erase_mino(self, field, mino, left_top_x, left_top_y):
        height = len(mino)
        width  = len(mino[0])
        for i in range(height):
            for j in range(width):
                if mino[i][j] == KindOfMarker.MINO_:
                    field[i + left_top_y][j + left_top_x] = KindOfMarker.BLANK_

    def is_intersect(self, field, mino, left_top_x, left_top_y):
        height = len(mino)
        width  = len(mino)

        for i in range(height):
            for j in range(width):
                if mino[i][j] != KindOfMarker.MINO_:
                    continue
                if j + left_top_x < 0 or self.FIELD_WIDTH_ <= j + left_top_x:
                    return True
                if i + left_top_y < 0 or self.FIELD_HEIGHT_ <= i + left_top_y:
                    return True
                if field[i + left_top_y][j + left_top_x] != KindOfMarker.BLANK_:
                    return True

        return False

    def rotation(self, mino):
        height = len(mino)
        width  = len(mino[0])

        ret_mino = copy.deepcopy(mino)

        for i in range(height):
            for j in range(width):
                ret_mino[i][j] = mino[j][height - i - 1]

        return ret_mino

    def keyboard_processing(self, field, mino, left_top_x, left_top_y):
        key = getch()

        if key == 'l':
            ret_mino = self.rotation(mino)
            if self.is_intersect(field, ret_mino, left_top_x, left_top_y):
                return (mino, left_top_x, left_top_y)
            return (ret_mino, left_top_x, left_top_y)

        offset_x = 0
        offset_y = 0

        offset_x -= int(key == 'a')
        offset_x += int(key == 'd')
        offset_y += int(key == 's')

        if self.is_intersect(
                field, mino, left_top_x + offset_x, left_top_y + offset_y):
            offset_x += int(key == 'a')
            offset_x -= int(key == 'd')
            offset_y -= int(key == 's')

        return (mino, left_top_x + offset_x, left_top_y + offset_y)

    def arive_bottom_processing(self, field, mino, left_top_x, left_top_y):
        height = len(mino)
        width  = len(mino[0])
        for i in range(height):
            for j in range(width):
                if mino[i][j] != KindOfMarker.MINO_:
                    continue
                field[i + left_top_y][j + left_top_x] = KindOfMarker.FALLEN_MINO_

    def copy_row_to_under(self, field, y):
        for i in range(y):
            for j in range(self.FIELD_WIDTH_):
                field[y - i][j] = field[y - i - 1][j]

    def delete_complete_row(self, field, y):
        for i in range(self.FIELD_WIDTH_):
            field[y][i] = KindOfMarker.BLANK_

    def delete_complete_row_processing(self, field):
        delete_row_count = 0
        for i in range(self.FIELD_HEIGHT_):
            for j in range(self.FIELD_WIDTH_):
                if field[i][j] != KindOfMarker.FALLEN_MINO_:
                    break
                if j != self.FIELD_WIDTH_ - 1:
                    continue
                self.delete_complete_row(field, i)
                self.copy_row_to_under(field, i)
                delete_row_count += 1
        self.score_ += delete_row_count * self.DELETE_ROW_POINT_
        self.score_ += int(delete_row_count == 4) * self.TETRIS_POINT_

    def tetris_processing(self):
        field = self.init_field_array()
        for i in range(self.FIELD_HEIGHT_ + 2):
            print('')

        last_clock = time.time()

        while 1:
            mino = self.generate_new_mino()

            left_top_x = int((self.FIELD_WIDTH_ - len(mino[0])) / 2)
            left_top_y = 0
            if self.is_intersect(field, mino, left_top_x, left_top_y):
                print('game over.')
                break

            self.set_mino(field, mino, left_top_x, left_top_y)
            self.print_field(field)

            while 1:
                if kbhit():
                    self.erase_mino(field, mino, left_top_x, left_top_y)
                    (mino, left_top_x, left_top_y) = self.keyboard_processing(
                                                field, mino, left_top_x, left_top_y)

                    self.set_mino(field, mino, left_top_x, left_top_y)
                    self.print_field(field)
                now_clock = time.time()
                if now_clock - last_clock > 0.5:
                    self.erase_mino(field, mino, left_top_x, left_top_y)
                    last_clock = now_clock
                    if self.is_intersect(field, mino, left_top_x, left_top_y + 1):
                        self.arive_bottom_processing(field, mino, left_top_x, left_top_y)
                        self.delete_complete_row_processing(field)
                        break

                    left_top_y += 1

                    self.set_mino(field, mino, left_top_x, left_top_y)
                    self.print_field(field)

def main():
    tetris = Tetris()
    tetris.tetris_processing()

if __name__ == "__main__":
    main()
