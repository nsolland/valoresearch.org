from pathlib import Path


PAGE = Path(__file__).parents[1] / "habitat" / "research" / "economic-autonomy" / "index.html"


def page_text() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_protocol_separates_existing_financial_constructs_from_habitat_construct():
    text = page_text()
    assert "Objektiv økonomisk kapasitet" in text
    assert "Faktisk boligbelastning" in text
    assert "Financial well-being" in text
    assert "Boligbetinget økonomisk handlingsrom" in text
    assert "Economic Home Fit" not in text


def test_protocol_does_not_reinvent_general_financial_wellbeing():
    text = page_text()
    assert "CFPBs validerte Financial Well-Being Scale" in text
    assert "må derfor forklare noe mer spesifikt" in text
    assert "negativ kontroll" in text
    assert "Hvis Habitat-leddene ikke tilfører informasjon utover dette" in text


def test_protocol_operationalizes_housing_constrained_option_set():
    text = page_text()
    assert "option set" in text
    assert "Switching cost" in text
    assert "Reversibilitet" in text
    assert "Boligens marginale effekt" in text
    assert "Arbeid" in text
    assert "Sted" in text
    assert "Livsendring" in text
    assert "Sjokk og reversibilitet" in text


def test_protocol_avoids_premature_composite_score():
    text = page_text()
    assert "Ikke kall dette en generell Economic Autonomy Score" in text
    assert "Housing-Constrained Economic Agency-indeks" in text
    assert "først etter construct validation" in text


def test_protocol_requires_incremental_value_beyond_validated_control():
    text = page_text()
    assert "Modell A · Objektiv økonomi" in text
    assert "Modell B · Boligbelastning" in text
    assert "Modell C · Financial well-being" in text
    assert "Modell D · Housing-Constrained Economic Agency" in text
    assert "Bare inkrementell verdi utover A–C" in text
    assert "Δ boligbetinget handlingsrom kommer før" in text


def test_protocol_connects_fit_and_option_set_without_making_move_the_outcome():
    text = page_text()
    assert "Human–Habitat Fit × Option Set over time" in text
    assert "Flytting er ikke fasiten" in text
    assert "gir ikke modellen autoritet til å anbefale flytting" in text


def test_protocol_is_prospective_and_falsifiable():
    text = page_text()
    assert "Prediction lock" in text
    assert "3, 6, 12 og 24 måneder" in text
    assert "Ingen inkrementell verdi" in text
    assert "Ingen diskriminant validitet" in text
    assert "Ingen boligspesifisitet" in text
    assert "Ingen lead time" in text
    assert "Hypotesen skal kunne dø" in text


def test_protocol_anchors_external_controls_without_claiming_proof():
    text = page_text()
    assert "consumerfinance.gov" in text
    assert "Økonomiske analyser 2/2026" in text
    assert "kapittel 5.4.3 og 5.8" in text
    assert "Dette beviser ikke Habitat-hypotesen" in text
    assert "ssb.no" in text
