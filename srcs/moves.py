from ursina import Entity, invoke, destroy, curve
from srcs.cube import cubes, cube_group


class Moves:
    # axis, sign, selector_axis, selector_value
    FACES = {
        "R": ("x", 1, "x", 1),
        "L": ("x", -1, "x", -1),
        "U": ("y", 1, "y", 1),
        "D": ("y", -1, "y", -1),
        "F": ("z", 1, "z", -1),
        "B": ("z", -1, "z", 1),
        "R2": ("x", 1, "x", 1),
        "L2": ("x", -1, "x", -1),
        "U2": ("y", 1, "y", 1),
        "D2": ("y", -1, "y", -1),
        "F2": ("z", 1, "z", -1),
        "B2": ("z", -1, "z", 1),
    }

    def __init__(self):
        self.is_animating = False
        self.move_queue = []

    def snap_cube(self, cube):
        # snap position to integer grid
        cube.x = round(cube.x)
        cube.y = round(cube.y)
        cube.z = round(cube.z)
        # snap rotations to nearest multiple of 90
        cube.rotation_x = round(cube.rotation_x / 90) * 90
        cube.rotation_y = round(cube.rotation_y / 90) * 90
        cube.rotation_z = round(cube.rotation_z / 90) * 90

    def finish_move(self, pivot):
        for cube in pivot.children:
            cube.world_parent = cube_group
            self.snap_cube(cube)

        destroy(pivot)
        self.is_animating = False
        self.process_queue()

    def process_queue(self):
        if not self.move_queue:
            return
        next_move, direction = self.move_queue.pop(0)
        invoke(lambda: self.do_move(next_move, direction), delay=0.01)

    def do_move(self, face, direction):
        if self.is_animating:
            self.move_queue.append((face, direction))
            return
        self.is_animating = True

        axis, sign, selector_axis, selector_value = self.FACES[face]

        pivot = Entity(parent=cube_group)

        for cube in cubes:
            if round(getattr(cube, selector_axis)) == selector_value:
                cube.world_parent = pivot

        turns = 2 if face.endswith("2") else 1

        pivot.position = (0, 0, 0)

        animate = getattr(pivot, f"animate_rotation_{axis}")
        animate(sign * 90 * direction * turns, duration=0.2, curve=curve.linear)

        invoke(lambda: self.finish_move(pivot), delay=0.5)

    def mouv_R(self, direction):
        self.do_move("R", direction)

    def mouv_L(self, direction):
        self.do_move("L", direction)

    def mouv_U(self, direction):
        self.do_move("U", direction)

    def mouv_D(self, direction):
        self.do_move("D", direction)

    def mouv_F(self, direction):
        self.do_move("F", direction)

    def mouv_B(self, direction):
        self.do_move("B", direction)


rMoves = Moves()
