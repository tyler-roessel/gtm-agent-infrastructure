# n8n Pipeline Logic

## Workflows

1. Source Discovery: scheduled source polling, normalization, dedupe.
2. Enrichment Pipeline: calls orchestrator/MCP tools and updates Airtable.
3. Voice And Criteria Check: compares draft language, ICP fit, exclusion rules, and source evidence before routing.
4. Review Gate: watches review status and routes approvals/rejections.
5. CRM Sync: maps approved records to CRM payloads and writes them.
6. Activity Sync: sends CRM activity context back into Airtable.
7. Team Handoff: routes approved next steps to Slack, task queues, implementation, finance, marketing, sales, or customer success.

## Node Naming Convention

Use `[Stage] Action`, for example:

- `[Discover] Normalize Company`
- `[Enrich] Score ICP`
- `[Review] Check Brand Voice`
- `[Review] Check Writing Boundary`
- `[Review] Build CRM Payload`
- `[CRM] Dedupe Company`
- `[CRM] Write Activity Log`
- `[Route] Notify Customer Success`

## Credential Convention

Credentials are referenced by name in n8n. No workflow JSON should contain raw tokens, webhook secrets, base IDs, object IDs, or customer data.
