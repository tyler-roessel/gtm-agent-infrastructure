# ICP Builder

The ICP layer segments pipeline records so the agent can route enrichment, review cadence, and CRM handoff correctly.

ICP is treated as a decision system, not a static persona list. Each segment needs fit signals, disqualifiers, source evidence, confidence thresholds, and a clear routing rule for what happens next.

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

## Search And Filter Criteria

Each discovery rule should preserve why a record was found and why it remained in the queue:

- inclusion criteria: role, market, trigger, company stage, tech stack, hiring signal, funding signal, category movement, or workflow pain;
- exclusion criteria: wrong company size, weak buying signal, irrelevant geography, stale source, duplicate account, bad domain match, or no clear owner;
- evidence fields: source URL, observed text, timestamp, source trust level, matched rule, and reviewer decision;
- confidence fields: fit score, reason code, missing data, and whether the record can move automatically or needs review.

## Voice And Writing Boundaries

ICP fit should not automatically produce outreach or CRM notes. Drafting requires a separate writing layer:

- approved company language and positioning;
- claims that can be made;
- claims that should be avoided;
- tone and level of directness;
- when to write a summary, task, email draft, Slack handoff, or internal note;
- when not to write because the evidence is too thin.
