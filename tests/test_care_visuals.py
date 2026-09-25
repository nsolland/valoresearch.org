from pathlib import Path
from PIL import Image

ROOT = Path(__file__).parents[1]
PAGE = ROOT / "care" / "index.html"
ASSETS = ROOT / "assets" / "care"
NAMES = ["care-hero.jpg", "care-home.jpg", "care-training.jpg", "care-health.jpg"]


def test_care_visual_assets_exist():
    for name in NAMES:
        assert (ASSETS / name).is_file(), name


def test_care_visual_assets_are_decodable_images():
    for name in NAMES:
        with Image.open(ASSETS / name) as image:
            image.verify()


def test_care_page_uses_visuals_with_accessible_alt_text():
    html = PAGE.read_text(encoding="utf-8")
    for name in NAMES:
        assert f"/assets/care/{name}" in html, name
    assert html.count("<img") >= 4
    assert html.count("alt=\"") >= 4
