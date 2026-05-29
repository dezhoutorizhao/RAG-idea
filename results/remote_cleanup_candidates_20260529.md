# Remote Cleanup Candidate Audit

Generated: `2026-05-29T07:58:46.037638+00:00`
Remote: `syk@192.168.103.101:22`
Destructive operations executed: `False`

## Summary

- Recommended reclaim lower bound: `182.8 GiB`.
- Running Docker containers observed: `23`.
- Top Docker log bytes scanned: `134.1 GiB`.
- Root cache: `30.4 GiB`.
- User cache: `18.4 GiB`.
- Conda package cache: `4.9 GiB`.

## Recommended Cleanup Scope

- `truncate_docker_json_logs`
- `clear_root_cache_contents`
- `clear_user_cache_contents`

## Largest Docker JSON Logs

| Size GiB | Running | Container | Image | Path |
|---:|---:|---|---|---|
| 39.71 | `True` | `docker-worker-1` | `opencti/worker:6.4.0` | `/var/lib/docker/containers/ed846c3bee9aa37bbf97e2585142898f3d0f94e2184c1ad21852e6f38de8ba10/ed846c3bee9aa37bbf97e2585142898f3d0f94e2184c1ad21852e6f38de8ba10-json.log` |
| 26.01 | `True` | `docker-worker-2` | `opencti/worker:6.4.0` | `/var/lib/docker/containers/acdbfa192cf6617111abe637250392059a835fb408644cbee3191a699d5a3ced/acdbfa192cf6617111abe637250392059a835fb408644cbee3191a699d5a3ced-json.log` |
| 15.22 | `True` | `docker-worker-3` | `opencti/worker:6.4.0` | `/var/lib/docker/containers/31f8bd8454af80ff2b095e0da141bec9e22a7ad60c890f5614dda5a470e39008/31f8bd8454af80ff2b095e0da141bec9e22a7ad60c890f5614dda5a470e39008-json.log` |
| 7.21 | `True` | `cve-connector-cve-1` | `opencti/connector-cve:6.4.2` | `/var/lib/docker/containers/1633dd4f013353e9fb3ae1d652e101dc97ecdd0dbc05e04075f5a1523fda04c3/1633dd4f013353e9fb3ae1d652e101dc97ecdd0dbc05e04075f5a1523fda04c3-json.log` |
| 6.23 | `True` | `docker-connector-cve-1` | `opencti/connector-cve:6.4.2` | `/var/lib/docker/containers/240580b52935786be83a1bed3821b19f2efefb675f11e730c81df217bfcad14a/240580b52935786be83a1bed3821b19f2efefb675f11e730c81df217bfcad14a-json.log` |
| 5.94 | `True` | `docker-connector-export-file-stix-1` | `opencti/connector-export-file-stix:6.4.0` | `/var/lib/docker/containers/4a7cbbe257d1661c14cef2c92e0c5611dcb90812ce546ca1942c8945c3b20901/4a7cbbe257d1661c14cef2c92e0c5611dcb90812ce546ca1942c8945c3b20901-json.log` |
| 5.94 | `True` | `docker-connector-export-file-txt-1` | `opencti/connector-export-file-txt:6.4.0` | `/var/lib/docker/containers/d657ff973cc50daeb85f78dd7cc6b8670c45ef8df80b193061e14e2776abea2d/d657ff973cc50daeb85f78dd7cc6b8670c45ef8df80b193061e14e2776abea2d-json.log` |
| 5.94 | `True` | `docker-connector-export-file-csv-1` | `opencti/connector-export-file-csv:6.4.0` | `/var/lib/docker/containers/862116afe99e88a63fdd6bb0225d841bbdebd1ff0c828c854e66d7f90c685b35/862116afe99e88a63fdd6bb0225d841bbdebd1ff0c828c854e66d7f90c685b35-json.log` |
| 5.80 | `True` | `docker-connector-import-file-stix-1` | `opencti/connector-import-file-stix:6.4.0` | `/var/lib/docker/containers/6b2c56cf30a9d763869dc098f35d60db7306a0fdbccd8d49cf341c7914cfc66e/6b2c56cf30a9d763869dc098f35d60db7306a0fdbccd8d49cf341c7914cfc66e-json.log` |
| 4.63 | `True` | `opencti-connector-opencti-1` | `opencti/connector-opencti:6.4.2` | `/var/lib/docker/containers/3cb6aaaaca9187833baa094ffb5edbf40e7c0f19d184232a18b27ed33c1adf18/3cb6aaaaca9187833baa094ffb5edbf40e7c0f19d184232a18b27ed33c1adf18-json.log` |

## Largest Root Cache Entries

| Size GiB | Path |
|---:|---|
| 10.24 | `/root/.cache/huggingface` |
| 10.16 | `/root/.cache/pip` |
| 8.94 | `/root/.cache/uv` |
| 0.93 | `/root/.cache/modelscope` |
| 0.05 | `/root/.cache/node-gyp` |
| 0.04 | `/root/.cache/flashinfer` |
| 0.01 | `/root/.cache/tracker` |
| 0.00 | `/root/.cache/JNA` |
| 0.00 | `/root/.cache/conda` |
| 0.00 | `/root/.cache/conda-anaconda-tos` |

## Largest User Cache Entries

| Size GiB | Path |
|---:|---|
| 10.56 | `/home/syk/.cache/huggingface` |
| 6.63 | `/home/syk/.cache/pip` |
| 1.05 | `/home/syk/.cache/torch` |
| 0.11 | `/home/syk/.cache/vllm` |
| 0.02 | `/home/syk/.cache/flashinfer` |
| 0.01 | `/home/syk/.cache/virtualenv` |
| 0.00 | `/home/syk/.cache/fontconfig` |
| 0.00 | `/home/syk/.cache/matplotlib` |
| 0.00 | `/home/syk/.cache/modelscope` |
| 0.00 | `/home/syk/.cache/outlines` |

## Claim Policy

This is a read-only cleanup candidate audit. It does not delete, truncate, prune, unmount, or modify server files. It supports cleanup approval decisions only.
