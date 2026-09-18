import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PrincipalLibraryStaticTests(unittest.TestCase):
    def test_external_page_has_required_controls_and_script(self):
        html = (ROOT / "principal/library/external/index.html").read_text()
        for token in [
            'id="research-search"',
            'id="topic-filter"',
            'id="type-filter"',
            'id="year-filter"',
            'id="research-results"',
            'src="/principal/library/external/library.js"'
        ]:
            self.assertIn(token, html)

    def test_external_script_loads_canonical_json(self):
        js = (ROOT / "principal/library/external/library.js").read_text()
        self.assertIn('/data/research/external-research.json', js)
        self.assertIn('/data/research/topics.json', js)
        self.assertIn('principal_relevance', js)
        self.assertIn('source_url', js)

    def test_no_external_pdf_binary_paths_are_hardcoded(self):
        html = (ROOT / "principal/library/external/index.html").read_text()
        js = (ROOT / "principal/library/external/library.js").read_text()
        self.assertNotIn('.pdf"', html.lower())
        self.assertNotIn('.pdf"', js.lower())

    def test_library_landing_separates_valo_and_external(self):
        html = (ROOT / "principal/library/index.html").read_text()
        self.assertIn('VALO Research', html)
        self.assertIn('External Research', html)
        self.assertIn('href="/publications/"', html)
        self.assertIn('href="/principal/library/external/"', html)

    def test_principal_home_links_to_library(self):
        html = (ROOT / "principal/index.html").read_text()
        self.assertIn('href="/principal/library/"', html)


if __name__ == "__main__":
    unittest.main()
