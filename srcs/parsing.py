from srcs.utils import VALID_MOVES, REVERSE_MODIFIERS, DOUBLE_MODIFIERS


def parse_moves(moves: list[str]) -> tuple[bool, list[str]]:
    parsed_moves = []

    for move in moves:

        if len(move) > 2 or len(move) < 1:
            return False, []

        if move[0] not in VALID_MOVES:
            return False, []

        if len(move) == 2:
            if move[1] not in REVERSE_MODIFIERS and move[1] not in DOUBLE_MODIFIERS:
                return False, []

        parsed_moves.append(move)

    return True, parsed_moves
