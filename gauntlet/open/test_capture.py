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


def test_twenty_small_revisions_accumulate_into_property_loss():
    cases=tuple("NEG-%02d" % n for n in range(20))
    base=ProtectedTest("GAUNTLET-CAPTURE-001", "NEGATIVE_TEST_PRESERVATION",
                       cases, frozenset(cases))
    events=[]
    digest="0"*64
    for step in range(20):
        surviving=frozenset(cases[step+1:])
        updated=ProtectedTest(base.test_id,base.property_id,cases,surviving)
        event=next_event(digest,event_id=str(step+1),proposal_id="P-%02d" % step,
                         reason="Minor editorial simplification",test=updated)
        events.append(event)
        digest=evaluate_history(base,tuple(events)).event_chain_digest
    result=evaluate_history(base,tuple(events))
    assert result.classification=="DOCUMENTED_VIOLATION"
    assert result.missing==cases


def test_restoring_dropped_negative_test_does_not_hide_historical_breach():
    b=baseline()
    reduced=ProtectedTest(b.test_id,b.property_id,b.counterexamples,
                          frozenset({"receipt-tamper"}))
    first=next_event("0"*64,event_id="1",proposal_id="P1",
                     reason="Simplification",test=reduced)
    chain=evaluate_history(b,(first,)).event_chain_digest
    second=next_event(chain,event_id="2",proposal_id="P2",
                      reason="Restoration",test=b)
    result=evaluate_history(b,(first,second))
    assert result.missing==()
    assert result.classification=="DOCUMENTED_VIOLATION"


def test_newly_admitted_negative_test_remains_protected():
    b=baseline()
    new=ProtectedTest(b.test_id,b.property_id,
                      b.counterexamples+("new-attack",),
                      b.detected|{"new-attack"})
    first=next_event("0"*64,event_id="1",proposal_id="P1",
                     reason="Add verified exploit",test=new)
    chain=evaluate_history(b,(first,)).event_chain_digest
    weaker=ProtectedTest(b.test_id,b.property_id,new.counterexamples,
                         b.detected)
    second=next_event(chain,event_id="2",proposal_id="P2",
                      reason="Editorial cleanup",test=weaker)
    result=evaluate_history(b,(first,second))
    assert result.missing==("new-attack",)
    assert result.classification=="DOCUMENTED_VIOLATION"
