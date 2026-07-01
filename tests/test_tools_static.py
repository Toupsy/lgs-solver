import unittest
from pathlib import Path


HTML = Path(__file__).resolve().parents[1].joinpath("index.html").read_text(encoding="utf-8")


class ModeNavigationTests(unittest.TestCase):
    def test_topnav_has_three_modes(self):
        self.assertIn('data-mode="schnitt"', HTML)
        self.assertIn('data-mode="lage"', HTML)
        self.assertIn('data-mode="darst"', HTML)

    def test_mode_panels_exist(self):
        self.assertIn('id="mode-schnitt"', HTML)
        self.assertIn('id="mode-lage"', HTML)
        self.assertIn('id="mode-darst"', HTML)


class LagebeziehungTests(unittest.TestCase):
    def test_both_sub_modes_present(self):
        self.assertIn('id="lbMode"', HTML)
        self.assertIn('value="ee"', HTML)
        self.assertIn('value="eg"', HTML)

    def test_solver_wired(self):
        self.assertIn('function lageSolve()', HTML)
        self.assertIn('Schnittgerade', HTML)
        self.assertIn('echt parallel', HTML)
        self.assertIn('identisch', HTML)


class DarstellungsformenTests(unittest.TestCase):
    def test_form_selector_has_three_forms(self):
        self.assertIn('id="dfForm"', HTML)
        self.assertIn('value="param"', HTML)
        self.assertIn('value="normal"', HTML)
        self.assertIn('value="koord"', HTML)

    def test_converter_wired(self):
        self.assertIn('function darstSolve()', HTML)
        self.assertIn('paramFromNormal', HTML)
        self.assertIn('Vcross', HTML)
        self.assertIn('alle drei Darstellungsformen', HTML)


if __name__ == "__main__":
    unittest.main()
