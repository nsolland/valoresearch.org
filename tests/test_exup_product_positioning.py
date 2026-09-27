from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_exup_is_presented_as_workload_execution_optimizer():
    html = (ROOT / 'exup' / 'index.html').read_text()
    assert 'Workload Execution Optimizer' in html
    assert 'Baseline workload' in html
    assert 'Acceptance gate' in html
    assert 'Candidate execution paths' in html
    assert 'Verified result' in html
    assert 'Cost per verified result' in html
    assert '</section>\n<section class="section" id="proof">' in html


def test_exup_public_page_does_not_expose_private_optimizer_mechanics():
    html = (ROOT / 'exup' / 'index.html').read_text().lower()
    forbidden = ['search trajectory', 'optimizer state', 'private transformation logs']
    assert not any(term in html for term in forbidden)


def test_homepage_explains_core_product_structure():
    html = (ROOT / 'index.html').read_text()
    assert 'A system for intelligence, authority and execution economics.' in html
    assert '>CAI<' in html
    assert '>HEIMEL<' in html
    assert '>EXUP<' in html
    assert 'Find and evaluate what should happen.' in html
    assert 'Decide whether it may happen now.' in html
    assert 'Find the best valid way to execute it.' in html
