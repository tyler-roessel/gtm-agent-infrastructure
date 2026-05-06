# GTM Infrastructure Public Showcase

This repo is a sanitized public mirror of a private GTM automation architecture. It preserves the real system shape, stage progression, orchestration patterns, review gates, MCP transition, CRM mapping logic, and implementation lessons while replacing private business data, credentials, schemas, prompts, webhooks, and customer/prospect details with safe examples.

It is not a product and it is not a turnkey integration. It is a reference system for how sales pipeline data, enrichment workflows, CRM tooling, and AI agents can fit together when the workflow is built in stages instead of wired directly into production.

## What This Demonstrates

- How a messy GTM process was modeled as a five-stage operating workflow.
- How AI outputs were moved from terminal experiments to sandbox runs, human review, and automation-ready execution.
- How Airtable, Attio, n8n, MCP tools, and agent code can be separated by ownership boundary.
- How field authority, deduplication, review gates, retries, and CRM write paths are documented before they are automated.
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

## How A CTO Or Engineer Should Review This Sample

Review it as an architecture and implementation evidence sample, not as a packaged SaaS app.

Start with these questions:

- Does the repo show where each system owns state?
- Does the code demonstrate a real pipeline shape rather than vague AI claims?
- Does the review gate prevent blind CRM writes?
- Are failure modes explicit?
- Can the workflow be mapped from terminal run to enrichment, Airtable review, n8n routing, and CRM handoff?
- Is the abstraction portable to Attio, Salesforce, HubSpot, or another CRM?
- Is private data excluded while the implementation pattern remains concrete?

The answer should be yes. The runnable sandbox exists so reviewers can inspect the pipeline mechanics without needing credentials.

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

