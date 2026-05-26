from ursina import *
import sys
import cube.cube as cube
import cube.controls as controls
from parsing import parse_moves, mix_cube
# sys.argv[1]

if len(sys.argv) > 1:
    app = Ursina()
    sequence = sys.argv[1]
    moves = sequence.split(' ')

    if (parse_moves(moves)):

        cube.create_cube()
        

        def input(key):
            controls.input(key)

        def update():
            controls.update()
        mix_cube(moves)
        app.run()

