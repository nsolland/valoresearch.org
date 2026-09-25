import json
from pathlib import Path
import pytest

from engage._core.generate import EngagementBuildError, build_page


def base_content():
    return {
        "customer": {"slug": "stmicro", "name": "STMicroelectronics"},
        "visibility": "public",
        "hero": {
            "eyebrow": "Prepared for STMicroelectronics",
            "title": "Retrofit intelligence with governed physical effect.",
            "summary": "A customer-specific decision surface."
        },
        "assets": [{
            "type": "diagram",
            "path": "/engage/customers/stmicro/assets/architecture.svg",
            "alt": "Reference architecture",
            "caption": "Reference architecture.",
            "source": "VALO Research",
            "public": True
        }],
        "situation": {
            "title": "The situation",
            "body": ["Existing equipment needs local intelligence without losing control of physical effects."]
        },
        "theses": [{
            "title": "Local inference is not enough",
            "body": "The action boundary needs fresh authority immediately before effect."
        }],
        "demos": [{
            "title": "Carrier-substitution demonstrator",
            "body": "Replace the compute carrier while preserving the execution contract.",
            "asset": "/engage/customers/stmicro/assets/architecture.svg",
            "link": {"label": "Open demo", "href": "https://example.com/demo"}
        }],
        "evidence": [{
            "title": "Fresh authority",
            "body": "Decision is evaluated at consequence time.",
            "status": "verified"
        }],
        "proposal": {
            "title": "Proposed next test",
            "body": "Define one bounded retrofit workload and its success criteria."
        },
        "questions": ["Which effects must remain physically local?"],
        "cta": {
            "title": "Define the pilot",
            "body": "Agree workload, boundary and evidence.",
            "action": {"label": "Define pilot", "href": "mailto:njaal@valoresearch.org?subject=STMicro%20pilot"}
        }
    }


def write_content(tmp_path, payload):
    customer = tmp_path / "engage" / "customers" / payload["customer"]["slug"]
    customer.mkdir(parents=True)
    path = customer / "content.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    for asset in payload.get("assets", []):
        asset_path = tmp_path / asset["path"].lstrip("/")
        asset_path.parent.mkdir(parents=True, exist_ok=True)
        asset_path.write_text("asset", encoding="utf-8")
    return path


def test_generates_static_customer_page_in_slug_route(tmp_path):
    path = write_content(tmp_path, base_content())
    output = build_page(path, repo_root=tmp_path)
    html = output.read_text(encoding="utf-8")
    assert output == tmp_path / "engage" / "stmicro" / "index.html"
    assert "STMicroelectronics" in html
    assert "The situation" in html
    assert "Carrier-substitution demonstrator" in html
    assert "Define pilot" in html
    assert "fetch(" not in html
    assert "<script src=" not in html


def test_rejects_non_public_page(tmp_path):
    payload = base_content()
    payload["visibility"] = "private"
    path = write_content(tmp_path, payload)
    with pytest.raises(EngagementBuildError, match="visibility.*public"):
        build_page(path, repo_root=tmp_path)


def test_rejects_undeclared_asset_reference(tmp_path):
    payload = base_content()
    payload["demos"][0]["asset"] = "/engage/customers/stmicro/assets/not-declared.webp"
    path = write_content(tmp_path, payload)
    with pytest.raises(EngagementBuildError, match="declared public asset"):
        build_page(path, repo_root=tmp_path)


def test_rejects_customer_asset_from_another_customer(tmp_path):
    payload = base_content()
    payload["assets"][0]["path"] = "/engage/customers/retonai/assets/architecture.svg"
    payload["demos"][0]["asset"] = payload["assets"][0]["path"]
    path = write_content(tmp_path, payload)
    with pytest.raises(EngagementBuildError, match="customer asset"):
        build_page(path, repo_root=tmp_path)


def test_optional_sections_can_be_omitted(tmp_path):
    payload = base_content()
    del payload["demos"]
    del payload["questions"]
    path = write_content(tmp_path, payload)
    output = build_page(path, repo_root=tmp_path)
    html = output.read_text(encoding="utf-8")
    assert "Carrier-substitution demonstrator" not in html
    assert "Open questions" not in html
    assert "Define pilot" in html


def test_rejects_declared_asset_missing_from_repository(tmp_path):
    payload = base_content()
    path = write_content(tmp_path, payload)
    asset_path = tmp_path / payload["assets"][0]["path"].lstrip("/")
    asset_path.unlink()
    with pytest.raises(EngagementBuildError, match="does not exist"):
        build_page(path, repo_root=tmp_path)
