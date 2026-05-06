# Progression

This system was built in stages: terminal experiments, sandbox runs, human review, repeatable gates, and finally automation-ready execution.

## Stage 1: Discovery And Intake

The first version was manual. A terminal run or Claude Code session took a source list, normalized company identity, and produced CSV/Markdown output for review.

What changed:

- Raw source data became structured intake records.
- Manual research became repeatable enrichment steps.
- Source, timestamp, domain, and identity confidence became required fields.

Lesson: a prompt is not a system. The system begins when input, output, and review state are repeatable.

## Stage 2: Human Identity Review And Cleanup

The early failures were mostly identity failures: wrong company, duplicate domain, partial contact data, or records that looked promising but did not match the ICP.

What changed:

- Human cleanup became an explicit review gate.
- Dedupe moved before CRM writes.
- Rejection reasons were captured instead of discarded.

Lesson: review is not overhead. Review is training data for the workflow.

## Stage 3: Verification, Enrichment, And Scoring

Once identity became cleaner, the system added enrichment and scoring. Companies were scored against ICP segments and routed by confidence.

What changed:

- Enrichment status became tracked state.
- ICP score and segment became routing fields.
- Missing fields and low-confidence records were queued instead of forced through.

Lesson: scoring only helps if it changes routing behavior.

## Stage 4: Drafting, Recommendation, And Review

The AI began producing CRM-ready drafts: summary, suggested actions, source context, likely ICP, and write recommendation.

What changed:

- Drafts went to the review queue, not directly to the CRM.
- Reviewer edits overrode AI output.
- Approval, rejection, and edit reasons fed back into the scoring logic.

Lesson: AI becomes useful when its output is shaped for a decision, not when it produces more text.

## Stage 5: CRM Handoff And Automation-Ready Execution

Only after the workflow stabilized did approved records move into CRM write paths.

What changed:

- Field maps became explicit.
- Airtable and CRM field authority was documented.
- n8n handled triggers, retries, polling fallback, and error logging.
- MCP tools provided a standard interface for enrichment, scoring, mapping, and drafting.

Lesson: automation is the maturity state of a stable workflow. It is not a separate stage.

## MCP Transition

Before MCP, the integration was manually coded: terminal scripts, local CLIs, webhook wrappers, and direct API calls. The useful pattern was already there before MCP was installed.

MCP did not create the architecture. It standardized the interface:

```text
Before: terminal -> script -> API -> CSV/review
After: n8n/agent -> MCP tool -> enrichment/scoring/mapping -> review gate
```

That distinction matters. The engineering work was mapping the process, not only adopting a protocol.

