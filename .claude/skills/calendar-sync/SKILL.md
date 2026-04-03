---
name: calendar-sync
description: Syncs active Obsidian sprints to Google Calendar (Projects Roadmap). Use whenever the user says "sync calendar", "update the calendar", "run calendar sync", "push sprints to calendar", or any variation of wanting their sprint timeline visible in Google Calendar. Always use this skill for calendar sync tasks — don't try to run the script directly without following this workflow.
---

# Calendar Sync — Projects Roadmap

This skill syncs active sprint files from the Obsidian vault to the "Projects Roadmap" Google Calendar. It follows a read → propose → approve → execute flow.

## Step 1: Read active sprint files

Read all `.md` files in `C:/Users/reonz/Cursor/obsidian/sprints/active/`.

For each file, extract from frontmatter:
- `id` — sprint identifier (e.g. `2026-03-sprint-1`)
- `start` — start date (YYYY-MM-DD)
- `end` or `due` — end date (use `end` if present, fall back to `due`)
- `projects` — list of project IDs
- `goal` — one-line description

## Step 2: Check for missing dates

If any sprint is missing `start` or both `end`/`due`, **stop and ask the user** to provide the missing dates before continuing. Do not proceed with incomplete data — the calendar event would be malformed.

Example:
> Sprint `2026-04-sprint-2` is missing an end date. What date should it finish?

Once the user provides dates, update the sprint frontmatter before running the script.

## Step 3: Propose changes

Present a clear table of what the script will do — do not run anything yet:

```
Proposed calendar sync:

  CREATE  2026-03-sprint-1  →  ClinicPro Capture — Landing Page       (Mar 27 – Apr 6)
  CREATE  2026-03-sprint-2  →  Referral Images — Paid Launch           (Mar 31 – Apr 5)
  SKIP    2026-04-sprint-1  →  no changes

Proceed? (yes / adjust)
```

The script determines CREATE/UPDATE/SKIP/DELETE automatically based on what's already in the calendar — you don't need to predict this yourself. Just show the sprint data and say "I'll sync these sprints — proceed?"

## Step 4: Execute on approval

Once the user approves, run:

```bash
cd C:/Users/reonz/Cursor && python calendar_sync.py
```

Show the terminal output to the user. A successful run looks like:

```
  CREATE 2026-03-sprint-1 (2026-03-27 -> 2026-04-06)
  SKIP   2026-04-sprint-1 (no changes)
Done! Open Google Calendar -> Projects Roadmap to see your timeline.
```

## Reference

- **Script:** `C:/Users/reonz/Cursor/calendar_sync.py`
- **Auth token:** `C:/Users/reonz/Cursor/token.json` (cached after first run — no browser prompt needed on repeat runs)
- **Sprint files:** `C:/Users/reonz/Cursor/obsidian/sprints/active/*.md`
- **Calendar name:** `Projects Roadmap`
- **Color map:** clinicpro-capture=blue, referral-images=green, nexwave-rd=purple, ai-scribe=orange, gp-fellowship=yellow, 12-month-prescription=pink

## When a sprint ends

When a sprint moves from `sprints/active/` to `sprints/archive/`, the next calendar sync automatically deletes its calendar event. No manual cleanup needed.
