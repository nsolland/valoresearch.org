from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "research" / "human-control" / "index.html"


def test_human_control_research_has_bounded_public_claims():
    html = PAGE.read_text()
    assert "Human Control Research" in html
    assert "When is human-in-the-loop actually meaningful human control?" in html
    for term in ("HCM", "Human Control Barometer", "HCS", "HEIMEL"):
        assert term in html
    assert "Observation → Evidence → Latent hypothesis → Control state" in html
    assert "No global attention score" in html
    assert "No patient-affecting study" in html
    assert "Physiology is not ground truth" in html
    assert "Failed hypotheses remain valid results" in html
    assert "https://github.com/Heimel-open/human-control-barometer" in html


def test_human_control_research_is_discoverable():
    research = (ROOT / "research" / "index.html").read_text()
    home = (ROOT / "index.html").read_text()
    sitemap = (ROOT / "sitemap.xml").read_text()
    path = "/research/human-control/"
    assert path in research
    assert path in home
    assert "https://valoresearch.org/research/human-control/" in sitemap
