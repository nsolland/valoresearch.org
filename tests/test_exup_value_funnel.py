from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def text(path):
    return (ROOT / path).read_text()


def test_product_logic_and_proof_are_visible():
    html = text('exup/index.html')
    for marker in [
        'Workload Execution Optimizer',
        'Baseline workload',
        'Acceptance gate',
        'Candidate execution paths',
        'Verified result',
        'Cost per verified result',
        'EXUP-PUBLIC-01',
        '+23.2%',
        '6.62 host-hours',
        'EXUP-PUBLIC-02',
        'EXUP-COST-CAPACITY-01',
        'EXUP-COMPUTE-ALLOCATION-DOWN-01',
        'PHYSICAL-01',
        '€2.85',
        'not yet realized savings',
    ]:
        assert marker in html
    assert '/exup/evidence/public-01/' in html
    assert '/exup/evidence/open-hw-01/' in html
    assert '/exup/evidence/cost-capacity-01/' in html
    assert '/exup/evidence/compute-allocation-down-01/' in html


def test_savings_calculator_is_scenario_not_claim():
    html = text('exup/index.html')
    for marker in [
        'id="monthly-cost"',
        'id="improvement-rate"',
        'id="monthly-savings"',
        'id="annual-savings"',
        'Scenario estimate — not a measured customer result.',
        'calculateSavings',
    ]:
        assert marker in html


def test_buying_logic_is_concrete():
    html = text('exup/access/index.html')
    for marker in [
        '1. Lock the baseline',
        '2. Lock the acceptance gate',
        '3. Run a bounded benchmark',
        '4. Verify economic value',
        '5. Continue only if value exists',
        'What you provide',
        'What you get',
        'Request a bounded EXUP benchmark',
    ]:
        assert marker in html


def test_homepage_exposes_exup_execution_economics():
    html = text('index.html')
    assert 'EXUP' in html
    assert 'Execution economics' in html
    assert '/exup/' in html
    assert 'Proof-led optimization' in html
