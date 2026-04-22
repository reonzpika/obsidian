---
name: adopt
description: One-time setup skill for this vault. Writes vault-config.json with correct folder mappings so /daily, /weekly, and /monthly know where everything lives. Run once after installing these skills.
allowed-tools: Read, Write, Edit, Glob, Grep
user-invocable: true
---

# Adopt Skill

One-time configuration for Ryo's NexWave/ClinicPro Obsidian vault. Writes `vault-config.json` with the correct folder mappings so `/daily`, `/weekly`, and `/monthly` resolve paths correctly without prompting.

This vault is already structured. `/adopt` does not restructure anything — it only writes config.

## Usage

```
/adopt    # Run once from vault root after installing skills
```

## What it does

### Step 1: Verify vault structure

Check that these paths exist:

| Path | Purpose |
|------|---------|
| `tasks/open/` | Active task files |
| `tasks/done/` | Completed task files |
| `sprints/archive/` | Completed sprints — read-only archive |
| `projects/` | Project metadata files |
| `daily/` | Daily notes |
| `reviews/weekly/` | Weekly review outputs |
| `reviews/monthly/` | Monthly review outputs |
| `inbox/` | Quick capture |
| `templates/` | Obsidian templates |

If any path is missing, create it silently (no files, just the directory).

### Step 2: Write vault-config.json

Write `vault-config.json` to vault root:

```json
{
  "name": "Ryo",
  "vault": "NexWave / ClinicPro",
  "setupDate": "YYYY-MM-DD",
  "version": "1.0",
  "folderMapping": {
    "dailyNotes": "daily",
    "tasks": "tasks/open",
    "tasksDone": "tasks/done",
    "sprintsArchive": "sprints/archive",
    "projects": "projects",
    "reviewsWeekly": "reviews/weekly",
    "reviewsMonthly": "reviews/monthly",
    "inbox": "inbox",
    "templates": "templates"
  },
  "repos": [
    "clinicpro-saas",
    "clinicpro-medtech",
    "nexwave-rd",
    "gp-fellowship"
  ],
  "rdIsolation": true,
  "reviewDay": "Friday"
}
```

### Step 3: Confirm

Print a summary:

```
Vault configured.

Folder mapping:
  Daily notes    → daily/
  Tasks (open)   → tasks/open/
  Tasks (done)   → tasks/done/
  Sprint archive → sprints/archive/
  Projects       → projects/
  Weekly reviews → reviews/weekly/
  Monthly reviews→ reviews/monthly/
  Inbox          → inbox/

R&D isolation: enabled
Review day: Friday

Run /daily to create today's note.
Run /weekly for a project review.
Run /monthly at end of month.
```

## Notes

- This skill is idempotent — safe to re-run if paths change
- Do not modify `.obsidian/` — Obsidian GUI manages that
- Do not touch `dashboards/` — those are Dataview-managed
- If `vault-config.json` already exists, overwrite it (it's generated config, not hand-edited)
