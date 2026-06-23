# Changelog

All notable changes to the E1M specification are recorded here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning is `major.minor` per the rules in `README.md`.

## [Unreleased]

## [1.2] — 2026-06-23

### Added (normative — E1M pinout)

- **Dedicated debug-console UART on E1M** at previously-reserved pads:
  AD3 = `DBG_TX`, AE3 = `DBG_RX`, mirroring the E1M-X mapping (source:
  E1M-AEN SoM Altium netlist, rev 2626-R2). Each pad keeps a `GPIO`
  alt, like its E1M-X counterpart. E1M `RSVD` count drops 36 → 34
  (§7.2, §7.3.3); §7.2 "Debug UART (console)" E1M column now `1`;
  §7.3.10 lists the pads. `pinout/v1.json` regenerated from the
  Altium source. The Loom form-factor version stays `1.0`; this is a
  doc-level revision (v1.2).

### Changed (normative — E1M-X pinout)

- **E1M-X Ethernet MDI pair order reversed** (Altium export
  2026-06-09). On both `ETH0` and `ETH1` the differential pairs now
  run DD→DA instead of DA→DD across the pad rows; e.g. `ETH1_DA_P`
  moves AQ49 → AQ52 and `ETH0_DA_P` moves AQ56 → AQ59 (16 pads total,
  `_P` and `_N` rows of both groups). LED pads unchanged. E1M (35×35)
  is unaffected. §7.3.6 table and the V2N-M1 example manifest updated.
  The Loom form-factor version stays `1.0` (form factor still
  pre-release) despite the README's major-bump rule for pad moves;
  carried in doc revision v1.2.

### Added (normative — E1M-X pinout)

- **Dedicated debug-console UART** on previously-reserved pads:
  AC62 = `DBG_TX`, AD62 = `DBG_RX` (the E1M counterpart at AD3/AE3
  landed later — see the E1M pinout entry above). New
  `DBG_TX` / `DBG_RX` SignalKinds in
  the Loom schema; §7.2 gains a "Debug UART (console)" row; E1M-X
  RSVD count drops 22 → 20 (§7.2, §7.3.3); §7.3.10 lists the pads.
  Gives the existing §9.3 "non-debug pad" clause a concrete referent.

## [1.1.2] — 2026-05-24

### Fixed

- §7.2 *Interface count overview* and §7.3.1 *Power & control* prose
  counts corrected to match the authoritative pin JSON (`pinout/v1.json`
  / `pinout/x-v1.json`, CI-checked against the Altium source). The
  hand-written tables had drifted (issue #1):
  - E1M `GND`: §7.3.1 said "46 pads" → **49**.
  - E1M `GPIO` (default-function): §7.2 said 25 → **23**.
  - E1M-X `NC`: §7.2 said 35 → **34** (the §7.3.4 pad list already
    enumerated the correct 34).

  Prose-only reconciliation — no pinout or other normative change.

## [1.1.1] — 2026-05-10

### Changed

- Repo moved from `github.com/alpCaner/e1m-spec` to
  `github.com/alplabai/e1m-spec` (Alp Lab AI org). Repo remains
  private; no content change beyond URL references.
- All internal references to the old `alpCaner/e1m-spec` URL
  updated to `alplabai/e1m-spec`:
  - `pinout/schema/loom-v1.schema.json` `$id` field.
  - `examples/alp-aen.som-manifest.json` `spec_repo`.
  - `examples/alp-x-v2n-m1.som-manifest.json` `spec_repo`.
  - `examples/README.md` (manifest example).
  - `STANDARD.md` Annex C manifest example.
- The old `alpCaner/e1m-spec` URL keeps redirecting to the new
  location automatically (GitHub repo-transfer behaviour); existing
  external references will continue to work but should be updated
  at next opportunity.

## [1.1] — 2026-05-09

### Added (normative)

- New §6.5 *Mandatory on-module components*. Promotes a family-wide
  architectural invariant to a normative SHALL clause: every
  conformant SoM **SHALL** integrate, on the module itself,
  - at least one Ethernet PHY (and a second when the SoC supports
    two MACs), connected to the SoC over SoM-internal RGMII / RMII;
    the carrier-side `ETH*_*` pads are post-PHY differential MDI;
  - a Wi-Fi 6 + BLE 5.4 combo radio with mandatory 2.4 GHz and 5 GHz
    operation and optional 6 GHz operation;
  - a CAN transceiver for every CAN group the SoM exposes
    (carrier-side pads are bus-level `CANxH`, `CANxL`).
- §7.3.2 (Antenna), §7.3.6 (Ethernet), §7.3.14 (CAN) updated to
  reference §6.5 explicitly. Antenna populating rule tightened from
  "MAY populate any subset" to "SHALL populate the bands the
  on-module radio supports".
- §9.1 SoM conformance: new clause **5. Mandatory on-module
  components** referencing §6.5.

This is a normative addition relative to v1.0; it does not change
the pinout itself. Existing v1.0 conformant SoMs (the AEN family,
V2N, V2N-M1) are also v1.1 conformant — they all already satisfy
the new clause.

### Changed

- §6.6 *Electrical characteristics* — section number bumped (was §6.5
  in v1.0).

## [1.0.3] — 2026-05-09

### Changed

- `examples/alp-x-v2n-m1.som-manifest.json`: every route's `soc_pin`
  now uses the canonical Renesas RZ/V2N datasheet name (e.g.
  `RIIC0_SCL0`, `MD_BOOT0`, `CSI0_DATA0N`, `TCK_SWCLK`), with the
  matching BGA coordinate in a new `soc_pin_bga` field. Sourced from
  `R9A09G056N44GBG Pin Out.csv` in the design-documentation folder.
- E1M-X `BOOT3` (pad Y1) now correctly maps to Renesas `MD_BOOT4`,
  not `MD_BOOT3` (the chip has no `MD_BOOT3`). `MD_BOOT4` is the strap
  the V2N uses for boot-CPU selection (CA55 vs CM33).
- Ethernet routes in the manifest now carry `soc_via: "Realtek
  RTL8211FDI"` instead of fictional Renesas pin names — the Renesas
  drives the on-module PHY over RGMII (not exposed on E1M-X), and
  the E1M-X ETH pads are the post-PHY differential MDI.
- Added the missing `BOOT2` (pad X1) route entry that earlier drafts
  dropped.

## [1.0.2] — 2026-05-09

### Fixed

- `examples/alp-x-v2n-m1.som-manifest.json` and Annex A.2 now use
  the canonical Renesas part number `R9A09G056N44GBG#AC0` (was
  `R9A09G057`).
- Annex A.2 lists the supporting silicon stack with real part numbers:
  - PMIC: Renesas `DA9292` (was placeholder `RAA215300`).
  - I/O MCU: GigaDevice `GD32G553` (Cortex-M33 @ 216 MHz).
  - Ethernet PHY: Realtek `RTL8211FDI-VD-CG` (one per ETH group).
  - Wi-Fi 6 + BLE 5.4 module: Murata `LBEE5HY2FY` (Type2FY,
    Infineon `CYW55513`).
- DRP-AI3 figure reconciled to **4 TOPS** at the V2N grade
  (chip family rated up to 15 TOPS; per-SKU configuration is 4 TOPS
  per the V2N / V2N-M1 ordering tables).

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
