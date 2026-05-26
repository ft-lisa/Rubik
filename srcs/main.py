from ursina import Ursina
import srcs.cube as cube
import srcs.controls as controls


def main():
    import sys
    app = Ursina()
    cube.create_cube()

    main_module = sys.modules["__main__"]
    main_module.input = lambda key: controls.input(key)
    main_module.update = lambda: controls.update()

    app.run()


if __name__ == "__main__":
    main()
