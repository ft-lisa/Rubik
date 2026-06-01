from srcs.rubik import rubik
import time


class BFS:

    def __init__(self):
        self.visited_edges = {}
        self.visited_corners = {}
        self.visited_slice = {}

        self.resolved_edges = {}
        self.resolved_corners = {}

        self.max_depth = 40

    def apply_edge_move(self, state: tuple[int], move: int) -> tuple[int]:
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

    def apply_corner_move(self, state: tuple[int], move: int) -> tuple[int]:
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

    # def apply_slice_move(self, state: tuple[int], move: int) -> tuple[int]:
    #     perm = rubik.move_ep[move]

    #     new_slice = [0] * 12

    #     # state[i] == 1 si la position i contient une arete de tranche.
    #     # On suit uniquement la position (pas l'identite), donc on applique
    #     # la meme permutation que pour les aretes au masque tranche/pas-tranche.
    #     for i in range(12):
    #         new_slice[i] = state[perm[i]]

    #     return tuple(new_slice)

    # def build_slice_heuristic(
    #     self,
    # ) -> dict:

    #     start_slice = tuple([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1])

    #     queue = [(start_slice, 0)]

    #     self.visited_slice[start_slice] = 0

    #     while queue:
    #         state, depth = queue.pop(0)

    #         if depth >= self.max_depth:
    #             continue

    #         for move in rubik.moves:
    #             new_slice = self.apply_slice_move(state, move)

    #             if new_slice not in self.visited_slice:
    #                 self.visited_slice[new_slice] = depth + 1
    #                 queue.append((new_slice, depth + 1))

    def calculate_heuristic(self) -> None:
        self.build_edges_heuristic()
        self.build_corner_heuristic()
        # self.build_slice_heuristic()

        print(len(self.visited_edges))
        print(len(self.visited_corners))
        print(len(self.visited_slice))

        print(self.visited_slice)

    def apply_edge_permutation(self, move: int, prev_state: tuple[int]) -> tuple[int]:
        perm = rubik.move_ep[move]

        new_er = [0] * 12
        new_state = [0] * 12

        # print("-" * 30)
        # print("prev_state", prev_state)

        for i in range(12):
            new_state[i] = prev_state[perm[i]]
            new_er[i] = 0 if i == new_state[i] else 1
            # print(prev_state[perm[i]])
            # print("new_state", new_state)
            # print("new_er", new_er)

        return tuple(new_er), new_state

    def build_edges_resolution(self) -> None:

        prev_state = tuple([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        start_er = tuple([0] * 12)

        queue = [(prev_state, 0)]
        self.resolved_edges[start_er] = 0

        while queue:
            prev_state, depth = queue.pop(0)

            if depth >= self.max_depth:
                continue

            for move in rubik.legal_moves:
                # print("-" * 20)
                # print("Applying move:", move)
                new_er, new_state = self.apply_edge_permutation(move, prev_state)

                # print("new_er", new_er)
                # print("new_state", new_state)

                if new_er not in self.resolved_edges:
                    self.resolved_edges[new_er] = depth + 1
                    queue.append((new_state, depth + 1))

    def calculate_resolution(self) -> None:
        start_time = time.time()
        self.build_edges_resolution()

        end_time = time.time()
        print(f"Resolution time: {end_time - start_time}")
        print(len(self.resolved_edges))
        # print(self.resolved_edges)


bfs = BFS()
