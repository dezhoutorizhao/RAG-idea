from experiments.guarded_remote_ext4_cleanup import (
    CONFIRM_TOKEN,
    build_guarded_cleanup_plan,
    render_markdown,
    validate_cleanup_candidates,
)


def _candidates(reclaim=182.8):
    return {
        "destructive_operations_executed": False,
        "recommended_reclaim_gib_lower_bound": reclaim,
        "recommended_cleanup_scope": [
            "truncate_docker_json_logs",
            "clear_root_cache_contents",
            "clear_user_cache_contents",
        ],
    }


def test_validate_cleanup_candidates_requires_read_only_scope_and_reclaim():
    assert validate_cleanup_candidates(_candidates(), min_reclaim_gib=180.0)["passed"] is True
    assert (
        validate_cleanup_candidates(_candidates(reclaim=100.0), min_reclaim_gib=180.0)["passed"]
        is False
    )

    unsafe = _candidates()
    unsafe["destructive_operations_executed"] = True
    assert validate_cleanup_candidates(unsafe, min_reclaim_gib=180.0)["passed"] is False


def test_guarded_plan_refuses_execute_without_confirmation_token():
    plan = build_guarded_cleanup_plan(
        candidates=_candidates(),
        host="192.0.2.1",
        user="syk",
        port=22,
        target="/home/syk",
        min_free_gib=180.0,
        execute=True,
        confirm_token="wrong",
    )

    assert plan["execute_requested"] is True
    assert plan["confirmation_valid"] is False
    assert plan["can_execute"] is False
    assert plan["destructive_operations_executed"] is False


def test_guarded_plan_can_execute_only_with_confirmation_and_preflight():
    plan = build_guarded_cleanup_plan(
        candidates=_candidates(),
        host="192.0.2.1",
        user="syk",
        port=22,
        target="/home/syk",
        min_free_gib=180.0,
        execute=True,
        confirm_token=CONFIRM_TOKEN,
    )

    assert plan["confirmation_valid"] is True
    assert plan["preflight"]["passed"] is True
    assert plan["can_execute"] is True
    assert CONFIRM_TOKEN in plan["execute_command"]


def test_render_markdown_includes_non_scope_and_probe_command():
    plan = build_guarded_cleanup_plan(
        candidates=_candidates(),
        host="192.0.2.1",
        user="syk",
        port=22,
        target="/home/syk",
        min_free_gib=180.0,
        execute=False,
        confirm_token=None,
    )

    text = render_markdown(plan)

    assert "Guarded Remote Ext4 Cleanup Plan" in text
    assert "no Docker volume deletion" in text
    assert "check_remote_storage_status" in text
