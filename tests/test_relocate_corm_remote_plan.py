from experiments.relocate_corm_remote_plan import (
    relocate_corm_remote_plan,
    validate_relocated_plan,
)


def _plan():
    return {
        "claim_policy": "planned only",
        "remote": {
            "remote_root": "/mnt/ntfs-disk/csrm_corm_reconstruction",
            "storage_policy": "old policy",
            "host": "192.0.2.1",
            "user": "syk",
            "ssh_port": 22,
        },
        "remote_steps": [
            {
                "name": "build",
                "command": (
                    "cd /mnt/ntfs-disk/csrm_corm_reconstruction/workspace && "
                    "python build.py --output /mnt/ntfs-disk/csrm_corm_reconstruction/data/wiki.faiss"
                ),
                "expected_outputs": ["/mnt/ntfs-disk/csrm_corm_reconstruction/data/wiki.faiss"],
            }
        ],
        "missing_local_reconstruction_inputs": [],
    }


def test_relocate_corm_remote_plan_rewrites_remote_root_everywhere():
    new_root = "/home/syk/csrm_corm_reconstruction"
    relocated = relocate_corm_remote_plan(_plan(), new_remote_root=new_root)

    validation = validate_relocated_plan(
        relocated,
        old_root="/mnt/ntfs-disk/csrm_corm_reconstruction",
        new_root=new_root,
    )

    assert validation["passed"] is True
    assert relocated["remote"]["remote_root"] == new_root
    assert relocated["status"] == "planned_not_executed_ext4_relocation"
    assert relocated["relocation"]["requires_post_cleanup_probe"] is True
    assert "/mnt/ntfs-disk/csrm_corm_reconstruction" not in str(relocated["remote_steps"])
    assert new_root in relocated["remote_steps"][0]["command"]


def test_validate_relocated_plan_rejects_stale_root():
    plan = _plan()

    validation = validate_relocated_plan(
        plan,
        old_root="/mnt/ntfs-disk/csrm_corm_reconstruction",
        new_root="/home/syk/csrm_corm_reconstruction",
    )

    assert validation["passed"] is False
    assert validation["old_root_absent"] is False
