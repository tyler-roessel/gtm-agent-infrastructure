# Error Handling

## Categories

| Category | Examples | Action |
| --- | --- | --- |
| Transient | timeout, 429, 5xx | retry with backoff |
| Recoverable | duplicate, schema mismatch, validation error | preserve payload and queue review |
| Terminal | missing credentials, deleted base, invalid webhook | pause and alert |

## Batch Rule

A single bad record should not stop a batch. Preserve the failed record, continue the run, and pause only when the failure rate suggests a systemic problem.

| Failure Rate | Action |
| --- | --- |
| < 5% | log and continue |
| 5-20% | log, continue, flag for review |
| > 20% | pause pipeline |

