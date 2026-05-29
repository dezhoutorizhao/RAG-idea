#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def build_claims_ledger_markdown(
    ledger_path: Path,
    verification_path: Path,
) -> dict[str, Any]:
    ledger = _load_json(ledger_path)
    verification = _load_json(verification_path)
    verification_by_id = {claim["id"]: claim for claim in verification.get("claims", [])}
    rows = []
    for claim in ledger.get("claims", []):
        verified = verification_by_id.get(claim["id"], {})
        checks = verified.get("checks", claim.get("checks", []))
        evidence_files = sorted(
            {
                check.get("file")
                for check in checks
                if isinstance(check, dict) and check.get("file")
            }
        )
        rows.append(
            {
                "id": claim.get("id"),
                "declared_status": claim.get("status"),
                "verification_status": verified.get("verification_status", "missing"),
                "text": claim.get("text", ""),
                "evidence_files": evidence_files,
                "check_count": len(checks),
                "passed_check_count": sum(1 for check in checks if check.get("status") == "pass"),
                "failed_check_count": sum(1 for check in checks if check.get("status") == "fail"),
                "limitations": claim.get("limitations", []),
            }
        )
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": {
            "ledger": str(ledger_path),
            "verification": str(verification_path),
        },
        "total_claims": len(rows),
        "verification_total_claims": verification.get("total_claims"),
        "passed_claims": verification.get("passed_claims"),
        "failed_claims": verification.get("failed_claims"),
        "status_counts": dict(Counter(row["declared_status"] for row in rows)),
        "verification_status_counts": dict(Counter(row["verification_status"] for row in rows)),
        "claims": rows,
        "claim_boundary": (
            "This markdown ledger mirrors CLAIMS_LEDGER.json and results/claims_verification.json. "
            "It documents support and limitations; it does not upgrade bridge, proxy, or pending "
            "human-audit evidence into NeurIPS-ready main-claim support."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Claims Ledger",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        "",
        f"Claims: `{summary['total_claims']}`; verified pass/fail: "
        f"`{summary['passed_claims']}` / `{summary['failed_claims']}`.",
        "",
        f"Declared status counts: `{summary['status_counts']}`.",
        f"Verification status counts: `{summary['verification_status_counts']}`.",
        "",
        "## Claim Index",
        "",
        "| ID | Declared status | Verification | Evidence files | Checks |",
        "|---|---|---|---|---:|",
    ]
    for claim in summary["claims"]:
        evidence = "<br>".join(f"`{path}`" for path in claim["evidence_files"]) or "none"
        lines.append(
            f"| `{claim['id']}` | `{claim['declared_status']}` | "
            f"`{claim['verification_status']}` | {evidence} | `{claim['check_count']}` |"
        )

    lines.extend(["", "## Claims", ""])
    for claim in summary["claims"]:
        lines.extend(
            [
                f"### {claim['id']}",
                "",
                f"- Declared status: `{claim['declared_status']}`.",
                f"- Verification status: `{claim['verification_status']}` "
                f"({claim['passed_check_count']}/{claim['check_count']} checks passed).",
                f"- Claim: {claim['text']}",
                "- Evidence files:",
            ]
        )
        if claim["evidence_files"]:
            lines.extend(f"  - `{path}`" for path in claim["evidence_files"])
        else:
            lines.append("  - none")
        lines.append("- Limitations:")
        if claim["limitations"]:
            lines.extend(f"  - {item}" for item in claim["limitations"])
        else:
            lines.append("  - none recorded")
        lines.append("")

    lines.extend(["## Claim Boundary", "", summary["claim_boundary"], ""])
    return "\n".join(lines)


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=Path("CLAIMS_LEDGER.json"))
    parser.add_argument("--verification", type=Path, default=Path("results/claims_verification.json"))
    parser.add_argument("--output-md", type=Path, default=Path("CLAIMS_LEDGER.md"))
    parser.add_argument("--output-json", type=Path, default=Path("results/claims_ledger_markdown_summary_20260529.json"))
    args = parser.parse_args()

    summary = build_claims_ledger_markdown(args.ledger, args.verification)
    _write_json(args.output_json, summary)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
