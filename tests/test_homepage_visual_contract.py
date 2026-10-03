from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'index.html').read_text(encoding='utf-8')
CSS = (ROOT / 'assets/home-redesign.css').read_text(encoding='utf-8')


class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.feed(HTML)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def test_homepage_preserves_identity_and_metadata():
    assert '<link rel="canonical" href="https://valoresearch.org/">' in HTML
    assert '/img/valo-research-wordmark.webp' in HTML
    assert '>AI-native IP<' in HTML
    assert '/img/product-logos/ai-native-ip-mark.webp' in HTML
    assert '/img/product-logos/goi-mark.webp' in HTML
    assert 'OLAV.WORLD' not in HTML


def test_research_precedes_products_and_covers_four_tracks():
    research = HTML.split('id="research"', 1)[1].split('</section>', 1)[0]
    for track in ['Silicon intelligence', 'Execution economics', 'Physical systems', 'Human control']:
        assert track in research
    assert HTML.index('id="research"') < HTML.index('id="products"')


def test_hero_explorer_has_native_controls_and_honest_boundary():
    hero = HTML.split('<section class="editorial-hero">', 1)[1].split('</section>', 1)[0]
    assert 'not an experimental result' in hero
    assert '<details open>' in hero
    assert hero.count('<summary>') == 3
    assert 'role="img"' in hero
    assert 'aria-labelledby="network-title network-desc"' in hero
    assert '/assets/editorial/' not in HTML


def test_palette_and_accessible_responsive_contract():
    for color in ['#F4F2EC', '#11252D', '#24483d', '#9A6F32']:
        assert color in CSS
    assert ':focus-visible' in CSS
    assert 'prefers-reduced-motion' in CSS
    assert '@media(max-width:560px)' in CSS
    assert 'class="mobile-nav"' in HTML
    assert 'href="#main"' in HTML
    assert len([tag for tag, _ in Document().tags if tag == 'h1']) == 1


def test_local_navigation_resolves_and_fragment_targets_exist():
    doc = Document()
    ids = {attrs['id'] for _, attrs in doc.tags if 'id' in attrs}
    for tag, attrs in doc.tags:
        if tag != 'a':
            continue
        href = attrs.get('href', '')
        if href.startswith('#'):
            assert href[1:] in ids, href
        elif href.startswith('/'):
            assert (ROOT / href.split('#')[0].lstrip('/')).exists(), href


def test_team_relationships_and_inspectable_artifacts_preserved():
    for person in ['Njål Gaute Solland', 'Triin Solland', 'Elsa Sklavounou', 'Margaret Stokes', 'Charles R. Rupp', 'Jasper van de Meent', 'Zaid Hasan Khan']:
        assert person in HTML
    assert 'no current operational delivery obligation' in HTML
    assert 'representation is not proof of an outcome' in HTML
    assert '/exup/evidence/cost-capacity-01/' in HTML
    assert '/demos/insurance-authority/' in HTML
