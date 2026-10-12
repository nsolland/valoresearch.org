"""GAUNTLET-CAPTURE: prevent silent cumulative weakening of normative tests.

The protected object is a property plus historical counterexamples, not merely
test source text. This engine is a technical regression gate, not a voting body.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Literal


def digest(value: object) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                             allow_nan=False).encode()).hexdigest()


@dataclass(frozen=True)
class ProtectedTest:
    test_id: str
    property_id: str
    counterexamples: tuple[str, ...]
    detected: frozenset[str]
    jurisdiction: str = "UNIVERSAL"

    def __post_init__(self):
        if not self.test_id or not self.property_id or not self.counterexamples:
            raise ValueError("test identity, property and counterexamples required")
        if len(set(self.counterexamples)) != len(self.counterexamples):
            raise ValueError("duplicate counterexample")


@dataclass(frozen=True)
class ChangeEvent:
    event_id: str
    proposal_id: str
    public_reason: str
    proposed: ProtectedTest
    technical_evidence_digest: str = ""
    independent_review_ref: str = ""
    appeal_status: Literal["NONE", "OPEN", "RESOLVED"] = "NONE"
    previous_digest: str = ""


@dataclass(frozen=True)
class CaptureFinding:
    classification: Literal["NO_REGRESSION", "INVESTIGATION", "DOCUMENTED_VIOLATION"]
    missing: tuple[str, ...]
    reasons: tuple[str, ...]
    event_chain_digest: str


def evaluate_history(baseline: ProtectedTest, events: tuple[ChangeEvent, ...]) -> CaptureFinding:
    protected = set(baseline.counterexamples)
    current = baseline
    reasons: list[str] = []
    chain = "0" * 64
    history_valid = True
    for event in events:
        if event.previous_digest != chain or not event.event_id or not event.proposal_id or not event.public_reason:
            history_valid = False
            reasons.append("BROKEN_PUBLIC_CHANGE_CHAIN")
        if event.proposed.test_id != baseline.test_id or event.proposed.property_id != baseline.property_id:
            reasons.append("PROTECTED_PROPERTY_REPLACED")
        if event.proposed.jurisdiction != baseline.jurisdiction:
            reasons.append("JURISDICTION_SCOPE_CHANGED")
        removed = protected - set(event.proposed.detected)
        if removed:
            reasons.append("HISTORICAL_COUNTEREXAMPLE_NOT_DETECTED")
            if not event.technical_evidence_digest or not event.independent_review_ref:
                reasons.append("MISSING_INDEPENDENT_CHANGE_EVIDENCE")
        if event.appeal_status == "OPEN":
            reasons.append("UNRESOLVED_APPEAL")
        chain = digest({"previous": chain, "event_id": event.event_id,
                        "proposal_id": event.proposal_id,
                        "public_reason": event.public_reason,
                        "proposed": {
                            "test_id": event.proposed.test_id,
                            "property_id": event.proposed.property_id,
                            "counterexamples": event.proposed.counterexamples,
                            "detected": sorted(event.proposed.detected),
                            "jurisdiction": event.proposed.jurisdiction},
                        "technical_evidence_digest": event.technical_evidence_digest,
                        "independent_review_ref": event.independent_review_ref,
                        "appeal_status": event.appeal_status})
        current = event.proposed
    missing = tuple(sorted(protected - set(current.detected)))
    if missing or not history_valid or "PROTECTED_PROPERTY_REPLACED" in reasons:
        classification = "DOCUMENTED_VIOLATION"
    elif reasons:
        classification = "INVESTIGATION"
    else:
        classification = "NO_REGRESSION"
    return CaptureFinding(classification, missing, tuple(sorted(set(reasons))), chain)


def next_event(previous_hash: str, *, event_id: str, proposal_id: str,
               reason: str, test: ProtectedTest, evidence: str = "",
               review: str = "", appeal: str = "NONE") -> ChangeEvent:
    return ChangeEvent(event_id, proposal_id, reason, test, evidence, review,
                       appeal, previous_hash)
