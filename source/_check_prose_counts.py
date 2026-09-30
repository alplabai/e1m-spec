#!/usr/bin/env python3
"""Assert STANDARD.md §7.2 / §7.3.1 prose counts match pinout/*.json.

Stdlib only. Exit 1 on any mismatch. Run from anywhere.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# §7.2 row label -> count from JSON. `n(x)` = pads whose default is x.
# Each interface is counted via one signal that appears once per instance.
PARCAM = "Parallel camera (8 / 16-bit)"
ROWS = {
    "Ethernet 1 GbE": lambda n: n("ETH_DA_P"),
    "USB 2.0": lambda n: n("USB_DP") - n("USB_RX_P"),  # USB3 ports also carry D+/D-
    "USB 3.x": lambda n: n("USB_RX_P"),
    "UART": lambda n: n("UART_TX"),
    "Debug UART (console)": lambda n: n("DBG_TX"),
    "SPI": lambda n: n("SPI_SCK"),
    "I²C": lambda n: n("I2C_SCL"),
    "I³C": lambda n: n("I3C_SCL"),
    "I²S": lambda n: n("I2S_WS"),
    "SDIO / SD card (4-bit)": lambda n: n("SD_CLK"),
    "CAN-BUS": lambda n: n("CAN_H"),
    "JTAG / SWD": lambda n: n("JTAG_TCK"),
    "GPIO (default-function)": lambda n: n("GPIO"),
    "PDM microphone": lambda n: n("PDM_CLK"),
    "Audio master clock": lambda n: n("AUDIO_CLK"),
    "RTC clock output": lambda n: n("RTC_CLKOUT"),
    "Boot-strap pins": lambda n: n("BOOT"),
    "Analogue input (ADC)": lambda n: n("ADC"),
    "Analogue output (DAC)": lambda n: n("DAC"),
    "Quadrature encoder": lambda n: n("ENC_X"),
    "PWM": lambda n: n("PWM"),
    "MIPI CSI-2 4-lane": lambda n: n("MIPI_CSI2_CLK_P"),
    "MIPI DSI 4-lane": lambda n: n("MIPI_DSI_CLK_P"),
    "Parallel LCD (24-bit RGB)": lambda n: 1 if n("LCD_HSYNC") else 0,
    "PCIe 4-lane": lambda n: n("PCIE_CLK_P"),
    "Reserved (RSVD)": lambda n: n("RSVD"),
    "Not connected (NC)": lambda n: n("NC"),
}


def counter(json_name):
    pads = json.loads((ROOT / "pinout" / json_name).read_text(encoding="utf-8"))["pads"]
    c = Counter(p["default"] for p in pads)
    return lambda k: c[k], c


def section(text, heading):
    m = re.search(rf"^#+ {re.escape(heading)}\b.*?(?=^#+ )", text, re.S | re.M)
    if not m:
        sys.exit(f"STANDARD.md: section {heading} not found")
    return m.group(0)


def check(text):
    errs = []
    n_e1m, c_e1m = counter("v1.json")
    n_x, c_x = counter("x-v1.json")
    rows = {}
    for line in section(text, "7.2").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 3 and cells[0] in ROWS or cells[0] == PARCAM:
            rows[cells[0]] = cells[1:]
    for label, fn in ROWS.items():
        if label not in rows:
            errs.append(f"§7.2: row '{label}' missing")
            continue
        for form, cell, n in (("E1M", rows[label][0], n_e1m), ("E1M-X", rows[label][1], n_x)):
            m = re.match(r"\d+", cell)
            want = fn(n)
            got = int(m.group()) if m else 0  # "—" means none
            if got != want:
                errs.append(f"§7.2 {label} [{form}]: prose {got}, JSON {want}")
    # Parallel camera: "1 (8 bit)" / "1 (16 bit)" = data-line width.
    cell = rows.get(PARCAM)
    if cell:
        for form, c, cnt in (("E1M", cell[0], c_e1m), ("E1M-X", cell[1], c_x)):
            bits = sum(1 for k in cnt if re.fullmatch(r"PARCAM_D\d+", k))
            m = re.search(r"\((\d+) bit\)", c)
            if not m or int(m.group(1)) != bits:
                errs.append(f"§7.2 Parallel camera [{form}]: prose '{c}', JSON {bits} data lines")
    else:
        errs.append("§7.2: row 'Parallel camera (8 / 16-bit)' missing")
    # §7.3.1 GND "N pads" cell: E1M-X column first, E1M second.
    m = re.search(r"\|\s*(\d+) pads[^|]*\|\s*(\d+) pads[^|]*\|\s*`GND`", section(text, "7.3.1"))
    if not m:
        errs.append("§7.3.1: GND row not found")
    else:
        for form, got, cnt in (("E1M-X", int(m.group(1)), c_x["GND"]), ("E1M", int(m.group(2)), c_e1m["GND"])):
            if got != cnt:
                errs.append(f"§7.3.1 GND [{form}]: prose {got}, JSON {cnt}")
    return errs


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    errs = check((ROOT / "STANDARD.md").read_text(encoding="utf-8"))
    for e in errs:
        print("MISMATCH:", e)
    print("prose counts OK" if not errs else f"{len(errs)} mismatch(es)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
