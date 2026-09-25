#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path, PurePosixPath

REQUIRED_FIELDS = ("type", "path", "alt", "caption", "source", "public")
SHARED_ROOT = "/engage/_assets/common/"
CUSTOMER_RE = re.compile(r"^/engage/customers/[a-z0-9][a-z0-9-]*/assets/.+")


class AssetValidationError(ValueError):
    pass


def _validate_asset(asset, index):
    if not isinstance(asset, dict):
        raise AssetValidationError(f"asset[{index}] must be an object")

    for field in REQUIRED_FIELDS:
        if field not in asset:
            raise AssetValidationError(f"asset[{index}] missing required field: {field}")

    if asset["public"] is not True:
        raise AssetValidationError(f"asset[{index}] must be explicitly public:true")

    for field in ("type", "path", "alt", "caption", "source"):
        if not isinstance(asset[field], str) or not asset[field].strip():
            raise AssetValidationError(f"asset[{index}] field {field} must be a non-empty string")

    path = asset["path"]
    if "://" in path or path.startswith("//"):
        raise AssetValidationError(f"asset[{index}] path must be repository-local")

    pure = PurePosixPath(path)
    if not path.startswith("/") or ".." in pure.parts:
        raise AssetValidationError(f"asset[{index}] path must be repository-local")

    if not (path.startswith(SHARED_ROOT) or CUSTOMER_RE.fullmatch(path)):
        raise AssetValidationError(
            f"asset[{index}] path must be under allowed asset roots: "
            f"{SHARED_ROOT} or /engage/customers/<customer>/assets/"
        )


def validate_manifest(path):
    manifest_path = Path(path)
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AssetValidationError(f"cannot read valid JSON manifest: {manifest_path}: {exc}") from exc

    if not isinstance(payload, dict):
        raise AssetValidationError("manifest root must be an object")

    assets = payload.get("assets")
    if not isinstance(assets, list):
        raise AssetValidationError("manifest must contain an assets array")

    for index, asset in enumerate(assets):
        _validate_asset(asset, index)

    return len(assets)


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print("usage: validate_assets.py <content.json> [<content.json> ...]", file=sys.stderr)
        return 2

    total = 0
    try:
        for item in args:
            total += validate_manifest(item)
    except AssetValidationError as exc:
        print(f"asset validation failed: {exc}", file=sys.stderr)
        return 1

    print(f"validated {total} public engagement asset(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
