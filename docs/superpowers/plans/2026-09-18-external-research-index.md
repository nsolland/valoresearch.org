# External Research Index Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a canonical, validated external-research index from the user's collected third-party research, expose it through a searchable Principal library, and keep external sources clearly separated from VALO-authored publications.

**Architecture:** Store the canonical external corpus and topic taxonomy as static JSON in the public repository. Validate those files with a dependency-free Python validator and unittest suite, then render the Principal library directly from the JSON using static HTML/CSS/JavaScript. ChatGPT Library is the ingestion source; the repository stores bibliographic metadata and source links, not third-party PDF binaries unless redistribution is explicitly justified.

**Tech Stack:** Static GitHub Pages HTML/CSS/JavaScript; JSON data files; Python 3 standard library (`json`, `urllib.parse`, `unittest`, `pathlib`) for validation/tests. No build system, database, server-side search, GitHub Actions, external deployment service, or new runtime dependency.

**Spec:** `docs/superpowers/specs/2026-09-18-external-research-index-design.md`

## Global Constraints

- `main` is the production branch; publishing is triggered by merge/push to `main`.
- Do not add GitHub Actions, CI deployment workflows, external build services, or another hosting control plane.
- Do not place credentials, private claims, internal application code, confidential/NDA material, patent drafts, partner-private material, or runtime secrets in this public repository.
- Do not call the work live until the canonical production URL returns the expected content.
- External sources must never be visually presented as VALO-authored research.
- Unknown or uncertain redistribution rights default to metadata/link-only; do not commit third-party binaries without explicit license/provenance evidence.
- Keep the taxonomy deliberately small; add a topic only when repeated material does not fit existing categories.
- No citation graph or backend is required in v1.

---

## File Structure

- Create `data/research/topics.json` — controlled topic taxonomy and display labels.
- Create `data/research/schema.json` — machine-readable contract documenting required/optional record fields and enums.
- Create `data/research/external-research.json` — canonical external corpus, one record per unique source.
- Create `scripts/validate_external_research.py` — deterministic validator for taxonomy and corpus invariants.
- Create `tests/test_external_research.py` — standard-library tests for valid data and each failure mode.
- Create `principal/library/index.html` — unified Principal knowledge-library landing page separating VALO and external research.
- Create `principal/library/external/index.html` — external-research browser surface.
- Create `principal/library/library.css` — shared library visual system.
- Create `principal/library/external/library.js` — client-side load/render/search/filter logic for external records.
- Modify `principal/index.html` — add canonical navigation/card into the Principal library.
- Modify `publications/index.html` only if needed to add a reciprocal “Principal library” link; do not mix external records into VALO Publications.
- Create `.claims/external-research-index-v1` — scope/ownership marker following existing repository convention.

---

### Task 1: Establish the taxonomy and canonical data contract

**Files:**
- Create: `data/research/topics.json`
- Create: `data/research/schema.json`
- Create: `.claims/external-research-index-v1`

**Interfaces:**
- Consumes: the approved design spec.
- Produces: topic IDs and record enums consumed by the corpus, validator, tests, and UI.

- [ ] **Step 1: Create the claim file**

Write `.claims/external-research-index-v1` with this content:

```text
owner: external-research-index
purpose: Canonical Principal index of collected third-party research
public_surface: /principal/library/
canonical_data:
  - data/research/topics.json
  - data/research/schema.json
  - data/research/external-research.json
excludes:
  - confidential/NDA/trade-secret material
  - patent and filing material
  - partner/customer-private material
  - personal documents
  - unlicensed third-party binary mirroring
```

- [ ] **Step 2: Create the controlled topic taxonomy**

Write `data/research/topics.json` exactly as a JSON object with a `version` and `topics` array. Each topic object has `id`, `label`, and `description`. Seed these IDs:

