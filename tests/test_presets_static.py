import unittest
from pathlib import Path


HTML = Path(__file__).resolve().parents[1].joinpath("index.html").read_text(encoding="utf-8")


class PresetButtonTests(unittest.TestCase):
    def test_index_exposes_three_preset_buttons(self):
        self.assertIn('id="presetBtns"', HTML)
        self.assertEqual(HTML.count('class="presetBtn"'), 3)
        self.assertIn('const PRESETS = [', HTML)
        self.assertIn('loadPreset(index)', HTML)

    def test_preset_buttons_are_wired_to_load_presets(self):
        self.assertIn('document.querySelectorAll(".presetBtn")', HTML)
        self.assertIn('Number(btn.dataset.preset)', HTML)
        self.assertTrue(
            '.onclick=()=>loadPreset' in HTML or 'btn.onclick=()=>loadPreset' in HTML
        )


if __name__ == "__main__":
    unittest.main()
