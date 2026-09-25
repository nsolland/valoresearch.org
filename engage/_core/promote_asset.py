#!/usr/bin/env python3
import argparse
import json
import re
import shutil
from pathlib import Path

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
ALLOWED_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".svg"}
PLACEHOLDER = "UPLOAD_HERE.txt"


class PromotionError(ValueError):
    pass


def _slug(value, field):
    if not isinstance(value, str) or not SLUG_RE.fullmatch(value):
        raise PromotionError(f"{field} must be a lowercase slug")
    return value


def _nonempty(value, field):
    if not isinstance(value, str) or not value.strip():
        raise PromotionError(f"{field} must be non-empty")
    return value.strip()


def _uploaded_files(inbox):
    if not inbox.is_dir():
        return []
    return sorted(
        p for p in inbox.iterdir()
        if p.is_file() and p.name != PLACEHOLDER and not p.name.startswith(".")
    )


def _bind(payload, dotted_path, value):
    parts = dotted_path.split(".")
    if not parts or any(not part for part in parts):
        raise PromotionError("bind must be a dotted content path")
    node = payload
    for part in parts[:-1]:
        child = node.get(part)
        if not isinstance(child, dict):
            raise PromotionError(f"bind parent does not exist: {part}")
        node = child
    node[parts[-1]] = value


def promote_asset(
    repo_root,
    customer,
    slot,
    alt,
    caption,
    source_label,
    bind,
    build=True,
    cleanup=True,
):
    repo_root = Path(repo_root)
    customer = _slug(customer, "customer")
    slot = _slug(slot, "slot")
    alt = _nonempty(alt, "alt")
    caption = _nonempty(caption, "caption")
    source_label = _nonempty(source_label, "source_label")
    bind = _nonempty(bind, "bind")

    inbox = repo_root / "asset-inbox" / customer / slot
    uploaded = _uploaded_files(inbox)
    if len(uploaded) != 1:
        raise PromotionError(
            f"upload slot must contain exactly one asset; found {len(uploaded)} in {inbox}"
        )

    source = uploaded[0]
    suffix = source.suffix.lower()
    if suffix not in ALLOWED_SUFFIXES:
        raise PromotionError(f"unsupported asset type: {suffix or '<none>'}")

    content_path = repo_root / "engage" / "customers" / customer / "content.json"
    if not content_path.is_file():
        raise PromotionError(f"customer content not found: {content_path}")

    try:
        payload = json.loads(content_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PromotionError(f"cannot read customer content: {exc}") from exc

    if payload.get("customer", {}).get("slug") != customer:
        raise PromotionError("content customer slug does not match upload slot")
    if payload.get("visibility") != "public":
        raise PromotionError("customer content must be explicitly public")
    if not isinstance(payload.get("assets"), list):
        raise PromotionError("customer content must contain an assets array")

    target = repo_root / "engage" / "customers" / customer / "assets" / f"{slot}{suffix}"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)

    public_path = f"/engage/customers/{customer}/assets/{slot}{suffix}"
    slot_prefix = f"/engage/customers/{customer}/assets/{slot}."
    payload["assets"] = [
        item for item in payload["assets"]
        if not (isinstance(item, dict) and str(item.get("path", "")).startswith(slot_prefix))
    ]
    payload["assets"].append({
        "type": "image",
        "path": public_path,
        "alt": alt,
        "caption": caption,
        "source": source_label,
        "public": True,
    })
    _bind(payload, bind, public_path)
    content_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    if build:
        from engage._core.generate import build_page
        build_page(content_path, repo_root=repo_root)

    if cleanup:
        source.unlink()

    return target


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Promote one asset from a scoped upload slot into a customer engagement page."
    )
    parser.add_argument("customer")
    parser.add_argument("slot")
    parser.add_argument("--alt", required=True)
    parser.add_argument("--caption", required=True)
    parser.add_argument("--source", dest="source_label", required=True)
    parser.add_argument("--bind", required=True, help="Dotted content path, e.g. hero.image")
    parser.add_argument("--keep-inbox", action="store_true")
    args = parser.parse_args(argv)

    repo_root = Path(__file__).resolve().parents[2]
    try:
        target = promote_asset(
            repo_root=repo_root,
            customer=args.customer,
            slot=args.slot,
            alt=args.alt,
            caption=args.caption,
            source_label=args.source_label,
            bind=args.bind,
            build=True,
            cleanup=not args.keep_inbox,
        )
    except PromotionError as exc:
        parser.error(str(exc))
    print(target.relative_to(repo_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
