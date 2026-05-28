#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence


PASS = "pass"
FAIL = "fail"


def verify_claims(ledger_path: Path, root: Path) -> dict:
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    claim_results = []
    for claim in ledger.get("claims", []):
        checks = [_run_check(check, root) for check in claim.get("checks", [])]
        claim_results.append(
            {
                "id": claim["id"],
                "declared_status": claim.get("status"),
                "text": claim.get("text"),
                "verification_status": PASS if all(c["status"] == PASS for c in checks) else FAIL,
                "checks": checks,
                "limitations": claim.get("limitations", []),
            }
        )

    return {
        "ledger": str(ledger_path),
        "total_claims": len(claim_results),
        "passed_claims": sum(1 for item in claim_results if item["verification_status"] == PASS),
        "failed_claims": sum(1 for item in claim_results if item["verification_status"] == FAIL),
        "claims": claim_results,
    }


def _run_check(check: dict, root: Path) -> dict:
    check_type = check["type"]
    file_path = root / check["file"]
    if not file_path.exists():
        return {**check, "status": FAIL, "error": f"missing file: {file_path}"}
    payload = json.loads(file_path.read_text(encoding="utf-8"))

    try:
        if check_type == "metric_equals":
            actual = _get_path(payload, check["path"])
            expected = check["expected"]
            tolerance = check.get("tolerance", 0.0)
            ok = abs(float(actual) - float(expected)) <= float(tolerance)
            return _result(check, ok, actual=actual, expected=expected)

        if check_type == "metric_less_than":
            left = _get_path(payload, check["left"])
            right = _get_path(payload, check["right"])
            return _result(check, float(left) < float(right), left_value=left, right_value=right)

        if check_type == "metric_greater_than":
            left = _get_path(payload, check["left"])
            right = _get_path(payload, check["right"])
            return _result(check, float(left) > float(right), left_value=left, right_value=right)

        if check_type == "metric_less_than_value":
            actual = _get_path(payload, check["path"])
            threshold = check["threshold"]
            return _result(check, float(actual) < float(threshold), actual=actual, threshold=threshold)

        if check_type == "metric_greater_than_value":
            actual = _get_path(payload, check["path"])
            threshold = check["threshold"]
            return _result(check, float(actual) > float(threshold), actual=actual, threshold=threshold)

        if check_type == "value_equals":
            actual = _get_path(payload, check["path"])
            expected = check["expected"]
            return _result(check, actual == expected, actual=actual, expected=expected)

    except (KeyError, TypeError, ValueError) as exc:
        return {**check, "status": FAIL, "error": str(exc)}

    return {**check, "status": FAIL, "error": f"unknown check type: {check_type}"}


def _get_path(payload: Any, path: Sequence[str]) -> Any:
    cursor = payload
    for part in path:
        cursor = cursor[part]
    return cursor


def _result(check: dict, ok: bool, **details: Any) -> dict:
    return {**check, "status": PASS if ok else FAIL, **details}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=Path("CLAIMS_LEDGER.json"))
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = verify_claims(args.ledger, args.root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["failed_claims"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
