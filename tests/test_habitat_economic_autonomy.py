from pathlib import Path


PAGE = Path(__file__).parents[1] / "habitat" / "research" / "economic-autonomy" / "index.html"


def page_text() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_protocol_separates_economic_constructs():
    text = page_text()
    assert "Objektiv økonomisk kapasitet" in text
    assert "Faktisk boligbelastning" in text
    assert "Opplevd økonomisk autonomi" in text
    assert "Economic Home Fit" in text
    assert "Økonomisk tilfredshet" in text


def test_protocol_operationalizes_autonomy_as_choice_not_satisfaction():
    text = page_text()
    assert "reelle økonomiske handlingsalternativer" in text
    assert "Jeg kan gjøre vesentlige endringer i livet mitt" in text
    assert "Jeg opplever at jeg styrer mine økonomiske valg" in text
    assert "Economic Autonomy Score" in text
    assert "behold alle enkeltledd" in text


def test_protocol_includes_behavioural_and_discriminant_validation():
    text = page_text()
    assert "Atferdsmessig validering" in text
    assert "Scenario · jobb" in text
    assert "Scenario · flytting" in text
    assert "Scenario · uventet utgift" in text
    assert "Scenario · ny retning" in text
    assert "Diskriminant test" in text
    assert "Ingen diskriminant validitet" in text


def test_protocol_tests_incremental_value_beyond_burden_and_satisfaction():
    text = page_text()
    assert "Modell A · Belastning" in text
    assert "Modell B · Tilfredshet" in text
    assert "Modell C · Autonomi" in text
    assert "ytterligere prediktiv verdi" in text
    assert "Δ autonomi kommer før" in text


def test_protocol_is_prospective_and_falsifiable():
    text = page_text()
    assert "Prediction lock" in text
    assert "3, 6, 12 og 24 måneder" in text
    assert "Ingen inkrementell verdi" in text
    assert "Ingen lead time" in text
    assert "Hypotesen skal kunne dø" in text


def test_protocol_does_not_turn_signal_into_move_trigger():
    text = page_text()
    assert "Flytting er ikke fasiten" in text
    assert "gir ikke modellen autoritet til å anbefale flytting" in text


def test_protocol_anchors_ssb_evidence_without_claiming_proof():
    text = page_text()
    assert "Økonomiske analyser 2/2026" in text
    assert "kapittel 5.4.3 og 5.8" in text
    assert "Dette beviser ikke Habitat-hypotesen" in text
    assert "ssb.no" in text
