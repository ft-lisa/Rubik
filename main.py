from ursina import *
import scene_cube

app = Ursina()

scene_cube.create_rubik()
scene_cube.mouv_R()

def input(key):
    scene_cube.input(key)

def update():
    scene_cube.update()


app.run()

