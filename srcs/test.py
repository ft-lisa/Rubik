import random
import time

from srcs.rubik import rubik
from srcs.bfs import bfs
from srcs.ida import ida
from srcs.utils import VALID_MOVES, DOUBLE_MODIFIERS, REVERSE_MODIFIERS

NB_TESTS = 100
MIN_LEN = 2
MAX_LEN = 20
TIME_LIMIT = 3.0
MOVE_LIMIT = 25


def random_scramble() -> list[str]:
    length = random.randint(MIN_LEN, MAX_LEN)
    return [
        random.choice(VALID_MOVES)
        + random.choice(["", *REVERSE_MODIFIERS, *DOUBLE_MODIFIERS])
        for _ in range(length)
    ]


def solve() -> list[str]:
    g1_moves = ida.run_G1()
    if g1_moves:
        rubik.shuffle_rubik(g1_moves)

    resolution_moves = ida.run_resolution()
    if resolution_moves:
        rubik.shuffle_rubik(resolution_moves)

    return g1_moves + resolution_moves


def main() -> None:
    bfs.load_heuristics()

    passed = 0
    time_avgs = []
    nb_moves_avgs = []

    for i in range(1, NB_TESTS + 1):
        scramble = random_scramble()

        rubik.initialize()
        rubik.shuffle_rubik(scramble)

        start = time.time()
        solution = solve()
        elapsed = time.time() - start

        is_solved = rubik.solved()
        nb_moves = len(solution)

        ok = is_solved and elapsed < TIME_LIMIT and nb_moves <= MOVE_LIMIT

        if ok:
            passed += 1
            time_avgs.append(elapsed)
            nb_moves_avgs.append(nb_moves)
            print(
                f"[OK] test {i:3d} | {nb_moves:2d} coups | {elapsed:5.2f}s "
                f"| scramble: {' '.join(scramble)}"
            )
        else:
            reasons = []
            if not is_solved:
                reasons.append("NON RÉSOLU")
            if elapsed >= TIME_LIMIT:
                reasons.append(f"trop lent ({elapsed:.2f}s)")
            if nb_moves > MOVE_LIMIT:
                reasons.append(f"trop long ({nb_moves} coups)")
            print(
                f"[ÉCHEC] test {i:3d} | {nb_moves:2d} coups | {elapsed:5.2f}s "
                f"| {' '.join(reasons)}"
            )
            print(f"        scramble: {' '.join(scramble)}")

    print(f"\nRésultat : {passed}/{NB_TESTS} tests réussis")
    print(f"Temps moyen : {sum(time_avgs) / len(time_avgs):.2f}s")
    print(f"Nombre moyen de coups : {sum(nb_moves_avgs) / len(nb_moves_avgs):.2f}")


if __name__ == "__main__":
    main()