```json
{
  "version": 1,
  "topics": [
    {"id":"agentic-systems","label":"Agentic Systems","description":"Agents, orchestration, multi-agent systems and autonomous workflows."},
    {"id":"governance-authority","label":"Governance & Authority","description":"Mandate, delegation, decision rights, execution authority and governance boundaries."},
    {"id":"edge-distributed-compute","label":"Edge & Distributed Compute","description":"Edge inference, fog, local compute, distributed execution and placement."},
    {"id":"network-intelligence","label":"Network Intelligence","description":"Relational, collective, distributed and network-level intelligence."},
    {"id":"human-ai-systems","label":"Human–AI Systems","description":"Human oversight, interaction, teaming, literacy and socio-technical systems."},
    {"id":"security-resilience","label":"Security & Resilience","description":"Security, cyber resilience, failure containment and adversarial operation."},
    {"id":"regulation-policy","label":"Regulation & Policy","description":"Law, regulation, public policy, standards and institutional governance."},
    {"id":"economics-markets","label":"Economics & Markets","description":"Markets, investment, productivity, industrial structure and adoption economics."},
    {"id":"energy-compute","label":"Energy & Compute","description":"Compute infrastructure, energy demand, capacity and resource constraints."},
    {"id":"software-systems","label":"Software Systems","description":"Software architecture, synthesis, lifecycle, runtime systems and tooling."},
    {"id":"education-learning","label":"Education & Learning","description":"Education, learning systems, pedagogy and capability development."},
    {"id":"identity-access","label":"Identity & Access","description":"Identity, authentication, authorization, access control and delegated rights."},
    {"id":"evidence-verification","label":"Evidence & Verification","description":"Evidence quality, provenance, validation, reproducibility and verification."},
    {"id":"organizational-design","label":"Organizational Design","description":"Roles, operating models, management structure and human-agent organization."},
    {"id":"finance-monetary-systems","label":"Finance & Monetary Systems","description":"Payments, banking, stablecoins, monetary policy and financial infrastructure."}
  ]
}
```

- [ ] **Step 3: Create the machine-readable schema contract**

Write `data/research/schema.json` with required fields `id`, `title`, `authors`, `organization`, `year`, `date`, `document_type`, `topics`, `keywords`, `summary`, `principal_relevance`, `source_url`, `doi`, `isbn`, `license`, `redistribution`, `local_file_name`, `content_hash`, `duplicate_of`, `status`, and `notes`; enum values:

```json
{
  "document_type": ["paper","book","report","standard","regulatory-report","industry-report","working-paper","thesis","article","other"],
  "redistribution": ["allowed","link-only","unknown"],
  "status": ["indexed","needs-metadata","needs-source","excluded"]
}
```

The schema must document that nullable bibliographic fields may be `null`, while `id`, `title`, `authors`, `topics`, `keywords`, `summary`, `principal_relevance`, `redistribution`, and `status` remain structurally present.

- [ ] **Step 4: Validate the JSON syntax locally**

Run:

```bash
python -m json.tool data/research/topics.json >/dev/null
python -m json.tool data/research/schema.json >/dev/null
```

Expected: both commands exit `0` with no stderr.

- [ ] **Step 5: Commit Task 1**

```bash
git add .claims/external-research-index-v1 data/research/topics.json data/research/schema.json
git commit -m "feat: define external research taxonomy and schema"
```

---

### Task 2: Implement deterministic corpus validation first

**Files:**
- Create: `scripts/validate_external_research.py`
- Create: `tests/test_external_research.py`
- Create temporarily empty/minimal: `data/research/external-research.json`

**Interfaces:**
- Consumes: `data/research/topics.json`, `data/research/schema.json`, and the external corpus.
- Produces: CLI exit code `0` for valid data, `1` for invalid data; importable `validate_records(records, topics)` returning a list of human-readable error strings.

- [ ] **Step 1: Write failing tests for the validation contract**

Create `tests/test_external_research.py` using `unittest`. It must cover at least:

