# Review Gate Example

```text
AI draft -> review queue -> approve/edit/reject -> CRM write plan -> write result
```

## Gate States

| Status | Meaning |
| --- | --- |
| pending | draft created, no write allowed |
| approved | ready for CRM write |
| edited | reviewer changed the AI draft before approval |
| rejected | do not write |
| duplicate | link to existing record |
| write_failed | approved, but CRM write failed |

## Automation Maturity

- Full Gate: every record reviewed.
- Batch Gate: stable sources reviewed in small batches.
- Sampling Gate: trusted workflows review a random sample.
- Monitoring Only: low-risk internal syncs write directly and revert to Full Gate on anomaly.

