import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bidra_exposes_general_core_and_modular_model():
    page = (ROOT / "bidra" / "index.html").read_text(encoding="utf-8")
    assert "BIDRA Core" in page
    assert "Contribution Score" in page
    assert "Charity Impact" in page
    assert "Organisasjonsadapter" in page
    assert "frivillig" in page.lower()


def test_bidra_machine_model_separates_core_modules_and_org_adapter():
    model = json.loads((ROOT / "bidra" / "model.json").read_text(encoding="utf-8"))
    assert model["schema_version"] == "1.0"
    assert model["core"]["flow"] == ["purpose", "need", "contribution", "action", "verification", "impact", "feedback"]
    assert {"money", "time", "skills", "network", "attention", "equipment", "transport"}.issubset(model["modules"])
    assert "organization_adapter" in model
    assert "contribution_score" in model["scoring"]
    assert "charity_impact" in model["scoring"]
