from html.parser import HTMLParser
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class AnchorParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.hrefs.extend(value for key, value in attrs if key == "href")


class FractalPamOverviewTests(unittest.TestCase):
    def test_overview_links_to_gasket_and_both_carpet_runs(self):
        overview = ROOT / "simulations" / "fractal-pam.html"
        self.assertTrue(overview.is_file(), "missing standalone fractal PAM overview")
        parser = AnchorParser()
        parser.feed(overview.read_text())
        expected = {
            "./pam.html",
            "./carpet-pam-lambda1-startupframes.html",
            "./carpet-pam-low-noise-startupframes.html",
        }
        self.assertTrue(expected.issubset(set(parser.hrefs)))
        for href in expected:
            self.assertTrue((overview.parent / href).is_file(), f"broken overview link: {href}")

    def test_research_section_has_one_link_to_the_overview(self):
        research = (ROOT / "_pages" / "reasearch.md").read_text()
        include = (ROOT / "_includes" / "pam-simulation.html").read_text()
        self.assertIn("{% include pam-simulation.html %}", research)
        self.assertIn("/simulations/fractal-pam.html", include)
        self.assertNotIn("/simulations/pam.html", include)
        self.assertNotIn("<iframe", research.lower())
        self.assertNotIn("<iframe", include.lower())
        self.assertNotIn("/simulations/pam.html", research)


if __name__ == "__main__":
    unittest.main()
