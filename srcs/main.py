from ursina import Ursina
import argparse
import srcs.cube as cube
import srcs.controls as controls
from srcs.parsing import parse_moves, mix_cube
from srcs.rubik import rubik
from srcs.bfs import bfs
from srcs.ida import ida
import sys


def get_args() -> tuple[argparse.Namespace, argparse.ArgumentParser]:
    parser = argparse.ArgumentParser(description="Image augmentation")
    parser.add_argument(
        "--moves",
        type=str,
        required=False,
        metavar="N",
        help="Sequence of moves (e.g. \"R U R' U'\")",
    )
    parser.add_argument(
        "--hands-on",
        action="store_true",
        help="Enable hands-on mode for interactive cube manipulation",
    )
    return parser.parse_args(), parser


def check_args(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    if not args.moves and not args.hands_on:
        parser.error("At least one of --moves or --hands-on must be provided.")


def input(key):
    controls.input(key)


def update():
    controls.update()


sys.modules["__main__"].input = input
sys.modules["__main__"].update = update


def apply_moves(moves):
    moves = moves.strip().split()

    is_valid, real_moves = parse_moves(moves)
    if is_valid:
        app = Ursina()
        cube.create_cube()
        mix_cube(real_moves)
        rubik.shuffle_rubik(real_moves)

        bfs.calculate_heuristic()
        bfs.calculate_resolution()

        # moves = ida.run()
        # print("Moves to solve the cube:", moves)
        # # app.run()
    else:
        raise ValueError(
            "Invalid move sequence. Moves must be in the format: "
            "R, R', R2, U, U', U2, etc."
        )


def apply_hands_on():
    app = Ursina()
    cube.create_cube()
    app.run()


def main():
    args, parser = get_args()
    try:
        check_args(args, parser)
        if args.hands_on:
            apply_hands_on()
        elif args.moves:
            apply_moves(args.moves)
    except (ValueError, AssertionError) as error:
        print(type(error).__name__ + ":", error)


if __name__ == "__main__":
    main()
