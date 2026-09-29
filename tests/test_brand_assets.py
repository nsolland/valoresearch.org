from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_brand_marks_exist_and_are_used():
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    ip = (ROOT / "ip" / "index.html").read_text(encoding="utf-8")
    digital_habitat = (ROOT / "digital-habitat" / "index.html").read_text(encoding="utf-8")

    ai_mark = "/img/product-logos/ai-native-ip-mark.webp"
    dh_mark = "/img/product-logos/goi-mark.webp"
    valo_mark = "/img/valo-research-wordmark.webp"

    assert (ROOT / ai_mark.lstrip("/")).exists()
    assert (ROOT / dh_mark.lstrip("/")).exists()
    assert ai_mark in home and ai_mark in ip
    assert dh_mark in home and dh_mark in digital_habitat
    assert valo_mark in home


def test_ai_native_replaces_olav_world_on_homepage():
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "OLAV.WORLD" not in home
    assert "AI-native IP" in home
