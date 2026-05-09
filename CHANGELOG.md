# Changelog

All notable changes to the E1M specification are recorded here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning is `major.minor` per the rules in `README.md`.

## [1.0] — 2026-05-09

Initial public draft of the E1M™ Standard.

### Added
- `STANDARD.md` — full prose specification in OSM-style (Designation
  `E1M-STD-1.0`, Status: Draft for review, Publisher: Alp Lab AB).
- `pinout/v1.json` — canonical machine-readable pinout for E1M
  (35 × 35 mm, 312 pads). Mechanically generated from
  `source/altium-e1m.tsv` by `source/_build.py`.
- `pinout/x-v1.json` — canonical machine-readable pinout for E1M-X
  (45 × 65 mm, 496 pads). Same generator pipeline.
- `pinout/schema/loom-v1.schema.json` — JSON Schema (draft 2020-12)
  validating both pinout files.
- `images/` — pinout drawings, footprint mechanical drawings,
  height-class cross-sections, component-placement diagram, plus
  three OSM reference screenshots (informative). See `images/CONTENTS.md`.
- `examples/alp-aen.som-manifest.json`, `examples/alp-x-v2n-m1.som-manifest.json`
  — reference per-SoM manifests with full silicon stack and routing
  caveats.
- `Annex A` of `STANDARD.md` — informative reference SoM details:
  ALP-AEN family (six SKUs E3/E4/E5/E6/E7/E8 sharing one E1M routing),
  ALP-X-V2N (Renesas RZ/V2N + DRP-AI3), ALP-X-V2N-M1 (V2N + DeepX M1
  25 TOPS).
- `.github/workflows/validate.yml` — CI that re-runs `source/_build.py`
  against the Altium TSVs and rejects any pinout drift, plus ajv schema
  validation.
- 11 explicit `> **TODO (Alp Lab):**` placeholders in `STANDARD.md`
  flagging every section that requires Alp Lab author input
  (footprint dimensions, height envelopes, electrical characteristics,
  power sequencing, packaging, boot-strap normative interpretation).
