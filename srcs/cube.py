from ursina import Entity, color

cube_group = Entity()

cubes = []


def create_default_cube(x, y, z):

    cube = Entity(
        parent=cube_group,
        model="cube",
        color=color.black,
        texture="white_cube",
        position=(x, y, z),
    )

    # FACE AVANT
    Entity(
        parent=cube,
        model="quad",
        color=color.green,
        position=(0, 0, -0.51),
        scale=(0.90),
    )

    # FACE ARRIÈRE
    Entity(
        parent=cube,
        model="quad",
        color=color.blue,
        rotation_y=180,
        position=(0, 0, 0.51),
        scale=(0.90),
    )

    # FACE DROITE
    Entity(
        parent=cube,
        model="quad",
        color=color.red,
        rotation_y=-90,
        position=(0.51, 0, 0),
        scale=(0.90),
    )

    # FACE GAUCHE
    Entity(
        parent=cube,
        model="quad",
        color=color.orange,
        rotation_y=90,
        position=(-0.51, 0, 0),
        scale=(0.90),
    )

    # FACE HAUT
    Entity(
        parent=cube,
        model="quad",
        color=color.white,
        rotation_x=90,
        position=(0, 0.51, 0),
        scale=(0.90),
    )

    # FACE BAS
    Entity(
        parent=cube,
        model="quad",
        color=color.yellow,
        rotation_x=-90,
        position=(0, -0.51, 0),
        scale=(0.90),
    )
    return cube


def create_cube():
    for z in range(3):
        for y in range(3):
            for x in range(3):
                cube = create_default_cube(x - 1, y - 1, z - 1)
                cubes.append(cube)
