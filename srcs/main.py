from ursina import Ursina
import argparse
import srcs.cube as cube
import srcs.controls as controls
from srcs.parsing import parse_moves, mix_cube


def get_args() -> tuple[argparse.Namespace, argparse.ArgumentParser]:
    parser = argparse.ArgumentParser(description="Image augmentation")
    parser.add_argument(
        "--moves",
        type=str,
        required=True,
        metavar="N",
        help="Sequence of moves (e.g. \"R U R' U'\")",
    )
    return parser.parse_args(), parser


def check_args(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    if not args.moves:
        parser.error("You must provide a sequence of moves using --moves")


def apply_moves(moves):
    moves = moves.split(" ")

    if parse_moves(moves):
        app = Ursina()

        cube.create_cube()

        def input(key):
            controls.input(key)

        def update():
            controls.update()

        mix_cube(moves)
        app.run()
    else:
        raise ValueError(
            "Invalid move sequence. Moves must be in the format: "
            "R, R', R2, U, U', U2, etc."
        )


def main():
    args, parser = get_args()
    try:
        check_args(args, parser)
        apply_moves(args.moves)
    except (ValueError, AssertionError) as error:
        print(type(error).__name__ + ":", error)


if __name__ == "__main__":
    main()
