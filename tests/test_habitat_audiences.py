from pathlib import Path

PAGE = Path(__file__).parents[1] / "habitat" / "index.html"


def html():
    return PAGE.read_text(encoding="utf-8")


def test_existing_habitat_story_is_preserved():
    page = html()
    assert "Et hjem som kan utvikles. Et nettverk som kan endres." in page
    assert "Privat når det trengs." in page
    assert "Felles når det fungerer bedre." in page
    assert "Fra ett hjem" in page
    assert "til et nettverk." in page
    assert "VALO30 har en målpris på 1 000 000 kr inkl. mva" in page


def test_shared_adds_live_not_just_reside_frame():
    page = html()
    assert "Ikke bare bo. Lev." in page
    assert "fellesfunksjoner" in page.lower()
    assert "hverdagsliv" in page.lower()


def test_deployment_adds_three_new_use_cases():
    page = html()
    for term in ["Førstegangskjøpere", "Konvertering og omregulering", "Grått til grønt"]:
        assert term in page


def test_builder_and_public_sections_exist_and_are_linked():
    page = html()
    for term in ['id="developer"', 'id="municipality"', 'href="#developer"', 'href="#municipality"']:
        assert term in page
    for term in ["For utbygger", "For kommune og forvaltning", "feste", "opsjon", "underutnyttet", "pilotområde"]:
        assert term.lower() in page.lower()
