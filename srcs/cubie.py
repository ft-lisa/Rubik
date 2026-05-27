from srcs.cube import cubes
import numpy as np


class Rubik:

    def __init__(self):
        self.colors = ["green", "blue", "red", "orange", "white", "yellow"]

        self.front = self.fill_grid(0)
        self.back = self.fill_grid(1)
        self.right = self.fill_grid(2)
        self.left = self.fill_grid(3)
        self.upper = self.fill_grid(4)
        self.down = self.fill_grid(5)

        self.grid = np.array(
            [self.front, self.back, self.right, self.left, self.upper, self.down]
        )

    def fill_grid(self, face_index):
        face = []
        for row in range(3):
            line = []
            for col in range(3):
                line.append([face_index, row, col])
            face.append(line)
        return face

    def resolve_cube(self, moves):
        for move in moves:
            face = move[0]
            direction = 1

            if len(move) > 1:
                if move[1] == "'":
                    direction = -1
                elif move[1] == "2":
                    self.rotate_face(face, direction)
                    self.rotate_face(face, direction)
                    continue

            self.rotate_face(face, direction)

        self.grid = np.array(
            [self.front, self.back, self.right, self.left, self.upper, self.down]
        )

    def rotate_face(self, face, direction):
        if face == "F":
            self.rotate_F(direction)
        elif face == "R":
            self.rotate_R(direction)
        elif face == "U":
            self.rotate_U(direction)
        elif face == "B":
            self.rotate_B(direction)
        elif face == "L":
            self.rotate_L(direction)
        elif face == "D":
            self.rotate_D(direction)

    def rotate_F(self, direction):
        if direction == 1:
            self.left[2], self.upper[2], self.right[0], self.down[0] = (
                self.down[0],
                self.left[2],
                self.upper[2],
                self.right[0],
            )
        else:
            self.left[2], self.upper[2], self.right[0], self.down[0] = (
                self.upper[2],
                self.right[0],
                self.down[0],
                self.left[2],
            )

    def rotate_R(self, direction):
        if direction == 1:
            self.front[2], self.upper[2], self.back[0], self.down[2] = (
                self.down[2],
                self.front[2],
                self.upper[2],
                self.back[0],
            )
        else:
            self.front[2], self.upper[2], self.back[0], self.down[2] = (
                self.upper[2],
                self.back[0],
                self.down[2],
                self.front[2],
            )

    def rotate_U(self, direction):
        if direction == 1:
            self.front[0], self.right[0], self.back[0], self.left[0] = (
                self.left[0],
                self.front[0],
                self.right[0],
                self.back[0],
            )
        else:
            self.front[0], self.right[0], self.back[0], self.left[0] = (
                self.right[0],
                self.back[0],
                self.left[0],
                self.front[0],
            )

    def rotate_B(self, direction):
        if direction == 1:
            self.left[0], self.upper[0], self.right[2], self.down[2] = (
                self.upper[0],
                self.right[2],
                self.down[2],
                self.left[0],
            )
        else:
            self.left[0], self.upper[0], self.right[2], self.down[2] = (
                self.down[2],
                self.left[0],
                self.upper[0],
                self.right[2],
            )

    def rotate_L(self, direction):
        if direction == 1:
            self.front[0], self.upper[0], self.back[2], self.down[0] = (
                self.down[0],
                self.front[0],
                self.upper[0],
                self.back[2],
            )
        else:
            self.front[0], self.upper[0], self.back[2], self.down[0] = (
                self.upper[0],
                self.back[2],
                self.down[0],
                self.front[0],
            )

    def rotate_D(self, direction):
        if direction == 1:
            self.front[2], self.right[2], self.back[2], self.left[2] = (
                self.right[2],
                self.back[2],
                self.left[2],
                self.front[2],
            )
        else:
            self.front[2], self.right[2], self.back[2], self.left[2] = (
                self.left[2],
                self.front[2],
                self.right[2],
                self.back[2],
            )


rubik = Rubik()
