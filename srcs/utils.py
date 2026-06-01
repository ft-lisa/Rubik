from srcs.parsing import REVERSE_MODIFIERS
from srcs.moves import rMoves


def determine_move(move: str) -> tuple[str, int]:
    direction = 1

    if len(move) > 1 and move[1] in REVERSE_MODIFIERS:
        direction = -1
        move = move[0]

    return move, direction


def mix_cube(moves):
    parsed_moves = {}

    for move in moves:
        move, direction = determine_move(move)
        parsed_moves[move] = direction

    for move, direction in parsed_moves.items():
        rMoves.do_move(move, direction)

    for move, direction in parsed_moves.items():
        rMoves.do_move(move, direction)
