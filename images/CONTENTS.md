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
| `e1m-pinout-drawing.png` | E1M (35 × 35 mm) | Top view with row letters A…AH (34 rows, top to bottom) and column numbers 1…34 (left to right). Pad band two pads deep top and bottom, three pads deep left and right; centre is reserved for top-side components. |
| `e1m-x-pinout-drawing.png` | E1M-X (45 × 65 mm) | Top view, landscape, with row letters A…AR (44 rows, top to bottom) and column numbers 1…64 (left to right). Pad band two pads deep along the long edges, three pads deep along the short edges. |

## Footprint mechanical drawings

| File | Form factor | Notes |
| --- | --- | --- |
| `e1m-footprint.png` | E1M (35 × 35 mm) | Mechanical drawing with overall 35 × 35 mm dimensions, 29 × 27 mm centre cavity, and Detail A (5:1 scale corner view) showing 0.5 mm pad pitch and 0.4 mm pad diameter. |
| `e1m-x-footprint.png` | E1M-X (45 × 65 mm) | Mechanical drawing with overall 45 × 65 mm dimensions, 39.45 × 57.45 mm centre cavity, and Detail A and Detail B (5:1 scale corner views). |
| `e1m-x-footprint.svg` | E1M-X (45 × 65 mm) | Vector version of `e1m-x-footprint.png` (same drawing, scalable). |

## Mechanical cross-sections

| File | Notes |
| --- | --- |
| `module-cross-section-spacer-pcb.svg` | Mounting option (a), §5.2: module on a spacer PCB soldered on both faces; the SoM bottom-side components under the central cavity clear the carrier surface. Not to scale; heights TBD. |
| `module-cross-section-carrier-cutout.svg` | Mounting option (b), §5.2: module over a carrier through-cutout of the central-cavity size and position. Not to scale; heights TBD. |

## Component placement areas

| File | Notes |
| --- | --- |
| `component-placement-areas.png` | Top-side and bottom-side placement diagrams. Shows the central component zone (≈30 × 16.5 mm and 30 × 17.5 mm) within the LGA pad band, with cut-out hints for the spacer / base-board cavity. |
| `form-factor-zones.png` | Form-factor outline schematic with peripheral pad bands and central placement zones (45 × ~30 mm with 30 × 30 mm centre). |

## Brand

| File | Notes |
| --- | --- |
| `logo-alp-lab.png` | Faded white-on-white Alp Lab logo. Header asset. |

## Unidentified

| File | Notes |
| --- | --- |
| `misc-floating.svg` | Floating SVG inside the docx with no caption. View-box 193 × 138 mm. |

## Re-extraction

If figures are added or replaced in the docx, re-run:

```sh
python source/_extract_images.py
```

The script will re-create `images/` with caption-derived names; you
will need to rename them back to the descriptive names listed above.
