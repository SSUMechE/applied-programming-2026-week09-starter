"""Provided finite Panda posture catalog. Students do not edit this module.

Each value contains seven revolute-joint targets in radians, in joint1..joint7
order. The fingers remain open. These are teaching presets, not an exhaustive
description of all physically possible moves. X has a pose but no graph edge.
"""

import math

POSTURES = {
    "S": (-0.60, -0.50, 0.0, -2.10, 0.0, 1.60, 0.7854),
    "A": (-0.60, -0.80, 0.0, -2.10, 0.0, 1.60, 0.7854),
    "C": (0.00, -1.00, 0.0, -2.10, 0.0, 1.60, 0.7854),
    "D": (0.60, -0.80, 0.0, -2.10, 0.0, 1.60, 0.7854),
    "G": (0.60, -0.50, 0.0, -2.10, 0.0, 1.60, 0.7854),
    "B": (0.00, -0.50, 0.0, -2.10, 0.0, 1.60, 0.7854),
    "X": (0.00, -0.35, 0.0, -2.10, 0.0, 1.60, 0.7854),
    "E": (-0.30, -0.90, 0.0, -2.10, 0.0, 1.60, 0.7854),
    "F": (0.30, -0.90, 0.0, -2.10, 0.0, 1.60, 0.7854),
    "H": (-0.75, -0.80, 0.0, -2.10, 0.0, 1.60, 0.7854),
    "I": (0.00, -1.05, 0.0, -2.10, 0.0, 1.60, 0.7854),
    "J": (0.00, -0.40, 0.0, -2.10, 0.0, 1.60, 0.7854),
    "K": (0.00, -1.20, 0.0, -2.10, 0.0, 1.60, 0.7854),
    "L": (0.75, -0.80, 0.0, -2.10, 0.0, 1.60, 0.7854),
}

# These are the larger Assignment graph's undirected connections.
# Each pair allows both directions. Missing pairs are outside this catalog.
PERMITTED_EDGES = (
    ('S', 'A'), ('S', 'B'), ('A', 'H'), ('A', 'E'),
    ('B', 'J'), ('B', 'G'), ('E', 'C'), ('E', 'I'),
    ('C', 'K'), ('C', 'F'), ('F', 'D'), ('F', 'I'),
    ('D', 'L'), ('D', 'G'),
)

PROVIDED_PREVIEW_PATH = ('S', 'B', 'G')
DT_S = 0.01
INITIAL_SETTLE_STEPS = 60
RAMP_STEPS = 80
HOLD_STEPS = 80
ENDPOINT_TOLERANCE_RAD = 0.025

# First two joint ranges from the installed Panda MJCF. The forbidden rectangle
# is a course-defined software constraint, NOT a measured collision obstacle.
SLICE_LIMITS_RAD = ((-2.8973, 2.8973), (-1.7628, 1.7628))
FORBIDDEN_RECTANGLE_RAD = ((-0.20, 0.20), (-0.85, -0.65))


def slice_edge_is_allowed(left, right):
    """Check the straight segment between two (q1, q2) pairs, in radians.

Both pairs must lie inside the supplied joint ranges. The closed forbidden
rectangle, including its boundary, must not intersect the segment. The other
    five arm joints are fixed by the posture catalog. Segment clipping uses a
    conservative 1e-12 tolerance in its dimensionless segment parameter to
    retain corner touches despite floating-point rounding. This 2-D test does
    not test the robot's physical collision geometry.
"""
    if len(left) != 2 or len(right) != 2:
        raise ValueError('each slice point must contain q1 and q2')
    left, right = tuple(float(x) for x in left), tuple(float(x) for x in right)
    if not all(math.isfinite(x) for x in (*left, *right)):
        raise ValueError('slice coordinates must be finite')
    for point in (left, right):
        if any(not low <= value <= high
               for value, (low, high) in zip(point, SLICE_LIMITS_RAD)):
            return False
    enter, leave = 0.0, 1.0
    for start, finish, (low, high) in zip(left, right, FORBIDDEN_RECTANGLE_RAD):
        delta = finish - start
        if delta == 0.0:
            if start < low or start > high:
                return True
            continue
        near, far = sorted(((low - start) / delta, (high - start) / delta))
        enter, leave = max(enter, near), min(leave, far)
        if enter > leave + 1e-12:
            return True
    return False


def slice_state_is_allowed(point):
    """Return whether one (q1, q2) pair satisfies the declared slice rule."""
    return slice_edge_is_allowed(point, point)
