# CRM API Patterns

The private implementation used Attio patterns, but the public architecture is CRM-portable.

## Create Path

```text
approved review -> field map -> dedupe -> create/update company -> create/update contacts -> log activity -> update review result
```

## Dedupe Keys

| Object | Primary Key | Fallback |
| --- | --- | --- |
| Company | normalized domain | normalized name + location |
| Contact | email | LinkedIn URL |
| Deal | CRM account ID + opportunity name | external source ID |

## Error Handling

- 400 validation error: queue for manual review with payload.
- 401/403 auth error: pause workflow and alert admin.
- 404 object missing: log drift and queue repair.
- 429 rate limit: exponential backoff.
- 5xx server error: retry, then preserve failure for replay.

## Environment Variables

```bash
CRM_API_TOKEN=
CRM_WORKSPACE_ID=
CRM_API_BASE_URL=
AIRTABLE_API_KEY=
AIRTABLE_BASE_ID=
```

These are placeholders only. Do not commit real values.

