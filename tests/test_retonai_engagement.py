import json
import re
from pathlib import Path

ROOT = Path(__file__).parents[1]
CONTENT = ROOT / "engage" / "customers" / "retonai" / "content.json"
PAGE = ROOT / "engage" / "retonai" / "index.html"


def test_retonai_surface_is_public_bounded_and_commercial_first():
    payload = json.loads(CONTENT.read_text(encoding="utf-8"))
    assert payload["visibility"] == "public"
    assert payload["customer"] == {"slug": "retonai", "name": "RETONAI"}
    text = CONTENT.read_text(encoding="utf-8").lower()
    for term in ["carrier substitution", "commercial basis", "bounded demonstrator"]:
        assert term in text
    assert payload["cta"]["title"] == "Define the commercial basis"


def test_retonai_surface_has_one_public_next_gate_and_no_private_markers():
    html = PAGE.read_text(encoding="utf-8")
    assert "Prepared for RETONAI" in html
    assert "Define the commercial basis" in html
    assert "http://localhost" not in html
    assert "fetch(" not in html
    assert "<script src=" not in html
    text = (CONTENT.read_text(encoding="utf-8") + html).lower()
    for forbidden in ["confidential", "private ip", "patent filing", "internal retonai"]:
        assert forbidden not in text
    assert re.search(r"\bnda\b", text) is None