```python
import unittest
from scripts.validate_external_research import validate_records

TOPICS = {"agentic-systems", "governance-authority"}


def record(**overrides):
    base = {
        "id": "example-paper",
        "title": "Example Paper",
        "authors": ["A. Researcher"],
        "organization": None,
        "year": 2026,
        "date": "2026-01-01",
        "document_type": "paper",
        "topics": ["agentic-systems"],
        "keywords": ["agents"],
        "summary": "Factual summary.",
        "principal_relevance": "Relevant to agent-system design.",
        "source_url": "https://example.org/paper",
        "doi": None,
        "isbn": None,
        "license": None,
        "redistribution": "link-only",
        "local_file_name": "paper.pdf",
        "content_hash": None,
        "duplicate_of": None,
        "status": "indexed",
        "notes": None
    }
    base.update(overrides)
    return base


class ExternalResearchValidationTests(unittest.TestCase):
    def test_valid_record_passes(self):
        self.assertEqual(validate_records([record()], TOPICS), [])

    def test_duplicate_id_fails(self):
        errors = validate_records([record(), record()], TOPICS)
        self.assertTrue(any("duplicate id" in e.lower() for e in errors))

    def test_missing_title_fails(self):
        errors = validate_records([record(title="")], TOPICS)
        self.assertTrue(any("title" in e.lower() for e in errors))

    def test_non_integer_year_fails(self):
        errors = validate_records([record(year="2026")], TOPICS)
        self.assertTrue(any("year" in e.lower() for e in errors))

    def test_unknown_topic_fails(self):
        errors = validate_records([record(topics=["not-a-topic"])], TOPICS)
        self.assertTrue(any("topic" in e.lower() for e in errors))

    def test_invalid_redistribution_fails(self):
        errors = validate_records([record(redistribution="public")], TOPICS)
        self.assertTrue(any("redistribution" in e.lower() for e in errors))

    def test_invalid_status_fails(self):
        errors = validate_records([record(status="done")], TOPICS)
        self.assertTrue(any("status" in e.lower() for e in errors))

    def test_allowed_requires_license_or_provenance_note(self):
        errors = validate_records([record(redistribution="allowed", license=None, notes=None)], TOPICS)
        self.assertTrue(any("allowed" in e.lower() for e in errors))

    def test_same_source_url_for_unrelated_records_fails(self):
        second = record(id="another-paper", title="Another Paper")
        errors = validate_records([record(), second], TOPICS)
        self.assertTrue(any("source_url" in e.lower() for e in errors))
```

- [ ] **Step 2: Run tests and verify they fail because validator is absent**

Run:

```bash
python -m unittest tests.test_external_research -v
```

Expected: import/module failure for `scripts.validate_external_research`.

- [ ] **Step 3: Implement the minimal validator**

Create `scripts/validate_external_research.py` with:

```python
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
```

Create `data/research/external-research.json` initially as:

```json
{"version":1,"generated_at":"2026-09-18","records":[]}
```

- [ ] **Step 4: Run validator tests**

```bash
python -m unittest tests.test_external_research -v
```

Expected: all tests PASS.

- [ ] **Step 5: Run validator against the empty seed corpus**

```bash
python scripts/validate_external_research.py
```

Expected: `validated 0 external research records` and exit `0`.

- [ ] **Step 6: Commit Task 2**

```bash
git add scripts/validate_external_research.py tests/test_external_research.py data/research/external-research.json
git commit -m "test: add external research index validation"
```

---

### Task 3: Inventory and classify the existing external Library corpus

**Files:**
- Modify: `data/research/external-research.json`

**Interfaces:**
- Consumes: ChatGPT Library PDFs/documents, the taxonomy, validator contract, and the exclusion rules.
- Produces: one canonical public-safe metadata record per unique external source, with local duplicate provenance captured without public duplication.

- [ ] **Step 1: Enumerate the Library corpus completely**

Use the Library file listing with PDF/document filtering and pagination until no `next_cursor` remains. Build a working inventory with at least: file ID, filename, creation date, and size. Do not assume semantic search alone is complete.

- [ ] **Step 2: Separate obvious non-candidates before bibliographic work**

Exclude from external-public indexing when content or filename identifies any of:

```text
VALO-authored releases already represented in /publications/
REHT confidential/NDA/trade-secret suite
patent drafts / USPTO / filing / invention disclosure material
partner/customer-private decks or proposals
personal/private documents
```

Do not delete these Library files; only omit them from the public external corpus.

- [ ] **Step 3: Resolve generic filenames to real bibliographic identities**

For every remaining generic filename such as `file_<uuid>.pdf`, read enough parsed text to establish title, authors/organization, year, and document type. If metadata cannot be established, create a record only when public indexing is still safe, with `status: "needs-metadata"` and conservative `redistribution: "unknown"`.

- [ ] **Step 4: Deduplicate**

For each candidate apply:

```text
1. Exact content hash match, when local bytes are materialized => duplicate.
2. Same normalized title + author/organization + year => probable duplicate.
3. Distinct versions/revisions remain separate when content/version differs materially.
```

Only one canonical record is public. Put duplicate local filenames in the canonical record `notes`; use `duplicate_of` only when a separate record must remain for explicit version/provenance reasons.

- [ ] **Step 5: Resolve canonical source links**

Prefer DOI/publisher/government/arXiv/institutional repository URLs. Do not use random mirrors as canonical sources. If no trustworthy source can be established, use `source_url: null`, `status: "needs-source"`, and `redistribution: "unknown"`.

