from srcs.rubik import rubik
from tqdm import tqdm


class BFS:

    def __init__(self):
        self.visited_edges = {}
        self.visited_corners = {}
        self.max_moves = 20

    def build_edges_heuristic(
        self,
        state: str,
        actions: list[tuple[str, int]],
    ) -> dict:
        initial_eo = "".join(map(str, rubik.get_edges_binary()))
        self.visited_edges = {initial_eo: 0}
        visited_states = {state}
        queue = [(state, 0)]

        with tqdm(desc="Heuristic DB") as pbar:
            while queue:
                state, depth = queue.pop(0)
                if depth >= self.max_moves:
                    continue

                for action, direction in actions:
                    rubik.set_rubik_from_string(state)
                    rubik.rotate_face(action, direction)

                    next_state = "".join(rubik.rubik.flatten())
                    if next_state not in visited_states:
                        eo_key = "".join(map(str, rubik.get_edges_binary()))
                        if (
                            eo_key not in self.visited_edges
                            or self.visited_edges[eo_key] > depth + 1
                        ):
                            self.visited_edges[eo_key] = depth + 1
                            queue.append((next_state, depth + 1))
                            visited_states.add(next_state)
                    pbar.update(1)

    def build_corner_heuristic(
        self,
        state: str,
        actions: list[tuple[str, int]],
    ) -> dict:
        initial_eo = "".join(map(str, rubik.get_edges_binary()))
        visited_states = {state}
        self.visited_corners = {initial_eo: 0}
        queue = [(state, 0)]

        with tqdm(desc="Heuristic DB") as pbar:
            while queue:
                state, depth = queue.pop(0)
                if depth >= self.max_moves:
                    continue

                for action, direction in actions:
                    rubik.set_rubik_from_string(state)
                    rubik.rotate_face(action, direction)

                    next_state = "".join(rubik.rubik.flatten())
                    co_key = "".join(map(str, rubik.get_corners_binary()))

                    if next_state not in visited_states:
                        co_key = "".join(map(str, rubik.get_corners_binary()))
                        if (
                            co_key not in self.visited_corners
                            or self.visited_corners[co_key] > depth + 1
                        ):
                            self.visited_corners[co_key] = depth + 1
                            queue.append((next_state, depth + 1))
                            visited_states.add(next_state)

                    pbar.update(1)

    def calculate_heuristic(self):
        rubik.initialize_cube()
        self.build_edges_heuristic("".join(rubik.rubik.flatten()), rubik.actions)
        self.build_corner_heuristic("".join(rubik.rubik.flatten()), rubik.actions)

        print(len(self.visited_edges))
        print(len(self.visited_corners))


bfs = BFS()
