import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "engage" / "customers" / "reqvaris" / "content.json"
PAGE = ROOT / "engage" / "reqvaris" / "index.html"


def test_reqvaris_surface_locks_public_reproduction_gate():
    assert CONTENT.exists(), "REQVARIS content contract must exist"
    data = json.loads(CONTENT.read_text(encoding="utf-8"))
    assert data["visibility"] == "public"
    assert data["customer"]["slug"] == "reqvaris"
    text = json.dumps(data).lower()
    for required in (
        "3/3 local reproduction",
        "valid authority",
        "revoked/no authority",
        "revoked before consequence-time check",
        "pending export gate",
        "vision edge",
        "mithril",
    ):
        assert required in text
    assert "public_reopen_allowed" not in text
    assert "source attestation" not in text


def test_reqvaris_static_page_is_public_safe():
    assert PAGE.exists(), "REQVARIS static page must exist"
    html = PAGE.read_text(encoding="utf-8").lower()
    assert "prepared for reqvaris" in html
    assert "3/3 local reproduction" in html
    assert "pending export gate" in html
    assert "valid authority" in html
    assert "revoked/no authority" in html
    assert "revoked before consequence-time check" in html
    assert "vision edge" in html
    assert "mithril" in html
    assert "private implementation" not in html
    assert "source attestation" not in html
    assert "internal" not in html
