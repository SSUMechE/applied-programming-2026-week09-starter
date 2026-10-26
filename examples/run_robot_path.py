"""Run the supplied posture preview or a path from the student's search code."""

import argparse
from html import escape
from pathlib import Path
from urllib.parse import quote
import webbrowser

from ap_week09.cases import assignment_cases
from ap_week09.robotposes import PROVIDED_PREVIEW_PATH
from ap_week09.simulation import run_path, save_run_status, validate_graph_path
from ap_week09.workflow import solve


def show_capture_preview(result, output_dir, open_browser=True):
    """Show only this successful run's saved node images, not an animation.

    Display problems are warnings. They do not change the simulation result.
    No directory scan, external content or additional dependency is used.
    """
    if result.get('status') != 'EXECUTED' or result.get('executed') is not True:
        return None
    preview = Path(output_dir).absolute() / 'preview.html'
    try:
        out = Path(output_dir).resolve()
        preview = out / 'preview.html'
        if not out.is_dir() or preview.is_symlink():
            raise ValueError('preview must be a regular file in the output directory')
        frames = result.get('frames', [])
        path = result.get('path', [])
        if not frames or [frame['node'] for frame in frames] != list(path):
            raise ValueError('current frame records must match the executed path in order')
        figures = []
        seen = set()
        for number, frame in enumerate(frames):
            relative = Path(frame['file'])
            image = (out / relative).resolve()
            if (relative.is_absolute() or '..' in relative.parts
                    or not image.is_relative_to(out) or not image.is_file()
                    or image.suffix.lower() != '.png' or image in seen):
                raise ValueError(f"invalid or missing current PNG: {frame['file']}")
            seen.add(image)
            image_url = escape(quote(image.relative_to(out).as_posix(), safe='/'), quote=True)
            node = escape(str(frame['node']), quote=True)
            figures.append(
                f'<figure><figcaption>{number + 1}. Node / 노드 {node}</figcaption>'
                f'<a href="{image_url}"><img src="{image_url}" alt="Node / 노드 {node}"></a></figure>')
        summary = escape(' → '.join(str(node) for node in path))
        started = escape(str(result.get('started_utc', '')))
        document = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Week 9 saved images / 저장 이미지</title>
<style>
body { font-family: sans-serif; color: #000; background: #fff;
       max-width: 1200px; margin: 24px auto; padding: 0 20px; }
h1 { font-size: 1.6rem; }
p { line-height: 1.5; }
.frames { display: grid; gap: 16px;
          grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr)); }
figure { margin: 0; padding: 12px; border: 1px solid #000; }
figcaption { font-size: 1.2rem; margin-bottom: 10px; }
img { display: block; width: 100%; height: auto; }
</style></head><body>
<h1>Week 9 saved images / 저장 이미지</h1>
<p>Static images at the reached nodes, not an animation.<br>
도착한 노드의 정지 이미지입니다. 연속 애니메이션이 아닙니다.</p>
<p>Click an image for full size. / 이미지를 클릭하면 원본 크기로 열립니다.</p>
'''
        document += f'<p>Path / 경로: {summary}</p>\n'
        if started:
            document += f'<p>Run / 실행 (UTC): {started}</p>\n'
        document += '<div class="frames">\n' + '\n'.join(figures) + '\n</div></body></html>\n'
        preview.write_text(document, encoding='utf-8')
    except Exception as error:
        print(f'Warning: image preview could not be generated: {error}')
        print(f'Preview target: {preview}')
        print(f'Saved PNG folder: {Path(output_dir).absolute()}')
        return None
    print(f'Image preview: {preview}')
    if open_browser:
        try:
            if not webbrowser.open(preview.as_uri(), new=2):
                raise RuntimeError('the default browser did not accept the local page')
        except Exception as error:
            print(f'Warning: image preview did not open automatically: {error}')
            print(f'Open this local file manually: {preview}')
    return preview


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--algorithm', choices=('provided', 'bfs', 'dfs'), default='provided')
    parser.add_argument('--case', choices=tuple(assignment_cases()), default='original')
    parser.add_argument('--output', type=Path, default=Path('artifacts/robot_path'))
    parser.add_argument('--capture', action='store_true', help='Save actual camera frames at the reached nodes')
    parser.add_argument('--no-open', action='store_true', help='Save the capture overview without opening a browser')
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
    if args.capture and result['status'] == 'EXECUTED' and result['executed'] is True:
        show_capture_preview(result, args.output, open_browser=not args.no_open)
    return 0 if result['status'] in ('EXECUTED', 'NO_PATH') else 1


if __name__ == '__main__':
    raise SystemExit(main())
