#!/usr/bin/env python3
import html
import json
import re
import sys
from pathlib import Path

from .validate_assets import AssetValidationError, validate_manifest

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
ALLOWED_LINK_PREFIXES = ("/", "https://", "http://", "mailto:")


class EngagementBuildError(ValueError):
    pass


def _text(value, field):
    if not isinstance(value, str) or not value.strip():
        raise EngagementBuildError(f"{field} must be a non-empty string")
    return value.strip()


def _safe_href(value, field):
    href = _text(value, field)
    if not href.startswith(ALLOWED_LINK_PREFIXES):
        raise EngagementBuildError(f"{field} uses an unsupported link")
    return href


def _paragraphs(body):
    if isinstance(body, str):
        body = [body]
    if not isinstance(body, list) or not body:
        raise EngagementBuildError("section body must be a non-empty string or list")
    return "".join(f"<p>{html.escape(_text(p, 'body'))}</p>" for p in body)


def _cards(items, with_status=False):
    if not isinstance(items, list) or not items:
        raise EngagementBuildError("card section must contain at least one item")
    parts = []
    for idx, item in enumerate(items):
        if not isinstance(item, dict):
            raise EngagementBuildError(f"item[{idx}] must be an object")
        title = html.escape(_text(item.get("title"), f"item[{idx}].title"))
        body = html.escape(_text(item.get("body"), f"item[{idx}].body"))
        badge = ""
        if with_status and item.get("status") is not None:
            badge = f'<div class="status">{html.escape(_text(item["status"], f"item[{idx}].status"))}</div>'
        parts.append(f'<article class="card">{badge}<h3>{title}</h3><p>{body}</p></article>')
    return "".join(parts)


def _section(title, body, section_id):
    return (
        f'<section class="section" id="{html.escape(section_id)}">'
        f'<div class="wrap"><h2>{html.escape(title)}</h2>{body}</div></section>'
    )


def _declared_assets(payload, content_path, repo_root, slug):
    try:
        validate_manifest(content_path)
    except AssetValidationError as exc:
        raise EngagementBuildError(str(exc)) from exc

    declared = {}
    customer_root = f"/engage/customers/{slug}/assets/"
    for asset in payload["assets"]:
        path = asset["path"]
        if path.startswith("/engage/customers/") and not path.startswith(customer_root):
            raise EngagementBuildError(f"customer asset must belong to {slug}: {path}")
        disk_path = repo_root / path.lstrip("/")
        if not disk_path.is_file():
            raise EngagementBuildError(f"declared asset does not exist: {path}")
        declared[path] = asset
    return declared


def _render_media(asset):
    path = html.escape(asset["path"], quote=True)
    alt = html.escape(asset["alt"], quote=True)
    caption = html.escape(asset["caption"])
    kind = asset["type"].lower()
    if kind in {"image", "diagram", "screenshot", "logo", "background"}:
        media = f'<img src="{path}" alt="{alt}" loading="lazy">'
    else:
        media = f'<a class="asset-link" href="{path}">{alt}</a>'
    return f'<figure>{media}<figcaption>{caption}</figcaption></figure>'


