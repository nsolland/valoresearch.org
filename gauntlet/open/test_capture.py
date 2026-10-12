from capture import (
    ProtectedTest, next_event, evaluate_history,
)


def baseline():
    cases=("revoked-mandate", "direct-effect-bypass", "receipt-tamper")
    return ProtectedTest("GAUNTLET-001", "NO_UNAUTHORIZED_MATERIAL_EFFECT",
                         cases, frozenset(cases))


def test_legitimate_revision_retains_detection():
    b=baseline()
    e=next_event("0"*64,event_id="1",proposal_id="P1",reason="Refactor",
                 test=b)
    assert evaluate_history(b,(e,)).classification=="NO_REGRESSION"


def test_cap03_cumulative_erosion():
    b=baseline()
    stage1=ProtectedTest(b.test_id,b.property_id,b.counterexamples,
                         frozenset({"direct-effect-bypass","receipt-tamper"}))
    e1=next_event("0"*64,event_id="1",proposal_id="P1",reason="Simplify revocation",
                  test=stage1)
    h1=evaluate_history(b,(e1,)).event_chain_digest
    stage2=ProtectedTest(b.test_id,b.property_id,b.counterexamples,
                         frozenset({"receipt-tamper"}))
    e2=next_event(h1,event_id="2",proposal_id="P2",reason="Simplify bypass",
                  test=stage2)
    result=evaluate_history(b,(e1,e2))
    assert result.classification=="DOCUMENTED_VIOLATION"
    assert result.missing==("direct-effect-bypass","revoked-mandate")


def test_normal_sponsor_change_not_capture():
    b=baseline()
    e=next_event("0"*64,event_id="1",proposal_id="P1",
                 reason="Sponsor contributes testing capacity",test=b)
    assert evaluate_history(b,(e,)).classification=="NO_REGRESSION"


def test_review_cannot_silently_erase_failure():
    b=baseline()
    weaker=ProtectedTest(b.test_id,b.property_id,b.counterexamples,frozenset())
    event=next_event("0"*64,event_id="1",proposal_id="P1",reason="New scope",
                     test=weaker,evidence="evidence-digest",review="review-ref")
    assert evaluate_history(b,(event,)).classification=="DOCUMENTED_VIOLATION"


def test_unresolved_appeal_suspends_clear_result():
    b=baseline()
    event=next_event("0"*64,event_id="1",proposal_id="P1",reason="Disputed",
                     test=b,appeal="OPEN")
    assert evaluate_history(b,(event,)).classification=="INVESTIGATION"


def test_broken_chain_detected():
    b=baseline()
    event=next_event("malicious",event_id="1",proposal_id="P1",
                     reason="Change",test=b)
    assert evaluate_history(b,(event,)).classification=="DOCUMENTED_VIOLATION"


def test_local_jurisdiction_cannot_be_promoted_to_universal():
    b=baseline()
    changed=ProtectedTest(b.test_id,b.property_id,b.counterexamples,
                          b.detected,jurisdiction="EU")
    event=next_event("0"*64,event_id="1",proposal_id="P1",
                     reason="Different legal profile",test=changed)
    result=evaluate_history(b,(event,))
    assert result.classification=="INVESTIGATION"
    assert "JURISDICTION_SCOPE_CHANGED" in result.reasons
