from srcs.rubik import rubik
from srcs.bfs import bfs


class IDA_STAR:

    def __init__(self, max_depth=20):
        self.moves = []
        self.threshold = 20
        self.min_threshold = None

    def run(self) -> list[tuple[str, int]]:
        state = "".join(rubik.rubik.flatten())
        rubik.set_rubik_from_string(state)

        print("state:", state)

        # while True:
        #     self.min_threshold = float("inf")
        #     status = self.search(state, 1)
        #     if status == -1:
        #         return self.moves
        #     self.moves = []
        #     self.threshold = self.min_threshold

    def search(self, state: str, g_score: int) -> int:
        rubik.set_rubik_from_string(state)
        if (
            rubik.get_edges_binary() == [0] * 11
            and rubik.get_corners_binary() == [0] * 7
        ):
            return -1
        # elif len(self.moves) >= self.threshold:
        #     return False

        eo_key = "".join(map(str, rubik.get_edges_binary()))
        co_key = "".join(map(str, rubik.get_corners_binary()))

        h_score = max(bfs.visited_edges[eo_key], bfs.visited_corners[co_key])

        f_score = g_score + h_score

        if f_score > self.threshold:
            return f_score

        if h_score == 0:
            return -1

        for action, direction in rubik.actions:
            rubik.set_rubik_from_string(state)
            rubik.rotate_face(action, direction)

            self.moves.append([action, direction])

            next_state = "".join(rubik.rubik.flatten())
            result = self.search(next_state, g_score + 1)
            if result == -1:
                return -1

            self.min_threshold = min(self.min_threshold, result)

            self.moves.pop()

        return self.min_threshold


ida = IDA_STAR()
