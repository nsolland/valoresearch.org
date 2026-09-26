from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "exup/evidence/public-01/index.html"
RESULT = ROOT / "exup/evidence/public-01/result.json"


def test_public_evidence_page_has_measured_claim_and_boundary():
    html = PAGE.read_text()
    assert "+23.2%" in html
    assert "−18.9%" in html
    assert "−33.5%" in html
    assert "Headline values use medians" in html
    assert "not an official MLPerf submission" in html
    assert "does not establish performance on STM32, Axelera" in html


def test_public_result_passes_accuracy_gate():
    data = json.loads(RESULT.read_text())
    assert data["acceptance_gate"]["pass"] is True
    assert data["candidate"]["mAP_50_95"] >= data["acceptance_gate"]["minimum"]
    assert data["candidate"]["mAP_50_95"] >= data["baseline"]["mAP_50_95"]


def test_public_page_does_not_disclose_internal_mechanism_terms():
    html = PAGE.read_text().lower()
    forbidden = ["system prompt", "candidate generator implementation", "search tree", "ranking weights", "private prompt"]
    assert all(term not in html for term in forbidden)
