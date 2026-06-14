# Rubik

Made by [Lisa](https://github.com/ft-lisa) and [Mateo](https://github.com/MatLBS)  🥷🏻🥷🏻

**Rubik** is a 3D Rubik's Cube solver and visualizer. Give it a sequence of moves to scramble the cube, and it computes a solution and replays it in an interactive 3D window.

The solver is based on **Kociemba's two-phase algorithm**: instead of brute-forcing the whole cube at once (the search space is ~4.3 × 10¹⁹ states), the cube is solved in two smaller, tractable phases driven by an **IDA\*** search and pre-computed **BFS heuristic tables**.

## Live version 📡

https://portfolio-rubik.vercel.app/

## 📚 Key concepts

### Why two phases?

A Rubik's Cube has 43 quintillion possible states. Searching all of them directly is impossible. Kociemba's idea is to split the problem in two:

1. **Phase 1 — reach the G1 subgroup.** First we only care about *orientation*: getting every edge and corner correctly oriented, and moving the four "slice" edges (the FR, FL, BL, BR edges) into the middle layer. We allow all 18 moves (`U, U', U2, D, D2, ..., B2`).

<img width="837" height="754" alt="rubik_G1" src="https://github.com/user-attachments/assets/6cca5664-ac17-49cc-81ab-f510816c3a56" />

2. **Phase 2 — solve from G1.** From G1 the cube can be solved using only a restricted move set: `U, U', U2, D, D', D2, L2, R2, F2, B2`. These moves preserve the orientation already achieved, so we only have to fix *permutation* — putting every piece back in its home position.

<img width="1999" height="1098" alt="rubik_solved" src="https://github.com/user-attachments/assets/f9d2e42f-979c-4faf-b4b8-3801c38a0a3c" />

Splitting the work this way turns one gigantic search into two much shallower ones.

### Building the heuristic tables (BFS)

For IDA\* to be fast, it needs a good *heuristic*: a lower bound on the number of moves still required. We pre-compute these bounds once with a **Breadth-First Search** and store them on disk as pickled dictionaries.

Each table maps a partial cube coordinate to the minimum number of moves needed to bring that coordinate back to its solved value. We build four of them:

| Table | Phase | What it measures |
|-------|-------|------------------|
| `eo_so.pkl` | 1 | Edge **o**rientation + **s**lice **o**ccupancy |
| `co_so.pkl` | 1 | **C**orner **o**rientation + **s**lice **o**ccupancy |
| `ep_sp.pkl` | 2 | Edge **p**ermutation + **s**lice **p**ermutation |
| `cp_sp.pkl` | 2 | **C**orner **p**ermutation + **s**lice **p**ermutation |

Because BFS explores level by level, the first time a state is reached is guaranteed to be by a shortest path — so the stored depth is an *admissible* heuristic (it never overestimates), which keeps IDA\* optimal.

### Searching with IDA\*

**IDA\*** (Iterative Deepening A\*) combines the low memory cost of depth-first search with the optimality of A\*. It repeatedly runs a depth-limited DFS using a threshold on `f = g + h`, where:

- `g` = number of moves applied so far,
- `h` = the heuristic value, read from the BFS tables (we take the **max** of the two relevant tables for a tighter bound).

Whenever a branch exceeds the current threshold, it is pruned and the smallest exceeding `f` becomes the next threshold. The search also prunes redundant move sequences (e.g. doing the same face twice in a row, or a face right after its opposite).

The solver runs IDA\* twice — once to reach G1 (`run_G1`), then once to finish the solve from G1 (`run_resolution`) — and concatenates both move lists into the final solution that gets animated.

## Setup

This project uses [uv](https://docs.astral.sh/uv/) as its package manager.

1. Clone the repository:

```bash
git clone https://github.com/ft-lisa/Rubik.git
cd Rubik
```

2. Install the dependencies (uv reads `pyproject.toml` and `uv.lock`):

```bash
uv sync
```

That's it — uv creates the virtual environment and installs Ursina, NumPy, tqdm and the rest automatically.

## Commands

All commands are run through `uv run`. At least one of `--moves`, `--hands-on`, or `--calculate-heuristics` must be provided.

### 1. Generate the heuristic tables

Before solving for the first time, build the BFS heuristic tables. They are written to the [heuristics/](heuristics/) directory and only need to be generated once (this can take 1 or 2 minutes...)

```bash
uv run rubik --calculate-heuristics
```

### 2. Solve a scrambled cube

Pass a sequence of moves to scramble the cube. The solver reaches G1, finishes the solve, then opens a 3D window and animates the full solution.

```bash
uv run rubik --moves "R U R' U' F2 L D'"
```

Moves follow standard cube notation: a face letter (`F`, `R`, `U`, `B`, `L`, `D`), optionally followed by `'` for a counter-clockwise turn or `2` for a 180° turn.

### 3. Play with the cube interactively

Open the 3D cube in hands-on mode and manipulate it yourself with the keyboard.

```bash
uv run rubik --hands-on
```

| Key | Move | Key | Move |
|-----|------|-----|------|
| `r` | R | `t` | R' |
| `l` | L | `;` | L' |
| `u` | U | `i` | U' |
| `d` | D | `s` | D' |
| `f` | F | `g` | F' |
| `b` | B | `n` | B' |

Drag with the **left mouse button** to rotate the camera around the cube.

## CLI options

| Option | Description |
|--------|-------------|
| `--moves "N"` | Sequence of moves to scramble the cube (e.g. `"R U R' U'"`). The cube is then solved and the solution is animated. |
| `--hands-on` | Open the cube in interactive mode for manual keyboard manipulation. |
| `--calculate-heuristics` | Generate the BFS heuristic tables used by the solver and save them to `heuristics/`. |

## Project architecture

```tree
rubik/
├── heuristics/             # Pre-computed BFS heuristic tables (generated)
│   ├── eo_so.pkl           # Edge orientation + slice occupancy (phase 1)
│   ├── co_so.pkl           # Corner orientation + slice occupancy (phase 1)
│   ├── ep_sp.pkl           # Edge + slice permutation (phase 2)
│   └── cp_sp.pkl           # Corner + slice permutation (phase 2)
├── srcs/
│   ├── main.py             # CLI entry point, argument parsing and orchestration
│   ├── rubik.py            # Cube model: state, faces, moves and coordinate readers
│   ├── bfs.py              # Builds and loads the heuristic tables
│   ├── ida.py              # IDA* search for phase 1 (G1) and phase 2 (resolution)
│   ├── cube.py             # 3D cube construction (Ursina entities)
│   ├── moves.py            # Animated face rotations in the 3D scene
│   ├── controls.py         # Keyboard and mouse input handling
│   ├── parsing.py          # Validation of user-provided move sequences
│   ├── utils.py            # Move parsing helpers and scramble application
│   └── test.py             # Tests
├── pyproject.toml          # Project metadata and dependencies (uv)
└── README.md
```

## Sources

### Rubik visualizater
- https://onlinecube.com/#solver

### Articles
- https://www.cuberoot.me/en/code/algorithms/kociemba
- https://medium.com/data-science/rubiks-cube-solver-96fa6c56fbe4
- https://medium.com/@muhammadalikhan0003/kociembas-two-phase-algorithm-how-it-works-and-its-applications-3d8f97a3562a

### Youtube
- https://www.youtube.com/watch?v=fxwVmTI5nGM -> To understand edge-orientation

### BFS 
- https://www.geeksforgeeks.org/python/python-program-for-breadth-first-search-or-bfs-for-a-graph/

### IDA
- https://www.geeksforgeeks.org/artificial-intelligence/iterative-deepening-a-algorithm-ida-artificial-intelligence/

### GitHub
- https://github.com/bellerb/RubiksCube_Solver
