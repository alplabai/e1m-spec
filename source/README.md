# source/

Authoritative inputs for the E1M specification.

## Files

- `altium-e1m.tsv` — Altium pin-list export for E1M (35 × 35, 312 pads).
- `altium-e1m-x.tsv` — Altium pin-list export for E1M-X (45 × 65, 496 pads).
- `_build.py` — generator that reads both `.tsv` files and writes
  `pinout/v1.json` (E1M) and `pinout/x-v1.json` (E1M-X).

## Format

Each `.tsv` is a two-column whitespace-separated text file:

```
<pad-id>\t<pin-name>
```

- `pad-id` is the BGA-style coordinate (`A1`, `K63`, `AQ15`, …).
- `pin-name` is the Altium net/pad designator. Compound names use slash
  (`JTAG_TCK/SWDCLK`); not-connected pads use `NC`; reserved pads use
  `RSVD`.

The order of lines is irrelevant; `_build.py` sorts by pad id.

## Rules

1. **Altium is the source of truth.** Any change to the pinout starts in
   the Altium project and is exported into the corresponding `.tsv`.
2. After updating a `.tsv`, run `python source/_build.py`. The script
   re-generates the JSON files and prints any anomalies (typos, case
   mismatches, unmapped names). Resolve them before committing.
3. Do **not** hand-edit `pinout/v1.json` or `pinout/x-v1.json`. CI runs
   `_build.py` and diffs the result against the committed JSON; any
   manual edit will fail CI.

## Anomaly handling

`_build.py` auto-corrects a small set of known input issues so the JSON
schema passes; the original Altium silkscreen is preserved in the
`silkscreen` field for traceability. Current auto-fixes:

| Input | Output | Reason |
| --- | --- | --- |
| `RVSD` | `RSVD` (signal) | Typo. |
| `ANT_2.4GHz`, `ANT_5GHz`, `ANT_6GHz` | uppercase `…GHZ` | Case-insensitive enum. |

Any other unmapped name aborts the build.
