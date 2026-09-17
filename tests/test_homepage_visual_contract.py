from pathlib import Path

html = Path("index.html").read_text(encoding="utf-8")


def test_cinematic_homepage_structure():
    required = [
        'class="cinematic-hero"',
        'class="hero-stage"',
        'id="portfolio"',
        'class="product-band"',
        'Build before belief.',
        '/artist-management/',
        'https://heimel.xyz/',
        '/underwriters/',
    ]
    for marker in required:
        assert marker in html, marker


def test_edu_is_not_in_canonical_product_map():
    start = html.index('id="portfolio"')
    end = html.index('id="method"')
    portfolio = html[start:end]
    assert 'VALO Edu' not in portfolio
    assert 'Education Content Factory' not in portfolio


def test_canonical_product_tracks_are_present():
    products = [
        'Heimel', 'TraXin', 'GCU', 'Factory OS', 'Factory Line', 'OLAV',
        'relAIon / relAI', 'Just You', 'JustIT', 'Protocol Layer',
        'Edge / MCU / NPU', 'Capability Layer', 'EmplAI',
        'Cleanroom / Model & Reasoning Profiler', 'AI-Artist / Music Rights',
        'REHT', 'Personal Sovereignty Conformance', 'VALO'
    ]
    for product in products:
        assert product in html, product
