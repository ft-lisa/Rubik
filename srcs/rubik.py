import numpy as np
from srcs.parsing import REVERSE_MODIFIERS


class Rubik:

    def __init__(self):
        self.colors = ["G", "B", "R", "O", "W", "Y"]
        self.actions = [
            ("F", 1),
            ("F", -1),
            ("R", 1),
            ("R", -1),
            ("U", 1),
            ("U", -1),
            ("B", 1),
            ("B", -1),
            ("L", 1),
            ("L", -1),
            ("D", 1),
            ("D", -1),
        ]

        self.COULEURS_UD = {"W", "Y"}
        self.COULEURS_FB = {"G", "B"}

        self.ARETES = [
            ("U", "F"),
            ("U", "R"),
            ("U", "B"),
            ("U", "L"),
            ("D", "F"),
            ("D", "R"),
            ("D", "B"),
            ("D", "L"),
            ("F", "R"),
            ("F", "L"),
            ("B", "R"),
            ("B", "L"),
        ]

        self.CORNERS = [
            ("U", "R", "F"),
            ("U", "F", "L"),
            ("U", "L", "B"),
            ("U", "B", "R"),
            ("D", "F", "R"),
            ("D", "L", "F"),
            ("D", "B", "L"),
        ]

        self.initialize_cube()

        self.size = 3

    def solved(self) -> bool:
        for face in self.rubik:
            if not np.all(face == face[0, 0]):
                return False
        return True

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
            direction = 1

            if len(move) > 1:
                if move[1] in REVERSE_MODIFIERS:
                    direction = -1
                move = move[0]

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

    def get_edge_orientation(self, stickers: dict[str, str]) -> int:
        face_ref, _ = stickers.keys()
        couleur_ref = stickers[face_ref]

        if face_ref in ("U", "D"):
            return 0 if couleur_ref in self.COULEURS_UD else 1

        return 0 if couleur_ref in self.COULEURS_FB else 1

    def read_edge(self, emplacement: tuple[str, str]) -> dict[str, str]:
        face1, face2 = emplacement
        if face1 == "U" and face2 == "F":
            return {"U": self.upper[2, 1], "F": self.front[0, 1]}
        elif face1 == "U" and face2 == "R":
            return {"U": self.upper[1, 2], "R": self.right[0, 1]}
        elif face1 == "U" and face2 == "B":
            return {"U": self.upper[0, 1], "B": self.back[0, 1]}
        elif face1 == "U" and face2 == "L":
            return {"U": self.upper[1, 0], "L": self.left[0, 1]}
        elif face1 == "D" and face2 == "F":
            return {"D": self.down[0, 1], "F": self.front[2, 1]}
        elif face1 == "D" and face2 == "R":
            return {"D": self.down[1, 2], "R": self.right[2, 1]}
        elif face1 == "D" and face2 == "B":
            return {"D": self.down[2, 1], "B": self.back[2, 1]}
        elif face1 == "D" and face2 == "L":
            return {"D": self.down[1, 0], "L": self.left[2, 1]}
        elif face1 == "F" and face2 == "R":
            return {"F": self.front[1, 2], "R": self.right[1, 0]}
        elif face1 == "F" and face2 == "L":
            return {"F": self.front[1, 0], "L": self.left[1, 2]}
        elif face1 == "B" and face2 == "R":
            return {"B": self.back[1, 0], "R": self.right[1, 2]}
        elif face1 == "B" and face2 == "L":
            return {"B": self.back[1, 2], "L": self.left[1, 0]}

    def get_edges_binary(self) -> list[int]:
        ori_coord = []
        for _, emplacement in enumerate(self.ARETES[:11]):
            stickers = self.read_edge(emplacement)
            ori = self.get_edge_orientation(stickers)
            ori_coord.append(ori)
        return ori_coord

    def get_corner_orientation(self, stickers: dict[str, str, str]) -> int:
        first_ref, second_ref, _ = stickers.keys()
        first_color = stickers[first_ref]
        second_color = stickers[second_ref]

        if first_color in self.COULEURS_UD:
            return 0
        elif second_color in self.COULEURS_UD:
            return 1
        else:
            return 2

    def read_corner(self, emplacement: tuple[str, str, str]) -> dict[str, str, str]:
        face1, face2, face3 = emplacement
        if face1 == "U" and face2 == "R" and face3 == "F":
            return {"U": self.upper[2, 2], "R": self.right[0, 0], "F": self.front[0, 2]}
        elif face1 == "U" and face2 == "F" and face3 == "L":
            return {"U": self.upper[2, 0], "F": self.front[0, 0], "L": self.left[0, 2]}
        elif face1 == "U" and face2 == "L" and face3 == "B":
            return {"U": self.upper[0, 0], "L": self.left[0, 0], "B": self.back[0, 2]}
        elif face1 == "U" and face2 == "B" and face3 == "R":
            return {"U": self.upper[0, 2], "B": self.back[0, 0], "R": self.right[0, 2]}
        elif face1 == "D" and face2 == "F" and face3 == "R":
            return {"D": self.down[0, 2], "F": self.front[2, 2], "R": self.right[2, 0]}
        elif face1 == "D" and face2 == "L" and face3 == "F":
            return {"D": self.down[0, 0], "L": self.left[2, 2], "F": self.front[2, 0]}
        elif face1 == "D" and face2 == "B" and face3 == "L":
            return {"D": self.down[2, 0], "B": self.back[2, 2], "L": self.left[2, 0]}
        elif face1 == "D" and face2 == "R" and face3 == "B":
            return {"D": self.down[2, 2], "R": self.right[2, 2], "B": self.back[2, 0]}

    def get_corners_binary(self) -> list[int]:
        corners_coord = []
        for _, emplacement in enumerate(self.CORNERS[:7]):
            stickers = self.read_corner(emplacement)
            ori = self.get_corner_orientation(stickers)
            corners_coord.append(ori)
        return corners_coord


rubik = Rubik()
