# Client Communications To CRM Showcase

Pattern:

```text
call/email/notes/MSA/stage change
  -> action extraction
  -> sales-cycle interpretation
  -> owner routing
  -> CRM status update
  -> team handoff
  -> feedback loop
```

The system identifies next steps, names the owner, routes to marketing/sales/engineering/customer success/finance, updates CRM state, and preserves the handoff trail.

## Sales-Cycle Signals

Examples of events that should change routing:

- a discovery call creates a follow-up task and updates the activity timeline;
- an objection creates a sales note and a research request;
- a technical blocker routes to engineering or implementation;
- a signed MSA updates deal state and routes onboarding, finance, and customer success;
- a new stakeholder creates a contact update and owner task;
- a renewal or expansion signal routes to account management.

## Handoff Shape

Each handoff should include:

- source evidence;
- recommended action;
- owner;
- target system;
- fields to update;
- fields that require review;
- writing boundary if a customer-facing draft is created.
