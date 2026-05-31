from srcs.moves import rMoves

REVERSE_MODIFIERS = {"'", "’"}
DOUBLE_MODIFIERS = {"2"}
VALID_MOVES = {"F", "R", "U", "B", "L", "D"}


def determine_move(move: str) -> tuple[str, int]:
    direction = 1

    if len(move) > 1:
        if move[1] in REVERSE_MODIFIERS:
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


def parse_moves(moves: list[str]) -> tuple[bool, list[str]]:
    real_moves = []

    for move in moves:

        # longueur valide : "R" / "R'" / "R2"
        if len(move) > 2 or len(move) < 1:
            return False, []

        # Première lettre
        if move[0] not in VALID_MOVES:
            return False, []

        real_moves.append(move[0])

        # Deuxième caractère si présent
        if len(move) == 2:
            if move[1] not in REVERSE_MODIFIERS and move[1] not in DOUBLE_MODIFIERS:
                return False, []
            if move[1] in REVERSE_MODIFIERS:
                real_moves[-1] += "'"
            elif move[1] in DOUBLE_MODIFIERS:
                real_moves.append(move[0])

    return True, real_moves
