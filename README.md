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

## Head-to-head (forge benchmark, same metrics)

| | regimes | bed% | shelf cm² |
|---|---|---|---|
| human Backside | 2 | 30 | 0.0 |
| **ours (t7)** | **1** | **31** | **0.0** |

Generated case matches or beats the human reference on every static
metric — support-free, flat-bed, uniform silhouette. What the human
still has that we don't (v2 backlog): printed cable channels for the
scanner ribbon, the dedicated scanner sub-enclosure, snap hooks
(we use friction + open end).

## Regenerate

```sh
python3 scripts/validate.py && python3 scripts/build.py
```
