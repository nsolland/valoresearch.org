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
        "lab-engineer.webp",
        "engineers-whiteboard.webp",
        "electronics-workbench.webp",
    ]
    for name in images:
        path = ROOT / "assets" / "editorial" / name
        assert path.exists(), name
        assert f'/assets/editorial/{name}' in HTML
    assert "ThisIsEngineering / Pexels" not in HTML
    assert "Pexels" not in HTML


def test_homepage_product_identity_uses_current_marks():
    assert "OLAV.WORLD" not in HTML
    assert ">AI-native IP<" in HTML
    assert '/img/product-logos/ai-native-ip-mark.webp' in HTML
    assert '/img/product-logos/goi-mark.webp' in HTML
    assert '/img/valo-research-wordmark.webp' in HTML
    assert (ROOT / "img" / "product-logos" / "ai-native-ip-mark.webp").exists()
    assert (ROOT / "img" / "product-logos" / "goi-mark.webp").exists()


def test_artifact_strip_has_clean_three_column_layout():
    assert "grid-template-columns:1.2fr .9fr .9fr" in HTML
    assert "grid-row:span 2" not in HTML
    assert "min-height:570px" not in HTML
    assert "aspect-ratio:4/3" in HTML
