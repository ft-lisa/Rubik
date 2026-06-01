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

    def run(self) -> list[str]:

        eo_key = rubik.get_edges_binary()
        co_key = rubik.get_corners_binary()
        so_key = rubik.get_slice_binary()

        self.threshold = max(
            max(
                bfs.visited_edges[eo_key],
                bfs.visited_corners[co_key],
                bfs.visited_slice[so_key],
            ),
            self.threshold,
        )

        while True:
            self.min_threshold = float("inf")
            print("-" * 30)
            print("Current threshold:", self.threshold)
            status = self.search(0, eo_key, co_key, so_key)
            if status:
                return self.moves
            self.moves = []
            self.threshold = self.min_threshold

    def search(
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

            new_eo = bfs.apply_edge_move(eo_key, move)
            new_co = bfs.apply_corner_move(co_key, move)
            new_so = bfs.apply_slice_move(so_key, move)

            h_score = max(
                bfs.visited_edges[new_eo],
                bfs.visited_corners[new_co],
                bfs.visited_slice[new_so],
            )
            if h_score == 0:
                self.moves.append(move)
                return True

            f_score = g_score + h_score
            if f_score > self.threshold:
                self.min_threshold = min(self.min_threshold, f_score)
                continue

            self.moves.append(move)
            if self.search(g_score + 1, new_eo, new_co, new_so, move):
                return True

            self.moves.pop()

        return False


ida = IDA_STAR()
