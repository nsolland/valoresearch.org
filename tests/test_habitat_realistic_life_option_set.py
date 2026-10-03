from pathlib import Path


PAGE = Path(__file__).parents[1] / "habitat" / "research" / "realistic-life-option-set" / "index.html"


def page_text() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_rlos_is_distinct_from_existing_constructs():
    text = page_text()
    assert "Financial well-being" in text
    assert "Housing satisfaction" in text
    assert "Human–Habitat Fit" in text
    assert "Realistic Life Option Set" in text
    assert "lik financial well-being" in text


def test_rlos_measures_realistic_not_theoretical_options():
    text = page_text()
    assert "Tilgjengelig" in text
    assert "Tilgjengelig med moderat offer" in text
    assert "Teknisk mulig, men urealistisk" in text
    assert "Utilgjengelig" in text


def test_rlos_includes_core_metrics():
    text = page_text()
    assert "Option Count" in text
    assert "Option Diversity" in text
    assert "Housing Constraint Share" in text
    assert "Switching / Reversal Cost" in text
    assert "Option Resilience" in text


def test_rlos_tests_housing_attribution_and_counterfactuals():
    text = page_text()
    assert "Boligattribusjon" in text
    assert "Hold personen fast. Bytt boligstrukturen." in text
    assert "samme person + samme livssituasjon + bolig A" in text
    assert "samme person + samme livssituasjon + bolig B" in text


def test_rlos_is_longitudinal_and_falsifiable():
    text = page_text()
    assert "RLOS(t0)" in text
    assert "Time to recovery" in text
    assert "Persistent option loss" in text
    assert "Hypotesen skal kunne dø" in text
    assert "Ingen longitudinal verdi" in text


def test_rlos_preserves_separate_dimensions_before_indexing():
    text = page_text()
    assert "Ingen tvungen aggregasjon" in text
    assert "En samlet indeks kan først vurderes etter construct validation" in text


def test_rlos_connects_to_habitat_core_model():
    text = page_text()
    assert "Human–Habitat Fit × Option Set over time" in text
    assert "Pre-Need tester når fit er på vei til å endres" in text
    assert "Decision Window tester om reelle valg fortsatt finnes" in text
