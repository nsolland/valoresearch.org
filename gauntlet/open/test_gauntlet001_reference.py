from pathlib import Path
from gauntlet001_reference import simulate, TRIALS, contract_case_ids, canonical_digest


CONTRACT = Path(__file__).resolve().parents[1] / "GAUNTLET-001.json"


def test_reference_matches_public_contract():
    assert contract_case_ids(CONTRACT) == tuple(t.case_id for t in TRIALS)


def test_standing_permission_fails_revocation_and_drift():
    report = simulate("standing-demo", CONTRACT)
    assert report["simulated_result"] == "SIMULATED_FAIL"
    assert {"T02", "T03", "T04", "T05", "T06", "T07", "T08"} <= set(report["failure_cases"])
    assert any(o["unauthorized_effect"] for o in report["observations"])


def test_fresh_consequence_check_simulation():
    report = simulate("fresh-demo", CONTRACT)
    assert report["simulated_result"] == "SIMULATED_PASS"
    assert all(o["matching_expected"] for o in report["observations"])
    assert report["verification_grade"] == "NOT_INDEPENDENTLY_VERIFIED"


def test_deny_all_is_not_a_pass():
    report = simulate("deny-all-demo", CONTRACT)
    assert report["simulated_result"] == "SIMULATED_FAIL"
    assert "T01" in report["failure_cases"]
    assert report["observations"][0]["missed_legitimate"]


def test_deterministic_replay_report_digest():
    first = simulate("fresh-demo", CONTRACT)
    second = simulate("fresh-demo", CONTRACT)
    assert first == second
    report_digest = first.pop("report_digest")
    assert canonical_digest(first) == report_digest


def test_harness_observes_effect_independent_of_policy_claim():
    report = simulate("standing-demo", CONTRACT)
    revoked = next(x for x in report["observations"] if x["case_id"] == "T02")
    assert revoked["decision"] == "ALLOW"
    assert revoked["simulated_ledger_effect"] is True
    assert revoked["oracle_allows_effect"] is False
    assert revoked["unauthorized_effect"] is True
