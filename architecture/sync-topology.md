# Sync Topology

Core rule: no field is writable from two systems.

| Flow | Direction | Trigger | Purpose |
| --- | --- | --- | --- |
| Source discovery | Source -> Airtable | schedule/manual | create identity-stage records |
| Enrichment | Agent/MCP -> Airtable | webhook | add context, ICP score, draft |
| Review gate | Airtable -> n8n | status change/polling | process approval, rejection, or edit |
| CRM write | Airtable -> CRM | approved review | create/update company/contact/deal records |
| Activity sync | CRM -> Airtable | CRM webhook/daily batch | feed call/email/meeting context back into scoring |

Attio, Salesforce, and HubSpot can all fit this pattern. The CRM adapter changes; the authority model should not.

