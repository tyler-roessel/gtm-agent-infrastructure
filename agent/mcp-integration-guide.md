# MCP Integration Guide

Before MCP, the system used manually coded scripts and CLI runs:

```text
terminal -> Python script -> API call -> CSV/review packet
```

MCP turned those scripts into tools with a stable interface:

```text
n8n or agent -> MCP server -> enrich_company / score_icp / map_fields / draft_record
```

MCP did not create the workflow. It made the already-mapped workflow easier to call from agents and automation.

## Tool Shape

Each tool should expose:

- name
- purpose
- JSON input schema
- JSON output schema
- error contract
- idempotency key

## Example Tools

- `normalize_company_identity`
- `enrich_company`
- `score_icp`
- `map_to_crm_payload`
- `build_review_packet`
- `write_approved_record`

