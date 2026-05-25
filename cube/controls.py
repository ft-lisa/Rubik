from ursina import *
import cube.moves as cube
from cube.cube import cube_group


dragging = False
last_mouse_pos = Vec2(0, 0)
CLOCKWISE = 1
COUNTERCLOCKWISE = -1


def input(key):
    global dragging, last_mouse_pos

    if key == 'left mouse down':
        dragging = True
        last_mouse_pos = mouse.position

    if key == 'left mouse up':
        dragging = False
    
    if key == 'r':
        cube.mouv_R(CLOCKWISE)
    elif key == 'l':
        cube.mouv_L(CLOCKWISE)
    elif key == 'u':
        cube.mouv_U(CLOCKWISE)
    elif key == 'd':
        cube.mouv_D(CLOCKWISE)
    elif key == 'f':
        cube.mouv_F(CLOCKWISE)
    elif key == 'b':
        cube.mouv_B(CLOCKWISE)
    elif key == 't':
        cube.mouv_R(COUNTERCLOCKWISE)
    elif key == ';':
        cube.mouv_L(COUNTERCLOCKWISE)
    elif key == 'i':
        cube.mouv_U(COUNTERCLOCKWISE)
    elif key == 's':
        cube.mouv_D(COUNTERCLOCKWISE)
    elif key == 'g':
        cube.mouv_F(COUNTERCLOCKWISE)
    elif key == 'n':
        cube.mouv_B(COUNTERCLOCKWISE)


def update():
    global last_mouse_pos

    if dragging:
        delta = mouse.position - last_mouse_pos

        # rotation souris
        cube_group.rotation_y -= delta.x * 200
        cube_group.rotation_x += delta.y * 200

        last_mouse_pos = mouse.position


