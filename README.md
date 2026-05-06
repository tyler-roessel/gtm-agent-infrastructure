# GTM Infrastructure Public Showcase

This repo is a sanitized public mirror of a private GTM automation architecture. It preserves the real system shape, stage progression, orchestration patterns, review gates, MCP transition, CRM mapping logic, and implementation lessons while replacing private business data, credentials, schemas, prompts, webhooks, and customer/prospect details with safe examples.

It is not a product and it is not a turnkey integration. It is a reference system for how sales pipeline data, enrichment workflows, CRM tooling, and AI agents can fit together when the workflow is built in stages instead of wired directly into production.

## What This Demonstrates

- How a messy GTM process was modeled as a five-stage operating workflow.
- How AI outputs were moved from terminal experiments to sandbox runs, human review, and automation-ready execution.
- How Airtable, Attio, n8n, MCP tools, and agent code can be separated by ownership boundary.
- How field authority, deduplication, review gates, retries, and CRM write paths are documented before they are automated.
- How company voice, ICP rules, source criteria, and writing boundaries can be turned into explicit system inputs instead of informal tribal knowledge.
- How sales-cycle events such as calls, signed MSAs, new requirements, approvals, objections, and handoff notes can trigger different downstream actions.
- How the same pattern generalizes to Salesforce, HubSpot, Attio, or another CRM.

## The Five-Stage Workflow

The workflow stabilized into five stages:

1. Discovery and intake: identify a company, contact, activity, or signal from a source.
2. Human identity review and cleanup: normalize identity, remove obvious duplicates, and verify the record is worth enriching.
3. Verification, enrichment, and scoring: add firmographic/context data, score against ICPs, and validate required fields.
4. Drafting, recommendation, and review: create the CRM-ready draft, recommended action, routing decision, and reviewer notes.
5. CRM handoff and automation-ready execution: write approved records to the CRM, log outcomes, and sync downstream state.

Full automation happened after the five-stage workflow stabilized. Automation is the maturity state of the five stages, not a sixth stage.

## How The AI Was Taught

The AI was not asked to "just automate sales." It was taught through repeated feedback loops:

1. Sandbox outputs revealed failure patterns: wrong company identity, weak enrichment, duplicate risk, bad field mapping, overconfident CRM drafts.
2. Human review identified good and bad matches.
3. Review decisions became scoring rubrics.
4. Rubrics became prompts, schemas, validation checks, and field maps.
5. Validation checks became workflow gates.
6. Stable gates allowed parts of the workflow to move into automation.

This is the core lesson: the operating workflow came first, then the AI learned the workflow, then the system automated only the parts that had earned trust.

## Architecture And Data Flow

```text
Sources
  -> n8n discovery workflows
  -> agent/orchestrator.py or MCP tools
  -> Airtable review and enrichment layer
  -> human review gate
  -> CRM write path
  -> Attio / Salesforce / HubSpot style CRM objects
  -> activity sync and analytics
```

The important boundary is field authority:

- Airtable owns enrichment, review state, source attribution, ICP classification, and field maps.
- The CRM owns pipeline state, activity timeline, owner assignment, and rep-facing workflow.
- n8n owns triggers, retries, transforms, polling fallbacks, and webhooks.
- MCP exposes the agent/tool layer so workflows can call enrichment, scoring, mapping, and drafting tools through a standard interface.

## Operating Architecture

The repo is meant to show the infrastructure pattern behind a GTM system, not only a single enrichment script. A useful version has to preserve more than account fields:

```text
Company memory
  -> brand voice, positioning, offers, proof points, claims to avoid

ICP and source criteria
  -> fit rules, exclusion rules, source trust, scoring, confidence thresholds

Signal capture
  -> calls, emails, notes, web changes, job posts, funding, signed contracts

Agent review packet
  -> summary, evidence, recommended action, owner, routing reason, write payload

Human approval gate
  -> approve, reject, revise, hold, route to another team, update criteria

System handoff
  -> CRM, Slack, Airtable, n8n, Gong, data warehouse, marketing, sales, customer success
```

That means the system has to answer several practical questions before anything writes to a CRM:

- What language fits the company's brand, category, voice, and ethos?
- Which claims, terms, or outreach angles should not be written?
- Which ICP criteria matter for this motion, and what evidence supports the fit score?
- Which sources are trusted enough to route automatically, and which require review?
- What changed in the sales cycle: discovery call, objection, stakeholder add, MSA signed, renewal risk, implementation blocker, or new buying signal?
- Which team owns the next step, and which platform needs the update?
- What should become a CRM field, an activity note, a task, a Slack handoff, or a research queue item?

The sandbox uses synthetic records, but the implementation pattern is the same: collect evidence, score fit, generate a bounded recommendation, require review where confidence is low, then route approved outputs to the correct downstream system.

## What Was Preserved

- Real architecture shape and folder structure.
- Real five-stage workflow story.
- Real review gate and human-in-the-loop progression.
- Real MCP/CLI transition pattern.
- Real CRM mapping concerns: field authority, deduplication, retry behavior, webhook fallback, activity sync.
- Safe runnable sandbox code using synthetic records.

## What Was Sanitized

- No real prospects, customers, candidates, or company data.
- No webhook URLs, API keys, tokens, workspace IDs, field IDs, object IDs, or private schemas.
- No raw private prompts or session transcripts.
- No private business language.
- Sample data uses synthetic names and `.test` domains.

## Repo Map

```text
README.md
PROGRESSION.md
SANDBOX.md
ICP-BUILDER.md
LEGACY-DATA-NOTE.md
architecture/
agent/
airtable/
attio/
n8n/
sync/
showcases/
examples/
```

## Quick Start

```bash
cd agent
python3 orchestrator.py --sandbox --records 25
python3 orchestrator.py --sandbox --records 25 --export ../examples/sandbox-output.csv
python3 orchestrator.py --sandbox --records 50 --simulate-20pct-failure
```

No credentials are required. Sandbox mode calls no external APIs.
