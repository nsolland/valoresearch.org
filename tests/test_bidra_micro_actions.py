import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bidra_exposes_low_cost_micro_actions():
    page = (ROOT / "bidra" / "index.html").read_text(encoding="utf-8")
    for text in [
        "Små bidrag kan bety mye",
        "Følg en relevant organisasjon",
        "Redd Barna",
        "Svar på én undersøkelse",
        "Introduser én person",
        "Fem minutter",
    ]:
        assert text in page
    assert "illustrerende eksempel" in page.lower()


def test_micro_actions_are_machine_readable_and_effect_gated():
    model = json.loads((ROOT / "bidra" / "model.json").read_text(encoding="utf-8"))
    actions = model["micro_actions"]
    ids = {item["id"] for item in actions["catalog"]}
    assert {"follow_profile", "share_verified_content", "answer_survey", "introduce_contact", "five_minute_task"} <= ids
    assert actions["principle"] == "low effort can create high impact when the action is relevant to a verified need"
    assert actions["scoring_rule"] == "no impact credit without relevance and evidence"
