from ursina import Vec2, mouse
from srcs.moves import rMoves
from srcs.cube import cube_group

dragging = False
last_mouse_pos = Vec2(0, 0)
CLOCKWISE = 1
COUNTERCLOCKWISE = -1


def input(key):
    global dragging, last_mouse_pos

    if key == "left mouse down":
        dragging = True
        last_mouse_pos = mouse.position

    if key == "left mouse up":
        dragging = False


def update():
    global last_mouse_pos

    if dragging:
        delta = mouse.position - last_mouse_pos

        # rotation souris
        cube_group.rotation_y -= delta.x * 200
        cube_group.rotation_x += delta.y * 200

        last_mouse_pos = mouse.position
