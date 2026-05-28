from experiments.check_remote_storage_status import parse_df_pt


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
