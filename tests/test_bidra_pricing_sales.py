import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bidra_public_page_has_commercial_offer_and_prices():
    page = (ROOT / "bidra" / "index.html").read_text(encoding="utf-8")
    for text in [
        "BIDRA 30",
        "€4 900",
        "€590/mnd",
        "€1 490/mnd",
        "fra €4 900/mnd",
        "Stop / Scale",
        "Dere har allerede givere. BIDRA gjør dem til bidragsytere.",
    ]:
        assert text in page


def test_bidra_model_exposes_pricing_and_sales_kpis():
    model = json.loads((ROOT / "bidra" / "model.json").read_text(encoding="utf-8"))
    commercial = model["commercial_model"]
    assert commercial["donation_fee"] == "none"
    assert commercial["entry_offer"]["name"] == "BIDRA 30"
    assert commercial["entry_offer"]["price_eur"] == 4900
    assert commercial["plans"]["core"]["monthly_eur"] == 590
    assert commercial["plans"]["pro"]["monthly_eur"] == 1490
    assert commercial["plans"]["enterprise"]["monthly_eur_from"] == 4900
    assert "verified_impact_yield" in commercial["sales_kpis"]
    assert commercial["channel_strategy"]["nonprofit"] == "low_cost_or_sponsored"
    assert commercial["channel_strategy"]["enterprise_sponsor"] == "primary_high_value_buyer"
