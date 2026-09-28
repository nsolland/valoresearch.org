import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_model():
    return json.loads((ROOT / "bidra" / "model.json").read_text(encoding="utf-8"))


def test_need_feed_and_action_marketplace_exist():
    model = load_model()
    feed = model["need_feed"]
    market = model["action_marketplace"]
    assert feed["need_first"] is True
    assert "location" in feed["fields"]
    assert "deadline" in feed["fields"]
    assert "verification_rule" in feed["fields"]
    assert market["matching_engine"] == "smallest_relevant_action"
    assert market["effect_gated"] is True


def test_marketplace_has_low_cost_action_types():
    model = load_model()
    types = set(model["action_marketplace"]["action_types"])
    for item in ["micro_volunteering", "introduction", "local_relay", "resource_lending", "employer_action", "verified_witness", "translation_relay", "recurring_micro_action", "unused_capacity"]:
        assert item in types
