from experiments.prepare_remote_ext4_storage import (
    clear_directory_contents_command,
    cleanup_plan,
    docker_log_truncate_command,
    sudo_command,
    target_user_from_home,
)


def test_cleanup_plan_is_limited_to_logs_and_caches():
    plan = cleanup_plan("syk")

    commands = [item["command"] for item in plan]
    assert commands == [
        docker_log_truncate_command(),
        clear_directory_contents_command("/root/.cache"),
        clear_directory_contents_command("/home/syk/.cache"),
    ]
    assert all("docker system prune" not in command for command in commands)
    assert all("/mnt/ntfs-disk" not in command for command in commands)


def test_sudo_command_quotes_password_and_can_be_masked():
    command = sudo_command("echo ok", "secret value")
    masked = sudo_command("echo ok", "***")

    assert "secret value" not in masked
    assert "printf '%s\\n' 'secret value'" in command
    assert "sudo -S -p '' bash -lc" in command


def test_target_user_from_home_defaults_safely():
    assert target_user_from_home("/home/syk") == "syk"
    assert target_user_from_home("/home/syk/csrm") == "syk"
    assert target_user_from_home("/tmp/csrm") == "syk"
