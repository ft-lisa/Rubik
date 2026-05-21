from ursina import *
import cube.moves as cube
from cube.cube import cube_group


dragging = False
last_mouse_pos = Vec2(0, 0)


def input(key):
    global dragging, last_mouse_pos

    if key == 'left mouse down':
        dragging = True
        last_mouse_pos = mouse.position

    if key == 'left mouse up':
        dragging = False
    
    if key == 'r':
        cube.mouv_R()
    elif key == 'l':
        cube.mouv_L()
    elif key == 'u':
        cube.mouv_U()
    elif key == 'd':
        cube.mouv_D()
    elif key == 'f':
        cube.mouv_F()
    elif key == 'b':
        cube.mouv_B()

def update():
    global last_mouse_pos

    if dragging:
        delta = mouse.position - last_mouse_pos

        # rotation souris
        cube_group.rotation_y -= delta.x * 200
        cube_group.rotation_x += delta.y * 200

        last_mouse_pos = mouse.position


