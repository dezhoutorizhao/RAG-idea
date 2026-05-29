from experiments.audit_remote_cleanup_candidates import (
    annotate_docker_logs,
    container_id_from_log_path,
    first_size,
    parse_docker_ps,
    parse_size_path_lines,
    render_markdown,
)


def test_parse_size_path_lines_reads_byte_prefixed_rows():
    rows = parse_size_path_lines("1073741824\t/root/.cache/hf\nbad row\n512 /tmp/x\n")

    assert rows == [
        {"size_bytes": 1073741824, "size_gib": 1.0, "path": "/root/.cache/hf"},
        {"size_bytes": 512, "size_gib": 512 / 1024**3, "path": "/tmp/x"},
    ]
    assert first_size("1073741824\t/root/.cache\n") == 1073741824


def test_annotate_docker_logs_marks_running_containers():
    container_id = "a" * 64
    logs = [
        {
            "size_bytes": 2147483648,
            "size_gib": 2.0,
            "path": f"/var/lib/docker/containers/{container_id}/{container_id}-json.log",
        }
    ]
    running = parse_docker_ps(f"{container_id}\tapi\timage:latest\tUp 2 hours\n")

    annotated = annotate_docker_logs(logs, running)

    assert container_id_from_log_path(logs[0]["path"]) == container_id
    assert annotated[0]["container_running"] is True
    assert annotated[0]["container_name"] == "api"
    assert annotated[0]["container_image"] == "image:latest"


def test_render_markdown_states_read_only_policy():
    report = {
        "observed_at_utc": "now",
        "remote": {"user": "syk", "host": "192.0.2.1", "port": 22},
        "destructive_operations_executed": False,
        "recommended_reclaim_gib_lower_bound": 180.0,
        "recommended_cleanup_scope": ["truncate_docker_json_logs"],
        "docker": {
            "running_container_count": 1,
            "top_log_gib": 134.0,
            "top_logs": [
                {
                    "size_gib": 134.0,
                    "container_running": True,
                    "container_name": "api",
                    "container_image": "image",
                    "path": "/var/lib/docker/containers/a/a-json.log",
                }
            ],
        },
        "caches": {
            "root_cache_total_gib": 31.0,
            "user_cache_total_gib": 19.0,
            "conda_pkg_total_gib": 5.0,
            "root_cache_entries": [{"size_gib": 31.0, "path": "/root/.cache/hf"}],
            "user_cache_entries": [{"size_gib": 19.0, "path": "/home/syk/.cache/hf"}],
        },
        "claim_policy": "read-only cleanup candidate audit",
    }

    text = render_markdown(report)

    assert "Remote Cleanup Candidate Audit" in text
    assert "Destructive operations executed: `False`" in text
    assert "read-only cleanup candidate audit" in text
