from ursina import *

app = Ursina()
cube_group = Entity()


cubes = []

def create_cube(x, y, z):

    cube = Entity(
        parent=cube_group,
        model='cube',
        color=color.black,
        texture='white_cube',
        position=(x, y, z)
    )

    # FACE AVANT
    Entity(
        parent=cube,
        model='quad',
        color=color.green,
        position=(0, 0, -0.51),
        scale=(0.90)
    )

    # FACE ARRIÈRE
    Entity(
        parent=cube,
        model='quad',
        color=color.blue,
        rotation_y=180,
        position=(0, 0, 0.51),
        scale=(0.90)
    )

    # FACE DROITE
    Entity(
        parent=cube,
        model='quad',
        color=color.red,
        rotation_y=-90,
        position=(0.51, 0, 0),
        scale=(0.90)
    )

    # FACE GAUCHE
    Entity(
        parent=cube,
        model='quad',
        color=color.orange,
        rotation_y=90,
        position=(-0.51, 0, 0),
        scale=(0.90)
    )

    # FACE HAUT
    Entity(
        parent=cube,
        model='quad',
        color=color.white,
        rotation_x=90,
        position=(0, 0.51, 0),
        scale=(0.90)
    )

    # FACE BAS
    Entity(
        parent=cube,
        model='quad',
        color=color.yellow,
        rotation_x=-90,
        position=(0, -0.51, 0),
        scale=(0.90)
    )
    return cube

def create_rubik():
    for z in range(3):
        for y in range(3):
            for x in range(3):
                cube = create_cube(x, y, z)
                cubes.append(cube)

dragging = False
last_mouse_pos = Vec2(0, 0)


def input(key):
    global dragging, last_mouse_pos

    if key == 'left mouse down':
        dragging = True
        last_mouse_pos = mouse.position

    if key == 'left mouse up':
        dragging = False


def update():
    global last_mouse_pos

    if dragging:
        delta = mouse.position - last_mouse_pos

        # rotation selon mouvement souris
        cube_group.rotation_y -= delta.x * 200
        cube_group.rotation_x += delta.y * 200

        last_mouse_pos = mouse.position