from srcs.rubik import rubik
import time
import pickle
import os


class BFS:

    def __init__(self):
        self.dir_path = f"heuristics/"

        self.visited_edges = {}
        self.visited_corners = {}
        self.visited_slice = {}

        self.resolved_edges = {}
        self.resolved_corners = {}
        self.resolved_slice = {}

        self.max_depth = 40

    def save_heuristics(self, name: str) -> None:
        full_name = f"{self.dir_path}{name}"

        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)

        if name == "edges":
            with open(f"{full_name}_heuristic.pkl", "wb") as f:
                pickle.dump(self.visited_edges, f)
        elif name == "corners":
            with open(f"{full_name}_heuristic.pkl", "wb") as f:
                pickle.dump(self.visited_corners, f)
        elif name == "slices":
            with open(f"{full_name}_heuristic.pkl", "wb") as f:
                pickle.dump(self.visited_slice, f)

    def load_heuristics(self) -> None:

        if not os.path.exists(self.dir_path):
            raise FileNotFoundError(
                f"Heuristic directory '{self.dir_path}' not found. Please calculate heuristics first."
            )

        for file in os.listdir(self.dir_path):
            if file.endswith("edges_heuristic.pkl"):
                with open(f"{self.dir_path}{file}", "rb") as f:
                    self.visited_edges = pickle.load(f)
            elif file.endswith("corners_heuristic.pkl"):
                with open(f"{self.dir_path}{file}", "rb") as f:
                    self.visited_corners = pickle.load(f)
            else:
                with open(f"{self.dir_path}{file}", "rb") as f:
                    self.visited_slice = pickle.load(f)


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

        self.save_heuristics("edges")

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

        self.save_heuristics("corners")

    def apply_slice_move(self, state: tuple[int], move: int) -> tuple[int]:
        perm = rubik.move_ep[move]

        new_slice = [0] * 12

        # state[i] == 1 si la position i contient une arete de tranche.
        # On suit uniquement la position (pas l'identite), donc on applique
        # la meme permutation que pour les aretes au masque tranche/pas-tranche.
        for i in range(12):
            new_slice[i] = state[perm[i]]

        return tuple(new_slice)

    def build_slice_heuristic(
        self,
    ) -> dict:

        start_slice = tuple([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1])

        queue = [(start_slice, 0)]

        self.visited_slice[start_slice] = 0

        while queue:
            state, depth = queue.pop(0)

            if depth >= self.max_depth:
                continue

            for move in rubik.moves:
                new_slice = self.apply_slice_move(state, move)

                if new_slice not in self.visited_slice:
                    self.visited_slice[new_slice] = depth + 1
                    queue.append((new_slice, depth + 1))

        self.save_heuristics("slices")

    def calculate_heuristic(self) -> None:
        self.build_edges_heuristic()
        self.build_corner_heuristic()
        self.build_slice_heuristic()

    def apply_edge_permutation(self, move: int, prev_state: tuple[int]) -> tuple[int]:
        perm = rubik.move_ep[move]

        new_state = [0] * 8

        # print("-" * 30)
        # print("prev_state", prev_state)

        for i in range(8):
            new_state[i] = prev_state[perm[i]]
            # print(prev_state[perm[i]])
            # print("new_state", new_state)
            # print("new_er", new_er)

        return new_state

    def build_edges_resolution(self) -> None:

        prev_state = tuple([0, 1, 2, 3, 4, 5, 6, 7])

        queue = [(prev_state, 0)]
        self.resolved_edges[prev_state] = 0

        while queue:
            prev_state, depth = queue.pop(0)

            if depth >= self.max_depth:
                continue

            for move in rubik.legal_moves:
                # print("-" * 20)
                # print("Applying move:", move)
                new_state = tuple(self.apply_edge_permutation(move, prev_state))

                if new_state not in self.resolved_edges:
                    self.resolved_edges[new_state] = depth + 1
                    queue.append((new_state, depth + 1))


    def apply_corner_permutation(self, move: int, prev_state: tuple[int]) -> tuple[int]:
        perm = rubik.move_cp[move]

        new_po = [0] * 8

        # permutation des positions
        for i in range(8):

            new_po[i] = prev_state[perm[i]]

        return tuple(new_po)

    def build_corners_resolution(
        self,
    ) -> dict:

        start_cp = tuple([0, 1, 2, 3, 4, 5, 6, 7])

        queue = [(start_cp, 0)]

        self.resolved_corners[start_cp] = 0

        while queue:
            prev_cp, depth= queue.pop(0)

            if depth >= self.max_depth:
                continue

            for move in rubik.legal_moves:
                new_cp = self.apply_corner_permutation(move, prev_cp)

                if new_cp not in self.resolved_corners:
                    self.resolved_corners[new_cp] = depth + 1
                    queue.append((new_cp, depth + 1))

    def apply_slice_permutation(self, prev_slice: tuple[int], move: int) -> tuple[int]:
        perm = rubik.move_ep[move]

        new_slice = [0] * 12

        # state[i] == 1 si la position i contient une arete de tranche.
        # On suit uniquement la position (pas l'identite), donc on applique
        # la meme permutation que pour les aretes au masque tranche/pas-tranche.
        for i in range(12):
            new_slice[i] = prev_slice[perm[i]]

        return tuple(new_slice)

    def build_slice_resolution(
        self,
    ) -> dict:

        start_slice = tuple([0, 0, 0, 0, 0, 0, 0, 0, 8, 9, 10, 11])

        queue = [(start_slice, 0)]

        self.resolved_slice[start_slice] = 0

        while queue:
            prev_slice, depth = queue.pop(0)

            if depth >= self.max_depth:
                continue

            for move in rubik.legal_moves:
                new_slice = self.apply_slice_permutation(prev_slice, move)

                if new_slice not in self.resolved_slice:
                    self.resolved_slice[new_slice] = depth + 1
                    queue.append((new_slice, depth + 1))


    def calculate_resolution(self) -> None:
        start_time = time.time()
        self.build_edges_resolution()
        self.build_corners_resolution()
        self.build_slice_resolution()

        end_time = time.time()
        print(f"Resolution time: {end_time - start_time}")

        table = self.resolved_slice
        by_depth = {}
        for state_key, depth in table.items():
            if depth not in by_depth:
                by_depth[depth] = 0
            by_depth[depth] += 1

        print("\nStates by distance from solved:")
        for depth in sorted(by_depth.keys()):
            print(f"  Depth {depth}: {by_depth[depth]:,} states")

        print(f"\nExtracted {len(table):,} unique CO states")


bfs = BFS()
