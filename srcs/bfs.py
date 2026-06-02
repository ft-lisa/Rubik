from srcs.rubik import rubik
import pickle
import os
from collections import deque


class BFS:

    def __init__(self):
        self.dir_path = f"heuristics/"

        self.eo_so = {}
        self.co_so = {}

        self.ep_sp = {}
        self.cp_sp = {}
        self.permutation_slices = {}

        self.max_depth = 40

    def save_heuristics(self) -> None:

        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)

        with open(f"{self.dir_path}eo_so.pkl", "wb") as f:
            pickle.dump(self.eo_so, f)
        with open(f"{self.dir_path}co_so.pkl", "wb") as f:
            pickle.dump(self.co_so, f)

        with open(f"{self.dir_path}ep_sp.pkl", "wb") as f:
            pickle.dump(self.ep_sp, f)
        with open(f"{self.dir_path}cp_sp.pkl", "wb") as f:
            pickle.dump(self.cp_sp, f)

    def load_heuristics(self) -> None:

        if not os.path.exists(self.dir_path):
            raise FileNotFoundError(
                f"Heuristic directory '{self.dir_path}' not found. Please calculate heuristics first."
            )

        for file in os.listdir(self.dir_path):
            if file.endswith("eo_so.pkl"):
                with open(f"{self.dir_path}{file}", "rb") as f:
                    self.eo_so = pickle.load(f)
            elif file.endswith("co_so.pkl"):
                with open(f"{self.dir_path}{file}", "rb") as f:
                    self.co_so = pickle.load(f)

            elif file.endswith("ep_sp.pkl"):
                with open(f"{self.dir_path}{file}", "rb") as f:
                    self.ep_sp = pickle.load(f)
            elif file.endswith("cp_sp.pkl"):
                with open(f"{self.dir_path}{file}", "rb") as f:
                    self.cp_sp = pickle.load(f)

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

    def apply_position_slices(self, state: tuple[int], move: int) -> tuple[int]:
        perm = rubik.move_ep[move]

        new_slice = [0] * 12

        # state[i] == 1 si la position i contient une arete de tranche.
        # On suit uniquement la position (pas l'identite), donc on applique
        # la meme permutation que pour les aretes au masque tranche/pas-tranche.
        for i in range(12):
            new_slice[i] = state[perm[i]]

        return tuple(new_slice)

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

    def build_eo_so(
        self,
    ) -> dict:

        start_eo = tuple([0] * 12)
        start_so = tuple([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1])

        state = (start_eo, start_so)

        queue = deque([(state, 0)])
        self.eo_so[state] = 0

        while queue:
            (eo, so), depth = queue.popleft()

            if depth >= self.max_depth:
                continue

            for move in rubik.moves:
                new_eo = self.apply_orientation_edges(eo, move)
                new_so = self.apply_position_slices(so, move)

                new_state = (new_eo, new_so)
                if new_state not in self.eo_so:
                    self.eo_so[new_state] = depth + 1
                    queue.append((new_state, depth + 1))

    def build_co_so(
        self,
    ) -> dict:

        start_co = tuple([0] * 8)
        start_so = tuple([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1])

        state = (start_co, start_so)

        queue = deque([(state, 0)])
        self.co_so[state] = 0

        while queue:
            (co, so), depth = queue.popleft()

            if depth >= self.max_depth:
                continue

            for move in rubik.moves:
                new_co = self.apply_orientation_corners(co, move)
                new_so = self.apply_position_slices(so, move)

                new_state = (new_co, new_so)
                if new_state not in self.co_so:
                    self.co_so[new_state] = depth + 1
                    queue.append((new_state, depth + 1))

    def apply_permutation_edges(self, prev_state: tuple[int], move: int) -> tuple[int]:
        perm = rubik.move_ep[move]

        new_state = [0] * 8

        for i in range(8):
            new_state[i] = prev_state[perm[i]]

        return tuple(new_state)

    def apply_permutation_corners(
        self, prev_state: tuple[int], move: int
    ) -> tuple[int]:
        perm = rubik.move_cp[move]

        new_po = [0] * 8

        # permutation des positions
        for i in range(8):

            new_po[i] = prev_state[perm[i]]

        return tuple(new_po)

    def apply_permutation_slices(self, prev_state: tuple[int], move: int) -> tuple[int]:
        perm = rubik.move_ep[move]

        new_slice = [0] * 12

        # state[i] == 1 si la position i contient une arete de tranche.
        # On suit uniquement la position (pas l'identite), donc on applique
        # la meme permutation que pour les aretes au masque tranche/pas-tranche.
        for i in range(12):
            new_slice[i] = prev_state[perm[i]]

        return tuple(new_slice)

    def build_permutation_edges(self) -> None:

        start_ep = tuple([0, 1, 2, 3, 4, 5, 6, 7])
        start_sp = tuple([0, 0, 0, 0, 0, 0, 0, 0, 8, 9, 10, 11])

        state = (start_ep, start_sp)

        queue = deque([(state, 0)])
        self.ep_sp[state] = 0

        while queue:
            (ep, sp), depth = queue.popleft()

            if depth >= self.max_depth:
                continue

            for move in rubik.legal_moves:
                new_ep = self.apply_permutation_edges(ep, move)
                new_sp = self.apply_permutation_slices(sp, move)

                new_state = (new_ep, new_sp)
                if new_state not in self.ep_sp:
                    self.ep_sp[new_state] = depth + 1
                    queue.append((new_state, depth + 1))

    def build_permutation_corners(
        self,
    ) -> dict:

        start_cp = tuple([0, 1, 2, 3, 4, 5, 6, 7])
        start_sp = tuple([0, 0, 0, 0, 0, 0, 0, 0, 8, 9, 10, 11])

        state = (start_cp, start_sp)

        queue = deque([(state, 0)])

        self.cp_sp[state] = 0

        while queue:
            (cp, sp), depth = queue.popleft()

            if depth >= self.max_depth:
                continue

            for move in rubik.legal_moves:
                new_cp = self.apply_permutation_corners(cp, move)
                new_sp = self.apply_permutation_slices(sp, move)

                new_state = (new_cp, new_sp)

                if new_state not in self.cp_sp:
                    self.cp_sp[new_state] = depth + 1
                    queue.append((new_state, depth + 1))

    def calculate_heuristic(self) -> None:
        self.build_eo_so()
        self.build_co_so()

        self.build_permutation_edges()
        self.build_permutation_corners()

        self.save_heuristics()


bfs = BFS()
