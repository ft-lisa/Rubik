import numpy as np
from srcs.parsing import determine_move


class Rubik:

    def __init__(self):
        self.colors = ["G", "B", "R", "O", "W", "Y"]

        self.illegal_moves = {
            "F",
            "F'",
            "B",
            "B'",
            "R",
            "R'",
            "L",
            "L'",
        }

        self.legal_moves = {"U", "U'", "D", "D'", "U2", "D2", "L2", "R2", "F2", "B2"}

        self.moves = self.legal_moves | self.illegal_moves

        self.OPPOSITE_FACES = {
            "U": "D",
            "D": "U",
            "R": "L",
            "L": "R",
            "F": "B",
            "B": "F",
        }

        self.move_eo = {
            "U": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "D": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "R": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "L": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "F": [0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
            "B": [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1],
            "U'": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "D'": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "R'": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "L'": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "F'": [0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
            "B'": [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1],
            "F2": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "B2": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "R2": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "L2": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "U2": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "D2": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        }

        self.move_ep = {
            "U": [3, 0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11],
            "D": [0, 1, 2, 3, 5, 6, 7, 4, 8, 9, 10, 11],
            "R": [8, 1, 2, 3, 11, 5, 6, 7, 4, 9, 10, 0],
            "L": [0, 1, 10, 3, 4, 5, 9, 7, 8, 2, 6, 11],
            "F": [0, 9, 2, 3, 4, 8, 6, 7, 1, 5, 10, 11],
            "B": [0, 1, 2, 11, 4, 5, 6, 10, 8, 9, 3, 7],
            "U'": [1, 2, 3, 0, 4, 5, 6, 7, 8, 9, 10, 11],
            "D'": [0, 1, 2, 3, 7, 4, 5, 6, 8, 9, 10, 11],
            "R'": [11, 1, 2, 3, 8, 5, 6, 7, 0, 9, 10, 4],
            "L'": [0, 1, 9, 3, 4, 5, 10, 7, 8, 6, 2, 11],
            "F'": [0, 8, 2, 3, 4, 9, 6, 7, 5, 1, 10, 11],
            "B'": [0, 1, 2, 10, 4, 5, 6, 11, 8, 9, 7, 3],
            "U2": [2, 3, 0, 1, 4, 5, 6, 7, 8, 9, 10, 11],
            "D2": [0, 1, 2, 3, 6, 7, 4, 5, 8, 9, 10, 11],
            "R2": [4, 1, 2, 3, 0, 5, 6, 7, 11, 9, 10, 8],
            "L2": [0, 1, 6, 3, 4, 5, 2, 7, 8, 10, 9, 11],
            "F2": [0, 5, 2, 3, 4, 1, 6, 7, 9, 8, 10, 11],
            "B2": [0, 1, 2, 7, 4, 5, 6, 3, 8, 9, 11, 10],
        }

        self.move_co = {
            "U": [0, 0, 0, 0, 0, 0, 0, 0],
            "D": [0, 0, 0, 0, 0, 0, 0, 0],
            "R": [2, 1, 0, 0, 1, 2, 0, 0],
            "L": [0, 0, 2, 1, 0, 0, 1, 2],
            "F": [0, 2, 1, 0, 0, 1, 2, 0],
            "B": [1, 0, 0, 2, 2, 0, 0, 1],
            "U'": [0, 0, 0, 0, 0, 0, 0, 0],
            "D'": [0, 0, 0, 0, 0, 0, 0, 0],
            "R'": [2, 1, 0, 0, 1, 2, 0, 0],
            "L'": [0, 0, 2, 1, 0, 0, 1, 2],
            "F'": [0, 2, 1, 0, 0, 1, 2, 0],
            "B'": [1, 0, 0, 2, 2, 0, 0, 1],
            "U2": [0, 0, 0, 0, 0, 0, 0, 0],
            "D2": [0, 0, 0, 0, 0, 0, 0, 0],
            "R2": [0, 0, 0, 0, 0, 0, 0, 0],
            "L2": [0, 0, 0, 0, 0, 0, 0, 0],
            "F2": [0, 0, 0, 0, 0, 0, 0, 0],
            "B2": [0, 0, 0, 0, 0, 0, 0, 0],
        }

        self.move_cp = {
            "U": [3, 0, 1, 2, 4, 5, 6, 7],
            "D": [0, 1, 2, 3, 5, 6, 7, 4],
            "R": [1, 5, 2, 3, 0, 4, 6, 7],
            "L": [0, 1, 3, 7, 4, 5, 2, 6],
            "F": [0, 2, 6, 3, 4, 1, 5, 7],
            "B": [4, 1, 2, 0, 7, 5, 6, 3],
            "U'": [1, 2, 3, 0, 4, 5, 6, 7],
            "D'": [0, 1, 2, 3, 7, 4, 5, 6],
            "R'": [4, 0, 2, 3, 5, 1, 6, 7],
            "L'": [0, 1, 6, 2, 4, 5, 7, 3],
            "F'": [0, 5, 1, 3, 4, 6, 2, 7],
            "B'": [3, 1, 2, 7, 0, 5, 6, 4],
            "U2": [2, 3, 0, 1, 4, 5, 6, 7],
            "D2": [0, 1, 2, 3, 6, 7, 4, 5],
            "R2": [5, 4, 2, 3, 1, 0, 6, 7],
            "L2": [0, 1, 7, 6, 4, 5, 3, 2],
            "F2": [0, 6, 5, 3, 4, 2, 1, 7],
            "B2": [7, 1, 2, 4, 3, 5, 6, 0],
        }

        self.UD_COLORS = {"W", "Y"}
        self.LR_COLORS = {"O", "R"}
        self.FB_COLORS = {"G", "B"}

        self.EDGES = [
            ("U", "R"),
            ("U", "F"),
            ("U", "L"),
            ("U", "B"),
            ("D", "R"),
            ("D", "F"),
            ("D", "L"),
            ("D", "B"),
            ("F", "R"),
            ("F", "L"),
            ("B", "L"),
            ("B", "R"),
        ]

        self.CORNERS = [
            ("U", "R", "B"),
            ("U", "F", "R"),
            ("U", "L", "F"),
            ("U", "B", "L"),
            ("D", "R", "B"),
            ("D", "F", "R"),
            ("D", "L", "F"),
            ("D", "B", "L"),
        ]

        self.initialize_cube()

    def initialize_cube(self) -> None:
        self.front = self.fill_grid(self.colors[0])
        self.back = self.fill_grid(self.colors[1])
        self.right = self.fill_grid(self.colors[2])
        self.left = self.fill_grid(self.colors[3])
        self.upper = self.fill_grid(self.colors[4])
        self.down = self.fill_grid(self.colors[5])

        self.rubik = np.array(
            [self.front, self.back, self.right, self.left, self.upper, self.down]
        )

    def fill_grid(self, color: str) -> np.ndarray:
        face = np.empty((3, 3), dtype=object)
        for row in range(3):
            for col in range(3):
                face[row, col] = color
        return face

    def shuffle_rubik(self, moves: list[str]) -> None:
        for move in moves:
            move, direction = determine_move(move)

            self.rotate_face(move, direction)

    def apply_move(self, move: str) -> None:
        move, direction = determine_move(move)

        self.rotate_face(move, direction)

    def update_rubik(self) -> None:
        self.rubik = np.array(
            [self.front, self.back, self.right, self.left, self.upper, self.down]
        )

    def set_rubik_from_string(self, s: str) -> None:
        arr = np.array(list(s), dtype=object).reshape(6, 3, 3)
        self.front = arr[0]
        self.back = arr[1]
        self.right = arr[2]
        self.left = arr[3]
        self.upper = arr[4]
        self.down = arr[5]
        self.update_rubik()

    def rotate_face(self, face: str, direction: int) -> None:
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
        elif face == "F2":
            self.rotate_F(1)
            self.rotate_F(1)
        elif face == "R2":
            self.rotate_R(1)
            self.rotate_R(1)
        elif face == "U2":
            self.rotate_U(1)
            self.rotate_U(1)
        elif face == "B2":
            self.rotate_B(1)
            self.rotate_B(1)
        elif face == "L2":
            self.rotate_L(1)
            self.rotate_L(1)
        elif face == "D2":
            self.rotate_D(1)
            self.rotate_D(1)

        self.update_rubik()

    def rotate_F(self, direction):
        if direction == 1:
            self.front = np.rot90(self.front, -1)

            tmp = self.upper[2, :].copy()
            self.upper[2, :] = self.left[::-1, 2]
            self.left[:, 2] = self.down[0, :]
            self.down[0, :] = self.right[::-1, 0]
            self.right[:, 0] = tmp
        else:
            self.front = np.rot90(self.front, 1)

            tmp = self.upper[2, :].copy()
            self.upper[2, :] = self.right[:, 0]
            self.right[:, 0] = self.down[0, ::-1]
            self.down[0, :] = self.left[:, 2]
            self.left[:, 2] = tmp[::-1]

    def rotate_R(self, direction):
        if direction == 1:
            self.right = np.rot90(self.right, -1)

            tmp = self.upper[:, 2].copy()
            self.upper[:, 2] = self.front[:, 2]
            self.front[:, 2] = self.down[:, 2]
            self.down[:, 2] = self.back[::-1, 0]
            self.back[:, 0] = tmp[::-1]

        else:
            self.right = np.rot90(self.right, 1)

            tmp = self.upper[:, 2].copy()
            self.upper[:, 2] = self.back[::-1, 0]
            self.back[:, 0] = self.down[::-1, 2]
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

            tmp = self.upper[0, :].copy()
            self.upper[0, :] = self.right[:, 2]
            self.right[:, 2] = self.down[2, ::-1]
            self.down[2, :] = self.left[:, 0]
            self.left[:, 0] = tmp[::-1]
        else:
            self.back = np.rot90(self.back, 1)

            tmp = self.upper[0, :].copy()
            self.upper[0, :] = self.left[::-1, 0]
            self.left[:, 0] = self.down[2, :]
            self.down[2, :] = self.right[::-1, 2]
            self.right[:, 2] = tmp

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

    def get_edge_orientation(self, stickers_colors: tuple[str, str]) -> int:
        first_color, second_color = stickers_colors

        return (
            1 if first_color in self.LR_COLORS or second_color in self.UD_COLORS else 0
        )

    def read_edge(self, emplacement: tuple[str, str]) -> tuple[str, str]:
        face1, face2 = emplacement
        if face1 == "U" and face2 == "R":
            return (self.upper[1, 2], self.right[0, 1])
        elif face1 == "U" and face2 == "F":
            return (self.upper[2, 1], self.front[0, 1])
        elif face1 == "U" and face2 == "L":
            return (self.upper[1, 0], self.left[0, 1])
        elif face1 == "U" and face2 == "B":
            return (self.upper[0, 1], self.back[0, 1])
        elif face1 == "D" and face2 == "R":
            return (self.down[1, 2], self.right[2, 1])
        elif face1 == "D" and face2 == "F":
            return (self.down[0, 1], self.front[2, 1])
        elif face1 == "D" and face2 == "L":
            return (self.down[1, 0], self.left[2, 1])
        elif face1 == "D" and face2 == "B":
            return (self.down[2, 1], self.back[2, 1])
        elif face1 == "F" and face2 == "R":
            return (self.front[1, 2], self.right[1, 0])
        elif face1 == "F" and face2 == "L":
            return (self.front[1, 0], self.left[1, 2])
        elif face1 == "B" and face2 == "L":
            return (self.back[1, 2], self.left[1, 0])
        elif face1 == "B" and face2 == "R":
            return (self.back[1, 0], self.right[1, 2])

    def get_edges_binary(self) -> tuple[int]:

        edges_coord = ()
        for emplacement in self.EDGES:
            stickers_colors = self.read_edge(emplacement)
            ori = self.get_edge_orientation(stickers_colors)
            edges_coord += (ori,)
        return edges_coord

    def get_corner_orientation(self, stickers_colors: tuple[str, str, str]) -> int:
        for orientation, color in enumerate(stickers_colors):
            if color in self.UD_COLORS:
                return orientation

    def read_corner(self, emplacement: tuple[str, str, str]) -> tuple[str, str, str]:
        face1, face2, face3 = emplacement
        if face1 == "U" and face2 == "R" and face3 == "B":
            return (self.upper[0, 2], self.right[0, 2], self.back[0, 0])
        elif face1 == "U" and face2 == "F" and face3 == "R":
            return (self.upper[2, 2], self.front[0, 2], self.right[0, 0])
        elif face1 == "U" and face2 == "L" and face3 == "F":
            return (self.upper[2, 0], self.left[0, 2], self.front[0, 0])
        elif face1 == "U" and face2 == "B" and face3 == "L":
            return (self.upper[0, 0], self.back[0, 2], self.left[0, 0])
        elif face1 == "D" and face2 == "R" and face3 == "B":
            return (self.down[2, 2], self.back[2, 0], self.right[2, 2])
        elif face1 == "D" and face2 == "F" and face3 == "R":
            return (self.down[0, 2], self.right[2, 0], self.front[2, 2])
        elif face1 == "D" and face2 == "L" and face3 == "F":
            return (self.down[0, 0], self.front[2, 0], self.left[2, 2])
        elif face1 == "D" and face2 == "B" and face3 == "L":
            return (self.down[2, 0], self.left[2, 0], self.back[2, 2])

    def get_corners_binary(self) -> tuple[int]:

        corners_coord = ()
        for emplacement in self.CORNERS:
            stickers_colors = self.read_corner(emplacement)
            ori = self.get_corner_orientation(stickers_colors)
            corners_coord += (ori,)
        return corners_coord

    def get_middle_edge_orientation(self, stickers_colors: tuple[str, str]) -> int:
        first_color, second_color = stickers_colors

        return (
            1
            if (first_color in self.LR_COLORS or first_color in self.FB_COLORS)
            and (second_color in self.LR_COLORS or second_color in self.FB_COLORS)
            else 0
        )

    def get_slice_binary(self) -> tuple[int]:

        slice_coord = ()
        for emplacement in self.EDGES:
            stickers_colors = self.read_edge(emplacement)
            ori = self.get_middle_edge_orientation(stickers_colors)
            slice_coord += (ori,)
        return slice_coord


rubik = Rubik()
