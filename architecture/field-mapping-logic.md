# Field Mapping Logic

## Principles

1. Every field has one authority.
2. Transforms are documented before workflow nodes are changed.
3. Reviewer edits override AI-generated draft fields.
4. Dedupe runs before create.
5. Failed writes preserve the payload for replay.

## Example Map

| Source Field | CRM Target | Transform | Authority |
| --- | --- | --- | --- |
| Company Name | company.name | trim, normalize suffix | Airtable |
| Domain | company.domain | strip protocol, lowercase | Airtable |
| ICP Segment | company.icp_segment | direct | Airtable |
| ICP Score | company.icp_score | round to 2 decimals | Airtable |
| Review Status | none | internal only | Airtable |
| Owner | owner_id | CRM assignment | CRM |
| Deal Stage | deal.stage | CRM workflow | CRM |
| Activity Summary | activity.note | summarize from call/email/meeting | CRM -> Airtable context |

