import json
from pathlib import Path

import pytest

from engage._core.promote_asset import PromotionError, promote_asset


def make_customer(tmp_path, customer="acme"):
    inbox = tmp_path / "asset-inbox" / customer / "hero"
    inbox.mkdir(parents=True)
    (inbox / "UPLOAD_HERE.txt").write_text("upload here\n", encoding="utf-8")
    customer_dir = tmp_path / "engage" / "customers" / customer
    customer_dir.mkdir(parents=True)
    content = {
        "customer": {"slug": customer, "name": "ACME"},
        "visibility": "public",
        "hero": {"eyebrow": "Prepared for ACME", "title": "Title", "summary": "Summary"},
        "assets": [],
        "cta": {
            "title": "Next",
            "body": "Next step",
            "action": {"label": "Go", "href": "mailto:test@example.com"},
        },
    }
    (customer_dir / "content.json").write_text(json.dumps(content), encoding="utf-8")
    return inbox, customer_dir


def test_promotes_exactly_one_uploaded_asset_and_binds_hero(tmp_path):
    inbox, customer_dir = make_customer(tmp_path)
    source = inbox / "random-upload.png"
    source.write_bytes(b"exact-image-bytes")

    result = promote_asset(
        repo_root=tmp_path,
        customer="acme",
        slot="hero",
        alt="ACME hero",
        caption="ACME hero concept.",
        source_label="VALO Research / image generation",
        bind="hero.image",
        build=False,
    )

    target = tmp_path / "engage" / "customers" / "acme" / "assets" / "hero.png"
    assert target.read_bytes() == b"exact-image-bytes"
    assert result == target

    payload = json.loads((customer_dir / "content.json").read_text(encoding="utf-8"))
    assert payload["hero"]["image"] == "/engage/customers/acme/assets/hero.png"
    assert payload["assets"] == [{
        "type": "image",
        "path": "/engage/customers/acme/assets/hero.png",
        "alt": "ACME hero",
        "caption": "ACME hero concept.",
        "source": "VALO Research / image generation",
        "public": True,
    }]


def test_refuses_ambiguous_upload_slot(tmp_path):
    inbox, _ = make_customer(tmp_path)
    (inbox / "one.png").write_bytes(b"one")
    (inbox / "two.png").write_bytes(b"two")

    with pytest.raises(PromotionError, match="exactly one"):
        promote_asset(
            repo_root=tmp_path,
            customer="acme",
            slot="hero",
            alt="alt",
            caption="caption",
            source_label="source",
            bind="hero.image",
            build=False,
        )


def test_refuses_missing_upload(tmp_path):
    make_customer(tmp_path)
    with pytest.raises(PromotionError, match="exactly one"):
        promote_asset(
            repo_root=tmp_path,
            customer="acme",
            slot="hero",
            alt="alt",
            caption="caption",
            source_label="source",
            bind="hero.image",
            build=False,
        )
