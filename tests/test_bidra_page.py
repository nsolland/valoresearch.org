from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bidra_page_defines_contribution_not_just_donation():
    page = (ROOT / "bidra" / "index.html").read_text(encoding="utf-8")
    assert "Bidra, og ikke bare gi." in page
    assert "Penger + handling + dokumentert effekt" in page
    assert "like eller dele" in page


def test_bidra_page_includes_digital_contribution_tracker_and_partner_model():
    page = (ROOT / "bidra" / "index.html").read_text(encoding="utf-8")
    assert "Bidragsspor" in page
    assert "Penger" in page
    assert "Handling" in page
    assert "Effekt" in page
    assert "For veldedige organisasjoner" in page


def test_bidra_is_linked_from_product_map_and_sitemap():
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert 'href="/bidra/"' in home
    assert "https://valoresearch.org/bidra/" in sitemap
