# e1m-spec

Canonical specification for the **E1M** AI module-on-module pinout
standard, covering two form factors:

- **E1M** — 35 × 35 mm, 312 pads.
- **E1M-X** — 45 × 65 mm, 496 pads.

E1M defines the universe of physical pads on each form factor and
which peripheral signals each pad may carry. The standard is
intentionally silicon-agnostic — variants such as **ALP-AEN** (Alif
Ensemble), **ALP-X-V2N** (Renesas RZ/V2N), and **ALP-X-V2N-M1**
(DRP-AI3 + DeepX M1) share these pinouts and declare their routed
subset in per-variant SoM manifests held in consumer repositories
(e.g. `alp-studio`).

## Contents

| Path | Purpose |
| --- | --- |
| `STANDARD.md` | Prose specification (OSM-style). The normative document. |
| `pinout/v1.json` | Canonical machine-readable E1M pinout (Loom v1). |
| `pinout/x-v1.json` | Canonical machine-readable E1M-X pinout (Loom v1). |
| `pinout/schema/loom-v1.schema.json` | JSON Schema validating both pinout files. |
| `images/` | Pinout drawings, footprint mechanical drawings, cross-sections, placement diagrams. See `images/CONTENTS.md`. |
| `examples/` | Reference SoM manifest snippets showing how a variant declares its routed subset. |
| `source/altium-*.tsv` | Authoritative pin-list exports from Altium — the source from which `pinout/*.json` is built. |
| `source/_build.py` | Generator: `altium-*.tsv` → `pinout/*.json`. |
| `CHANGELOG.md` | Version history. |
| `LICENSE` | CC BY-SA 4.0 notice + scope + trademarks. |

## Open work

The specification has explicit `> **TODO (Alp Lab):** …` blocks in
every section that still needs author input — searchable via
`grep -n 'TODO (Alp Lab)' STANDARD.md`. They cover footprint
dimensions, height envelopes, electrical characteristics, power
sequencing, packaging, and the boot-strap normative interpretation.

## Status

**v1.0 — in preparation.** Pinout JSON files are generated from the
Altium pin-list exports in `source/altium-e1m.tsv` and
`source/altium-e1m-x.tsv` by `source/_build.py`. STANDARD.md is the
prose specification that goes alongside.

## Versioning

The form-factor uses `major.minor` (e.g. `1.0`, `1.1`, `2.0`).

- **Major** bumps for any backwards-incompatible pad change (pad removed,
  pad signal-set narrowed, pad position shifted).
- **Minor** bumps for additions only (new alt-function on an existing pad,
  new pad in a previously-reserved location).

Releases are tagged `v<major>.<minor>` (e.g. `v1.0`).

## Non-goals

This repo is the **standard**, nothing else. It does not contain:

- Per-SoM data (compute SoC, AI accelerator, peripheral exposure).
- Block-library content, Zephyr code, firmware, or Studio app code.
- Marketing material.

## License

The E1M specification is licensed under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). See
[`LICENSE`](./LICENSE) for the full notice, scope, and trademark terms.

The proprietary SoM designs that implement E1M (ALP-AEN, ALP-X-V2N,
ALP-X-V2N-M1, etc.) are **not** part of this repository and are **not**
covered by CC BY-SA 4.0.
