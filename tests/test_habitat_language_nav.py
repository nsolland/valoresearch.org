from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).parents[1] / "habitat"
NO = ROOT / "index.html"
EN = ROOT / "en" / "index.html"


def soup(path):
    return BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")


def section_ids(doc):
    return [s.get("id") for s in doc.find_all("section")]


def test_header_is_compact_and_has_language_switch():
    doc = soup(NO)
    primary = doc.select_one(".primary-nav")
    assert primary is not None
    assert [a.get_text(" ", strip=True) for a in primary.find_all("a", recursive=False)] == [
        "Bolig", "Utbygger", "Kommune", "Produksjonspartner"
    ]
    assert doc.select_one(".nav-more") is not None
    assert doc.select_one('.lang-switch a[hreflang="en"]')["href"] == "/habitat/en/"
    assert doc.select_one(".mobile-nav") is not None


def test_english_page_exists_and_mirrors_structure():
    no = soup(NO)
    en = soup(EN)
    assert en.html.get("lang") == "en"
    assert section_ids(en) == section_ids(no)
    assert en.select_one('.lang-switch a[hreflang="no"]')["href"] == "/habitat/"
    assert en.find("link", rel="canonical")["href"] == "https://valoresearch.org/habitat/en/"
    assert en.find("link", attrs={"hreflang": "no"}) is not None
    assert no.find("link", attrs={"hreflang": "en"}) is not None


def test_english_page_has_english_core_copy_and_currency():
    page = EN.read_text(encoding="utf-8")
    for text in [
        "A home that can evolve. A network that can change.",
        "First-time buyers",
        "For developers and landowners",
        "For municipalities and public authorities",
        "Do not just reside. Live.",
        "Intl.NumberFormat('en-GB'",
        "+' NOK'",
    ]:
        assert text in page
    for norwegian in ["Stedssjekk", "Avklares", "Førstegangskjøpere", "For kommune og forvaltning"]:
        assert norwegian not in page
