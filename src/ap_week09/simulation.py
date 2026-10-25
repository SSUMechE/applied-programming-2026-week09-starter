"""Provided bridge from a reconstructed node-ID path to physical execution.

No simulator is imported for a missing or invalid path. Student algorithms
return identifiers. This module looks up the supplied joint targets and delegates
motor control, stepping, measurements and rendering to the provided scene.
"""

from datetime import datetime, timezone
import json
from pathlib import Path

from .robotposes import PERMITTED_EDGES, POSTURES, slice_edge_is_allowed


def save_run_status(output_dir, result):
    """Replace the current generated result without deleting earlier frame files.

Only frames listed in the current result belong to that run. A failed or skipped
run must not leave a previous successful result.json as its apparent result.
"""
    if output_dir is not None:
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        (out / 'result.json').write_text(json.dumps(result, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def validate_path(path):
    """Return a new list of known IDs joined by permitted edges, or None.

This finite example accepts a nonempty list/tuple of distinct supplied IDs,
with at most as many entries as the posture catalog contains.
It rejects unknown IDs, repeated nodes and transitions outside the catalog.
The path may contain a single known node. None means that graph search found no
path, so there is no motion command to execute.
"""
    if path is None:
        return None
    if not isinstance(path, (list, tuple)) or not 1 <= len(path) <= len(POSTURES):
        raise ValueError(f'path must contain 1..{len(POSTURES)} known node IDs, or be None')
    if any(not isinstance(node, str) or node not in POSTURES for node in path):
        raise ValueError('path contains an unknown node ID')
    if len(set(path)) != len(path):
        raise ValueError('a reconstructed path must not repeat a node')
    allowed = {frozenset(edge) for edge in PERMITTED_EDGES}
    if any(frozenset((left, right)) not in allowed
           for left, right in zip(path, path[1:])):
        raise ValueError('path contains a transition outside the supplied catalog')
    if any(not slice_edge_is_allowed(POSTURES[left][:2], POSTURES[right][:2])
           for left, right in zip(path, path[1:])):
        raise ValueError('path crosses the declared forbidden joint-space region')
    return list(path)


def validate_graph_path(graph, start, goal, path):
    """Check a returned path against the selected graph and requested endpoints.

This supplied guard checks the path's structure, not search order, shortest-path
correctness or whether None is the correct search result. Those behaviors are
checked by the supplied core tests. An invalid returned path never reaches the
simulator.
"""
    path = validate_path(path)
    if path is None:
        return None
    if path[0] != start or path[-1] != goal:
        raise ValueError('returned path does not have the requested start and goal')
    if any(node not in graph for node in path):
        raise ValueError('returned path contains a node outside the selected graph')
    if any(right not in graph[left] for left, right in zip(path, path[1:])):
        raise ValueError('returned path uses an edge absent from the selected graph')
    return path


def run_path(path, output_dir=None, capture=False):
    """Execute one finite path and return supplied measurements as a dictionary.

Requires the existing applied-programming-cuda environment for an actual path.
No package, environment, device setting or cache path is changed. A missing path
returns NO_PATH without importing Genesis or starting a scene. Frame and trace
files are generated only when output_dir is supplied. They are not submissions.
"""
    path = validate_path(path)
    if path is None:
        result = {'status': 'NO_PATH', 'executed': False, 'path': None, 'steps': 0,
                  'frames': [], 'trace_file': None,
                  'started_utc': datetime.now(timezone.utc).isoformat()}
        save_run_status(output_dir, result)
        return result
    if capture and output_dir is None:
        raise ValueError('capture requires output_dir')
    started_utc = datetime.now(timezone.utc).isoformat()
    save_run_status(output_dir, {'status': 'RUNNING', 'executed': None,
        'path': path, 'frames': [], 'trace_file': None, 'started_utc': started_utc})
    try:
        from .robot_scene import run_scene
        result = run_scene(path, output_dir=output_dir, capture=capture)
    except BaseException as error:
        save_run_status(output_dir, {'status': 'FAILED', 'executed': None,
            'path': path, 'frames': [], 'trace_file': None, 'started_utc': started_utc,
            'reason': str(error),
            'scope': 'Execution did not complete. Partial motion may have occurred. '
                     'Earlier image/trace files are not current success evidence.'})
        raise
    result['started_utc'] = started_utc
    result['trace_file'] = 'trace.csv' if output_dir is not None else None
    save_run_status(output_dir, result)
    return result
