# n8n Pipeline Logic

## Workflows

1. Source Discovery: scheduled source polling, normalization, dedupe.
2. Enrichment Pipeline: calls orchestrator/MCP tools and updates Airtable.
3. Review Gate: watches review status and routes approvals/rejections.
4. CRM Sync: maps approved records to CRM payloads and writes them.
5. Activity Sync: sends CRM activity context back into Airtable.

## Node Naming Convention

Use `[Stage] Action`, for example:

- `[Discover] Normalize Company`
- `[Enrich] Score ICP`
- `[Review] Build CRM Payload`
- `[CRM] Dedupe Company`
- `[CRM] Write Activity Log`

## Credential Convention

Credentials are referenced by name in n8n. No workflow JSON should contain raw tokens, webhook secrets, base IDs, object IDs, or customer data.

