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


def test_homepage_uses_valo_owned_reference_photography():
    images = [
        "lab-engineer.jpg",
        "engineers-whiteboard.jpg",
        "electronics-workbench.jpg",
    ]
    for name in images:
        path = ROOT / "assets" / "editorial" / name
        assert path.exists(), name
        assert f'/assets/editorial/{name}' in HTML
    assert "ThisIsEngineering / Pexels" not in HTML
    assert "Pexels" not in HTML


def test_homepage_product_identity_uses_current_marks():
    assert "OLAV.WORLD" not in HTML
    assert ">AI Native<" in HTML
    assert '/img/product-logos/ai-native-mark.svg' in HTML
    assert '/img/product-logos/digital-habitat-mark.svg' in HTML
    assert '<img src="/img/valo-mark.svg"' in HTML
    assert (ROOT / "img" / "product-logos" / "ai-native-mark.svg").exists()
    assert (ROOT / "img" / "product-logos" / "digital-habitat-mark.svg").exists()
