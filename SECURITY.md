# Security And Sanitization

Do not commit secrets or live operational data.

Before publishing changes, run:

```bash
rg -n "TTR|fld[A-Za-z0-9]{10,}|pat[A-Za-z0-9]{10,}|key-[A-Za-z0-9]{10,}|sk-[A-Za-z0-9]{10,}|xox[baprs]-|hooks.slack.com|webhook.site|ngrok|airtable.com/app|api.attio.com|https://[^ ]*webhook" .
```

Expected matches are documentation references to public tool names such as Attio or Airtable. There should be no real IDs, tokens, webhook URLs, or private company/customer names.
