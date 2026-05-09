# Reference SoM manifest examples

This directory contains **non-normative** reference snippets showing how
a per-SoM manifest declares (a) which subset of the E1M pinout the SoM
actually routes and (b) the silicon behind those pins. Real SoM manifests
live in a separate **consumer** repository (e.g. `alp-studio`); these
examples are tracked here only to keep the manifest format aligned with
the standard.

The `som_manifest_version` is independent of the E1M `loom_format_version`.
Both can evolve, but a SoM manifest with `implements.spec_version: "1.0"`
SHALL only reference pad IDs that exist in the matching `pinout/v1.json`
(or `pinout/x-v1.json`) at v1.0 of this repository.

## Files

| File | SKU | Form factor | Silicon | Notes |
| --- | --- | --- | --- | --- |
| [`alp-aen.som-manifest.json`](./alp-aen.som-manifest.json) | `E1M-AEN301` | E1M (35×35) | Alif Semiconductor Ensemble E3 | Minimal example: routes a small subset (debug + I²C + a few GPIOs). Used to bring up first silicon. The `family_skus` field lists all six E1M-AEN SKUs (E1M-AEN301 / 401 / 501 / 601 / 701 / 801) that share this routing. |
| [`alp-x-v2n-m1.som-manifest.json`](./alp-x-v2n-m1.som-manifest.json) | `E1M-V2M101` | E1M-X (45×65) | Renesas RZ/V2N + DRP-AI3 + DeepX M1 | Extended example: shows multiple silicon parts on one SoM, broader routing, and the `not_routed` field. The `family_skus` field lists `E1M-V2M101` / `E1M-V2M102`; the sibling `E1M-X V2N` family (`E1M-V2N101` / `E1M-V2N102`) is the same module without DeepX M1. |

## Manifest format (v1)

```json
{
  "som_manifest_version": 1,
  "id": "ALP-AEN",
  "version": "0.1.0",
  "implements": {
    "spec_id": "E1M",
    "spec_version": "1.0",
    "spec_repo": "https://github.com/alpCaner/e1m-spec"
  },
  "silicon": [
    {
      "role": "primary",
      "vendor": "Alif Semiconductor",
      "family": "Ensemble",
      "part": "E3"
    }
  ],
  "routes": [
    {
      "pad_id": "A1",
      "use": "default",
      "soc_pin": "VSS"
    },
    {
      "pad_id": "AF2",
      "use": "default",
      "soc_pin": "P0_2",
      "as": "I2C_SCL",
      "instance": "I2C0"
    },
    {
      "pad_id": "AG2",
      "use": "alt",
      "soc_pin": "P0_4",
      "as": "GPIO"
    }
  ],
  "not_routed": ["B27", "A27", "B28", "A28"]
}
```

### Field meanings

| Field | Type | Description |
| --- | --- | --- |
| `som_manifest_version` | int | Manifest schema version. `1` for this rev. |
| `id` | string | Per-SoM identifier (e.g. `ALP-AEN`). |
| `version` | string (semver) | Per-SoM version, independent of E1M version. |
| `implements.spec_id` | string | Always `E1M` or `E1M-X`. |
| `implements.spec_version` | string | E1M version this SoM targets. |
| `implements.spec_repo` | string (URI) | Pointer to the canonical e1m-spec repo. |
| `silicon` | array | One entry per chip on the module that contributes routed pins. |
| `silicon[].role` | string | `primary`, `accelerator`, `pmic`, etc. — informational. |
| `silicon[].vendor`, `family`, `part` | string | Free-form silicon identification. |
| `routes` | array | One entry per E1M pad the SoM routes. |
| `routes[].pad_id` | string | MUST match a `pads[].id` in the target Loom JSON. |
| `routes[].use` | enum | `default` or `alt`. Selects which function the SoM routes. |
| `routes[].as` | SignalKind | When `use=alt`, the alt SignalKind the SoM exposes. Omit when `use=default` (the default is implied). |
| `routes[].instance` | PeripheralInstance | Optional, matches the pad's `instance` from the Loom JSON. |
| `routes[].soc_pin` | string | Free-form silicon pin label (datasheet name). |
| `not_routed` | array of strings | Pad IDs that the SoM intentionally leaves unconnected. Listing them is OPTIONAL; doing so makes diffs against future revisions clearer. |
