from ursina import *

app = Ursina()
cube_group = Entity()


cubes = []
for z in range(3):
    for y in range(3):
        for x in range(3):
            cube = Entity(parent=cube_group, 
                        model='cube',
                        color=color.red,
                        texture="white_cube", 
                        scale=(1), position=(x - 1, y - 1, z - 1)
                    )
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
        cube_group.rotation_y += delta.x * 200
        cube_group.rotation_x -= delta.y * 200

        last_mouse_pos = mouse.position


app.run()