- [ ] **Step 6: Seed at least the already-identified known external sources**

The corpus must include canonical records for these known items if confirmed by Library content:

```text
Sumsub — Stablecoin compliance in 2026: which rules apply to your business
Fivos Papadimitriou — Spatial Artificial Intelligence
UK Parliament Joint Committee on Human Rights — Human Rights and the Regulation of AI
Standard Chartered — The Islamic Finance Connector Era
Kristin J. Forbes / MIT Sloan — The Art of Monetary Policy: Lessons From Sun Tzu for Central Banks
```

Assign controlled topics based on actual content, not filename.

- [ ] **Step 7: Run validation after each corpus batch**

```bash
python scripts/validate_external_research.py
python -m unittest tests.test_external_research -v
```

Expected: both exit `0`.

- [ ] **Step 8: Commit Task 3**

```bash
git add data/research/external-research.json
git commit -m "data: index existing external research corpus"
```

---

### Task 4: Build the external-research browser with failing UI/data tests first

**Files:**
- Create: `principal/library/library.css`
- Create: `principal/library/external/index.html`
- Create: `principal/library/external/library.js`
- Create: `tests/test_principal_library_static.py`

**Interfaces:**
- Consumes: `/data/research/external-research.json` and `/data/research/topics.json`.
- Produces: static external-research page with search, topic, type, and year filtering; no backend.

- [ ] **Step 1: Write failing static contract tests**

Create `tests/test_principal_library_static.py`:

```python
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PrincipalLibraryStaticTests(unittest.TestCase):
    def test_external_page_has_required_controls_and_script(self):
        html = (ROOT / "principal/library/external/index.html").read_text()
        for token in [
            'id="research-search"',
            'id="topic-filter"',
            'id="type-filter"',
            'id="year-filter"',
            'id="research-results"',
            'src="/principal/library/external/library.js"'
        ]:
            self.assertIn(token, html)

    def test_external_script_loads_canonical_json(self):
        js = (ROOT / "principal/library/external/library.js").read_text()
        self.assertIn('/data/research/external-research.json', js)
        self.assertIn('/data/research/topics.json', js)
        self.assertIn('principal_relevance', js)
        self.assertIn('source_url', js)

    def test_no_external_pdf_binary_paths_are_hardcoded(self):
        html = (ROOT / "principal/library/external/index.html").read_text()
        js = (ROOT / "principal/library/external/library.js").read_text()
        self.assertNotIn('.pdf"', html.lower())
        self.assertNotIn('.pdf"', js.lower())
```

- [ ] **Step 2: Run tests and verify they fail because page files do not yet exist**

```bash
python -m unittest tests.test_principal_library_static -v
```

Expected: file-not-found failures.

- [ ] **Step 3: Build the external page shell**

Create `principal/library/external/index.html` with:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>External Research · Principal Network</title>
  <meta name="description" content="External research indexed by Principal Network for context, validation, challenge and technical reference.">
  <link rel="stylesheet" href="/principal/library/library.css">
</head>
<body>
  <header class="library-nav">
    <a href="/principal/">Principal Network</a>
    <nav><a href="/principal/library/">Library</a><a href="/publications/">VALO Research</a></nav>
  </header>
  <main class="library-shell">
    <section class="library-hero">
      <div class="eyebrow">Principal knowledge library</div>
      <h1>External Research</h1>
      <p>Third-party research collected for comparison, evidence, challenge and technical reference. These works are not VALO publications.</p>
    </section>
    <section class="controls" aria-label="Research filters">
      <input id="research-search" type="search" placeholder="Search title, author, organization or keyword">
      <select id="topic-filter"><option value="">All topics</option></select>
      <select id="type-filter"><option value="">All types</option></select>
      <select id="year-filter"><option value="">All years</option></select>
    </section>
    <section><p id="result-count" aria-live="polite"></p><div id="research-results" class="research-grid"></div></section>
  </main>
  <script src="/principal/library/external/library.js"></script>
</body>
</html>
```

- [ ] **Step 4: Add the shared visual system**

Create `principal/library/library.css` using the existing Principal palette (`#f3efe7`, `#163c31`, `#c79b45`, `#151515`) and responsive card/filter layouts. Required classes: `.library-nav`, `.library-shell`, `.library-hero`, `.eyebrow`, `.controls`, `.research-grid`, `.research-card`, `.meta`, `.topics`, `.topic`, `.relevance`, `.source-link`, `.empty-state`.

