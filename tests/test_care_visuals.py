from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).parents[1]
PAGE = ROOT / "care" / "index.html"
ASSETS = ROOT / "assets" / "care"

EXPECTED = {
    "care-hero.jpg": "3ce1b2817426c47039fd2d4783ede01b7d61abb22a9a8b4e96b4a955c53953b4",
    "care-home.jpg": "0aa62a176015019b023a4db8f15dd6ae9dc9127d91fee141e257f284d8498d11",
    "care-training.jpg": "cb8be150cfdd86c519417c56b03dd3840ee390604c272dadd3cb74243adc3be2",
    "care-health.jpg": "9695a246f80edb8a93a9f982830c93d6b55dba306660077e69acf6512a8ed8ec",
}


def test_care_visual_assets_exist():
    for name in EXPECTED:
        assert (ASSETS / name).is_file(), name


def test_care_visual_assets_are_exact_generated_files():
    for name, expected in EXPECTED.items():
        assert sha256((ASSETS / name).read_bytes()).hexdigest() == expected, name


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
