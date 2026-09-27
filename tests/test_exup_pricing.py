from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_canonical_pricing_is_public():
    html=(ROOT/'exup/index.html').read_text()
    for marker in [
        '€5k–15k',
        '€10k–50k',
        '20% of verified value',
        '24 months',
        '25%',
        '15%',
        'Strategic venue pilot',
        'credited against the value-share engagement',
    ]:
        assert marker in html

def test_access_page_matches_canonical_pricing():
    html=(ROOT/'exup/access/index.html').read_text()
    assert 'Benchmark fee: €5k–15k' in html
    assert 'Standard value share: 20% for 24 months' in html
    assert 'Continue only if verified value exists' in html
