from cube.moves import *

def mix_cube(moves):
    global move_queue
    
    parsed_moves = []
    for move in moves:
        face = move[0]
        direction = 1
        
        if len(move) > 1:
            if move[1] == "'":
                direction = -1
            elif move[1] == "2":
                # Pour R2, ajouter deux mouvements séparés
                parsed_moves.append((face, direction))
                parsed_moves.append((face, direction))
                continue
        
        parsed_moves.append((face, direction))
    
    move_queue.extend(parsed_moves)
    
    # Appeler le premier mouvement directement sans délai
    if not is_animating and move_queue:
        next_move, direction = move_queue.pop(0)
        func = globals().get('mouv_' + next_move)
        if func:
            func(direction)

def parse_moves(moves):
    valid_faces = {'F', 'R', 'U', 'B', 'L', 'D'}
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
