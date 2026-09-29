from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")


def test_homepage_is_editorial_not_saas_template():
    for marker in [
        'class="editorial-hero"',
        'class="hero-photo"',
        'class="field-notes"',
        'class="research-ledger"',
        'class="artifact-strip"',
        'class="mobile-nav"',
    ]:
        assert marker in HTML, marker
    assert 'class="pill"' not in HTML
    assert "overflow-x:auto" not in HTML


def test_homepage_uses_local_real_photography_with_credit():
    images = [
        "lab-engineer.jpg",
        "engineers-whiteboard.jpg",
        "electronics-workbench.jpg",
    ]
    for name in images:
        path = ROOT / "assets" / "editorial" / name
        assert path.exists(), name
        assert f'/assets/editorial/{name}' in HTML
    assert "ThisIsEngineering / Pexels" in HTML
    assert "Photo credit" in HTML
