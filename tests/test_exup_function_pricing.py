from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def test_function_pricing_is_canonical():
    html=(ROOT/'exup/index.html').read_text()
    for marker in [
        'EXUP Runtime / Control Plane',
        '€2.5k / month minimum',
        'per workload family',
        '€5k–10k / month',
        '€20k+ / month',
        'Platform fee + verified value share',
        'Developer / pilot',
        'OEM / embedded / venue integration',
    ]:
        assert marker in html

def test_access_explains_runtime_fee():
    html=(ROOT/'exup/access/index.html').read_text()
    assert 'Production runtime starts at €2.5k / month per workload family' in html
    assert 'value share remains separate' in html
