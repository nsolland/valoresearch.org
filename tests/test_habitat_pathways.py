from pathlib import Path

PAGE = Path(__file__).parents[1] / "habitat" / "index.html"


def page_text():
    return PAGE.read_text(encoding="utf-8")


def test_habitat_exposes_core_development_pathways():
    html = page_text()
    for term in [
        "Førstegangskjøpere",
        "Konvertering og omregulering",
        "Grått til grønt",
        "Ikke bare bo. Lev.",
        "Nye eierskapsmodeller",
        "Fortetting uten høyblokk",
        "Pilot som byutviklingsverktøy",
        "Underutnyttet areal",
    ]:
        assert term in html


def test_habitat_frames_land_reuse_as_the_core_strategy():
    html = page_text()
    assert "bruke eksisterende areal bedre" in html
    assert "parkering" in html.lower()
    assert "feste" in html.lower()
    assert "grønne" in html.lower()
