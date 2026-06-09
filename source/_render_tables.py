"""Render the §5.4 pinout tables for STANDARD.md from the Altium TSVs.
Writes _pinout-tables.md (gitignored). Run as part of the spec build
when pin data changes.
"""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TSV_E1M = ROOT / "source" / "altium-e1m.tsv"
TSV_E1MX = ROOT / "source" / "altium-e1m-x.tsv"
OUT = ROOT / "source" / "_pinout-tables.md"


def parse(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    with path.open(encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            parts = re.split(r"\s+", line, maxsplit=1)
            if len(parts) != 2:
                continue
            out[parts[0].strip()] = parts[1].strip()
    return out


# --- Classification ----------------------------------------------------------

# Stable ordering for the §5.4 subsections.
CLASS_ORDER = [
    ("Power & control", "5.4.1"),
    ("Antenna", "5.4.2"),
    ("Reserved", "5.4.3"),
    ("Not connected", "5.4.4"),
    ("USB", "5.4.5"),
    ("Ethernet", "5.4.6"),
    ("PCIe", "5.4.7"),
    ("I²C", "5.4.8"),
    ("I³C", "5.4.9"),
    ("UART", "5.4.10"),
    ("SPI", "5.4.11"),
    ("I²S", "5.4.12"),
    ("SWD / JTAG", "5.4.13"),
    ("CAN bus", "5.4.14"),
    ("SDIO / SD card", "5.4.15"),
    ("MIPI DSI display", "5.4.16"),
    ("MIPI CSI camera", "5.4.17"),
    ("Parallel camera", "5.4.18"),
    ("LCD parallel display", "5.4.19"),
    ("PDM microphone", "5.4.20"),
    ("Analog inputs", "5.4.21"),
    ("Analog outputs", "5.4.22"),
    ("Quadrature encoder", "5.4.23"),
    ("PWM", "5.4.24"),
    ("GPIO", "5.4.25"),
]


def classify(name: str) -> str:
    n = name.upper()
    if n == "GND":
        return "Power & control"
    if n in {"VDD", "VDD_5V_IN", "VIO_OUT", "+S_CAP",
             "MODULE_EN", "MODULE_STBY", "PORN",
             "RTC_CLKOUT", "AUDIO_CLK"}:
        return "Power & control"
    if n.startswith("BOOT"):
        return "Power & control"
    if n.startswith("+V_CAM") or n.startswith("CAM_VFB"):
        return "Power & control"
    if n.startswith("BL_LED") or n == "BL_LED_A/BL_PWM":
        return "Power & control"
    if n.startswith("ANT_"):
        return "Antenna"
    if n in {"RSVD", "RVSD"}:
        return "Reserved"
    if n == "NC":
        return "Not connected"
    if n.startswith("USB") or n in {"USB_CC1", "USB_CC2"}:
        return "USB"
    if n.startswith("ETH"):
        return "Ethernet"
    if n.startswith("PCIE"):
        return "PCIe"
    if n.startswith("I2C"):
        return "I²C"
    if n.startswith("I3C"):
        return "I³C"
    if n.startswith("UART") or n.startswith("DBG_"):
        return "UART"
    if n.startswith("SPI"):
        return "SPI"
    if n.startswith("I2S"):
        return "I²S"
    if n.startswith("JTAG") or "SWD" in n:
        return "SWD / JTAG"
    if n.startswith("CAN"):
        return "CAN bus"
    if n.startswith("SD_"):
        return "SDIO / SD card"
    if n.startswith("DSI"):
        return "MIPI DSI display"
    if n.startswith("CSI"):
        return "MIPI CSI camera"
    if n.startswith("CAM_"):
        return "Parallel camera"
    if n.startswith("LCD_"):
        return "LCD parallel display"
    if n.startswith("PDM_"):
        return "PDM microphone"
    if n.startswith("ANA_S"):
        return "Analog inputs"
    if n.startswith("DAC"):
        return "Analog outputs"
    if n.startswith("ENC"):
        return "Quadrature encoder"
    if n.startswith("PWM"):
        return "PWM"
    if n.startswith("IO"):
        return "GPIO"
    raise ValueError(f"Unclassified pin name: {name!r}")


# Logical key for matching the same pin across form factors despite
# Altium naming inconsistencies.
NAME_ALIASES = {
    "VDD": "VDD",
    "VDD_5V_IN": "VDD",
    "USB0_30_VBUS": "USB0_VBUS",
    "USB0_VBUS": "USB0_VBUS",
    "USB2_20_VBUS": "USB2_VBUS",
    "USB2_VBUS": "USB2_VBUS",
    "USB2_20_P": "USB2_DP",
    "USB2_P": "USB2_DP",
    "USB2_20_N": "USB2_DM",
    "USB2_N": "USB2_DM",
    "USB2_20_ID": "USB2_ID",
    "USB2_ID": "USB2_ID",
    "SD_VDD": "SD_VDD",
    "SD_VDD_OUT": "SD_VDD",
    "ANT_2.4GHz": "ANT_2.4GHZ",
    "ANT_2.4GHZ": "ANT_2.4GHZ",
    "ANT_5GHz": "ANT_5GHZ",
    "ANT_5GHZ": "ANT_5GHZ",
    "ANT_6GHz": "ANT_6GHZ",
    "ANT_6GHZ": "ANT_6GHZ",
    "RVSD": "RSVD",
}


def alias(name: str) -> str:
    return NAME_ALIASES.get(name, name)


def render_class(cls: str, e1m: dict, e1mx: dict) -> str:
    """Render one class as a markdown table.
    Rows: pin alias -> {form_factor: [coords]}.
    """
    grouped: dict[str, dict[str, list[str]]] = defaultdict(
        lambda: {"e1m": [], "e1mx": [], "name_e1m": "", "name_e1mx": ""})
    for coord, name in e1m.items():
        if classify(name) != cls:
            continue
        a = alias(name)
        grouped[a]["e1m"].append(coord)
        grouped[a]["name_e1m"] = name
    for coord, name in e1mx.items():
        if classify(name) != cls:
            continue
        a = alias(name)
        grouped[a]["e1mx"].append(coord)
        grouped[a]["name_e1mx"] = name

    if not grouped:
        return ""

    out: list[str] = []
    out.append("| E1M-X coord(s) | E1M coord(s) | Pin name |")
    out.append("| --- | --- | --- |")

    def name_key(a: str):
        """Natural sort: split into (text, number, text...) tuples so
        IO9 < IO10 < IO11 < IO35."""
        parts = re.split(r"(\d+)", a)
        return tuple(int(p) if p.isdigit() else p for p in parts)

    def coord_key(c: str):
        m = re.match(r"^([A-Z]+)(\d+)$", c)
        if not m:
            return (0, c, 0)
        return (len(m.group(1)), m.group(1), int(m.group(2)))

    for a in sorted(grouped.keys(), key=name_key):
        info = grouped[a]
        e1mx_coords = ", ".join(
            sorted(set(info["e1mx"]), key=coord_key)) or "_(E1M only)_"
        e1m_coords = ", ".join(
            sorted(set(info["e1m"]), key=coord_key)) or "_(E1M-X only)_"
        # Pin name: combine if E1M and E1M-X differ.
        n1, n2 = info["name_e1m"], info["name_e1mx"]
        if n1 and n2 and n1 != n2:
            name_cell = f"`{n2}` (E1M-X) / `{n1}` (E1M)"
        else:
            name_cell = "`" + (n2 or n1) + "`"
        # Cell length safety: GND can be huge.
        if len(e1mx_coords) > 1000 or len(e1m_coords) > 1000:
            # For very large lists (mainly GND), reference the JSON.
            e1m_count = len(set(info["e1m"]))
            e1mx_count = len(set(info["e1mx"]))
            e1mx_coords = f"{e1mx_count} pads (see `pinout/x-v1.json`)"
            e1m_coords = f"{e1m_count} pads (see `pinout/v1.json`)"
        out.append(f"| {e1mx_coords} | {e1m_coords} | {name_cell} |")
    return "\n".join(out)


def main() -> int:
    e1m = parse(TSV_E1M)
    e1mx = parse(TSV_E1MX)
    parts: list[str] = []
    parts.append("<!-- Generated by source/_render_tables.py. Do not edit. -->\n")
    for cls, num in CLASS_ORDER:
        body = render_class(cls, e1m, e1mx)
        if not body:
            continue
        parts.append(f"#### {num} {cls}\n")
        parts.append(body + "\n")
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