- [ ] **Step 5: Implement data loading and client-side filtering**

Create `principal/library/external/library.js` with these exact data-flow functions:

```javascript
const CORPUS_URL = '/data/research/external-research.json';
const TOPICS_URL = '/data/research/topics.json';

async function loadLibraryData() {
  const [corpusResponse, topicsResponse] = await Promise.all([fetch(CORPUS_URL), fetch(TOPICS_URL)]);
  if (!corpusResponse.ok || !topicsResponse.ok) throw new Error('Unable to load research index');
  return { corpus: await corpusResponse.json(), topics: await topicsResponse.json() };
}

function normalizedText(record) {
  return [record.title, ...(record.authors || []), record.organization, ...(record.keywords || []), record.summary, record.principal_relevance]
    .filter(Boolean).join(' ').toLowerCase();
}

function filterRecords(records, state) {
  const q = state.query.trim().toLowerCase();
  return records.filter(record => {
    if (record.status === 'excluded') return false;
    if (q && !normalizedText(record).includes(q)) return false;
    if (state.topic && !(record.topics || []).includes(state.topic)) return false;
    if (state.type && record.document_type !== state.type) return false;
    if (state.year && String(record.year ?? '') !== state.year) return false;
    return true;
  });
}
```

The same file must render cards with title, author/organization line, year/type metadata, topic chips, `summary`, `principal_relevance` under a visible “Why it matters” label, and a source link only when `source_url` is non-null. Render no PDF/local-file download links.

- [ ] **Step 6: Run UI/static contract tests**

```bash
python -m unittest tests.test_principal_library_static -v
```

Expected: PASS.

- [ ] **Step 7: Commit Task 4**

```bash
git add principal/library/library.css principal/library/external/index.html principal/library/external/library.js tests/test_principal_library_static.py
git commit -m "feat: add Principal external research browser"
```

---

### Task 5: Build the unified Principal library landing page and connect navigation

**Files:**
- Create: `principal/library/index.html`
- Modify: `principal/index.html`
- Modify: `tests/test_principal_library_static.py`

**Interfaces:**
- Consumes: existing VALO publication URLs and the external library surface.
- Produces: one Principal entry point with two clearly separated knowledge classes.

- [ ] **Step 1: Add failing navigation tests**

Extend `tests/test_principal_library_static.py`:

```python
    def test_library_landing_separates_valo_and_external(self):
        html = (ROOT / "principal/library/index.html").read_text()
        self.assertIn('VALO Research', html)
        self.assertIn('External Research', html)
        self.assertIn('href="/publications/"', html)
        self.assertIn('href="/principal/library/external/"', html)

    def test_principal_home_links_to_library(self):
        html = (ROOT / "principal/index.html").read_text()
        self.assertIn('href="/principal/library/"', html)
```

- [ ] **Step 2: Run tests and confirm the new landing-page test fails**

```bash
python -m unittest tests.test_principal_library_static -v
```

Expected: failure because `principal/library/index.html` does not exist and Principal has no canonical library link.

- [ ] **Step 3: Create the unified landing page**

Create `principal/library/index.html` using `library.css`, with two large sections/cards:

```html
<a class="library-class" href="/publications/">
  <div class="eyebrow">VALO-authored</div>
  <h2>VALO Research</h2>
  <p>Reports, working papers, technical notes and released research artifacts produced by VALO Research.</p>
</a>
<a class="library-class" href="/principal/library/external/">
  <div class="eyebrow">Third-party sources</div>
  <h2>External Research</h2>
  <p>Independent papers, books, regulatory reports, industry research and technical reference material indexed by Principal.</p>
</a>
```

The page must state explicitly that indexing an external source does not imply endorsement or VALO authorship.

- [ ] **Step 4: Connect Principal home without disturbing its existing research cards**

Modify `principal/index.html` so the research section contains one visible `Open knowledge library` link to `/principal/library/`. Keep the existing released VALO Research cards intact.

- [ ] **Step 5: Run static tests**

```bash
python -m unittest tests.test_principal_library_static -v
```

Expected: PASS.

- [ ] **Step 6: Commit Task 5**

```bash
git add principal/library/index.html principal/index.html tests/test_principal_library_static.py
git commit -m "feat: connect Principal knowledge library"
```

---

