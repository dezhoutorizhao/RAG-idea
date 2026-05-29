from experiments.check_remote_storage_status import _connect_kwargs, parse_df_pt


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
