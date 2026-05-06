# Legacy Data Note

The private system had large historical datasets, but this public repo does not include them.

The architectural decision was to rebuild around clean schemas and review gates instead of importing dirty historical records into a new model. Legacy data can be migrated later only by passing through the same identity, enrichment, validation, and review process as new records.

This repo uses synthetic sample data to show the system mechanics without exposing private records.

