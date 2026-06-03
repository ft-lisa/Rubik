from ursina import Ursina
import argparse
import srcs.cube as cube
import srcs.controls as controls
from srcs.parsing import parse_moves
from srcs.rubik import rubik
from srcs.bfs import bfs
from srcs.ida import ida
import sys
from srcs.utils import mix_cube


def get_args() -> tuple[argparse.Namespace, argparse.ArgumentParser]:
    parser = argparse.ArgumentParser(description="Rubik's Cube Solver")
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
        "--calculate-heuristics",
        action="store_true",
        help="Calculate heuristics for all configurations",
    )

    return parser.parse_args(), parser


def check_args(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    if not args.moves and not args.hands_on and not args.calculate_heuristics:
        parser.error(
            "At least one of --moves, --hands-on, or --calculate-heuristics must be provided."
        )


def input(key):
    controls.input(key)


def update():
    controls.update()


sys.modules["__main__"].input = input
sys.modules["__main__"].update = update


def apply_moves(moves):
    moves = moves.strip().split()

    is_valid, parsed_moves = parse_moves(moves)
    if is_valid:
        app = Ursina()
        cube.create_cube()
        mix_cube(parsed_moves)
        rubik.shuffle_rubik(parsed_moves)

        bfs.load_heuristics()

        g1_moves = ida.run_G1()
        if g1_moves:
            rubik.shuffle_rubik(g1_moves)

        resolution_moves = ida.run_resolution()

        full_moves = g1_moves + resolution_moves
        mix_cube(full_moves)

        app.run()
    else:
        raise ValueError(
            "Invalid move sequence. Moves must be in the format: "
            "R, R', R2, U, U', U2, etc."
        )


def hands_on():
    app = Ursina()
    cube.create_cube()
    app.run()


def main():
    args, parser = get_args()
    try:
        check_args(args, parser)
        if args.hands_on:
            hands_on()
        if args.calculate_heuristics:
            bfs.calculate_heuristic()
        elif args.moves:
            apply_moves(args.moves)
    except (ValueError, AssertionError) as error:
        print(type(error).__name__ + ":", error)


if __name__ == "__main__":
    main()
