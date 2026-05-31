from srcs.rubik import rubik
from srcs.bfs import bfs


class IDA_STAR:

    def __init__(self):
        self.moves = []
        self.threshold = None
        self.min_threshold = None
        self.max_depth = 20

    def run(self) -> list[str]:

        eo_key = rubik.get_edges_binary()
        co_key = rubik.get_corners_binary()

        self.threshold = max(bfs.visited_edges[eo_key], bfs.visited_corners[co_key])

        while True:
            self.min_threshold = float("inf")
            status = self.search(0, eo_key, co_key)
            if status:
                return self.moves
            self.moves = []
            self.threshold = self.min_threshold

    def search(self, g_score: int, eo_key: tuple[int], co_key: tuple[int]) -> bool:

        for move in rubik.moves:
            new_eo = bfs.apply_edge_move(eo_key, move)
            new_co = bfs.apply_corner_move(co_key, move)

            h_score = max(bfs.visited_edges[new_eo], bfs.visited_corners[new_co])
            if h_score == 0:
                self.moves.append(move)
                return True

            f_score = g_score + h_score
            if f_score > self.threshold:
                self.min_threshold = min(self.min_threshold, f_score)
                continue

            self.moves.append(move)
            if self.search(g_score + 1, new_eo, new_co):
                return True

            self.moves.pop()

        return False


ida = IDA_STAR()
