# Cron Delivery Debugging

When a cron job appears to run but the user didn't receive the output.

## Diagnostic Pipeline (in order)

### 1. Check job state
```
cronjob list → check last_run_at, last_status, last_delivery_error
```

If `last_status` is "ok" and `last_run_at` is current: the job ran. If `last_run_at` is stale: the scheduler didn't fire it.

### 2. Check agent log for execution
```bash
grep "<job_id>" ~/.hermes/logs/agent.log | grep "Turn ended"
```

This confirms the LLM session completed. Look for `response_len` — if it's very small (~100 chars) the agent may have produced a closing line but the actual output was in a preceding turn.

### 3. Check for delivery confirmation
```bash
grep "<job_id>.*deliver" ~/.hermes/logs/agent.log
```

Look for "delivered to <target> via live adapter" or "delivered to <target>". If present: the scheduler believes it delivered.

### 4. Check gateway log for delivery event
```bash
grep "<job_id>\|deliver" ~/.hermes/logs/gateway.log | grep "<timestamp>"
```

If agent.log says "delivered" but gateway.log has no corresponding event: **the gateway was down**. The scheduler handed off the message, but there was no gateway to push it.

### 5. Check output cache
```bash
ls -lt ~/.hermes/cron/output/<job_id>/
```

Output files are saved even when delivery fails. The file contains the prompt + agent response. If the response section is truncated (just a closing line), the actual output was in a preceding turn — check the agent.log for the full conversation.

## Common Failure Modes

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| "delivered" in agent.log, nothing in gateway.log | Gateway was down | Restart gateway, re-run job, add watchdog |
| Output file has prompt but no briefing content | Agent's final turn was a closing line; content was in prior turn | Read earlier agent.log entries for that session |
| Job never ran | Scheduler down or job paused | Check gateway status, check job enabled |
| Delivery logged but user didn't receive | Wrong deliver target, platform paused | Check deliver field, check /platform status |
| deliver=local instead of origin | Job was created with wrong delivery setting | Update job deliver to correct target |

## Key Insight

The cron scheduler logs delivery success optimistically — it records "delivered" when it hands off the message, not when the platform confirms receipt. A dead gateway means the message dies in transit with a false success log. Always cross-reference agent.log delivery timestamps with gateway.log.
