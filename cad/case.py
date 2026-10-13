"""Specter-DIY sandwich case: open-end rail tray + frame lid (target #7)."""

from __future__ import annotations

import cadquery as cq

from . import parameters as P

INT_U0, INT_U1 = 0.0, P.BOARD_W
INT_V0, INT_V1 = 0.0, P.BOARD_L
LID_Z0 = P.STACK_T


def _box(x0, y0, x1, y1, z0, z1):
    if x1 <= x0 or y1 <= y0 or z1 <= z0:
        return None
    return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, cq.Vector(x0, y0, z0))


def bottom_shell():
    ox0, oy0 = INT_U0 - P.WALL_T, INT_V0 - P.WALL_T
    ox1, oy1 = INT_U1 + P.WALL_T, INT_V1 + P.WALL_T
    cx, cy = (ox0 + ox1) / 2, (oy0 + oy1) / 2
    walls = (
        cq.Workplane("XY", origin=(cx, cy, -P.FLOOR_T))
        .rect(ox1 - ox0, oy1 - oy0).extrude(LID_Z0 + P.FLOOR_T)
        .edges("|Z").fillet(P.CORNER_R)
    ).val()
    # open connector end: remove the v=0 wall above the floor
    walls = walls.cut(_box(ox0 - 1, oy0 - 1, ox1 + 1, INT_V0,
                           -P.FLOOR_T - 1, LID_Z0 + 1))
    cavity = _box(INT_U0, INT_V0 - 0.05, INT_U1, INT_V1 + 0.05,
                  -P.FLOOR_T - 0.01, LID_Z0 + 1)
    solid = walls.cut(cavity)
    solid = solid.fuse(_box(INT_U0, INT_V0, INT_U1, INT_V1, -P.FLOOR_T, 0.0))

    # full-height guide rails alongside the sandwich (tall stacks slide
    # BETWEEN guides; retention = lid frame clamp, the human class)
    for u_wall in (INT_U0 - P.WALL_T, INT_U1):
        solid = solid.fuse(_box(u_wall, P.RAIL_V0, u_wall + P.WALL_T,
                                P.RAIL_V1, 0.0, P.STACK_T))
    return solid


def lid():
    ox0, oy0 = INT_U0 - P.WALL_T, INT_V0 - P.WALL_T
    ox1, oy1 = INT_U1 + P.WALL_T, INT_V1 + P.WALL_T
    cx, cy = (ox0 + ox1) / 2, (oy0 + oy1) / 2
    frame = (
        cq.Workplane("XY", origin=(cx, cy, LID_Z0))
        .rect(ox1 - ox0, oy1 - oy0).extrude(1.6)\
        .edges("|Z").fillet(P.CORNER_R)\
        .edges(">Z").chamfer(0.6)
    ).val()
    # measured_reference: ~2mm rim; aperture nearly the full face
    frame = frame.cut(_box(INT_U0 - 0.1, INT_V0 - 0.1, INT_U1 + 0.1,
                           INT_V1 + 0.1, LID_Z0 - 1, LID_Z0 + 2))
    ap_w, ap_l = P.BOARD_W - 2 * P.RIM_W, P.BOARD_L - 2 * P.RIM_W
    frame = frame.fuse(_box((INT_U0 + INT_U1) / 2 - ap_w / 2,
                            (INT_V0 + INT_V1) / 2 - ap_l / 2,
                            (INT_U0 + INT_U1) / 2 + ap_w / 2,
                            (INT_V0 + INT_V1) / 2 + ap_l / 2,
                            LID_Z0, LID_Z0 + 1.6))
    lip = _box(INT_U0 + P.LID_GAP, INT_V0 + P.LID_GAP,
               INT_U1 - P.LID_GAP, INT_V1 - P.LID_GAP,
               LID_Z0 - P.LID_LIP, LID_Z0)
    lip = _box(INT_U0 + P.LID_GAP + 1.2, INT_V0 + P.LID_GAP + 1.2,
               INT_U1 - P.LID_GAP - 1.2, INT_V1 - P.LID_GAP - 1.2,
               LID_Z0 - P.LID_LIP - 1, LID_Z0 + 1) if False else lip.cut(
        _box(INT_U0 + P.LID_GAP + 1.2, INT_V0 + P.LID_GAP + 1.2,
             INT_U1 - P.LID_GAP - 1.2, INT_V1 - P.LID_GAP - 1.2,
             LID_Z0 - P.LID_LIP - 1, LID_Z0 + 1))
    return frame.fuse(lip)


def scanner_tray():
    """Back-mounted QR-scanner frame (measured from the human Scanner.stl):
    56 x 123 x 9 open-back frame with 4.8mm cable channels along both
    side walls — the playbook's 'cable channels as first-class geometry'."""
    w, l, h = 56.0, 123.0, 9.0
    wall = 2.0
    ch_w = 4.8            # measured_reference: side channel width
    cx, cy = w / 2, l / 2
    frame = (
        cq.Workplane("XY", origin=(cx, cy, 0))
        .rect(w, l).extrude(h)
        .edges("|Z").fillet(P.CORNER_R)
    ).val()
    # module pocket (open back = z=0 face down when mounted)
    frame = frame.cut(_box(wall, wall, w - wall, l - wall, -0.1, h * 0.72))
    # cable channels through the side walls (full length, measured width)
    frame = frame.cut(_box(wall - 0.1, 47.0, wall + ch_w, 97.3, -0.1, h + 0.1))
    frame = frame.cut(_box(w - wall - ch_w, 47.0, w - wall + 0.1, 88.1,
                           -0.1, h + 0.1))
    return frame
