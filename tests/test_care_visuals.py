from pathlib import Path

ROOT = Path(__file__).parents[1]
PAGE = ROOT / "care" / "index.html"
ASSETS = ROOT / "assets" / "care"


def test_care_visual_assets_exist():
    for name in ["care-hero.jpg", "care-home.jpg", "care-training.jpg", "care-health.jpg"]:
        assert (ASSETS / name).is_file(), name


def test_care_page_uses_visuals_with_accessible_alt_text():
    html = PAGE.read_text(encoding="utf-8")
    for path in [
        "/assets/care/care-hero.jpg",
        "/assets/care/care-home.jpg",
        "/assets/care/care-training.jpg",
        "/assets/care/care-health.jpg",
    ]:
        assert path in html, path
    assert html.count("<img") >= 4
    assert html.count('alt="') >= 4
