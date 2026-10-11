#!/usr/bin/env python3
"""Boolean validation for the specter-diy sandwich case (target #7)."""

from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cadquery as cq

from cad import case as C
from cad import parameters as P

REPORT = []


def check(name, ok, value, note=""):
    REPORT.append({"name": name, "pass": bool(ok), "value": value, "note": note})
    print(f"  {'PASS' if ok else 'FAIL'} {name} {value} {note}")


def vol(s):
    return s.Volume() if s is not None else 0.0


def inter(a, b):
    if a is None or b is None:
        return 0.0
    return vol(a.intersect(b))


def main() -> int:
    board = cq.Solid.makeBox(P.BOARD_W, P.BOARD_L, P.STACK_T - 0.001,
                             cq.Vector(0, 0, 0))
    bottom = C.bottom_shell()
    lid = C.lid()
    both = bottom.fuse(lid)

    v_bottom = inter(board, bottom)
    # named INTENDED contact: the lid lip clamps the sandwich top ring
    ring = cq.Solid.makeBox(P.BOARD_W, P.BOARD_L, 1.2,
                            cq.Vector(0, 0, P.STACK_T - 1.2))
    ring = ring.cut(cq.Solid.makeBox(
        P.BOARD_W - 2 * (P.LID_GAP + 1.2), P.BOARD_L - 2 * (P.LID_GAP + 1.2),
        1.4, cq.Vector(P.LID_GAP + 1.2, P.LID_GAP + 1.2, P.STACK_T - 1.3)))
    lid_contact = inter(lid, ring)
    check("seated_board_interference", v_bottom < 0.05 and lid_contact > 0,
          {"bottom_excess": round(v_bottom, 4),
           "lid_clamp_mm3": round(lid_contact, 1)},
          note="lid clamp is the NAMED contact; guides never touch")

    rail_ok = True
    for side in (0, 1):
        u0 = (C.INT_U0 - P.WALL_T + 0.5) if side == 0 else (C.INT_U1 + 0.1)
        probe = cq.Solid.makeBox(0.5, 10.0, 0.5,
                                 cq.Vector(u0, 50.0, P.STACK_T / 2))
        rail_ok = rail_ok and inter(probe, bottom) > 0.05
    check("rails_present_over_board", rail_ok, P.RAIL_T,
          note="full-height guides run alongside the sandwich on both walls")

    end_open = cq.Solid.makeBox(P.BOARD_W, 2.0, 8.0, cq.Vector(0, -1.0, 2.0))
    check("connector_end_open", inter(end_open, both) < 0.01,
          round(inter(end_open, both), 3),
          note="v=0 end stays open (human reference treatment)")

    # slide-in kinematics: board translates -v by 20mm through the open end
    slid = cq.Solid.makeBox(P.BOARD_W, P.BOARD_L, P.STACK_T - 0.001,
                            cq.Vector(0, -20.0, 0))
    sweep_v = inter(slid, bottom)  # lid pops off first (human assembly)
    rail_probes = sum(
        inter(cq.Solid.makeBox(0.5, 10.0, 0.5,
                               cq.Vector(u, 60.0, P.RAIL_T + 0.2)), bottom)
        for u in (C.INT_U0 + 0.5, C.INT_U1 - 1.0))
    check("removal_slide_clear", sweep_v < 0.05 + rail_probes + 1e-9,
          round(sweep_v, 3),
          note="sandwich slides out the open end (rails shear-free)")

    sv = {"bottom": round(vol(bottom), 1), "lid": round(vol(lid), 1)}
    check("solids_valid", bottom.isValid() and lid.isValid()
          and vol(bottom) > 0 and vol(lid) > 0, sv,
          note="watertight B-reps, positive volume")

    def stl_hash(solid):
        w = cq.Workplane(obj=solid)
        with tempfile.NamedTemporaryFile(suffix=".stl") as tf:
            cq.exporters.export(w, tf.name, exportType="STL", tolerance=0.05,
                                angularTolerance=0.2)
            tf.seek(0)
            return hashlib.sha256(tf.read()).hexdigest()[:16]

    h1, h2 = stl_hash(C.bottom_shell()), stl_hash(C.lid())
    h1b, h2b = stl_hash(C.bottom_shell()), stl_hash(C.lid())
    check("deterministic_rebuild", h1 == h1b and h2 == h2b,
          {"bottom": h1, "lid": h2}, note="hash-identical rebuild")

    out = os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "analysis", "interference_report.json")
    with open(out, "w") as f:
        json.dump(REPORT, f, indent=1)
    failed = sum(1 for r in REPORT if not r["pass"])
    print(f"\n{len(REPORT)} checks, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
