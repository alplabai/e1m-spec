"""Build pinout/v1.json (E1M, 35x35) and pinout/x-v1.json (E1M-X, 45x65)
from the Altium pin-list exports in source/altium-e1m.tsv and
source/altium-e1m-x.tsv.

Altium is now the canonical source for pin enumeration and pin names.
The Word document at source/E1M-draft.docx is retained for prose
descriptions only.

Rules (locked-in by project owner, 2026-05-09):
- Standard fixes the PRIMARY function (the "Pin Name" from Altium).
- Secondary function is GPIO for any digital pad.
- Tertiary+ alts are silicon-specific and NOT part of E1M conformance.
- Slash-combo pin names ("JTAG_TCK/SWDCLK") put the second name in `alt`
  ahead of GPIO.
- Power, GND, antenna, reserved, NC, and backlight LED anode/cathode pads
  do NOT get a GPIO secondary.

Anomaly handling:
- Known typos (e.g. RVSD -> RSVD) are auto-corrected; the report lists
  the corrected pads.
- Case differences in antenna names (ANT_2.4GHz vs ANT_2.4GHZ) and
  naming differences between form factors (USB0_VBUS vs USB0_30_VBUS,
  VDD vs VDD_5V_IN, SD_VDD vs SD_VDD_OUT) are mapped to a single
  canonical SignalKind so JSON schema validation passes; the original
  Altium silkscreen is preserved for traceability.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parent.parent
TSV_E1M = ROOT / "source" / "altium-e1m.tsv"
TSV_E1MX = ROOT / "source" / "altium-e1m-x.tsv"
OUT_E1M = ROOT / "pinout" / "v1.json"
OUT_E1MX = ROOT / "pinout" / "x-v1.json"

LOOM_VERSION = 1
SPEC_VERSION = "1.0"

COORD_RE = re.compile(r"^[A-Z]+\d+$")


def parse_tsv(path: Path) -> list[tuple[str, str]]:
    """Read an Altium pin-list TSV with one (coord, name) pair per line.
    Tolerates either tab or multi-space as separator."""
    rows: list[tuple[str, str]] = []
    with path.open(encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\r\n")
            if not line.strip():
                continue
            parts = re.split(r"\s+", line.strip(), maxsplit=1)
            if len(parts) != 2:
                raise ValueError(f"{path.name}: unparseable line: {raw!r}")
            coord, name = parts[0].strip(), parts[1].strip()
            if not COORD_RE.match(coord):
                raise ValueError(f"{path.name}: bad coord {coord!r}")
            rows.append((coord, name))
    return rows


# --- Pin-name normaliser + signal mapping -------------------------------------

# Auto-correct typos and case noise on input. The corrected name is what
# the loader works with; the ORIGINAL pre-correction text is preserved
# in the JSON `silkscreen` field.
TYPO_FIXES = {
    "RVSD": "RSVD",
}

# Case-only canonicalisation — both forms in the input map to one form
# in the SignalKind enum, but `silkscreen` keeps the input form.
CASE_NORMS = {
    "ANT_2.4GHz": "ANT_2.4GHZ",
    "ANT_5GHz": "ANT_5GHZ",
    "ANT_6GHz": "ANT_6GHZ",
}


# Pin name -> (SignalKind, PeripheralInstance | None, alt SignalKind | None)
EXPLICIT: dict[str, tuple[str, str | None, str | None]] = {
    # Power / control
    "GND": ("GND", None, None),
    "VDD": ("POWER_5V0", None, None),
    "VDD_5V_IN": ("POWER_5V0", None, None),
    "VIO_OUT": ("POWER_VIO_OUT", None, None),
    "+S_CAP": ("POWER_SUPER_CAP", None, None),
    "PORn": ("RESET", None, None),
    "MODULE_EN": ("MODULE_EN", None, None),
    "MODULE_STBY": ("MODULE_STBY", None, None),
    "AUDIO_CLK": ("AUDIO_CLK", None, None),
    "RTC_CLKOUT": ("RTC_CLKOUT", None, None),
    "BL_LED_A": ("BL_LED_A", None, None),
    "BL_LED_K": ("BL_LED_K", None, None),
    "NC": ("NC", None, None),
    "RSVD": ("RSVD", None, None),
    # Antenna (case-canonicalised before lookup)
    "ANT_2.4GHZ": ("ANT_2_4GHZ", None, None),
    "ANT_5GHZ": ("ANT_5GHZ", None, None),
    "ANT_6GHZ": ("ANT_6GHZ", None, None),
    # USB top-level
    "USB_CC1": ("USB_CC1", None, None),
    "USB_CC2": ("USB_CC2", None, None),
    # USB2 alternate (E1M shorter naming) — same SignalKinds as E1M-X
    "USB2_P": ("USB_DP", "USB2", None),
    "USB2_N": ("USB_DM", "USB2", None),
    "USB2_ID": ("USB_ID", "USB2", None),
    "USB2_VBUS": ("USB_VBUS", "USB2", None),
    # USB0 alternate VBUS naming on E1M
    "USB0_VBUS": ("USB_VBUS", "USB0", None),
    # I3C
    "I3C_SCL": ("I3C_SCL", "I3C0", None),
    "I3C_SDA": ("I3C_SDA", "I3C0", None),
    # Debug console UART (E1M at AD3/AE3, E1M-X at AC62/AD62; dedicated,
    # not a numbered UART instance)
    "DBG_TX": ("DBG_TX", None, None),
    "DBG_RX": ("DBG_RX", None, None),
    # JTAG / SWD
    "JTAG_nRST": ("JTAG_NRST", "JTAG0", None),
    "JTAG_TCK/SWDCLK": ("JTAG_TCK", "JTAG0", "SWD_CLK"),
    "JTAG_TDI": ("JTAG_TDI", "JTAG0", None),
    "JTAG_TDO": ("JTAG_TDO", "JTAG0", None),
    "JTAG_TMS/SWDIO": ("JTAG_TMS", "JTAG0", "SWD_IO"),
    # CAN
    "CAN_STBY": ("CAN_STBY", None, None),
    "CAN0H/CAN0_TX": ("CAN_H", "CAN0", "CAN_TX"),
    "CAN0L/CAN0_RX": ("CAN_L", "CAN0", "CAN_RX"),
    "CAN1H/CAN1_TX": ("CAN_H", "CAN1", "CAN_TX"),
    "CAN1L/CAN1_RX": ("CAN_L", "CAN1", "CAN_RX"),
    # SDIO
    "SD_CLK": ("SD_CLK", "SDIO0", None),
    "SD_CMD": ("SD_CMD", "SDIO0", None),
    "SD_D0": ("SD_D0", "SDIO0", None),
    "SD_D1": ("SD_D1", "SDIO0", None),
    "SD_D2": ("SD_D2", "SDIO0", None),
    "SD_D3": ("SD_D3", "SDIO0", None),
    "SD_DET": ("SD_DET", "SDIO0", None),
    "SD_RST": ("SD_RST", "SDIO0", None),
    "SD_VDD": ("POWER_SD_VDD_OUT", "SDIO0", None),
    "SD_VDD_OUT": ("POWER_SD_VDD_OUT", "SDIO0", None),
    # Parallel camera sync/clock
    "CAM_HSYNC": ("PARCAM_HSYNC", "PARCAM0", None),
    "CAM_VSYNC": ("PARCAM_VSYNC", "PARCAM0", None),
    "CAM_PCLK": ("PARCAM_PCLK", "PARCAM0", None),
    "CAM_XVCLK": ("PARCAM_XVCLK", "PARCAM0", None),
    # LCD parallel sync
    "LCD_HSYNC": ("LCD_HSYNC", "LCD0", None),
    "LCD_VSYNC": ("LCD_VSYNC", "LCD0", None),
}


def _patterns() -> list[tuple[re.Pattern, Callable[[re.Match], tuple[str, str | None, str | None]]]]:
    return [
        (re.compile(r"^BOOT(\d+)$"),
         lambda m: ("BOOT", f"BOOT{m.group(1)}", None)),
        (re.compile(r"^\+V_CAM(\d+)$"),
         lambda m: ("POWER_CAM_LDO_OUT", f"CAM{m.group(1)}", None)),
        (re.compile(r"^CAM_VFB(\d+)$"),
         lambda m: ("POWER_CAM_LDO_FB", f"CAM{m.group(1)}", None)),
        # USB SuperSpeed (USB3.x) — E1M-X explicit naming
        (re.compile(r"^USB(\d+)_30_D_N$"),
         lambda m: ("USB_DM", f"USB{m.group(1)}", None)),
        (re.compile(r"^USB(\d+)_30_D_P$"),
         lambda m: ("USB_DP", f"USB{m.group(1)}", None)),
        (re.compile(r"^USB(\d+)_30_RX0_N$"),
         lambda m: ("USB_RX_N", f"USB{m.group(1)}", None)),
        (re.compile(r"^USB(\d+)_30_RX0_P$"),
         lambda m: ("USB_RX_P", f"USB{m.group(1)}", None)),
        (re.compile(r"^USB(\d+)_30_TX0_N$"),
         lambda m: ("USB_TX_N", f"USB{m.group(1)}", None)),
        (re.compile(r"^USB(\d+)_30_TX0_P$"),
         lambda m: ("USB_TX_P", f"USB{m.group(1)}", None)),
        (re.compile(r"^USB(\d+)_30_ID$"),
         lambda m: ("USB_ID", f"USB{m.group(1)}", None)),
        (re.compile(r"^USB(\d+)_30_VBUS$"),
         lambda m: ("USB_VBUS", f"USB{m.group(1)}", None)),
        # USB 2.0 — E1M-X "_20_" naming (E1M short form is in EXPLICIT)
        (re.compile(r"^USB(\d+)_20_N$"),
         lambda m: ("USB_DM", f"USB{m.group(1)}", None)),
        (re.compile(r"^USB(\d+)_20_P$"),
         lambda m: ("USB_DP", f"USB{m.group(1)}", None)),
        (re.compile(r"^USB(\d+)_20_ID$"),
         lambda m: ("USB_ID", f"USB{m.group(1)}", None)),
        (re.compile(r"^USB(\d+)_20_VBUS$"),
         lambda m: ("USB_VBUS", f"USB{m.group(1)}", None)),
        # Ethernet
        (re.compile(r"^ETH(\d+)_DA_N$"),
         lambda m: ("ETH_DA_N", f"ETH{m.group(1)}", None)),
        (re.compile(r"^ETH(\d+)_DA_P$"),
         lambda m: ("ETH_DA_P", f"ETH{m.group(1)}", None)),
        (re.compile(r"^ETH(\d+)_DB_N$"),
         lambda m: ("ETH_DB_N", f"ETH{m.group(1)}", None)),
        (re.compile(r"^ETH(\d+)_DB_P$"),
         lambda m: ("ETH_DB_P", f"ETH{m.group(1)}", None)),
        (re.compile(r"^ETH(\d+)_DC_N$"),
         lambda m: ("ETH_DC_N", f"ETH{m.group(1)}", None)),
        (re.compile(r"^ETH(\d+)_DC_P$"),
         lambda m: ("ETH_DC_P", f"ETH{m.group(1)}", None)),
        (re.compile(r"^ETH(\d+)_DD_N$"),
         lambda m: ("ETH_DD_N", f"ETH{m.group(1)}", None)),
        (re.compile(r"^ETH(\d+)_DD_P$"),
         lambda m: ("ETH_DD_P", f"ETH{m.group(1)}", None)),
        (re.compile(r"^ETH(\d+)_LED0$"),
         lambda m: ("ETH_LED0", f"ETH{m.group(1)}", None)),
        (re.compile(r"^ETH(\d+)_LED1$"),
         lambda m: ("ETH_LED1", f"ETH{m.group(1)}", None)),
        # PCIe per-lane
        (re.compile(r"^PCIE(\d+)_CLK_N$"),
         lambda m: ("PCIE_CLK_N", f"PCIE{m.group(1)}", None)),
        (re.compile(r"^PCIE(\d+)_CLK_P$"),
         lambda m: ("PCIE_CLK_P", f"PCIE{m.group(1)}", None)),
        (re.compile(r"^PCIE(\d+)_RX(\d+)_N$"),
         lambda m: (f"PCIE_RX{m.group(2)}_N", f"PCIE{m.group(1)}", None)),
        (re.compile(r"^PCIE(\d+)_RX(\d+)_P$"),
         lambda m: (f"PCIE_RX{m.group(2)}_P", f"PCIE{m.group(1)}", None)),
        (re.compile(r"^PCIE(\d+)_TX(\d+)_N$"),
         lambda m: (f"PCIE_TX{m.group(2)}_N", f"PCIE{m.group(1)}", None)),
        (re.compile(r"^PCIE(\d+)_TX(\d+)_P$"),
         lambda m: (f"PCIE_TX{m.group(2)}_P", f"PCIE{m.group(1)}", None)),
        # I2C
        (re.compile(r"^I2C(\d+)_SCL$"),
         lambda m: ("I2C_SCL", f"I2C{m.group(1)}", None)),
        (re.compile(r"^I2C(\d+)_SDA$"),
         lambda m: ("I2C_SDA", f"I2C{m.group(1)}", None)),
        # UART
        (re.compile(r"^UART(\d+)_TX$"),
         lambda m: ("UART_TX", f"UART{m.group(1)}", None)),
        (re.compile(r"^UART(\d+)_RX$"),
         lambda m: ("UART_RX", f"UART{m.group(1)}", None)),
        # SPI
        (re.compile(r"^SPI(\d+)_CS0$"),
         lambda m: ("SPI_CS0", f"SPI{m.group(1)}", None)),
        (re.compile(r"^SPI(\d+)_CS1$"),
         lambda m: ("SPI_CS1", f"SPI{m.group(1)}", None)),
        (re.compile(r"^SPI(\d+)_MOSI$"),
         lambda m: ("SPI_MOSI", f"SPI{m.group(1)}", None)),
        (re.compile(r"^SPI(\d+)_MISO$"),
         lambda m: ("SPI_MISO", f"SPI{m.group(1)}", None)),
        (re.compile(r"^SPI(\d+)_SCLK$"),
         lambda m: ("SPI_SCK", f"SPI{m.group(1)}", None)),
        # I2S
        (re.compile(r"^I2S(\d+)_SCLK$"),
         lambda m: ("I2S_SCLK", f"I2S{m.group(1)}", None)),
        (re.compile(r"^I2S(\d+)_SDI$"),
         lambda m: ("I2S_SDI", f"I2S{m.group(1)}", None)),
        (re.compile(r"^I2S(\d+)_SDO$"),
         lambda m: ("I2S_SDO", f"I2S{m.group(1)}", None)),
        (re.compile(r"^I2S(\d+)_WS$"),
         lambda m: ("I2S_WS", f"I2S{m.group(1)}", None)),
        # MIPI DSI per-lane
        (re.compile(r"^DSI(\d+)_(\d+)_N$"),
         lambda m: (f"MIPI_DSI_DATA{m.group(2)}_N", f"DSI{m.group(1)}", None)),
        (re.compile(r"^DSI(\d+)_(\d+)_P$"),
         lambda m: (f"MIPI_DSI_DATA{m.group(2)}_P", f"DSI{m.group(1)}", None)),
        (re.compile(r"^DSI(\d+)_C_N$"),
         lambda m: ("MIPI_DSI_CLK_N", f"DSI{m.group(1)}", None)),
        (re.compile(r"^DSI(\d+)_C_P$"),
         lambda m: ("MIPI_DSI_CLK_P", f"DSI{m.group(1)}", None)),
        # MIPI CSI-2 per-lane
        (re.compile(r"^CSI(\d+)_(\d+)_N$"),
         lambda m: (f"MIPI_CSI2_DATA{m.group(2)}_N", f"CSI{m.group(1)}", None)),
        (re.compile(r"^CSI(\d+)_(\d+)_P$"),
         lambda m: (f"MIPI_CSI2_DATA{m.group(2)}_P", f"CSI{m.group(1)}", None)),
        (re.compile(r"^CSI(\d+)_C_N$"),
         lambda m: ("MIPI_CSI2_CLK_N", f"CSI{m.group(1)}", None)),
        (re.compile(r"^CSI(\d+)_C_P$"),
         lambda m: ("MIPI_CSI2_CLK_P", f"CSI{m.group(1)}", None)),
        # Parallel camera data
        (re.compile(r"^CAM_D(\d+)$"),
         lambda m: (f"PARCAM_D{m.group(1)}", "PARCAM0", None)),
        # PDM
        (re.compile(r"^PDM_C(\d+)$"),
         lambda m: ("PDM_CLK", f"PDM{m.group(1)}", None)),
        (re.compile(r"^PDM_D(\d+)$"),
         lambda m: ("PDM_DATA", f"PDM{m.group(1)}", None)),
        # Analog
        (re.compile(r"^ANA_S(\d+)$"),
         lambda m: ("ADC", f"ADC{m.group(1)}", None)),
        (re.compile(r"^DAC(\d+)$"),
         lambda m: ("DAC", f"DAC{m.group(1)}", None)),
        # Quadrature encoder
        (re.compile(r"^ENC(\d+)_X$"),
         lambda m: ("ENC_X", f"ENC{m.group(1)}", None)),
        (re.compile(r"^ENC(\d+)_Y$"),
         lambda m: ("ENC_Y", f"ENC{m.group(1)}", None)),
        # PWM
        (re.compile(r"^PWM(\d+)$"),
         lambda m: ("PWM", f"PWM{m.group(1)}", None)),
        # GPIO
        (re.compile(r"^IO(\d+)$"),
         lambda m: ("GPIO", None, None)),
        # LCD parallel data
        (re.compile(r"^LCD_B(\d+)$"),
         lambda m: (f"LCD_B{m.group(1)}", "LCD0", None)),
    ]


PATTERNS = _patterns()


# Pads that do NOT get a GPIO secondary.
NOT_GPIO_CAPABLE = {
    "GND", "NC",
    "POWER_5V0", "POWER_3V3", "POWER_1V8", "POWER_VBAT",
    "POWER_VIO_OUT", "POWER_SUPER_CAP",
    "POWER_CAM_LDO_OUT", "POWER_CAM_LDO_FB",
    "POWER_SD_VDD_OUT",
    "ANT_2_4GHZ", "ANT_5GHZ", "ANT_6GHZ",
    "RSVD",
    "BL_LED_A", "BL_LED_K",
}


def normalise(name: str, anomalies: list[str]) -> str:
    """Apply typo fixes and case normalisation. Records every change."""
    if name in TYPO_FIXES:
        anomalies.append(f"typo: {name!r} -> {TYPO_FIXES[name]!r}")
        return TYPO_FIXES[name]
    if name in CASE_NORMS:
        anomalies.append(f"case: {name!r} -> {CASE_NORMS[name]!r}")
        return CASE_NORMS[name]
    return name


def resolve(name: str) -> tuple[str, str | None, str | None]:
    if name in EXPLICIT:
        return EXPLICIT[name]
    for rx, fn in PATTERNS:
        m = rx.match(name)
        if m:
            return fn(m)
    raise ValueError(f"Unmapped pin name: {name!r}")


def build_pad(coord: str, original_name: str, signal: str,
              instance: str | None, alt_signal: str | None) -> dict:
    pad: dict = {"id": coord, "silkscreen": original_name, "default": signal}
    if instance:
        pad["instance"] = instance
    alts: list[dict] = []
    if alt_signal:
        entry = {"signal": alt_signal}
        if instance:
            entry["instance"] = instance
        alts.append(entry)
    if signal not in NOT_GPIO_CAPABLE and signal != "GPIO":
        alts.append({"signal": "GPIO"})
    pad["alt"] = alts
    return pad


def build_form_factor(rows: list[tuple[str, str]]) -> tuple[list[dict], list[str]]:
    """Return (pads, anomaly-report-lines)."""
    pads: list[dict] = []
    anomalies: list[str] = []
    seen_coords: set[str] = set()
    for coord, original_name in rows:
        if coord in seen_coords:
            anomalies.append(f"duplicate coord {coord!r}")
            continue
        seen_coords.add(coord)
        ann_before = len(anomalies)
        normalised = normalise(original_name, anomalies)
        try:
            signal, instance, alt_signal = resolve(normalised)
        except ValueError as exc:
            anomalies.append(f"{coord}: {exc}")
            continue
        # Tag anomaly with the coord for traceability.
        if len(anomalies) > ann_before:
            anomalies[-1] = f"{coord}: " + anomalies[-1]
        pads.append(build_pad(coord, original_name, signal, instance, alt_signal))
    return pads, anomalies


def loom_doc(form_id: str, footprint_class: str, w_mm: int, h_mm: int,
             pads: list[dict]) -> dict:
    return {
        "loom_format_version": LOOM_VERSION,
        "id": form_id,
        "version": SPEC_VERSION,
        "footprint_class": footprint_class,
        "outline_mm": {"w": w_mm, "h": h_mm},
        "pads": pads,
    }


def sort_pads(pads: list[dict]) -> list[dict]:
    def key(pad):
        m = re.match(r"^([A-Z]+)(\d+)$", pad["id"])
        letters, num = (m.group(1), int(m.group(2))) if m else (pad["id"], 0)
        return (len(letters), letters, num)
    return sorted(pads, key=key)


def main() -> int:
    e1m_rows = parse_tsv(TSV_E1M)
    e1mx_rows = parse_tsv(TSV_E1MX)

    e1m_pads, e1m_anom = build_form_factor(e1m_rows)
    e1mx_pads, e1mx_anom = build_form_factor(e1mx_rows)

    e1m_pads = sort_pads(e1m_pads)
    e1mx_pads = sort_pads(e1mx_pads)

    OUT_E1M.parent.mkdir(parents=True, exist_ok=True)
    OUT_E1M.write_text(
        json.dumps(loom_doc("E1M", "FC_35x35", 35, 35, e1m_pads), indent=2),
        encoding="utf-8",
    )
    OUT_E1MX.write_text(
        json.dumps(loom_doc("E1M-X", "FC_45x65", 45, 65, e1mx_pads), indent=2),
        encoding="utf-8",
    )

    print(f"E1M  pads: {len(e1m_pads)} -> {OUT_E1M}")
    print(f"E1M-X pads: {len(e1mx_pads)} -> {OUT_E1MX}")
    if e1m_anom:
        print(f"\nE1M anomalies ({len(e1m_anom)}):")
        for a in e1m_anom:
            print(f"  - {a}")
    if e1mx_anom:
        print(f"\nE1M-X anomalies ({len(e1mx_anom)}):")
        for a in e1mx_anom:
            print(f"  - {a}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
