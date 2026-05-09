# images/

Figures referenced from `STANDARD.md`. All images were extracted from
the historical authoring document (`Alp Lab - E1M Standard.docx`, kept
on OneDrive outside this repository) by `source/_extract_images.py`,
then renamed by hand once their contents were verified.

The doc's original captions were unreliable — for example, the file
the doc captions as "Figure 1: E1M Pin-out drawing" actually shows the
44 × 64 grid that belongs to **E1M-X**, not E1M. The names below
reflect what each image actually depicts.

## Pinout drawings

| File | Form factor | Notes |
| --- | --- | --- |
| `e1m-pinout-drawing.png` | E1M (35 × 35 mm) | Top-view with column letters A…AH (34 cols) and rows 1…34. Three-row peripheral pad band; centre is reserved for top-side components. |
| `e1m-x-pinout-drawing.png` | E1M-X (45 × 65 mm) | Top-view with column letters A…AR (44 cols) and rows 1…64. Wider peripheral pad band on top and bottom edges. |

## Footprint mechanical drawings

| File | Form factor | Notes |
| --- | --- | --- |
| `e1m-footprint.png` | E1M (35 × 35 mm) | Mechanical drawing with overall 35 × 35 mm dimensions, 29 × 27 mm centre cavity, and Detail A (5:1 scale corner view) showing 0.5 mm pad pitch and 0.4 mm pad diameter. |
| `e1m-x-footprint.png` | E1M-X (45 × 65 mm) | Mechanical drawing with overall 45 × 65 mm dimensions, 39.45 × 57.45 mm centre cavity, and Detail A and Detail B (5:1 scale corner views). |
| `e1m-x-footprint.svg` | E1M-X (45 × 65 mm) | Vector version of `e1m-x-footprint.png` (same drawing, scalable). |

## Mechanical cross-sections

| File | Notes |
| --- | --- |
| `module-cross-section-standard-height.png` | Side view of a SoM mounted directly on a base board (standard-height class, no spacer). Top-side components are within the standard envelope. |
| `module-cross-section-extended-height.png` | Side view with a spacer-PCB layer between the SoM and the base board, allowing components on the bottom of the SoM to clear the base-board surface (extended-height class). |

## Component placement areas

| File | Notes |
| --- | --- |
| `component-placement-areas.png` | Top-side and bottom-side placement diagrams. Shows the central component zone (≈30 × 16.5 mm and 30 × 17.5 mm) within the LGA pad band, with cut-out hints for the spacer / base-board cavity. |
| `form-factor-zones.png` | Form-factor outline schematic with peripheral pad bands and central placement zones (45 × ~30 mm with 30 × 30 mm centre). |

## Reference / informative

These three are screenshots of the OSM (Open Standard Module)
Industrial specification, included because the doc author modelled
parts of E1M on OSM. They are kept here as bibliographic reference and
are **not** normative for this standard.

| File | Notes |
| --- | --- |
| `osm-ref-interface-overview.png` | OSM spec §2.1.4 *Interface Overview* — sizes 0/S/M/L feature counts. |
| `osm-ref-size0-pinout.png` | OSM spec §2.3.3.2 *Size-0 Detailed Contact Overview* — pad map for the smallest OSM size. |
| `osm-ref-size-s-additions.png` | OSM spec §2.3.4 *Size-S ADDITIONAL Functions* — additional features added at Size-S. |

## Brand

| File | Notes |
| --- | --- |
| `logo-alp-lab.png` | Faded white-on-white Alp Lab logo. Header asset. |

## Unidentified

| File | Notes |
| --- | --- |
| `misc-floating.svg` | Floating SVG inside the docx with no caption. View-box 193 × 138 mm. **TODO:** identify or delete. |

## Re-extraction

If figures are added or replaced in the docx, re-run:

```sh
python source/_extract_images.py
```

The script will re-create `images/` with caption-derived names; you
will need to rename them back to the descriptive names listed above.
