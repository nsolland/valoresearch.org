from pathlib import Path

PAGE = Path(__file__).parents[1] / "care" / "index.html"


def page_text():
    return PAGE.read_text(encoding="utf-8")


def test_care_route_exists_and_has_core_positioning():
    html = page_text()
    assert "CARE — AI care for dogs" in html
    assert "It’s a full-time job." in html
    assert "Keep track. Understand. Train. Care." in html


def test_care_explains_individual_learning_and_health_context_without_diagnosis_claim():
    html = page_text()
    assert "learns what is normal for your dog" in html
    assert "relevant dogs of similar breed, age and life stage" in html
    assert "CARE does not diagnose disease" in html


def test_care_includes_home_training_and_owner_controlled_sharing():
    html = page_text()
    for term in ["camera", "speaker", "clicker", "food and water", "veterinarian", "insurance"]:
        assert term in html.lower()
    assert "You decide who sees what." in html


def test_care_is_static_github_pages_compatible():
    html = page_text()
    assert "<meta name=\"viewport\"" in html
    assert "mailto:njaal@valoresearch.org?subject=CARE" in html
    assert "http://localhost" not in html
    assert "<script src=" not in html
