from srcs.rubik import rubik
from srcs.bfs import bfs


class IDA_STAR:

    def __init__(self):
        self.moves = []
        self.threshold = 3
        self.min_threshold = None
        self.max_depth = 20

    def prune_branch(self, prev_move: str, curr_move: str) -> bool:
        if prev_move is None:
            return False
        elif prev_move == curr_move:
            return True
        elif rubik.OPPOSITE_FACES.get(prev_move[0]) == curr_move[0]:
            return True
        elif prev_move[0] == curr_move[0]:
            return True
        return False

    def run_G1(self) -> list[str]:

        self.moves = []

        eo_key = rubik.get_orientation_edges()
        co_key = rubik.get_orientation_corners()
        so_key = rubik.get_position_slices()

        self.threshold = max(
            bfs.eo_so[(eo_key, so_key)],
            bfs.co_so[(co_key, so_key)],
        )

        while True:
            self.min_threshold = float("inf")
            status = self.search_G1(0, eo_key, co_key, so_key)
            if status:
                return self.moves
            self.moves = []
            self.threshold = self.min_threshold

    def search_G1(
        self,
        g_score: int,
        eo_key: tuple[int],
        co_key: tuple[int],
        so_key: tuple[int],
        prev_move: str = None,
    ) -> bool:

        h_score = max(
            bfs.eo_so[(eo_key, so_key)],
            bfs.co_so[(co_key, so_key)],
        )
        if h_score == 0:
            return True

        for move in rubik.moves:
            if self.prune_branch(prev_move, move):
                continue

            new_eo = bfs.apply_orientation_edges(eo_key, move)
            new_co = bfs.apply_orientation_corners(co_key, move)
            new_so = bfs.apply_position_slices(so_key, move)

            h_score = max(
                bfs.eo_so[(new_eo, new_so)],
                bfs.co_so[(new_co, new_so)],
            )

            f_score = (g_score + 1) + h_score
            if f_score > self.threshold:
                self.min_threshold = min(self.min_threshold, f_score)
                continue

            self.moves.append(move)
            if self.search_G1(g_score + 1, new_eo, new_co, new_so, move):
                return True
            self.moves.pop()

        return False

    def run_resolution(self) -> list[str]:

        self.moves = []

        ep_key = rubik.get_permutation_edges()
        cp_key = rubik.get_permutation_corners()
        sp_key = rubik.get_permutation_slices()

        self.threshold = max(
            bfs.ep_sp[(ep_key, sp_key)],
            bfs.cp_sp[(cp_key, sp_key)],
        )

        while True:
            self.min_threshold = float("inf")
            status = self.search_resolution(0, ep_key, cp_key, sp_key)
            if status:
                return self.moves
            self.moves = []
            self.threshold = self.min_threshold

    def search_resolution(
        self,
        g_score: int,
        ep_key: tuple[int],
        cp_key: tuple[int],
        sp_key: tuple[int],
        prev_move: str = None,
    ) -> bool:

        h_score = max(
            bfs.ep_sp[(ep_key, sp_key)],
            bfs.cp_sp[(cp_key, sp_key)],
        )
        if h_score == 0:
            return True

        for move in rubik.legal_moves:
            if self.prune_branch(prev_move, move):
                continue

            new_ep = bfs.apply_permutation_edges(ep_key, move)
            new_cp = bfs.apply_permutation_corners(cp_key, move)
            new_sp = bfs.apply_permutation_slices(sp_key, move)

            h_score = max(
                bfs.ep_sp[(new_ep, new_sp)],
                bfs.cp_sp[(new_cp, new_sp)],
            )

            f_score = (g_score + 1) + h_score
            if f_score > self.threshold:
                self.min_threshold = min(self.min_threshold, f_score)
                continue

            self.moves.append(move)
            if self.search_resolution(g_score + 1, new_ep, new_cp, new_sp, move):
                return True
            self.moves.pop()

        return False


ida = IDA_STAR()
