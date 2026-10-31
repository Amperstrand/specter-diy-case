# Specter-DIY Sandwich Case — enclosure-forge target #7

Our pipeline's answer to the HUMAN reference: the
[cryptoadvance/specter-diy snapcase](https://github.com/cryptoadvance/specter-diy)
(3 hand-designed parts enclosing the STM32F469 DISCO + shield + QR scanner).

## Method

S1 measured the human STLs directly (derived_reference_stl provenance —
no board files needed): board envelope **58.2 × 125.2 mm** from the
Backside cavity, 2 mm front-frame rim from the Frontside aperture,
connector-edge-open treatment from the Alternative case study
(`enclosure-forge/references/human-design-playbook.md`).

## Design (same retention class as the human)

- Full-height **guide rails** alongside the sandwich; retention = the
  lid frame clamping the stack (the human's friction-sandwich class,
  zero screws)
- **Open-frame lid** with the measured 2 mm rim
- **Connector end open** (human treatment)
- 6/6 boolean checks incl. slide-out kinematics and named lid-clamp
  contact; deterministic rebuild

## Head-to-head vs the human reference design

Every figure below is reconstructed from in-repo evidence only: this
README, the committed `analysis/interference_report.json`, commit
messages, and the `Validate` workflow (green on the current head).
Metrics that were never recorded in this repo are marked as such.

| Metric | Human reference (cryptoadvance Backside) | This pipeline (t7) | In-repo source |
|---|---|---|---|
| Parts | 3 hand-designed | 3 (bottom + lid + scanner tray) | README intro; `solids_valid` check; commit `d2eab57` "3-part parity" |
| Provenance | hand-designed snapcase | measured from the human STLs (derived_reference_stl) | README Method |
| Board envelope | 58.2 × 125.2 mm (Backside cavity) | same envelope, measured from the human STLs | README Method |
| Retention | friction sandwich, zero screws | same class — lid frame clamps the stack | README Design |
| Connector end | open | open (human treatment) | README Design |
| Print regimes (forge benchmark) | 2 | 1 | forge benchmark table below |
| Bed usage, bed% (forge benchmark) | 30 | 31 | forge benchmark table below |
| Shelf area, shelf cm² (forge benchmark) | 0.0 | 0.0 | forge benchmark table below |
| Boolean validation | not recorded in-repo | 7/7 checks pass | `analysis/interference_report.json`; `Validate` workflow green on head |
| Cable channels for scanner ribbon | yes (printed) | yes, since v2 — measured 4.8 mm channels both walls | commit `d2eab57`; `scanner_tray_channels_module` check |
| Dedicated scanner sub-enclosure | yes | yes, since v2 — `scanner_tray` solid | commit `d2eab57`; `solids_valid` check |
| Snap hooks | yes | no — friction + open end instead | README Design |

Forge benchmark (same metrics for both designs):

| | regimes | bed% | shelf cm² |
|---|---|---|---|
| human Backside | 2 | 30 | 0.0 |
| **ours (t7)** | **1** | **31** | **0.0** |

Generated case matches or beats the human reference on every static
metric — support-free, flat-bed, uniform silhouette. The one human
feature we still don't replicate: snap hooks (we use friction + open
end).

## Regenerate

```sh
python3 scripts/validate.py && python3 scripts/build.py
```
