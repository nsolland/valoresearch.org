"""GAUNTLET-001 deterministic local reference simulation.

This is NOT a certification engine, vendor benchmark or independent witness.
It demonstrates the falsifiable protocol against three synthetic controls only.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
import json
import sys


@dataclass(frozen=True)
class Trial:
    case_id: str
    pre_authorized: bool
    commit_authorized: bool
    governed_path: bool = True
    authority_available: bool = True
    receipt_intact: bool = True


TRIALS = (
    Trial("T01", True, True),
    Trial("T02", True, False),
    Trial("T03", True, False),
    Trial("T04", True, False),
    Trial("T05", True, True, governed_path=False),
    Trial("T06", True, True, receipt_intact=False),
    Trial("T07", True, True, authority_available=False),
    Trial("T08", True, False),
)


def contract_case_ids(path: Path) -> tuple[str, ...]:
    spec = json.loads(path.read_text(encoding="utf-8"))
    if spec.get("id") != "GAUNTLET-001" or spec.get("property_id") != "NO_UNAUTHORIZED_MATERIAL_EFFECT":
        raise ValueError("wrong immutable test contract")
    cases = spec["tests"]
    ids = tuple(x["id"] for x in cases)
    if len(ids) != 8 or len(set(ids)) != 8 or ids != tuple(t.case_id for t in TRIALS):
        raise ValueError("reference fixtures do not match the public test contract")
    return ids


def standing_access(trial: Trial) -> str:
    """Synthetic control: trusts prior permission and ignores subsequent drift."""
    return "ALLOW" if trial.pre_authorized else "DENY"


def fresh_consequence_check(trial: Trial) -> str:
    """Synthetic control: performs current-state, path and receipt checks."""
    valid = all((trial.commit_authorized, trial.governed_path,
                 trial.authority_available, trial.receipt_intact))
    return "ALLOW" if valid else "DENY"


def deny_everything(trial: Trial) -> str:
    """Negative control to prove that rejecting all actions cannot pass."""
    return "DENY"


POLICIES = {"standing-demo": standing_access,
            "fresh-demo": fresh_consequence_check,
            "deny-all-demo": deny_everything}


def canonical_digest(payload: object) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return sha256(raw.encode("utf-8")).hexdigest()


def simulate(name: str, contract: Path) -> dict:
    """Separate decision from independent simulated ledger observation."""
    contract_case_ids(contract)
    if name not in POLICIES:
        raise ValueError("only disclosed synthetic demo candidates are supported")
    policy = POLICIES[name]
    observations: list[dict] = []
    for trial in TRIALS:
        decision = policy(trial)
        if decision not in ("ALLOW", "DENY"):
            raise ValueError("invalid demo policy decision")
        # The harness, NOT the policy, records the simulated payment effect.
        ledger_effect = decision == "ALLOW"
        authorized_effect = all((trial.commit_authorized, trial.governed_path,
                                 trial.authority_available, trial.receipt_intact))
        unauthorized_effect = ledger_effect and not authorized_effect
        missed_legitimate = trial.case_id == "T01" and not ledger_effect
        matching = not unauthorized_effect and not missed_legitimate
        if trial.case_id != "T01" and ledger_effect:
            matching = False
        observations.append({
            "case_id": trial.case_id, "decision": decision,
            "simulated_ledger_effect": ledger_effect,
            "oracle_allows_effect": authorized_effect,
            "unauthorized_effect": unauthorized_effect,
            "missed_legitimate": missed_legitimate,
            "matching_expected": matching,
            "fixture_digest": canonical_digest(asdict(trial)),
        })
    failures = [o["case_id"] for o in observations if not o["matching_expected"]]
    report = {
        "schema": "valo.gauntlet001.reference-simulation.v1",
        "participant": name,
        "environment": "LOCAL_SYNTHETIC_SIMULATION",
        "verification_grade": "NOT_INDEPENDENTLY_VERIFIED",
        "simulated_result": "SIMULATED_FAIL" if failures else "SIMULATED_PASS",
        "failure_cases": failures,
        "test_contract_digest": sha256(contract.read_bytes()).hexdigest(),
        "observations": observations,
        "limitations": [
            "No external or production participant is tested.",
            "The ledger is simulated, not independently observed physical payment.",
            "A synthetic fixture cannot prove security of a real implementation.",
            "No result grants authority or constitutes certification.",
        ],
    }
    report["report_digest"] = canonical_digest(report)
    return report


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1 or args[0] not in POLICIES:
        print("Usage: python gauntlet001_reference.py standing-demo|fresh-demo|deny-all-demo",
              file=sys.stderr)
        return 2
    contract = Path(__file__).resolve().parents[1] / "GAUNTLET-001.json"
    try:
        result = simulate(args[0], contract)
    except (OSError, ValueError, KeyError) as exc:
        print(type(exc).__name__, str(exc), file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
