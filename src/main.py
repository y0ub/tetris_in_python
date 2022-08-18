from enum import Enum, unique
import random
from keyboard_operation import *

class KindOfMarker(Enum):
    BLANK_      = 0
    MINO_       = 1
    FALLEN_MINO = 2
    WALL_       = 3

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

    def select_marker(self, field_elm):
        if field_elm == KindOfMarker.BLANK_:
            return '　'
        elif field_elm == KindOfMarker.MINO_:
            return '◻️ '
        else:
            return '🔳'

    def print_field(self, field):
        for i in field:
            print('🔳', end = '')
            for j in i:
                print(self.select_marker(j), end = '')
            print('🔳')
        for i in range(self.FIELD_WIDTH_ + 2):
            print('🔳', end = '')
        print('')

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
                field[left_top_y + i][left_top_x + j] = mino[i][j]

    def print_test(self, mino):
        for i in mino:
            for j in mino[0]:
                print(j, end = '')
            print('')
        print('')

    def tetris_processing(self):
        field = self.init_field_array()
        self.print_field(field)

        while 1:
            mino = self.generate_new_mino()

            self.print_test(mino)

            left_top_x = int((self.FIELD_WIDTH_ - len(mino[0])) / 2)
            left_top_y = 0
            self.set_mino(field, mino, left_top_x, left_top_y)
            self.print_field(field)
            getch()
    # print
    # fall
    # print
    # key_processing
    # delete_processing
    # 

def main():
    tetris = Tetris()
    tetris.tetris_processing()

if __name__ == "__main__":
    main()
