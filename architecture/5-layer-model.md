# Five-Layer Model

## 1. Data Layer

Airtable holds enrichment, source attribution, review state, ICP scoring, and field maps. The CRM holds account/contact/deal state, ownership, and activity timeline.

## 2. Agent Layer

The orchestrator and MCP tools enrich records, score ICP fit, map fields, generate drafts, and return structured review packets.

## 3. Workflow Layer

n8n handles scheduled discovery, webhooks, transforms, retries, error workflows, and polling fallbacks.

## 4. Partnership And Source Layer

Source quality influences routing. A trusted referral, job-posting scrape, directory source, and manual entry should not receive identical review intensity.

## 5. Analytics Layer

Pipeline velocity, approval rate, rejection reasons, source quality, field completion, and CRM write failures determine when a workflow can move from full review to sampling or automation.

