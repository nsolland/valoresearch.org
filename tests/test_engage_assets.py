import json
from pathlib import Path

import pytest

from engage._core.validate_assets import AssetValidationError, validate_manifest


def write_manifest(tmp_path, assets):
    path = tmp_path / "content.json"
    path.write_text(json.dumps({"assets": assets}), encoding="utf-8")
    return path


def valid_asset(path="/engage/_assets/common/heimel-flow.svg"):
    return {
        "type": "diagram",
        "path": path,
        "alt": "Heimel authorization flow",
        "caption": "Fresh authority is checked before consequence.",
        "source": "VALO Research",
        "public": True,
    }


def test_accepts_explicitly_public_shared_asset(tmp_path):
    manifest = write_manifest(tmp_path, [valid_asset()])
    assert validate_manifest(manifest) == 1


def test_accepts_explicitly_public_customer_asset(tmp_path):
    manifest = write_manifest(
        tmp_path,
        [valid_asset("/engage/customers/stmicro/assets/hero.webp")],
    )
    assert validate_manifest(manifest) == 1


def test_rejects_asset_not_explicitly_public(tmp_path):
    asset = valid_asset()
    asset["public"] = False
    manifest = write_manifest(tmp_path, [asset])
    with pytest.raises(AssetValidationError, match="public:true"):
        validate_manifest(manifest)


@pytest.mark.parametrize("field", ["type", "path", "alt", "caption", "source", "public"])
def test_rejects_missing_required_metadata(tmp_path, field):
    asset = valid_asset()
    del asset[field]
    manifest = write_manifest(tmp_path, [asset])
    with pytest.raises(AssetValidationError, match=field):
        validate_manifest(manifest)


def test_rejects_asset_outside_engagement_asset_roots(tmp_path):
    manifest = write_manifest(tmp_path, [valid_asset("/img/private.png")])
    with pytest.raises(AssetValidationError, match="allowed asset roots"):
        validate_manifest(manifest)


def test_rejects_temporary_or_remote_asset_urls(tmp_path):
    manifest = write_manifest(tmp_path, [valid_asset("https://example.com/temporary.webp")])
    with pytest.raises(AssetValidationError, match="repository-local"):
        validate_manifest(manifest)
