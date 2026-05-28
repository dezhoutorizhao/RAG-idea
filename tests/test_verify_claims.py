import json

from experiments.verify_claims import verify_claims


def test_verify_claims_checks_metric_comparisons(tmp_path):
    result_file = tmp_path / "result.json"
    result_file.write_text(
        json.dumps({"summary": {"a": {"risk": 0.1}, "b": {"risk": 0.2}}}),
        encoding="utf-8",
    )
    ledger = tmp_path / "ledger.json"
    ledger.write_text(
        json.dumps(
            {
                "claims": [
                    {
                        "id": "c1",
                        "checks": [
                        {
                            "type": "metric_less_than",
                            "file": "result.json",
                            "left": ["summary", "a", "risk"],
                            "right": ["summary", "b", "risk"],
                        },
                        {
                            "type": "metric_greater_than_value",
                            "file": "result.json",
                            "path": ["summary", "b", "risk"],
                            "threshold": 0.1,
                        }
                    ],
                }
                ]
            }
        ),
        encoding="utf-8",
    )

    report = verify_claims(ledger, tmp_path)

    assert report["passed_claims"] == 1
    assert report["failed_claims"] == 0


def test_verify_claims_supports_string_value_equals(tmp_path):
    result_file = tmp_path / "result.json"
    result_file.write_text(json.dumps({"status": "blocked"}), encoding="utf-8")
    ledger = tmp_path / "ledger.json"
    ledger.write_text(
        json.dumps(
            {
                "claims": [
                    {
                        "id": "c1",
                        "checks": [
                            {
                                "type": "value_equals",
                                "file": "result.json",
                                "path": ["status"],
                                "expected": "blocked",
                            }
                        ],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    report = verify_claims(ledger, tmp_path)

    assert report["passed_claims"] == 1
    assert report["failed_claims"] == 0
