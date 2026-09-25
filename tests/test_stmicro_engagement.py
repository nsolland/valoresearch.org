import json
import re
from pathlib import Path

ROOT = Path(__file__).parents[1]
CONTENT = ROOT / "engage" / "customers" / "stmicro" / "content.json"
PAGE = ROOT / "engage" / "stmicro" / "index.html"
HERO = "/engage/customers/stmicro/assets/hero.png"


def test_stmicro_content_is_public_customer_specific_and_bounded():
    payload = json.loads(CONTENT.read_text(encoding="utf-8"))
    assert payload["visibility"] == "public"
    assert payload["customer"] == {"slug": "stmicro", "name": "STMicroelectronics"}
    text = CONTENT.read_text(encoding="utf-8").lower()
    for term in [
        "smallest st-based reference architecture",
        "local inference",
        "secure identity",
        "physical interfaces",
        "stm32-class",
        "carrier-neutral",
    ]:
        assert term in text


def test_stmicro_hero_uses_promoted_public_asset():
    payload = json.loads(CONTENT.read_text(encoding="utf-8"))
    assert payload["hero"]["image"] == HERO
    asset = next(item for item in payload["assets"] if item["path"] == HERO)
    assert asset["type"] == "image"
    assert asset["public"] is True
    assert asset["source"] == "VALO Research / image generation"
    assert (ROOT / HERO.lstrip("/")).is_file()

    html = PAGE.read_text(encoding="utf-8")
    assert f'src="{HERO}"' in html
    assert 'class="hero-media"' in html


def test_stmicro_surface_points_to_public_evidence_and_one_next_gate():
    html = PAGE.read_text(encoding="utf-8")
    assert "Prepared for STMicroelectronics" in html
    assert "/research/universal-retrofit-intelligence/" in html
    assert "https://heimel.xyz/" in html
    assert "Define the reference architecture" in html
    assert "http://localhost" not in html
    assert "fetch(" not in html
    assert "<script src=" not in html


def test_stmicro_surface_does_not_publish_partner_private_material():
    text = (CONTENT.read_text(encoding="utf-8") + PAGE.read_text(encoding="utf-8")).lower()
    for forbidden in ["st confidential", "patent filing", "internal st", "private ip"]:
        assert forbidden not in text
    assert re.search(r"\bnda\b", text) is None
