import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_model():
    return json.loads((ROOT / "bidra" / "model.json").read_text(encoding="utf-8"))


def test_campaign_contract_and_receipts_are_core_objects():
    model = load_model()
    objects = set(model["core"]["objects"])
    assert "campaign_contract" in objects
    assert "impact_receipt" in objects
    assert model["campaign_contract"]["required"] == [
        "target_outcome", "accepted_contributions", "verification_rules", "deadline", "failure_policy"
    ]
    assert "contribution_id" in model["impact_receipt"]["binds"]
    assert "impact_record_id" in model["impact_receipt"]["binds"]


def test_scoring_is_effect_based_private_and_anti_gaming():
    model = load_model()
    scoring = model["scoring"]
    assert "organization_impact_score" in scoring
    assert scoring["contribution_score"]["default_visibility"] == "private"
    assert scoring["organization_impact_score"]["activity_only_score"] is False
    assert model["anti_gaming"]["activity_without_relevance_or_effect"] == "no_credit"


def test_portable_profile_matching_cause_graph_and_open_api_exist():
    model = load_model()
    assert model["portable_profile"]["cross_organization"] is True
    assert model["team_contribution"]["supported"] is True
    assert model["cause_graph"]["primary_navigation"] == "cause_not_organization"
    assert model["matching_engine"]["objective"] == "smallest_relevant_action_now"
    assert "crm" in model["open_impact_api"]["integrates_with"]
    assert "payment" in model["open_impact_api"]["integrates_with"]


def test_public_page_explains_control_and_evidence_layer():
    page = (ROOT / "bidra" / "index.html").read_text(encoding="utf-8")
    for text in [
        "Campaign Contract",
        "Impact Receipt",
        "Organizational Impact Score",
        "Privacy by default",
        "Portable profile",
        "Cause graph",
        "Matching engine",
        "Open Impact API",
        "kontroll- og evidenslag",
    ]:
        assert text in page
