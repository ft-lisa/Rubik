from ursina import *
from cube.cube import cubes
from cube.cube import cube_group

is_animating = False
move_queue = []

def process_queue():
    global move_queue
    if not move_queue:
        return
    next_move = move_queue.pop(0)
    func = globals().get('mouv_' + next_move)
    if func:
        invoke(func, delay=0.01)


def snap_cube(cube):
    # snap position to integer gri
    cube.x = round(cube.x)
    cube.y = round(cube.y)
    cube.z = round(cube.z)
    # snap rotations to nearest multiple of 90
    cube.rotation_x = round(cube.rotation_x / 90) * 90
    cube.rotation_y = round(cube.rotation_y / 90) * 90
    cube.rotation_z = round(cube.rotation_z / 90) * 90

def finish_move(pivot):
    global is_animating
    for cube in pivot.children:
        cube.world_parent = cube_group
        snap_cube(cube)

    destroy(pivot)
    is_animating = False
    process_queue()

# DROITE
def mouv_R():
    global is_animating, move_queue
    if is_animating:
        move_queue.append('R')
        return
    is_animating = True

    pivot = Entity(parent=cube_group)

    for cube in cubes:
        if round(cube.x) == 1:
            cube.world_parent = pivot

    pivot.position = (0, 0, 0)

    pivot.animate_rotation_x(90, duration=0.2, curve=curve.linear)



    invoke(lambda: finish_move(pivot), delay=0.2)

# AVANT
def mouv_F():
    global is_animating, move_queue
    if is_animating:
        move_queue.append('F')
        return
    is_animating = True

    pivot = Entity(parent=cube_group)

    for cube in cubes:
        if round(cube.z) == -1:
            cube.world_parent = pivot

    pivot.position = (0, 0, 0)

    pivot.animate_rotation_z(90, duration=0.2, curve=curve.linear)

    invoke(lambda: finish_move(pivot), delay=0.2)

# HAUT
def mouv_U():
    global is_animating, move_queue
    if is_animating:
        move_queue.append('U')
        return
    is_animating = True

    pivot = Entity(parent=cube_group)

    for cube in cubes:
        if round(cube.y) == 1:
            cube.world_parent = pivot

    pivot.position = (0, 0, 0)

    pivot.animate_rotation_y(90, duration=0.2, curve=curve.linear)

    invoke(lambda: finish_move(pivot), delay=0.2)

# ARRIÈRE
def mouv_B():
    global is_animating, move_queue
    if is_animating:
        move_queue.append('B')
        return
    is_animating = True

    pivot = Entity(parent=cube_group)

    for cube in cubes:
        if round(cube.z) == 1:
            cube.world_parent = pivot

    pivot.position = (0, 0, 0)

    pivot.animate_rotation_z(-90, duration=0.2, curve=curve.linear)

    invoke(lambda: finish_move(pivot), delay=0.2)

# GAUCHE
def mouv_L():
    global is_animating, move_queue
    if is_animating:
        move_queue.append('L')
        return
    is_animating = True

    pivot = Entity(parent=cube_group)

    for cube in cubes:
        if round(cube.x) == -1:
            cube.world_parent = pivot

    pivot.position = (0, 0, 0)

    pivot.animate_rotation_x(-90, duration=0.2, curve=curve.linear)

    invoke(lambda: finish_move(pivot), delay=0.2)

# BAS
def mouv_D():
    global is_animating, move_queue
    if is_animating:
        move_queue.append('D')
        return
    is_animating = True

    pivot = Entity(parent=cube_group)

    for cube in cubes:
        if round(cube.y) == -1:
            cube.world_parent = pivot

    pivot.position = (0, 0, 0)

    pivot.animate_rotation_y(-90, duration=0.2, curve=curve.linear)

    invoke(lambda: finish_move(pivot), delay=0.2)
