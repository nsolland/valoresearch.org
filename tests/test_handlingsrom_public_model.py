import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
PAGE = ROOT / "handlingsrom" / "index.html"
DATA = ROOT / "handlingsrom" / "data" / "public-model-2026.json"


def test_public_model_inputs_and_thresholds_are_internally_consistent():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    sifo = data["sifo_2026"]["example_family"]["monthly_nok"]
    housing = data["ssb_housing_2025"]
    thresholds = data["worked_thresholds_example_family_monthly_nok"]

    assert sifo == 38538
    assert thresholds["renter_all"] == sifo + housing["renter_all"]["monthly_nok_rounded"]
    assert thresholds["renter_market"] == sifo + housing["renter_market"]["monthly_nok_rounded"]
    assert thresholds["owner_excluding_principal"] == sifo + housing["owner_all_excluding_principal"]["monthly_nok_rounded"]
    assert thresholds["owner_freehold_cashflow"] == sifo + housing["owner_freehold"]["monthly_nok_rounded"]


def test_page_keeps_stress_test_separate_from_prevalence_claim():
    text = PAGE.read_text(encoding="utf-8")
    assert "stresstest, ikke et prevalensestimat" in text
    assert "Vi publiserer ikke et konstruert nasjonalt prosenttall" in text
    assert "Terskler kan måles nå. Prevalens krever koblede data." in text


def test_page_publishes_sources_and_machine_readable_inputs():
    text = PAGE.read_text(encoding="utf-8")
    assert "SIFO rapport 7-2026" in text
    assert "SSB: Boforhold, levekårsundersøkelsen" in text
    assert "/handlingsrom/data/public-model-2026.json" in text
