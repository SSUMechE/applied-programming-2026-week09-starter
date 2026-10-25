"""Run the supplied posture preview or a path from the student's search code."""

import argparse
from pathlib import Path

from ap_week09.cases import assignment_cases
from ap_week09.robotposes import PROVIDED_PREVIEW_PATH
from ap_week09.simulation import run_path, save_run_status, validate_graph_path
from ap_week09.workflow import solve


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--algorithm', choices=('provided', 'bfs', 'dfs'), default='provided')
    parser.add_argument('--case', choices=tuple(assignment_cases()), default='original')
    parser.add_argument('--output', type=Path, default=Path('artifacts/robot_path'))
    parser.add_argument('--capture', action='store_true', help='Save actual camera frames at the reached nodes')
    args = parser.parse_args()
    graph = assignment_cases()[args.case]
    save_run_status(args.output, {'status': 'NOT_STARTED', 'executed': False,
        'algorithm': args.algorithm, 'case': args.case, 'frames': [], 'trace_file': None})
    if args.algorithm == 'provided':
        if args.case != 'original':
            parser.error('the supplied posture preview uses --case original')
        path = list(PROVIDED_PREVIEW_PATH)
        print('Provided posture preview: this command does not call student search code.')
    else:
        try:
            order, parent, path = solve(graph, 'S', 'G', args.algorithm)
        except NotImplementedError:
            save_run_status(args.output, {'status': 'NEEDS_IMPLEMENTATION', 'executed': False,
                'frames': [], 'trace_file': None})
            print('Complete the selected search and reconstruct_path in src/ap_week09/traversal.py first.')
            return 2
        print(f'Student {args.algorithm.upper()} traversal order: {order}')
        print(f'Reconstructed node-ID path: {path}')
    try:
        path = validate_graph_path(graph, 'S', 'G', path)
    except ValueError as error:
        save_run_status(args.output, {'status': 'PATH_REJECTED', 'executed': False,
            'reason': str(error), 'frames': [], 'trace_file': None})
        print(f'Path rejected before simulation: {error}')
        return 2
    if path is not None:
        print('Physical execution uses the supplied joint targets and controller.')
    try:
        result = run_path(path, output_dir=args.output, capture=args.capture)
    except Exception as error:
        print(f'Physical execution failed: {error}')
        print('Read the current result.json status. Earlier frame or trace files do not establish this run succeeded.')
        return 1
    print(f"Result: {result['status']}")
    if result['executed']:
        print(f"Edges: {result['edge_count']}")
        print(f"Physical steps: {result['steps']}")
        print(f"Largest reached-node joint error: {result['max_node_error_rad']:.6f} rad")
        print(f'Result files: {args.output}')
        print('These observations do not prove continuous collision avoidance or shortest physical distance.')
    else:
        print('No path returned. The simulator was not started.')
    return 0 if result['status'] in ('EXECUTED', 'NO_PATH') else 1


if __name__ == '__main__':
    raise SystemExit(main())
