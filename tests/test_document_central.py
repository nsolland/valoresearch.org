import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "library" / "document-central" / "registry.json"
PAGE = ROOT / "library" / "document-central" / "index.html"


def load_registry():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def test_registry_shape_and_unique_ids():
    data = load_registry()
    assert data["version"] == "1.0.0"
    ids = []
    for key in ("sources", "evidence", "claims", "analysis", "artifacts"):
        assert isinstance(data[key], list)
        ids.extend(row["id"] for row in data[key])
    assert len(ids) == len(set(ids))


def test_id_contracts_and_references_resolve():
    data = load_registry()
    source_ids = {x["id"] for x in data["sources"]}
    evidence_ids = {x["id"] for x in data["evidence"]}
    claim_ids = {x["id"] for x in data["claims"]}
    analysis_ids = {x["id"] for x in data["analysis"]}

    assert all(re.fullmatch(r"SRC-\d{4}-[A-Z0-9]+-\d{3}", x) for x in source_ids)
    assert all(re.fullmatch(r"EVD-\d{4}-[A-Z0-9]+-\d{3}", x) for x in evidence_ids)
    assert all(re.fullmatch(r"CLM-\d{4}", x) for x in claim_ids)
    assert all(re.fullmatch(r"ANL-\d{4}", x) for x in analysis_ids)

    for item in data["evidence"]:
        assert item["source_id"] in source_ids
    for item in data["claims"]:
        for ref in item["supporting_evidence"] + item["contradicting_evidence"]:
            assert ref in evidence_ids
    for item in data["analysis"]:
        assert item["classification"] == "VALO inference"
        assert all(ref in claim_ids for ref in item["basis_claims"])
        assert all(ref in evidence_ids for ref in item["basis_evidence"])
    for item in data["artifacts"]:
        assert all(ref in claim_ids for ref in item["depends_on_claims"])
        assert all(ref in analysis_ids for ref in item["depends_on_analysis"])


def test_independent_support_count_is_derived_from_source_families():
    data = load_registry()
    source_by_id = {x["id"]: x for x in data["sources"]}
    evidence_by_id = {x["id"]: x for x in data["evidence"]}
    for claim in data["claims"]:
        families = {
            source_by_id[evidence_by_id[ref]["source_id"]]["independence_family"]
            for ref in claim["supporting_evidence"]
        }
        assert claim["independent_support_count"] == len(families)


def test_public_page_exposes_provenance_contract():
    page = PAGE.read_text(encoding="utf-8")
    for token in ("Document Central", "Source", "Evidence", "Claim", "Analysis", "Artifact", "registry.json", "Evidence is not inference"):
        assert token in page
