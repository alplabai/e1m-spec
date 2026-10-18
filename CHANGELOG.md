# Changelog

All notable changes to the E1M specification are recorded here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning is `major.minor` per the rules in `README.md`.

## [Unreleased]

Targets document revision 1.3 of `E1M-STD-1.0` (Edition 1.0, draft for
review). The designation and edition stay `E1M-STD-1.0` / 1.0; only
the document revision advances. The pinout JSONs and the Loom
form-factor version (`1.0`) are unchanged.

### Added (normative — SoM and carrier electrical rules)

- **§6.1.1 5 V supply input.** Carrier window for any SoM:
  4.75–5.25 V at the `VDD_5V_IN` pads, ≤ 5.5 V absolute maximum
  (a TVS alone does not meet it), monotonic ramp 0 V → 4.75 V within
  40 ms (E1M-AEN-confirmed value); every 5 V pad connected; source
  sized for declared peak current; carrier OVP / reverse-polarity
  protection; declared hold-up capacitance; no back-feed when OR-ing
  sources. SoM side: operate across 4.75–5.25 V, withstand 5.5 V,
  declare the input values in the manifest. Informative table of
  reference-SoM values.
- **§6.1.2 `VIO_OUT`.** 1.8 V nominal (±5 %, V2N / V2N-M1-confirmed);
  output only, never driven or tied to another rail; permitted uses;
  any-SoM load limit ≤ 100 mA, ≤ 50 mA in the first 2 ms, ≤ 2.5 µF
  (E1M-AEN-confirmed); translators Hi-Z with V_CCA off; sensing rule.
  Informative: translators rated V_CCA 1.65–3.6 V for forward
  compatibility (no 3.3 V `VIO_OUT` class is defined).
- **§6.2 Power sequencing** (was a TODO). §6.2.1 power-up order
  (5 V → `VIO_OUT` and `PORn` high → drive pads; SoM declares the
  `PORn` release time); §6.2.2 power-down order (carrier outputs Hi-Z
  or low ≤ 1 ms after `PORn` falls; data-loss warning); §6.2.3
  back-powering and I/O gating (no drive or pull-up into
  `VIO_OUT`-domain pads while `VIO_OUT` is low; pull-ups only to
  `VIO_OUT`; −0.3 V to 1.98 V; debug-probe rule; switched pad groups).
- **§6.3 / §6.3.1 control pads.** `MODULE_STBY` is active-low (was
  TBD). `MODULE_EN` is 5 V tolerant (SoM SHALL tolerate −0.3 V to
  5.5 V) and driven open-drain; no pull-up to a rail that can be off;
  host buffering; 5.5 V-rated carrier parts; ≤ 0.1 µA leakage.
  `MODULE_STBY` open-drain, no pull-up above `VIO_OUT`. `PORn`
  open-drain only, no pull-up, ≥ 2 ms pulse, ≤ 1 nF. `JTAG_nRST`
  open-drain. A SoM SHALL boot with all control pads unconnected.
- **§6.6** table of the values now fixed, with clause references;
  remaining characteristics stay TODO.
- **§6.7 Pad voltage domains and safe default fits.** §6.7.1 lists the
  pads outside the `VIO_OUT` domain and the carrier rule for each;
  §6.7.2 requires a safe default fit for dual-meaning pads. For CAN
  the default is the carrier-transceiver path with the bypass DNP.

### Changed (normative)

- **CAN (§6.5, §7.3.14, §8.3, §9.1).** New declared **logic-level
  CAN** option: a SoM MAY expose a CAN group as controller-level
  `CANx_TX` / `CANx_RX` in the `VIO_OUT` domain, declared per group in
  its manifest, and the carrier then provides the transceiver.
  Bus-level CAN stays the default. `CAN_STBY` direction and polarity
  are declared per SoM. §8.3: the CAN compound-pad reading follows the
  SoM's declaration (JTAG/SWD stays a carrier choice). The §6.5
  cross-reference is corrected from §7.3.13 to §7.3.14. The E1M-AEN
  standard build is conformant under this option.
- **Ethernet (§6.5, §7.2, §7.3.6).** MDI pads are PHY-side
  (pre-magnetics); §6.5 said "post-magnetics". MDI ESD moves to a
  carrier SHALL (a SoM MAY add its own and declares it). Link rate per
  port is declared; any-SoM carriers route all four pairs with
  1000BASE-T magnetics; LED-pad strap rule. §7.2 row "Ethernet 1 GbE"
  renamed "Ethernet port (MDI, up to 1000BASE-T)" (counts unchanged);
  `source/_check_prose_counts.py` follows the new label.
- **Wi-Fi bands (§6.5, §7.3.2, §9.1).** 2.4 GHz operation is REQUIRED;
  5 GHz and 6 GHz are each OPTIONAL and declared in the SoM manifest
  (was: 2.4 GHz and 5 GHz required). A SoM that does not use
  `ANT_5GHz` / `ANT_6GHz` leaves the pad no-connect and declares it.
  E1M-AEN (2.4 GHz only) is conformant.
- **Boot strap (§6.4, §9.1, §9.3).** A SoM SHALL expose
  `BOOT0`–`BOOT3` on its footprint and MAY ignore them if its manifest
  declares so; carriers keep the strap circuit (pull-ups to `VIO_OUT`
  only). E1M-AEN (pads unconnected, strap declared ignored) is
  conformant.
- **§7.3.3 / §7.3.4.** RSVD pads: no trace, test point, pull, load or
  jumper. The NC routing permission applies only to spec-`NC` pads,
  not to pads a particular SoM leaves unrouted.
- **§7.3.10.** Debug UART carrier rules (drive `DBG_RX` only while
  `VIO_OUT` is high; console declared in the manifest).
- **§9.1 / §9.2.** SoM electrical and manifest clauses reference the
  new §6 clauses; carrier conformance gains clauses 4–10.

### Fixed

- §5.1.1 Figure 1 caption: the E1M signal grid is 1.0 mm pitch with
  0.40 mm pads (was "0.5 mm pitch"; 0.5 mm is the A1 fiducial). Added
  the normative pitch / pad statement and the E1M-AEN land pattern as
  informative text.
- Annex A.1: the E1M-AEN standard build has no on-module CAN
  transceiver (TI TCAN1044AVDRBRQ1 is an assembly option); debug UART
  and CAN routing notes added.
- Annex A.1: E1M-AEN Wi-Fi is 2.4 GHz only with `ANT_5GHZ` / `ANT_6GHZ`
  NC, and its boot strap is declared ignored.
- Annex C: example manifest shows the new `electrical`, `can`,
  `boot_strap` and `wireless` declarations (field names illustrative).

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
