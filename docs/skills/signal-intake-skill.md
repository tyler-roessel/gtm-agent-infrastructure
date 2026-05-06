# Signal Intake Skill

## Purpose

Collect source changes, market movement, account activity, and operating signals into a reviewable queue.

## What It Does

- Tracks what changed across selected sources.
- Preserves source, timestamp, observed text, and matched rule.
- Separates weak signals from records that deserve review.
- Creates a clean intake object that can be enriched, scored, or routed.

## Why It Matters

Most automated GTM systems fail at the first step because they treat every scraped or observed change as equal. This skill creates the first operating filter: what changed, why it may matter, and whether it deserves action.

## Outputs

- Signal summary
- Source evidence
- Matched criteria
- Confidence level
- Suggested next review queue

