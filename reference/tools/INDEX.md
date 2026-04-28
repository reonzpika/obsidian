---
name: Tools index
---

# Tools Index

Tool, resource, and industry-reference notes queued from Ryo's personal Gmail tips. Auto-populated by `/daily` Step 9. Each file has `researched: false` until I ask Claude to deep-dive one.

## All tools by category

```dataview
TABLE category, status, source-email-date AS "Date", researched
FROM "context/tools"
WHERE file.name != "INDEX"
SORT category ASC, source-email-date DESC
```

## Unresearched queue

```dataview
LIST
FROM "context/tools"
WHERE researched = false AND file.name != "INDEX"
SORT source-email-date DESC
```