### Task 6: Add explicit public-safety regression checks

**Files:**
- Modify: `tests/test_external_research.py`
- Modify: `scripts/validate_external_research.py`

**Interfaces:**
- Consumes: canonical corpus records.
- Produces: failure if obvious confidential/patent/private markers leak into public records.

- [ ] **Step 1: Write failing leak-detection tests**

Add tests using records whose title/notes/local filename contain these markers:

```python
BLOCKED_MARKERS = [
    "confidential",
    "nda required",
    "trade secret",
    "do not distribute",
    "patent draft",
    "invention disclosure"
]
```

Test that a record with `status != "excluded"` and any blocked marker yields an error, while an `excluded` record may retain the marker for traceability if such records are ever stored.

- [ ] **Step 2: Run tests and verify they fail**

```bash
python -m unittest tests.test_external_research -v
```

Expected: new blocked-marker test fails.

- [ ] **Step 3: Add blocked-marker validation**

Extend `validate_records()` so it builds a lowercase string from `title`, `local_file_name`, and `notes`; when `status != "excluded"`, reject any occurrence of the blocked markers above.

- [ ] **Step 4: Run full validation suite**

```bash
python -m unittest tests.test_external_research tests.test_principal_library_static -v
python scripts/validate_external_research.py
```

Expected: all tests PASS and validator exits `0`.

- [ ] **Step 5: Commit Task 6**

```bash
git add scripts/validate_external_research.py tests/test_external_research.py
git commit -m "test: prevent private research leakage"
```

---

### Task 7: Final corpus audit, static-site verification, PR and production verification

**Files:**
- Potentially modify: `data/research/external-research.json`
- Potentially modify: `principal/library/*`
- No new runtime/deployment files.

**Interfaces:**
- Consumes: all prior tasks.
- Produces: merge-ready static site with validated corpus and verified production paths.

- [ ] **Step 1: Run the complete local verification**

```bash
python -m json.tool data/research/topics.json >/dev/null
python -m json.tool data/research/schema.json >/dev/null
python -m json.tool data/research/external-research.json >/dev/null
python -m unittest tests.test_external_research tests.test_principal_library_static -v
python scripts/validate_external_research.py
```

Expected: every command exits `0`.

- [ ] **Step 2: Audit the public corpus manually for class-boundary errors**

Search the canonical corpus for these exact strings and variants:

```text
VALO RESEARCH - CONFIDENTIAL
NDA REQUIRED
TRADE SECRET
DO NOT DISTRIBUTE
USPTO
patent draft
invention disclosure
```

Expected: no non-excluded public record contains these markers.

- [ ] **Step 3: Verify no third-party PDF binaries were added accidentally**

Inspect the branch diff. Expected new external-research artifacts are JSON, Python, HTML, CSS, and JS only unless a separately reviewed source has explicit redistribution evidence. Any newly added external `.pdf` blocks merge until its license/provenance is documented.

- [ ] **Step 4: Open a PR against `main`**

PR body must state:

```text
- Canonical external corpus location
- Number of indexed unique external sources
- Number of duplicate local copies collapsed
- Number of records still needs-metadata / needs-source
- Confirmation that confidential/NDA/patent/private material is excluded
- Confirmation that no unlicensed third-party PDFs were mirrored
- Local verification commands and results
```

- [ ] **Step 5: Check repository status for the PR head**

Use the repository commit-status endpoint for the PR head. There is no required CI in this repo; absence of status checks is acceptable only after the local validation suite above passes.

- [ ] **Step 6: Merge only if the diff is limited to the planned public-safe files**

Use squash merge with the expected PR head SHA so the merge fails closed if the branch moved unexpectedly.

- [ ] **Step 7: Verify production after merge**

Fetch these canonical URLs after GitHub Pages has published the merge:

```text
https://valoresearch.org/principal/library/
https://valoresearch.org/principal/library/external/
https://valoresearch.org/data/research/external-research.json
https://valoresearch.org/data/research/topics.json
```

Expected:

```text
/principal/library/ => page contains "VALO Research" and "External Research"
/principal/library/external/ => page contains "External Research" and filter controls
external-research.json => valid JSON corpus
/topics.json => valid taxonomy JSON
```

Do not report the feature as live until all four production checks succeed.

- [ ] **Step 8: Report delivery evidence**

Return PR number, merge SHA, production URLs, indexed-source count, duplicate count, unresolved-metadata/source count, and validation result.
