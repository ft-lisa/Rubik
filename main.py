from ursina import *
import cube.cube as cube
import cube.controls as controls

app = Ursina()

cube.create_cube()

def input(key):
    controls.input(key)

def update():
    controls.update()

app.run()

