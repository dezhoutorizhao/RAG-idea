#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/00_env.sh"

WATCH_TIMEOUT_SECONDS="${WATCH_TIMEOUT_SECONDS:-21600}"
WATCH_INTERVAL_SECONDS="${WATCH_INTERVAL_SECONDS:-300}"
WATCH_OUTPUT_DIR="/mnt/ntfs-disk/csrm_corm_reconstruction/outputs/template_smoke_watcher"
mkdir -p "$WATCH_OUTPUT_DIR"

echo "Watch for reconstructed CoRM artifacts, then run the bounded template Biased-NQ smoke eval."
echo "timeout=$WATCH_TIMEOUT_SECONDS interval=$WATCH_INTERVAL_SECONDS"

START=$(date +%s)
while true; do
    NOW=$(date +%s)
    if [ "$((NOW - START))" -gt "$WATCH_TIMEOUT_SECONDS" ]; then
        cat > "$WATCH_OUTPUT_DIR/status.json" <<JSON
{"status":"timeout","observed_at":"$(date -Iseconds)","reason":"wiki.faiss or required smoke inputs were not ready before timeout"}
JSON
        exit 2
    fi

    if [ -f "/mnt/ntfs-disk/csrm_corm_reconstruction/data/wiki.faiss" ] && [ -f "/mnt/ntfs-disk/csrm_corm_reconstruction/data/wiki_passages.jsonl" ] && [ -f "/mnt/ntfs-disk/csrm_corm_reconstruction/data/biased_nq_test.template_smoke.jsonl" ]; then
        if [ -f "/mnt/ntfs-disk/csrm_corm_reconstruction/outputs/corm_reconstructed_eval_template_smoke/evaluation_results.json" ]; then
            cat > "$WATCH_OUTPUT_DIR/status.json" <<JSON
{"status":"already_completed","observed_at":"$(date -Iseconds)","evaluation_results":"/mnt/ntfs-disk/csrm_corm_reconstruction/outputs/corm_reconstructed_eval_template_smoke/evaluation_results.json"}
JSON
            exit 0
        fi
        echo "Required artifacts are ready; launching bounded template smoke eval."
        bash "$SCRIPT_DIR/04_run_template_biased_nq_smoke_eval.sh" > "$WATCH_OUTPUT_DIR/template_smoke_eval.log" 2>&1
        cat > "$WATCH_OUTPUT_DIR/status.json" <<JSON
{"status":"completed","observed_at":"$(date -Iseconds)","evaluation_results":"/mnt/ntfs-disk/csrm_corm_reconstruction/outputs/corm_reconstructed_eval_template_smoke/evaluation_results.json","log":"$WATCH_OUTPUT_DIR/template_smoke_eval.log"}
JSON
        exit 0
    fi

    echo "$(date -Iseconds) waiting for wiki.faiss, wiki_passages.jsonl, and biased_nq_test.template_smoke.jsonl"
    sleep "$WATCH_INTERVAL_SECONDS"
done
