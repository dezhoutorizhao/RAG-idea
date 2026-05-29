# NeurIPS Evidence Unblock Plan

Generated: `2026-05-29T08:23:28.849007+00:00`
Ready for NeurIPS main-track claim: `False`
Open blockers: `5`
External actions required: `4`
User approvals required: `1`

## Blockers

| Blocker | Status | External action | User approval | Current evidence | Next command |
|---|---|---:|---:|---|---|
| complete_human_audit_v4 | `blocked` | `True` | `False` | human_labels_complete=False; pending_auditor_labels=2000; pending_adjudicated_labels=1000; aggregate_pending=1300. | `python -m experiments.collect_human_audit_v4_assignment_batches --output-json results/human_audit_v4_batch_collection_20260529.json --output-md results/human_audit_v4_batch_collection_20260529.md`<br>`powershell -ExecutionPolicy Bypass -File scripts\run_main_tables.ps1` |
| run_api_backed_llm_judge | `blocked` | `True` | `False` | batch_status=blocked; ready_for_batch_submission=False; score_status=blocked; correlation_ready=False. | `$env:OPENAI_API_KEY='<set locally>'; python -m experiments.manage_openai_llm_judge_batch --action submit --request-jsonl results\llm_judge_nli_probe_requests_20260529.jsonl --batch-output-jsonl results\llm_judge_nli_probe_batch_output_20260529.jsonl`<br>`$env:OPENAI_API_KEY='<set locally>'; python -m experiments.manage_openai_llm_judge_batch --action retrieve --batch-id <batch_id> --request-jsonl results\llm_judge_nli_probe_requests_20260529.jsonl --batch-output-jsonl results\llm_judge_nli_probe_batch_output_20260529.jsonl`<br>`python -m experiments.normalize_llm_judge_batch_responses --batch-output-jsonl results\llm_judge_nli_probe_batch_output_20260529.jsonl --scores-jsonl results\llm_judge_nli_probe_scores_20260529.jsonl`<br>`python -m experiments.compute_llm_nli_correlation`<br>`powershell -ExecutionPolicy Bypass -File scripts\run_main_tables.ps1` |
| repair_storage_for_full_corm_reproduction | `blocked` | `True` | `True` | target=/mnt/ntfs-disk; target_available_gib=322.1; target_write_probe_passed=False; home_available_gib=12.2; home_write_probe_passed=True; home_min_free_met=False; ext4_mode=dry_run; destructive_operations_executed=False; cleanup_candidate_audit_ready=True; cleanup_reclaim_lower_bound_gib=182.8. | `$env:CORM_REMOTE_PASSWORD='<set locally>'; python -m experiments.guarded_remote_ext4_cleanup --host 192.168.103.101 --user syk --port 22 --target /home/syk --min-free-gib 180 --execute --confirm-token APPROVE_EXT4_LOG_CACHE_CLEANUP_FOR_FULL_CORM_RAG_REPRO`<br>`$env:CORM_REMOTE_PASSWORD='<set locally>'; python -m experiments.check_remote_storage_status --host 192.168.103.101 --user syk --port 22 --target /home/syk --output results/remote_storage_status_after_ext4_cleanup.json --min-free-gib 180`<br>`run results/corm_remote_scripts_ext4/02_build_wikipedia_and_faiss.sh only after the post-cleanup probe passes` |
| obtain_independent_external_review | `blocked` | `True` | `False` | packet_ready=True; external_review_completed=False; response_path=results\external_review_response_20260529.md. | `place independent review response at results\external_review_response_20260529.md`<br>`powershell -ExecutionPolicy Bypass -File scripts\run_main_tables.ps1` |
| risk_control_claim_boundary | `fail` | `False` | `False` | FEVER 0.20 CP transfer remains negative; this is scientific negative evidence, not an operational blocker. | `do not claim a general formal risk-control guarantee`<br>`use results/fever_nearmiss_corm_v3_cp_transfer_sweep_summary_20260529.json as boundary evidence` |

## Execution Order

1. `complete_human_audit_labels`
2. `run_api_backed_llm_judge_batch`
3. `approve_and_execute_remote_ext4_cleanup`
4. `rerun_full_corm_reproduction_after_storage_probe_passes`
5. `obtain_independent_external_review_response`
6. `rerun_main_tables_and_claim_verifier`

## Claim Policy

This is an unblock plan, not evidence that the blockers are solved. It records the minimum external actions and repository commands needed before NeurIPS main-track readiness can be re-evaluated.
