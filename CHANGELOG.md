# Changelog

All notable changes to the E1M specification are recorded here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning is `major.minor` per the rules in `README.md`.

## [1.0.1] — 2026-05-09

### Fixed

- Replaced placeholder SKU names (`ALP-AEN-E3`, `ALP-X-V2N`,
  `ALP-X-V2N-M1`) with the canonical SKUs from the per-family
  datasheets:
  - **E1M-AEN family** — `E1M-AEN301`, `E1M-AEN401`, `E1M-AEN501`,
    `E1M-AEN601`, `E1M-AEN701`, `E1M-AEN801`.
  - **E1M-X V2N family** — `E1M-V2N101`, `E1M-V2N102`.
  - **E1M-X V2N-M1 family** — `E1M-V2M101`, `E1M-V2M102`.
- Annex A.1 now lists the correct Alif part numbers
  (`AE722F80F55D5LS`, `AE822FA0E5597LS0`, `AE612FA0E5597LS0`,
  `AE402FA0E5597LE0`, `AE512F80F55D5LS`) and the correct CPU/NPU
  topology per Ensemble variant (E3–E8).
- Annex A.2 / A.3 add the canonical Renesas part number
  (`R9A09G056N44GBG#AC0`) and split each family into its 32 / 32 vs
  64 / 128 Gbit memory tiers.
- Example manifests updated: `id` is now the actual SKU
  (`E1M-AEN301`, `E1M-V2M101`); `family_skus` lists every SKU in the
  family.

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
