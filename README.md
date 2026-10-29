# e1m-spec

Canonical specification for the **E1M** AI system-on-module (SoM) pinout
standard, covering two form factors:

- **E1M** — 35 × 35 mm, 312 pads.
- **E1M-X** — 45 × 65 mm, 496 pads.

E1M defines the universe of physical pads on each form factor and
which peripheral signals each pad may carry. The standard is
intentionally silicon-agnostic — variants such as **E1M-AEN** (Alif
Ensemble), **E1M-X V2N** (Renesas RZ/V2N) and **E1M-X V2N-M1**
(Renesas RZ/V2N + DeepX DX-M1) share these pinouts and declare their
routed subset in per-variant SoM manifests held in the SoM vendor's
own repository or tooling.

## Contents

| Path | Purpose |
| --- | --- |
| `STANDARD.md` | Prose specification. The normative document. |
| `pinout/v1.json` | Canonical machine-readable E1M pinout (Loom v1). |
| `pinout/x-v1.json` | Canonical machine-readable E1M-X pinout (Loom v1). |
| `pinout/schema/loom-v1.schema.json` | JSON Schema validating both pinout files. |
| `images/` | Pinout drawings, footprint mechanical drawings, cross-sections, placement diagrams. See `images/CONTENTS.md`. |
| `examples/` | Reference SoM manifest snippets showing how a variant declares its routed subset. |
| `source/altium-*.tsv` | Authoritative pin-list exports from Altium — the source from which `pinout/*.json` is built. |
| `source/_build.py` | Generator: `altium-*.tsv` → `pinout/*.json`. |
| `CHANGELOG.md` | Version history. |
| `LICENSE` | CC BY-SA 4.0 notice + scope + trademarks. |

## Status

**v1.9 — released (2026-10-29)** (`E1M-STD-1.0` revision 1.9). Pinout JSON files are generated from the
Altium pin-list exports in `source/altium-e1m.tsv` and
`source/altium-e1m-x.tsv` by `source/_build.py`. STANDARD.md is the
prose specification that goes alongside.

## Versioning

Two version numbers apply, and they are independent.

**Document revision.** Releases of this repository are tagged
`v<X>.<Y>` (e.g. `v1.9`). Each tag is a document revision of
`E1M-STD-1.0` (Edition 1.0); the current one is revision 1.9 (tag
`v1.9`). A document revision corrects or extends the text, figures and
tooling; it does not by itself change the form-factor version.

**Form-factor (Loom) version.** The pinout JSONs carry the form-factor
version in their `version` field, as `major.minor`. It is currently
`1.0` for both `pinout/v1.json` and `pinout/x-v1.json`. It changes only
under these rules (`STANDARD.md` §1.5):

- **Major** bumps for any backwards-incompatible pad change (pad removed,
  pad signal-set narrowed, pad position shifted).
- **Minor** bumps for additions only (new alt-function on an existing pad,
  new pad in a previously-reserved location).

## Non-goals

This repo is the **standard**, nothing else. It does not contain:

- Per-SoM data (compute SoC, AI accelerator, peripheral exposure).
- Block-library content, Zephyr code, firmware, or Studio app code.
- Marketing material.

## License

The E1M specification is licensed under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). See
[`LICENSE`](./LICENSE) for the full notice, scope, and trademark terms.

The proprietary SoM designs that implement E1M (E1M-AEN, E1M-X V2N,
E1M-X V2N-M1, etc.) are **not** part of this repository and are **not**
covered by CC BY-SA 4.0.
