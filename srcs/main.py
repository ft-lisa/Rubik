from ursina import Ursina
import argparse
import srcs.cube as cube
import srcs.controls as controls
from srcs.parsing import parse_moves, mix_cube
from srcs.cubie import rubik
from srcs.bfs import bfs
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
    parser.add_argument(
        "--calculate-heuristic",
        action="store_true",
        help="Calculate heuristic database for the Rubik's cube",
    )
    return parser.parse_args(), parser


def check_args(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    if not args.moves and not args.hands_on and not args.calculate_heuristic:
        parser.error(
            "At least one of --moves, --hands-on, or --calculate-heuristic must be provided."
        )


def input(key):
    controls.input(key)


def update():
    controls.update()


sys.modules["__main__"].input = input
sys.modules["__main__"].update = update


def apply_moves(moves):
    moves = moves.split(" ")

    if parse_moves(moves):
        app = Ursina()
        cube.create_cube()
        mix_cube(moves)
        rubik.resolve_cube(moves)
        app.run()
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
        elif args.calculate_heuristic:
            bfs.calculate_heuristic()
        elif args.moves:
            apply_moves(args.moves)
    except (ValueError, AssertionError) as error:
        print(type(error).__name__ + ":", error)


if __name__ == "__main__":
    main()
