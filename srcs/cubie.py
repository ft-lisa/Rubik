from srcs.cube import cubes
import numpy as np


class Rubik:

    def __init__(self):
        self.colors = ["G", "B", "R", "O", "W", "Y"]

        self.front = self.fill_grid(self.colors[0])
        self.back = self.fill_grid(self.colors[1])
        self.right = self.fill_grid(self.colors[2])
        self.left = self.fill_grid(self.colors[3])
        self.upper = self.fill_grid(self.colors[4])
        self.down = self.fill_grid(self.colors[5])

        self.rubik = np.array(
            [self.front, self.back, self.right, self.left, self.upper, self.down]
        )

        self.size = 3

    def fill_grid(self, color: str) -> np.ndarray:
        face = np.empty((3, 3), dtype=object)
        for row in range(3):
            for col in range(3):
                face[row, col] = color
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

        self.rubik = np.array(
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
            self.front = np.rot90(self.front, -1)

            tmp = self.upper[2, :].copy()
            self.upper[2, :] = self.left[:, 2]
            self.left[:, 2] = self.down[0, :]
            self.down[0, :] = self.right[:, 0]
            self.right[:, 0] = tmp
        else:
            self.front = np.rot90(self.front, 1)

            tmp = self.upper[2, :].copy()
            self.upper[2, :] = self.right[:, 0]
            self.right[:, 0] = self.down[0, :]
            self.down[0, :] = self.left[:, 2]
            self.left[:, 2] = tmp

    def rotate_R(self, direction):
        if direction == 1:
            self.right = np.rot90(self.right, -1)

            tmp = self.upper[:, 2].copy()
            self.upper[:, 2] = self.front[:, 2]
            self.front[:, 2] = self.down[:, 2]
            self.down[:, 2] = self.back[:, 0]
            self.back[:, 0] = tmp

        else:
            self.right = np.rot90(self.right, 1)

            tmp = self.upper[:, 2].copy()
            self.upper[:, 2] = self.back[:, 0]
            self.back[:, 0] = self.down[:, 2]
            self.down[:, 2] = self.front[:, 2]
            self.front[:, 2] = tmp

    def rotate_U(self, direction):
        if direction == 1:
            self.upper = np.rot90(self.upper, -1)

            tmp = self.front[0, :].copy()
            self.front[0, :] = self.right[0, :]
            self.right[0, :] = self.back[0, :]
            self.back[0, :] = self.left[0, :]
            self.left[0, :] = tmp
        else:
            self.upper = np.rot90(self.upper, k=1)

            tmp = self.front[0, :].copy()
            self.front[0, :] = self.left[0, :]
            self.left[0, :] = self.back[0, :]
            self.back[0, :] = self.right[0, :]
            self.right[0, :] = tmp

    def rotate_B(self, direction):
        if direction == 1:
            self.back = np.rot90(self.back, -1)

            tmp = self.down[2, :].copy()
            self.down[2, :] = self.left[:, 0]
            self.left[:, 0] = self.upper[0, :]
            self.upper[0, :] = self.right[:, 2]
            self.right[:, 2] = tmp
        else:
            self.back = np.rot90(self.back, 1)

            tmp = self.left[0, :].copy()
            self.left[0, :] = self.down[2, :]
            self.down[2, :] = self.right[2, :]
            self.right[2, :] = self.upper[0, :]
            self.upper[0, :] = tmp

    def rotate_L(self, direction):
        if direction == 1:
            self.left = np.rot90(self.left, -1)

            tmp = self.down[:, 0].copy()
            self.down[:, 0] = self.front[:, 0]
            self.front[:, 0] = self.upper[:, 0]
            self.upper[:, 0] = self.back[::-1, 2]
            self.back[:, 2] = tmp[::-1]
        else:
            self.left = np.rot90(self.left, 1)

            tmp = self.down[:, 0].copy()
            self.down[:, 0] = self.back[::-1, 2]
            self.back[:, 2] = self.upper[::-1, 0]
            self.upper[:, 0] = self.front[:, 0]
            self.front[:, 0] = tmp

    def rotate_D(self, direction):
        if direction == 1:
            self.down = np.rot90(self.down, -1)

            tmp = self.front[2, :].copy()
            self.front[2, :] = self.left[2, :]
            self.left[2, :] = self.back[2, :]
            self.back[2, :] = self.right[2, :]
            self.right[2, :] = tmp

        else:
            self.down = np.rot90(self.down, 1)

            tmp = self.front[2, :].copy()
            self.front[2, :] = self.right[2, :]
            self.right[2, :] = self.back[2, :]
            self.back[2, :] = self.left[2, :]
            self.left[2, :] = tmp


rubik = Rubik()
