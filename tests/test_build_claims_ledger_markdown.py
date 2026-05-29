import json

from experiments.build_claims_ledger_markdown import (
    build_claims_ledger_markdown,
    render_markdown,
)


def test_build_claims_ledger_markdown_joins_ledger_and_verification(tmp_path):
    ledger = tmp_path / "CLAIMS_LEDGER.json"
    verification = tmp_path / "claims_verification.json"
    _write_json(
        ledger,
        {
            "claims": [
                {
                    "id": "C1",
                    "status": "supported_bridge",
                    "text": "Claim text",
                    "checks": [{"type": "value_equals", "file": "a.json"}],
                    "limitations": ["bridge only"],
                }
            ]
        },
    )
    _write_json(
        verification,
        {
            "total_claims": 1,
            "passed_claims": 1,
            "failed_claims": 0,
            "claims": [
                {
                    "id": "C1",
                    "verification_status": "pass",
                    "checks": [{"type": "value_equals", "file": "a.json", "status": "pass"}],
                }
            ],
        },
    )

    summary = build_claims_ledger_markdown(ledger, verification)

    assert summary["total_claims"] == 1
    assert summary["passed_claims"] == 1
    assert summary["claims"][0]["evidence_files"] == ["a.json"]
    assert summary["claims"][0]["passed_check_count"] == 1
    assert summary["status_counts"] == {"supported_bridge": 1}


def test_render_markdown_lists_claim_boundaries_and_evidence():
    summary = {
        "generated_at_utc": "now",
        "total_claims": 1,
        "passed_claims": 1,
        "failed_claims": 0,
        "status_counts": {"supported_bridge": 1},
        "verification_status_counts": {"pass": 1},
        "claims": [
            {
                "id": "C1",
                "declared_status": "supported_bridge",
                "verification_status": "pass",
                "text": "Claim text",
                "evidence_files": ["a.json"],
                "check_count": 1,
                "passed_check_count": 1,
                "failed_check_count": 0,
                "limitations": ["bridge only"],
            }
        ],
        "claim_boundary": "does not upgrade bridge evidence",
    }

    text = render_markdown(summary)

    assert "# Claims Ledger" in text
    assert "`a.json`" in text
    assert "bridge only" in text
    assert "does not upgrade bridge evidence" in text


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
