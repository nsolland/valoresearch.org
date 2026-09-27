from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_exup_presents_black_box_execution_api():
    html = (ROOT / "exup/index.html").read_text()
    for marker in [
        "Black-box Execution API",
        "POST /v1/execute",
        '"workload_id": "invoice_extraction"',
        '"execution_class": "managed"',
        '"receipt_id"',
        "Private by design",
        "Candidate generation",
        "internal search history",
        "optimizer working state",
        "not exposed",
    ]:
        assert marker in html
    assert "public hosted endpoint" not in html.lower()


def test_access_page_explains_private_api_delivery():
    html = (ROOT / "exup/access/index.html").read_text()
    assert "Black-box Execution API" in html
    assert "private integration" in html
    assert "No optimizer internals are returned" in html
