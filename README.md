# Week 9: Tree and Graph Data Structures and Traversal Algorithms

Read the [Week 9 Reading V7](docs/week09_reading_v7.pdf), including its final
Assignment section. It is the complete task specification. This page gives the
commands and file locations needed to carry it out.

## 1. Purpose and file to edit

Find a path through permitted connections using breadth-first search, iterative
depth-first search and parent-chain reconstruction.

The small seven-node `GRAPH` supports the Reading traces and stage commands.
The supplied `ASSIGNMENT_GRAPH` has 14 nodes, dead-end branches and cycles.
The final checks, comparison and robot runs use this larger input. Both graphs
are in `src/ap_week09/cases.py`. Apply the same functions without adding a TODO.

Edit only **src/ap_week09/traversal.py**, inside these three marked regions:

1. TODO 1: `reconstruct_path(parent, start, goal)`. Read the supplied `parent`
   argument and return a new path list, or `None` if the goal is absent from it.
   Do not create the parent mapping or run a traversal here.
2. TODO 2: `bfs(graph, start)`. Use the supplied graph and start node to create
   the BFS queue and visited set, and return new `order` and `parent` collections.
3. TODO 3: `dfs(graph, start)`. Use the supplied graph and start node to create
   the DFS stack and visited set, and return new `order` and `parent` collections.

Keep the signatures, imports, supplied validation and BEGIN/END markers intact.
Use the Reading and function docstrings for the algorithm contracts. Graph data,
validation, runners, tests and robot support are supplied. Do not edit them or
write new tests, reports or recording code.

## 2. Prepare the repository and existing environment

