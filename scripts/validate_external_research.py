#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

DOCUMENT_TYPES = {"paper","book","report","standard","regulatory-report","industry-report","working-paper","thesis","article","other"}
REDISTRIBUTION = {"allowed","link-only","unknown"}
STATUSES = {"indexed","needs-metadata","needs-source","excluded"}
REQUIRED_KEYS = {
    "id","title","authors","organization","year","date","document_type","topics","keywords",
    "summary","principal_relevance","source_url","doi","isbn","license","redistribution",
    "local_file_name","content_hash","duplicate_of","status","notes"
}


def validate_records(records, topics):
    errors = []
    ids = set()
    urls = {}
    for i, r in enumerate(records):
        prefix = f"record[{i}]"
        missing = REQUIRED_KEYS - set(r)
        if missing:
            errors.append(f"{prefix}: missing keys: {', '.join(sorted(missing))}")
            continue
        rid = r["id"]
        if not isinstance(rid, str) or not rid.strip():
            errors.append(f"{prefix}: id must be non-empty string")
        elif rid in ids:
            errors.append(f"{prefix}: duplicate id: {rid}")
        ids.add(rid)
        if not isinstance(r["title"], str) or not r["title"].strip():
            errors.append(f"{prefix}: title must be non-empty string")
        if r["year"] is not None and not isinstance(r["year"], int):
            errors.append(f"{prefix}: year must be integer or null")
        if r["document_type"] not in DOCUMENT_TYPES:
            errors.append(f"{prefix}: invalid document_type: {r['document_type']}")
        if r["redistribution"] not in REDISTRIBUTION:
            errors.append(f"{prefix}: invalid redistribution: {r['redistribution']}")
        if r["status"] not in STATUSES:
            errors.append(f"{prefix}: invalid status: {r['status']}")
        if not isinstance(r["authors"], list):
            errors.append(f"{prefix}: authors must be an array")
        if not isinstance(r["topics"], list) or any(t not in topics for t in r["topics"]):
            errors.append(f"{prefix}: unknown or invalid topic")
        if not isinstance(r["keywords"], list):
            errors.append(f"{prefix}: keywords must be an array")
        if r["redistribution"] == "allowed" and not (r["license"] or r["notes"]):
            errors.append(f"{prefix}: allowed redistribution requires license or provenance note")
        url = r["source_url"]
        if url is not None:
            parsed = urlparse(url)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                errors.append(f"{prefix}: source_url must be absolute http(s) URL or null")
            elif url in urls and urls[url] != rid:
                errors.append(f"{prefix}: duplicate source_url assigned to unrelated records: {url}")
            else:
                urls[url] = rid
    return errors


def main():
    root = Path(__file__).resolve().parents[1]
    topics_doc = json.loads((root / "data/research/topics.json").read_text())
    corpus_doc = json.loads((root / "data/research/external-research.json").read_text())
    topics = {t["id"] for t in topics_doc["topics"]}
    records = corpus_doc["records"]
    errors = validate_records(records, topics)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"validated {len(records)} external research records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
