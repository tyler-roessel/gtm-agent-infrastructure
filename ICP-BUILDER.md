# ICP Builder

The ICP layer segments pipeline records so the agent can route enrichment, review cadence, and CRM handoff correctly.

## Segments

| Segment | Typical Signals | Enrichment Priority | Review Cadence |
| --- | --- | --- | --- |
| Growth-First Founder | seed stage, small team, first sales hire, founder-led GTM | funding, team, tech stack, founder signal | daily batch |
| Revenue Operations Lead | tool sprawl, data quality issues, stack ownership | tool stack, schema drift, process ownership | per record |
| VP of Sales | pipeline coverage, forecast accuracy, rep productivity | sales org, activity patterns, CRM state | weekly summary |
| GTM Platform Builder | technical GTM role, workflow automation, APIs | GitHub/blog/API/tooling signals | triage queue |

## Feedback Loop

```text
review decision -> rejection reason -> scoring rule -> validation check -> routing gate
```

The ICP definitions should change only when review evidence supports a change.

