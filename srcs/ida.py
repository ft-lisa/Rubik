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
        elif rubik.OPPOSITE_FACES[prev_move[0]] == curr_move[0]:
            return True
        elif prev_move[0] == curr_move[0]:
            return True
        return False

    def run_G1(self) -> list[str]:

        eo_key = rubik.get_orientation_edges()
        co_key = rubik.get_orientation_corners()
        so_key = rubik.get_position_slices()

        self.threshold = max(
            max(
                bfs.orientation_edges[eo_key],
                bfs.orientation_corners[co_key],
                bfs.position_slices[so_key],
            ),
            self.threshold,
        )

        while True:
            self.min_threshold = float("inf")
            print("-" * 30)
            print("Current threshold G1:", self.threshold)
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

        for move in rubik.moves:
            if self.prune_branch(prev_move, move):
                continue

            new_eo = bfs.apply_orientation_edges(eo_key, move)
            new_co = bfs.apply_orientation_corners(co_key, move)
            new_so = bfs.apply_position_slices(so_key, move)

            h_score = max(
                bfs.orientation_edges[new_eo],
                bfs.orientation_corners[new_co],
                bfs.position_slices[new_so],
            )
            if h_score == 0:
                self.moves.append(move)
                return True

            f_score = g_score + h_score
            if f_score > self.threshold:
                self.min_threshold = min(self.min_threshold, f_score)
                continue

            self.moves.append(move)
            if self.search_G1(g_score + 1, new_eo, new_co, new_so, move):
                return True

            self.moves.pop()

        return False

    def run_resolution(self) -> list[str]:

        cp_key = rubik.get_orientation_edges()
        ep_key = rubik.get_orientation_corners()
        sp_key = rubik.get_position_slices()

        self.threshold = max(
            max(
                bfs.orientation_edges[cp_key],
                bfs.orientation_corners[ep_key],
                bfs.position_slices[sp_key],
            ),
            self.threshold,
        )

        while True:
            self.min_threshold = float("inf")
            print("-" * 30)
            print("Current threshold:", self.threshold)
            status = self.search_resolution(0, cp_key, ep_key, sp_key)
            if status:
                return self.moves
            self.moves = []
            self.threshold = self.min_threshold

    def search_resolution(
        self,
        g_score: int,
        cp_key: tuple[int],
        ep_key: tuple[int],
        sp_key: tuple[int],
        prev_move: str = None,
    ) -> bool:

        for move in rubik.moves:
            if self.prune_branch(prev_move, move):
                continue

            new_eo = bfs.apply_orientation_edges(cp_key, move)
            new_co = bfs.apply_orientation_corners(ep_key, move)
            new_so = bfs.apply_position_slices(sp_key, move)

            h_score = max(
                bfs.orientation_edges[new_eo],
                bfs.orientation_corners[new_co],
                bfs.position_slices[new_so],
            )
            if h_score == 0:
                self.moves.append(move)
                return True

            f_score = g_score + h_score
            if f_score > self.threshold:
                self.min_threshold = min(self.min_threshold, f_score)
                continue

            self.moves.append(move)
            if self.search_resolution(g_score + 1, new_eo, new_co, new_so, move):
                return True

            self.moves.pop()

        return False


ida = IDA_STAR()