Open the [Week 9 template](https://github.com/SSUMechE/applied-programming-2026-week09-starter)
identified in the LMS notice. Use **Use this template**
to create your own private `applied-programming-w09-YOUR-STUDENT-ID` repository.
Invite the exact collaborator account `SSUMechE`.

Open **Anaconda Prompt**. Replace the folder, GitHub account and student ID in
the following commands with your own values. Run one command per line:

```bat
cd /d "C:\your-course-folder"
git clone https://github.com/YOUR-GITHUB-ID/applied-programming-w09-YOUR-STUDENT-ID.git
cd applied-programming-w09-YOUR-STUDENT-ID
git remote -v
```

Both origin addresses must identify your own private Week 9 repository.
From this repository root, use the existing `applied-programming-cuda` environment
for **all** Week 9 examples, tests and GPU runs. Add pytest for the supplied tests.
Keep the installed PyTorch, CUDA, Genesis and NumPy unchanged.

```bat
set PYTHONUTF8=1
conda activate applied-programming-cuda
python -m pip install pytest==9.1.1
python -m pip install -e . --no-deps --no-build-isolation
python scripts/verify_environment.py
```

Expect `ENVIRONMENT PASS` after the active environment, required package versions,
this package's source location and a small CUDA calculation pass. This check does
not call unfinished TODOs or establish algorithm correctness. The editable install
registers this repository without installing dependencies or replacing build tools.

If CUDA setup is missing, complete the
[Week 5 CUDA guide](https://github.com/SSUMechE/applied-programming-2026-week05-starter/releases/tag/week05-v2-cuda-guide-v7).
If a version or import check fails, report the message rather than independently
replacing PyTorch, the driver or CUDA Toolkit. Do not create another environment.
In a new Anaconda Prompt, return to this repository, set `PYTHONUTF8=1` and
activate `applied-programming-cuda` again.

## 3. Inspect supplied input and complete the algorithms

This complete example runs before any TODO is finished:

```bat
python examples/inspect_graph.py
```

Expect 7 nodes, 6 undirected edges and the supplied parent mapping
`{'S': None, 'B': 'S', 'G': 'B'}`. X has no neighbors. This mapping is supplied
input, not an unfinished traversal's result.

Complete TODO 1 in `traversal.py`, then inspect its returned paths:

```bat
python examples/compare_traversals.py --stage reconstruct
```

Expected output:

```text
S -> G: ['S', 'B', 'G']
S -> S: ['S']
S -> X: None
```

Keep that completed function. Complete TODO 2, then inspect BFS:

```bat
python examples/compare_traversals.py --stage bfs
```

Expect processing order `['S', 'A', 'B', 'C', 'G', 'D']` and G's parent B.
Complete TODO 3, then inspect DFS:

```bat
python examples/compare_traversals.py --stage dfs
```

Expect processing order `['S', 'A', 'C', 'D', 'G', 'B']`, G's parent D and B's
parent G. Each stage calls only its named function. Compare a differing node or
parent with the Reading's queue or stack trace before editing that TODO.

## 4. Check the completed implementation

After completing all three bodies, run one final supplied test suite, the
changed-graph comparison and the local file check:

```bat
python -m pytest -q
python examples/compare_traversals.py
python scripts/verify_submission.py
```

Expect **9 passed** and `LOCAL FILE CHECK PASS`. The file check verifies supplied
files and edit boundaries. It does not rerun tests or check GitHub/LMS submission.

The comparison uses the larger Assignment graph and holds `S` and `G` fixed:

- Original Assignment graph: BFS returns `['S', 'B', 'G']`. DFS returns `['S', 'A', 'E', 'C', 'F', 'D', 'G']`.
- Only S's neighbor order reversed: both paths are `['S', 'B', 'G']`.
- B-G closed in both directions, with the original neighbor order: both paths are `['S', 'A', 'E', 'C', 'F', 'D', 'G']`.
- D-G also closed: G remains a valid node, but both paths are `None`.

No copied output or report is required. If you change an algorithm afterward,
rerun the affected check and necessary comparison, not unchanged full runs.
Dead ends H, J, K and L occur in the visitation order, not the recovered path to G.

## 5. Execute the returned path with the supplied robot arm

GPU robot execution is required. Stay in the same repository and
`applied-programming-cuda` environment. No further installation or environment
switch is needed. Execute the two original Assignment-graph paths:

```bat
python examples/run_robot_path.py --algorithm bfs --output artifacts/bfs --capture
python examples/run_robot_path.py --algorithm dfs --output artifacts/dfs --capture
```

Expect `Result: EXECUTED` for both runs. BFS follows S-B-G and DFS follows
S-A-E-C-F-D-G. After each successful capture, the saved node images open together
in your browser in path order. This is a static image overview, not an animation.
If the browser does not open, double-click `preview.html` in `artifacts/bfs` or
`artifacts/dfs`. The original PNG images remain in those folders. Add `--no-open`
only when you want to save the images without opening a window.
Generated images and records are inspection support,
not submission items. A successful run does not prove shortest physical motion
or continuous collision avoidance. Import/CUDA/setup failures are separate
from a wrong algorithm result. A CPU-only run does not satisfy this required GPU step.

Optional setup diagnosis, not a required or graded step:
`python examples/run_robot_path.py --algorithm provided --capture` runs the
supplied preview without your algorithms and saves it in `artifacts/robot_path`.

## 6. Push and submit

Keep using your own private Week 9 repository. A correctly addressed
`SSUMechE` invitation sent on time may remain pending while the instructor
accepts it. That alone is not a missing submission.

```bat
git status --short
git diff
git add src/ap_week09/traversal.py
git diff --staged
git commit -m "Complete Week 9 graph traversal"
git push origin main
git status --short
git rev-parse HEAD
git ls-remote origin refs/heads/main
```

Press `q` to leave a diff pager. The final status must be empty. Match the full
local and remote commit IDs and inspect the pushed revision on GitHub.

Within one week of the corresponding lab, by the date and time announced in
LMS, submit these two items:

- Your own repository URL.
- The full 40-character commit ID of the pushed revision.

Fictional format example. Replace both values with your own:

```text
Repository URL: https://github.com/student-example/applied-programming-w09-20260000
Commit ID: 0123456789abcdef0123456789abcdef01234567
```

Do not submit a public template URL, local path, branch name, `latest`, short
hash, unpushed commit or credential. Private visibility and instructor access
are checked from repository evidence. LMS requires no extra confirmation
sentence, ZIP, screenshot or report. GitHub upload alone is not LMS submission.
Later pushes do not replace the submitted commit. Continued work in another
week does not postpone this submission. Preserve the announced mandatory-format
zero-point rule and the timely-pending invitation exception. A failed numerical
test alone is not automatic zero for the whole Assignment.
