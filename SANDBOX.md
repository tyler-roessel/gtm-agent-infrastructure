# Sandbox

The sandbox runs the workflow with synthetic data only.

## Run

```bash
cd agent
python3 orchestrator.py --sandbox --records 25
```

Optional checks:

```bash
python3 orchestrator.py --sandbox --records 50 --simulate-rate-limit
python3 orchestrator.py --sandbox --records 50 --simulate-20pct-failure
python3 orchestrator.py --sandbox --records 25 --auto-approve
python3 orchestrator.py --sandbox --records 25 --export ../examples/sandbox-output.csv
```

## Expected Flow

```text
source -> identity -> enrichment -> scoring -> draft -> review -> CRM write plan
```

Sandbox mode does not call Airtable, Attio, Salesforce, HubSpot, n8n, Firecrawl, or any external API. It only simulates the boundaries.

## What To Inspect

- Whether records are created with synthetic `.test` domains.
- Whether low-confidence records are rejected or held for review.
- Whether approved records generate CRM write plans rather than blind writes.
- Whether failed records are preserved with error context.

