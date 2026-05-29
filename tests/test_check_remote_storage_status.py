from experiments.check_remote_storage_status import (
    _connect_kwargs,
    _default_probe_dirs,
    _parse_probe_json,
    parse_df_pt,
    parse_df_pti,
)


def test_parse_df_pt_extracts_mount_rows():
    output = """Filesystem     Type     1024-blocks      Used Available Capacity Mounted on
/dev/nvme0n1p2 ext4       123456789 100000000  23456789      82% /
/dev/nvme1n1p1 fuseblk    976762580 700000000 276762580      72% /mnt/ntfs-disk
tmpfs          tmpfs       16384000   1000000  15384000       7% /dev/shm
"""

    rows = parse_df_pt(output)

    assert rows[1]["filesystem"] == "/dev/nvme1n1p1"
    assert rows[1]["type"] == "fuseblk"
    assert rows[1]["available_1k_blocks"] == 276762580
    assert rows[1]["mount"] == "/mnt/ntfs-disk"


def test_parse_df_pti_extracts_inode_rows():
    output = """Filesystem     Type       Inodes IUsed     IFree IUse% Mounted on
/dev/nvme0n1p2 ext4    120000000  9000 119991000    1% /
/dev/nvme1n1p1 fuseblk 333000000 11000 332989000    1% /mnt/ntfs-disk
"""

    rows = parse_df_pti(output)

    assert rows[1]["filesystem"] == "/dev/nvme1n1p1"
    assert rows[1]["type"] == "fuseblk"
    assert rows[1]["ifree"] == 332989000
    assert rows[1]["mount"] == "/mnt/ntfs-disk"


def test_default_probe_dirs_include_target_and_writable_fallbacks():
    dirs = _default_probe_dirs(target="/mnt/ntfs-disk", user="syk", extra=None)

    assert "/mnt/ntfs-disk" in dirs
    assert "/mnt/ntfs-disk/csrm_corm_reconstruction/data" in dirs
    assert "/home/syk" in dirs
    assert "/dev/shm" in dirs


def test_parse_probe_json_reads_last_json_line():
    parsed = _parse_probe_json('noise\n{"ok": false, "errno": 28}\n')

    assert parsed == {"ok": False, "errno": 28}


def test_connect_kwargs_supports_key_or_agent_auth_without_password():
    kwargs = _connect_kwargs(
        host="192.168.103.101",
        user="syk",
        port=22,
        password=None,
        key_filename=None,
        allow_agent=True,
        look_for_keys=True,
        timeout=30,
    )

    assert kwargs["hostname"] == "192.168.103.101"
    assert kwargs["username"] == "syk"
    assert kwargs["allow_agent"] is True
    assert kwargs["look_for_keys"] is True
    assert "password" not in kwargs


def test_connect_kwargs_includes_explicit_key_and_password_when_provided():
    kwargs = _connect_kwargs(
        host="host",
        user="user",
        port=2200,
        password="secret",
        key_filename="/tmp/key",
        allow_agent=False,
        look_for_keys=False,
        timeout=5,
    )

    assert kwargs["password"] == "secret"
    assert kwargs["key_filename"] == "/tmp/key"
    assert kwargs["allow_agent"] is False
    assert kwargs["look_for_keys"] is False
