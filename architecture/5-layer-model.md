# Five-Layer Model

## 1. Data Layer

Airtable holds enrichment, source attribution, review state, ICP scoring, and field maps. The CRM holds account/contact/deal state, ownership, and activity timeline.

The data layer also needs operating memory: company positioning, brand voice, offer language, proof points, exclusion rules, ICP criteria, source trust, and team routing rules. Without those inputs, an agent can produce fluent text while still violating the way the company actually sells.

## 2. Agent Layer

The orchestrator and MCP tools enrich records, score ICP fit, map fields, generate drafts, and return structured review packets.

Agent outputs should be bounded by explicit instructions:

- what can be written;
- what should never be written;
- which evidence supports the recommendation;
- which fields can be changed automatically;
- which fields require human approval;
- which team owns the next action.

## 3. Workflow Layer

n8n handles scheduled discovery, webhooks, transforms, retries, error workflows, and polling fallbacks.

Workflow triggers can come from discovery sources or from sales-cycle events: call notes, signed MSAs, stage changes, objections, new stakeholders, implementation blockers, renewal signals, support escalations, or internal handoff requests.

## 4. Partnership And Source Layer

Source quality influences routing. A trusted referral, job-posting scrape, directory source, and manual entry should not receive identical review intensity.

Source criteria should be searchable and reviewable. The system should preserve why a record entered the queue, which rule matched, which rule excluded a similar record, and whether the result was accepted or rejected by a reviewer.

## 5. Analytics Layer

Pipeline velocity, approval rate, rejection reasons, source quality, field completion, and CRM write failures determine when a workflow can move from full review to sampling or automation.

The analytics layer should also measure writing quality and handoff quality: off-brand drafts, weak evidence, unclear owner, wrong team route, stale ICP assumptions, repeated rejection reasons, and downstream sync failures.