def build_page(content_path, repo_root=None):
    content_path = Path(content_path)
    repo_root = Path(repo_root) if repo_root is not None else Path(__file__).resolve().parents[2]

    try:
        payload = json.loads(content_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EngagementBuildError(f"cannot read content.json: {exc}") from exc
    if not isinstance(payload, dict):
        raise EngagementBuildError("content root must be an object")

    customer = payload.get("customer")
    if not isinstance(customer, dict):
        raise EngagementBuildError("customer must be an object")
    slug = _text(customer.get("slug"), "customer.slug")
    if not SLUG_RE.fullmatch(slug):
        raise EngagementBuildError("customer.slug must be lowercase letters, numbers and hyphens")
    customer_name = _text(customer.get("name"), "customer.name")

    if payload.get("visibility") != "public":
        raise EngagementBuildError("visibility must be explicitly public")

    hero = payload.get("hero")
    if not isinstance(hero, dict):
        raise EngagementBuildError("hero must be an object")
    eyebrow = _text(hero.get("eyebrow"), "hero.eyebrow")
    title = _text(hero.get("title"), "hero.title")
    summary = _text(hero.get("summary"), "hero.summary")

    assets = payload.get("assets")
    if not isinstance(assets, list):
        raise EngagementBuildError("assets must be an array")
    declared = _declared_assets(payload, content_path, repo_root, slug)

    sections = []

    situation = payload.get("situation")
    if situation is not None:
        if not isinstance(situation, dict):
            raise EngagementBuildError("situation must be an object")
        sections.append(_section(
            _text(situation.get("title"), "situation.title"),
            f'<div class="prose">{_paragraphs(situation.get("body"))}</div>',
            "situation",
        ))

    theses = payload.get("theses")
    if theses is not None:
        sections.append(_section("What we believe", f'<div class="grid">{_cards(theses)}</div>', "theses"))

    demos = payload.get("demos")
    if demos is not None:
        if not isinstance(demos, list) or not demos:
            raise EngagementBuildError("demos must contain at least one item")
        rendered = []
        for idx, demo in enumerate(demos):
            if not isinstance(demo, dict):
                raise EngagementBuildError(f"demos[{idx}] must be an object")
            demo_title = html.escape(_text(demo.get("title"), f"demos[{idx}].title"))
            demo_body = html.escape(_text(demo.get("body"), f"demos[{idx}].body"))
            asset_path = demo.get("asset")
            media = ""
            if asset_path is not None:
                asset_path = _text(asset_path, f"demos[{idx}].asset")
                asset = declared.get(asset_path)
                if asset is None:
                    raise EngagementBuildError(f"demos[{idx}].asset must reference a declared public asset")
                media = _render_media(asset)
            link_html = ""
            if demo.get("link") is not None:
                link = demo["link"]
                if not isinstance(link, dict):
                    raise EngagementBuildError(f"demos[{idx}].link must be an object")
                label = html.escape(_text(link.get("label"), f"demos[{idx}].link.label"))
                href = html.escape(_safe_href(link.get("href"), f"demos[{idx}].link.href"), quote=True)
                link_html = f'<a class="button" href="{href}">{label}</a>'
            rendered.append(
                f'<article class="demo"><div><h3>{demo_title}</h3><p>{demo_body}</p>{link_html}</div>{media}</article>'
            )
        sections.append(_section("Demonstrators", "".join(rendered), "demos"))

    evidence = payload.get("evidence")
    if evidence is not None:
        sections.append(_section("Evidence", f'<div class="grid">{_cards(evidence, with_status=True)}</div>', "evidence"))

    proposal = payload.get("proposal")
    if proposal is not None:
        if not isinstance(proposal, dict):
            raise EngagementBuildError("proposal must be an object")
        sections.append(_section(
            _text(proposal.get("title"), "proposal.title"),
            f'<div class="prose">{_paragraphs(proposal.get("body"))}</div>',
            "proposal",
        ))

    questions = payload.get("questions")
    if questions is not None:
        if not isinstance(questions, list) or not questions:
            raise EngagementBuildError("questions must contain at least one item")
        q_html = "".join(f"<li>{html.escape(_text(q, 'question'))}</li>" for q in questions)
        sections.append(_section("Open questions", f'<ol class="questions">{q_html}</ol>', "questions"))

    cta = payload.get("cta")
    if not isinstance(cta, dict):
        raise EngagementBuildError("cta must be an object")
    action = cta.get("action")
    if not isinstance(action, dict):
        raise EngagementBuildError("cta.action must be an object")
    cta_title = html.escape(_text(cta.get("title"), "cta.title"))
    cta_body = html.escape(_text(cta.get("body"), "cta.body"))
    cta_label = html.escape(_text(action.get("label"), "cta.action.label"))
    cta_href = html.escape(_safe_href(action.get("href"), "cta.action.href"), quote=True)
    sections.append(
        f'<section class="cta" id="next"><div class="wrap"><h2>{cta_title}</h2>'
        f'<p>{cta_body}</p><a class="button primary" href="{cta_href}">{cta_label}</a></div></section>'
    )

    doc = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="index,follow">
<title>__CUSTOMER__ · VALO Research</title>
<meta name="description" content="__SUMMARY__">
<style>
:root{--bg:#f4f1ea;--ink:#111;--muted:#66625b;--line:#d7d0c6;--panel:#fffdf8;--accent:#203c31;--accent2:#c8ff70}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.5}
a{color:inherit}.wrap{width:min(1120px,calc(100% - 32px));margin:auto}.top{padding:24px 0;border-bottom:1px solid var(--line);font-size:13px;display:flex;justify-content:space-between;gap:24px}
.hero{padding:96px 0 78px;background:#0b0f10;color:white}.eyebrow{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent2);font-weight:800}
h1{font-size:clamp(48px,8vw,96px);line-height:.94;letter-spacing:-.06em;max-width:1000px;margin:18px 0 28px}.hero p{font-size:clamp(19px,2.4vw,27px);color:#bdc6c8;max-width:820px}
.section{padding:70px 0;border-top:1px solid var(--line)}h2{font-size:clamp(34px,5vw,58px);line-height:1;letter-spacing:-.045em;margin:0 0 30px}h3{font-size:24px;letter-spacing:-.03em;margin:0 0 10px}
.prose{max-width:840px;font-size:19px;color:var(--muted)}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.card{background:var(--panel);border:1px solid var(--line);padding:24px;min-height:180px}.card p,.demo p{color:var(--muted)}
.status{font-size:11px;text-transform:uppercase;letter-spacing:.12em;font-weight:800;margin-bottom:28px;color:var(--accent)}.demo{display:grid;grid-template-columns:1fr 1fr;gap:34px;padding:28px 0;border-top:1px solid var(--line);align-items:start}figure{margin:0}img{display:block;width:100%;height:auto;border:1px solid var(--line);background:white}figcaption{font-size:12px;color:var(--muted);margin-top:8px}
.button{display:inline-flex;margin-top:18px;padding:12px 18px;border:1px solid currentColor;text-decoration:none;font-weight:750}.primary{background:white;color:#111;border-color:white}.questions{max-width:840px;padding-left:24px;font-size:18px}.questions li+li{margin-top:12px}
.cta{padding:78px 0;background:var(--accent);color:white}.cta p{font-size:20px;max-width:760px}.asset-link{display:block;padding:18px;border:1px solid var(--line);background:white}
footer{padding:32px 0;font-size:12px;color:var(--muted);border-top:1px solid var(--line)}
@media(max-width:800px){.grid,.demo{grid-template-columns:1fr}.hero{padding:72px 0 58px}.section{padding:54px 0}}
</style>
</head>
<body>
<header class="hero"><div class="wrap"><div class="top"><strong>VALO Research</strong><span>Prepared for __CUSTOMER__</span></div><div style="padding-top:72px"><div class="eyebrow">__EYEBROW__</div><h1>__TITLE__</h1><p>__SUMMARY_TEXT__</p></div></div></header>
<main>__SECTIONS__</main>
<footer><div class="wrap">Customer-specific evidence and decision surface · VALO Research</div></footer>
</body>
</html>"""
    doc = (doc
        .replace("__CUSTOMER__", html.escape(customer_name))
        .replace("__SUMMARY__", html.escape(summary, quote=True))
        .replace("__EYEBROW__", html.escape(eyebrow))
        .replace("__TITLE__", html.escape(title))
        .replace("__SUMMARY_TEXT__", html.escape(summary))
        .replace("__SECTIONS__", "".join(sections))
    )

    output = repo_root / "engage" / slug / "index.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(doc, encoding="utf-8")
    return output


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print("usage: python -m engage._core.generate <content.json> [<content.json> ...]", file=sys.stderr)
        return 2
    repo_root = Path(__file__).resolve().parents[2]
    try:
        for item in args:
            output = build_page(item, repo_root=repo_root)
            print(output.relative_to(repo_root))
    except EngagementBuildError as exc:
        print(f"engagement build failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
