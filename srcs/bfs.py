from srcs.rubik import rubik
import time
import pickle
import os


class BFS:

    def __init__(self):
        self.dir_path = f"heuristics/"

        self.orientation_edges = {}
        self.orientation_corners = {}
        self.position_slices = {}

        self.permutation_edges = {}
        self.permutation_corners = {}
        self.permutation_slices = {}

        self.max_depth = 40

    def save_heuristics(self) -> None:

        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)

        with open(f"{self.dir_path}orientation_edges_heuristic.pkl", "wb") as f:
            pickle.dump(self.orientation_edges, f)
        with open(f"{self.dir_path}orientation_corners_heuristic.pkl", "wb") as f:
            pickle.dump(self.orientation_corners, f)
        with open(f"{self.dir_path}position_slices_heuristic.pkl", "wb") as f:
            pickle.dump(self.position_slices, f)

        with open(f"{self.dir_path}permutation_edges_heuristic.pkl", "wb") as f:
            pickle.dump(self.permutation_edges, f)
        with open(f"{self.dir_path}permutation_corners_heuristic.pkl", "wb") as f:
            pickle.dump(self.permutation_corners, f)
        with open(f"{self.dir_path}permutation_slices_heuristic.pkl", "wb") as f:
            pickle.dump(self.permutation_slices, f)

    def load_heuristics(self) -> None:

        if not os.path.exists(self.dir_path):
            raise FileNotFoundError(
                f"Heuristic directory '{self.dir_path}' not found. Please calculate heuristics first."
            )

        for file in os.listdir(self.dir_path):
            if file.endswith("orientation_edges_heuristic.pkl"):
                with open(f"{self.dir_path}{file}", "rb") as f:
                    self.orientation_edges = pickle.load(f)
            elif file.endswith("orientation_corners_heuristic.pkl"):
                with open(f"{self.dir_path}{file}", "rb") as f:
                    self.orientation_corners = pickle.load(f)
            elif file.endswith("position_slices_heuristic.pkl"):
                with open(f"{self.dir_path}{file}", "rb") as f:
                    self.position_slices = pickle.load(f)
            elif file.endswith("permutation_edges_heuristic.pkl"):
                with open(f"{self.dir_path}{file}", "rb") as f:
                    self.permutation_edges = pickle.load(f)
            elif file.endswith("permutation_corners_heuristic.pkl"):
                with open(f"{self.dir_path}{file}", "rb") as f:
                    self.permutation_corners = pickle.load(f)
            elif file.endswith("permutation_slices_heuristic.pkl"):
                with open(f"{self.dir_path}{file}", "rb") as f:
                    self.permutation_slices = pickle.load(f)

    def apply_orientation_edges(self, state: tuple[int], move: int) -> tuple[int]:
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

    def build_orientation_edges(
        self,
    ) -> dict:

        start_eo = tuple([0] * 12)

        queue = [(start_eo, 0)]

        self.orientation_edges[start_eo] = 0

        while queue:
            state, depth = queue.pop(0)

            if depth >= self.max_depth:
                continue

            for move in rubik.moves:
                new_eo = self.apply_orientation_edges(state, move)

                if new_eo not in self.orientation_edges:
                    self.orientation_edges[new_eo] = depth + 1
                    queue.append((new_eo, depth + 1))

    def apply_orientation_corners(self, state: tuple[int], move: int) -> tuple[int]:
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

    def build_orientation_corners(
        self,
    ) -> dict:

        start_co = tuple([0] * 8)

        queue = [(start_co, 0)]

        self.orientation_corners[start_co] = 0

        while queue:
            state, depth = queue.pop(0)

            if depth >= self.max_depth:
                continue

            for move in rubik.moves:
                new_co = self.apply_orientation_corners(state, move)

                if new_co not in self.orientation_corners:
                    self.orientation_corners[new_co] = depth + 1
                    queue.append((new_co, depth + 1))

    def apply_position_slices(self, state: tuple[int], move: int) -> tuple[int]:
        perm = rubik.move_ep[move]

        new_slice = [0] * 12

        # state[i] == 1 si la position i contient une arete de tranche.
        # On suit uniquement la position (pas l'identite), donc on applique
        # la meme permutation que pour les aretes au masque tranche/pas-tranche.
        for i in range(12):
            new_slice[i] = state[perm[i]]

        return tuple(new_slice)

    def build_position_slices(
        self,
    ) -> dict:

        start_slice = tuple([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1])

        queue = [(start_slice, 0)]

        self.position_slices[start_slice] = 0

        while queue:
            state, depth = queue.pop(0)

            if depth >= self.max_depth:
                continue

            for move in rubik.moves:
                new_slice = self.apply_position_slices(state, move)

                if new_slice not in self.position_slices:
                    self.position_slices[new_slice] = depth + 1
                    queue.append((new_slice, depth + 1))

    def apply_permutation_edges(self, move: int, prev_state: tuple[int]) -> tuple[int]:
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

    def build_permutation_edges(self) -> None:

        prev_state = tuple([0, 1, 2, 3, 4, 5, 6, 7])

        queue = [(prev_state, 0)]
        self.permutation_edges[prev_state] = 0

        while queue:
            prev_state, depth = queue.pop(0)

            if depth >= self.max_depth:
                continue

            for move in rubik.legal_moves:
                # print("-" * 20)
                # print("Applying move:", move)
                new_state = tuple(self.apply_permutation_edges(move, prev_state))

                if new_state not in self.permutation_edges:
                    self.permutation_edges[new_state] = depth + 1
                    queue.append((new_state, depth + 1))

    def apply_permutation_corners(
        self, move: int, prev_state: tuple[int]
    ) -> tuple[int]:
        perm = rubik.move_cp[move]

        new_po = [0] * 8

        # permutation des positions
        for i in range(8):

            new_po[i] = prev_state[perm[i]]

        return tuple(new_po)

    def build_permutation_corners(
        self,
    ) -> dict:

        start_cp = tuple([0, 1, 2, 3, 4, 5, 6, 7])

        queue = [(start_cp, 0)]

        self.permutation_corners[start_cp] = 0

        while queue:
            prev_cp, depth = queue.pop(0)

            if depth >= self.max_depth:
                continue

            for move in rubik.legal_moves:
                new_cp = self.apply_permutation_corners(move, prev_cp)

                if new_cp not in self.permutation_corners:
                    self.permutation_corners[new_cp] = depth + 1
                    queue.append((new_cp, depth + 1))

    def apply_permutation_slices(self, prev_slice: tuple[int], move: int) -> tuple[int]:
        perm = rubik.move_ep[move]

        new_slice = [0] * 12

        # state[i] == 1 si la position i contient une arete de tranche.
        # On suit uniquement la position (pas l'identite), donc on applique
        # la meme permutation que pour les aretes au masque tranche/pas-tranche.
        for i in range(12):
            new_slice[i] = prev_slice[perm[i]]

        return tuple(new_slice)

    def build_permutation_slices(
        self,
    ) -> dict:

        start_slice = tuple([0, 0, 0, 0, 0, 0, 0, 0, 8, 9, 10, 11])

        queue = [(start_slice, 0)]

        self.permutation_slices[start_slice] = 0

        while queue:
            prev_slice, depth = queue.pop(0)

            if depth >= self.max_depth:
                continue

            for move in rubik.legal_moves:
                new_slice = self.apply_permutation_slices(prev_slice, move)

                if new_slice not in self.permutation_slices:
                    self.permutation_slices[new_slice] = depth + 1
                    queue.append((new_slice, depth + 1))

    def calculate_heuristic(self) -> None:
        self.build_orientation_edges()
        self.build_orientation_corners()
        self.build_position_slices()

        self.build_permutation_edges()
        self.build_permutation_corners()
        self.build_permutation_slices()

        self.save_heuristics()


bfs = BFS()
