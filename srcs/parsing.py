from srcs.moves import rMoves


def mix_cube(moves):
    parsed_moves = {}

    for move in moves:
        face = move[0]
        direction = 1

        if len(move) > 1:
            if move[1] == "'":
                direction = -1
            elif move[1] == "2":
                parsed_moves[face] = direction
                parsed_moves[face] = direction

        parsed_moves[face] = direction

    for face, direction in parsed_moves.items():
        rMoves.do_move(face, direction)


def parse_moves(moves):
    valid_faces = {"F", "R", "U", "B", "L", "D"}
    valid_modifiers = {"'", "2"}

    for move in moves:

        # longueur valide : "R" / "R'" / "R2"
        if len(move) > 2 or len(move) < 1:
            return False

        # Première lettre
        if move[0] not in valid_faces:
            return False

        # Deuxième caractère si présent
        if len(move) == 2:
            if move[1] not in valid_modifiers:
                return False

    return True
