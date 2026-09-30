"""Run: python -m unittest discover tests  (stdlib only)."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "source"))
import _check_prose_counts as chk  # noqa: E402

TEXT = (ROOT / "STANDARD.md").read_text(encoding="utf-8")


class ProseCounts(unittest.TestCase):
    def test_committed_standard_is_clean(self):
        self.assertEqual(chk.check(TEXT), [])

    def test_gpio_drift_detected(self):
        bad = TEXT.replace("| GPIO (default-function) | 23 | 34 |", "| GPIO (default-function) | 25 | 34 |")
        self.assertNotEqual(bad, TEXT)
        self.assertTrue(any("GPIO" in e and "E1M]" in e for e in chk.check(bad)))

    def test_gnd_drift_detected(self):
        bad = TEXT.replace("49 pads", "46 pads")
        self.assertNotEqual(bad, TEXT)
        self.assertTrue(any("GND" in e for e in chk.check(bad)))


if __name__ == "__main__":
    unittest.main()
