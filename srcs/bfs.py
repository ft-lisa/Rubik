from collections import defaultdict
import numpy as np
from tqdm import tqdm
from srcs.cubie import rubik


class BFS:

    def __init__(self):
        self.visited_edges = {}
        self.max_moves = 20

        self.heuristic_edges = []
        self.heuristic_corners = []

    def build_edges_heuristic(
        self,
        state: str,
        actions: list[tuple[str, int]],
    ) -> dict:
        initial_eo = "".join(map(str, rubik.get_edges_binary()))
        self.visited_edges = {initial_eo: 0}
        queue = [(state, 0)]

        with tqdm(desc="Heuristic DB") as pbar:
            while queue:
                s, d = queue.pop(0)
                if d >= self.max_moves:
                    continue

                for action, direction in actions:
                    rubik.set_rubik_from_string(s)
                    rubik.rotate_face(action, direction)

                    next_state = "".join(rubik.rubik.flatten())
                    eo_key = "".join(map(str, rubik.get_edges_binary()))

                    if (
                        eo_key not in self.visited_edges
                        or self.visited_edges[eo_key] > d + 1
                    ):
                        self.visited_edges[eo_key] = d + 1
                        queue.append((next_state, d + 1))
                    pbar.update(1)
        return self.visited_edges

    def build_corner_heuristic(
        self,
        state: str,
        actions: list[tuple[str, int]],
    ) -> dict:
        initial_eo = "".join(map(str, rubik.get_edges_binary()))
        self.visited_corners = {initial_eo: 0}
        queue = [(state, 0)]

        with tqdm(desc="Heuristic DB") as pbar:
            while queue:
                s, d = queue.pop(0)
                if d >= self.max_moves:
                    continue

                for action, direction in actions:
                    rubik.set_rubik_from_string(s)
                    rubik.rotate_face(action, direction)

                    next_state = "".join(rubik.rubik.flatten())
                    eo_key = "".join(map(str, rubik.get_corners_binary()))

                    if (
                        eo_key not in self.visited_corners
                        or self.visited_corners[eo_key] > d + 1
                    ):
                        self.visited_corners[eo_key] = d + 1
                        queue.append((next_state, d + 1))
                    pbar.update(1)
        return self.visited_corners

    def calculate_heuristic(self):
        rubik.initialize_cube()
        self.heuristic_edges = self.build_edges_heuristic(
            "".join(rubik.rubik.flatten()), rubik.actions
        )
        self.heuristic_corners = self.build_corner_heuristic(
            "".join(rubik.rubik.flatten()), rubik.actions
        )


bfs = BFS()
