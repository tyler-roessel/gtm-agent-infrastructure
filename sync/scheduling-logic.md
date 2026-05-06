# Scheduling Logic

| Workflow | Pattern | Frequency |
| --- | --- | --- |
| Source Discovery | periodic | daily or weekly |
| Enrichment | event-driven | on demand |
| Review Gate Check | polling fallback | every 15 minutes during business hours |
| CRM Sync | event-driven | on approval |
| Activity Sync | event-driven or batch | near real-time or daily |
| Data Quality Check | periodic | weekly |
| Re-enrichment | periodic | monthly or source-specific |

Schedules should be documented before they are changed in n8n.

