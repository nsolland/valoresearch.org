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

    def test_confidential_marker_fails_for_public_record(self):
        errors = validate_records([record(notes="CONFIDENTIAL — NDA REQUIRED")], TOPICS)
        self.assertTrue(any("blocked marker" in e.lower() for e in errors))

    def test_do_not_distribute_marker_fails_for_public_record(self):
        errors = validate_records([record(summary="Internal analysis — DO NOT DISTRIBUTE")], TOPICS)
        self.assertTrue(any("blocked marker" in e.lower() for e in errors))

    def test_patent_marker_fails_for_public_record(self):
        errors = validate_records([record(title="Patent draft for new execution mechanism")], TOPICS)
        self.assertTrue(any("blocked marker" in e.lower() for e in errors))

    def test_excluded_record_may_carry_blocked_marker(self):
        errors = validate_records([record(status="excluded", notes="Trade secret — do not distribute")], TOPICS)
        self.assertFalse(any("blocked marker" in e.lower() for e in errors))


if __name__ == "__main__":
    unittest.main()
