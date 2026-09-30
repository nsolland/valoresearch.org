from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")


def test_hero_image_has_no_visible_caption():
    hero = HTML.split('<section class="editorial-hero">', 1)[1].split('</section>', 1)[0]
    assert '<figcaption' not in hero
    assert 'Engineering work in a laboratory.' not in hero
    assert 'VALO reference image.' not in hero



def test_homepage_images_have_no_visible_captions():
    assert 'Engineering teams make assumptions visible before they become systems.' not in HTML
    assert 'Hands-on electronics work.' not in HTML
    assert 'Governed workspace / contract artifact from the public REHT material.' not in HTML
    assert 'VALO reference image.' not in HTML


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
