"""Specter-DIY case parameters (enclosure-forge target #7).

S1 measured from the HUMAN reference STLs (snapcase): board envelope
58.2 x 125.2, full sandwich ~14 thick, front = 2mm open frame,
connector edge left open. Rail-class retention (the human class).
"""

from __future__ import annotations

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEOM = json.load(open(os.path.join(ROOT, "analysis", "pcb_geometry.json")))

BOARD_W = GEOM["outline"]["w"]          # 58.2 (derived_reference_stl)
BOARD_L = GEOM["outline"]["h"]          # 125.2
STACK_T = GEOM["thickness"]             # 14.0 conservative

WALL_T = 1.6            # enclosure_design_decision
FLOOR_T = 1.6           # enclosure_design_decision
CORNER_R = 2.0          # enclosure_design_decision (human case has small radii)

RAIL_LIP = 1.0          # enclosure_design_decision (human: friction sandwich)
RAIL_T = 1.6            # enclosure_design_decision
RAIL_V0, RAIL_V1 = 8.0, 117.0   # rail band leaves the open end clear

RIM_W = 2.0             # measured_reference: front frame rim width
LID_LIP = 1.2           # enclosure_design_decision
LID_GAP = 0.25          # enclosure_design_decision
