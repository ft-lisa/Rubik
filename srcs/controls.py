from ursina import Vec2, mouse
from srcs.moves import moves
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

    if key == "r":
        moves.mouv_R(CLOCKWISE)
    elif key == "l":
        moves.mouv_L(CLOCKWISE)
    elif key == "u":
        moves.mouv_U(CLOCKWISE)
    elif key == "d":
        moves.mouv_D(CLOCKWISE)
    elif key == "f":
        moves.mouv_F(CLOCKWISE)
    elif key == "b":
        moves.mouv_B(CLOCKWISE)
    elif key == "t":
        moves.mouv_R(COUNTERCLOCKWISE)
    elif key == ";":
        moves.mouv_L(COUNTERCLOCKWISE)
    elif key == "i":
        moves.mouv_U(COUNTERCLOCKWISE)
    elif key == "s":
        moves.mouv_D(COUNTERCLOCKWISE)
    elif key == "g":
        moves.mouv_F(COUNTERCLOCKWISE)
    elif key == "n":
        moves.mouv_B(COUNTERCLOCKWISE)


def update():
    global last_mouse_pos

    if dragging:
        delta = mouse.position - last_mouse_pos

        # rotation souris
        cube_group.rotation_y -= delta.x * 200
        cube_group.rotation_x += delta.y * 200

        last_mouse_pos = mouse.position
