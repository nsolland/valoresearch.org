# External Research Index for Principal — Design

## Objective

Build a canonical external-research library for Principal that indexes third-party papers, books, regulatory reports, industry reports, and other source material already collected in the user's ChatGPT Library, while keeping VALO-authored publications separate.

The system must make external knowledge discoverable without turning Principal or the repository into an indiscriminate public PDF mirror.

## Core model

Principal becomes the presentation layer for two distinct knowledge classes:

1. **VALO Research** — VALO-authored reports, technical notes, working papers, explainers, and released research artifacts.
2. **External Research** — third-party material collected for research, comparison, validation, challenge, regulation, market context, or technical reference.

The repository is the canonical index. ChatGPT Library is an ingestion source / inbox, not the final public archive.

## Canonical location

Public surface:

- `/principal/library/` — unified knowledge library
- `/principal/library/external/` — external research index
- Existing `/publications/` remains the canonical VALO-authored publication surface.

Repository data:

- `data/research/external-research.json` — canonical structured index
- `data/research/topics.json` — controlled topic taxonomy
- `data/research/schema.json` — machine-readable validation contract for entries

The public HTML is rendered from or kept mechanically aligned with the canonical data. The JSON is the source of truth, not duplicated prose spread across pages.

## External research record

Each unique source receives one canonical record with these fields:

- `id` — stable slug / identifier
- `title`
- `authors` — array; organizations may be used where author names are absent
- `organization`
- `year`
- `date` — when known
- `document_type` — e.g. paper, book, report, standard, regulatory-report, industry-report, working-paper, thesis
- `topics` — controlled topic IDs
- `keywords` — free keywords
- `summary` — factual 1–3 sentence description
- `principal_relevance` — why the source matters to Principal / VALO research
- `source_url` — canonical publisher, DOI, repository, arXiv, government, or organization URL when known
- `doi` — when known
- `isbn` — when relevant
- `license` — when known
- `redistribution` — one of `allowed`, `link-only`, `unknown`
- `local_file_name` — source Library filename for traceability
- `content_hash` — SHA-256 of local bytes when the source can be materialized
- `duplicate_of` — canonical ID if a duplicate local copy exists
- `status` — `indexed`, `needs-metadata`, `needs-source`, or `excluded`
- `notes` — optional internal indexing note

## Taxonomy

Initial controlled topics:

- `agentic-systems`
- `governance-authority`
- `edge-distributed-compute`
- `network-intelligence`
- `human-ai-systems`
- `security-resilience`
- `regulation-policy`
- `economics-markets`
- `energy-compute`
- `software-systems`
- `education-learning`
- `identity-access`
- `evidence-verification`
- `organizational-design`
- `finance-monetary-systems`

The taxonomy is deliberately small. New topics are added only when repeated material does not fit existing categories.

## Ingestion and classification

Ingestion proceeds from existing Library PDFs and later from newly added material.

For each candidate:

1. Identify the actual document title and producer from parsed content, not filename alone.
2. Determine whether it is VALO-authored or external.
3. Exclude internal/partner/NDA/patent material from the external public index.
4. Detect local duplicates by title/metadata and, when materialized, SHA-256.
5. Normalize title, authors/organization, year, type, and topics.
6. Find a canonical source URL where possible.
7. Determine redistribution posture conservatively.
8. Add one canonical record plus duplicate references.

Unknown copyright or redistribution rights default to `link-only` or `unknown`; they are not committed as public PDF binaries merely because the user possesses a copy.

## Binary storage policy

The repository must not become a generic mirror of third-party PDFs.

A third-party PDF may be committed only when at least one of the following is true:

- explicit license permits redistribution;
- the publisher/author distributes it under a clearly permissive license;
- the document is public-domain government material and repository inclusion is appropriate.

Otherwise the repo stores metadata, source URL, and optional local content hash only.

If redistribution status is uncertain, use `redistribution: unknown` and do not commit the binary.

## Principal UI

`/principal/library/` presents:

- VALO Research
- External Research
- search field
- topic filters
- document-type filter
- year filter

External cards show:

- title
- authors / organization
- year
- type
- topics
- short summary
- "Why it matters" / Principal relevance
- source link when available

The first version may use lightweight client-side filtering over static JSON. No database, backend, account state, or server-side search is required for v1.

## Relationship to VALO research

VALO-authored research pages may later reference relevant external source IDs, but v1 does not require a full citation graph.

The external library is context and evidence infrastructure, not publication credit. External sources must never be visually presented as VALO-authored work.

## Initial corpus

The first indexing pass must cover the external PDFs already present in Library, including generically named files. Known examples already identified include:

- Sumsub — *Stablecoin compliance in 2026: which rules apply to your business*
- Fivos Papadimitriou — *Spatial Artificial Intelligence*
- UK Parliament Joint Committee on Human Rights — *Human Rights and the Regulation of AI*
- Standard Chartered — *The Islamic Finance Connector Era*
- Kristin J. Forbes / MIT Sloan — *The Art of Monetary Policy: Lessons From Sun Tzu for Central Banks*

The corpus is expected to include many more external documents than these examples. The indexing pass should paginate through the Library rather than assume the first result page is complete.

## Deduplication

Duplicates may arise from repeated downloads, filename variants such as `(1)`, or copied exports.

Canonicalization rules:

1. Exact SHA-256 match => duplicate.
2. Same normalized title + same author/organization + same year => probable duplicate.
3. Versioned papers with different content remain separate records or explicit versions; do not collapse them solely because titles match.

Only one canonical record is shown in Principal. Duplicate local filenames may be retained in metadata for provenance.

## Safety and exclusion rules

The following must not be surfaced publicly through this index:

- material marked confidential, NDA required, trade secret, do not distribute;
- patent drafts, filing material, counsel memos, invention disclosures;
- partner/customer-specific private proposals;
- private personal documents;
- external material whose public source or redistribution status cannot be established, except as metadata-only `unknown` records if indexing itself is safe.

## Validation

The data layer must fail on:

- duplicate canonical IDs;
- missing title;
- invalid year type;
- unknown topic IDs;
- invalid `redistribution` or `status` values;
- `allowed` binary entries without license/provenance evidence;
- duplicate exact source URLs assigned to unrelated records.

The page should degrade gracefully when a record lacks DOI, organization, source URL, or year.

## Delivery sequence

1. Create schema and controlled taxonomy.
2. Build an initial external corpus index from Library.
3. Add validation script/tests.
4. Build Principal library pages and client-side filters.
5. Connect Principal navigation.
6. Verify no confidential/internal/patent material was indexed publicly.
7. Merge only after corpus and UI validation pass.

## Success criteria

- External material is clearly separated from VALO publications.
- Principal exposes a searchable/filterable external research library.
- The index is canonical and machine-readable in repo.
- Generic filenames are resolved to real bibliographic identities where possible.
- Duplicate copies do not create duplicate public entries.
- Third-party PDFs are not mirrored without redistribution justification.
- Confidential, partner-specific, patent, and internal material remain excluded.
- The design supports continued ingestion of future Library research without restructuring the site.
