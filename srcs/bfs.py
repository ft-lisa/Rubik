from srcs.rubik import rubik


class BFS:

    def __init__(self):
        self.visited_edges = {}
        self.visited_corners = {}
        self.max_depth = 20

    def apply_edge_move(self, state, move):
        perm = rubik.move_ep[move]
        flip = rubik.move_eo[move]

        new_eo = [0] * 12

        # permutation des positions
        for i in range(12):
            src = perm[i]

            # l'orientation de la nouvelle arête à la position i vient de l'arête à src
            # plus le flip créé par le mouvement à cette position
            new_eo[i] = state[src] ^ flip[i]

        return tuple(new_eo)

    def build_edges_heuristic(
        self,
    ) -> dict:

        start_eo = tuple([0] * 12)

        queue = [(start_eo, 0)]

        self.visited_edges[start_eo] = 0

        while queue:
            state, depth = queue.pop(0)

            if depth >= self.max_depth:
                continue

            for move in rubik.moves:
                new_eo = self.apply_edge_move(state, move)

                if new_eo not in self.visited_edges:
                    self.visited_edges[new_eo] = depth + 1
                    queue.append((new_eo, depth + 1))

    def apply_corner_move(self, state, move):
        perm = rubik.move_cp[move]
        twist = rubik.move_co[move]

        new_co = [0] * 8

        # permutation des positions
        for i in range(8):
            src = perm[i]

            # l'orientation du nouveau coin à la position i vient du coin à src
            # plus le twist créé par le mouvement à cette position
            new_co[i] = (state[src] + twist[i]) % 3

        return tuple(new_co)

    def build_corner_heuristic(
        self,
    ) -> dict:

        start_co = tuple([0] * 8)

        queue = [(start_co, 0)]

        self.visited_corners[start_co] = 0

        while queue:
            state, depth = queue.pop(0)

            if depth >= self.max_depth:
                continue

            for move in rubik.moves:
                new_co = self.apply_corner_move(state, move)

                if new_co not in self.visited_corners:
                    self.visited_corners[new_co] = depth + 1
                    queue.append((new_co, depth + 1))

    def calculate_heuristic(self):
        self.build_edges_heuristic()
        self.build_corner_heuristic()


bfs = BFS()
