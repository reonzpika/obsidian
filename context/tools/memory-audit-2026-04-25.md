---
title: Memory file audit
created: 2026-04-25
type: audit
---

## Summary

- Total memory files: 20 (excluding MEMORY.md index)
- By type: feedback (12), reference (3), project (3), user (1), unclassified (1 — `feedback_human_review_required.md` missing `type:` field)
- All 20 files are listed in MEMORY.md. No unlisted files found.
- All MEMORY.md links resolve to actual files.
- 2 files missing `type:` frontmatter field.
- 2 project-state memories are probably stale or partially stale.
- 1 contradiction found (PowerShell profile path).
- 0 broken links.

---

## Audit table

| File | Type | Classification | Issue | Recommended action |
|---|---|---|---|---|
| feedback_yaml_quoting.md | feedback | Green | None | Keep |
| project_nexwave_rd_obj1_state.md | project | Stale (partial) | Describes Step 2 as "next"; vault shows Steps 2 and 3 complete as of 14 Apr. Sprint goals also stale (Sprint 1 Apr described as current; Sprint 2 ends today). | Update or replace with current Step 4/Sprint 3 state |
| project_nexwave_health_name.md | project | Green | Name check was April 2026; no staleness risk short-term | Keep; re-verify if approaching TGA/regulatory filing |
| project_indici_contacts.md | project | Probably stale | Last outreach logged 2026-04-16. Fallback deadline (2026-04-16 for warm intros) has passed. Task rd-20260329-020 still `in-progress`. Outreach status likely changed. | Verify current status of rd-20260329-020 and update outreach history |
| feedback_gmail_draft_skill.md | feedback | Green | None | Keep |
| feedback_use_gws_not_mcp.md | feedback | Green | None | Keep |
| reference_powershell_profile.md | reference | Contradiction | States PS profile is at OneDrive path. `reference_documents_path.md` states "Always C:\\Users\\reonz\\Documents, never OneDrive." These two rules are not contradictory in substance (PS profile is a legacy exception), but the wording creates a likely mis-application: the documents rule says "never OneDrive" with no exceptions, while the PS profile rule relies on an exception. The exception is documented inline but easy to miss. | Add explicit cross-reference note in reference_documents_path.md flagging the PS profile as a named exception |
| feedback_task_approval.md | feedback | Green | None | Keep |
| feedback_decisions_routing.md | feedback | Green | References `/daily` skill update on 2026-04-15; skill may have evolved since but the rule itself is durable | Keep |
| feedback_daily_status_updates.md | feedback | Green | None | Keep |
| feedback_vault_file_placement.md | feedback | Green | None | Keep |
| user_helen_accountant_scope.md | user | Green | Scope agreed 2026-04-19; still current | Keep |
| feedback_daily_quickwins_dedup.md | feedback | Green | None | Keep |
| reference_documents_path.md | reference | Green — with caveat | Rule is correct but does not name the PS profile exception explicitly. Contradiction risk with reference_powershell_profile.md (see above). | Consider adding: "Exception: PowerShell profile is legacy at OneDrive path — see reference_powershell_profile.md" |
| reference_motionsites.md | reference | Green | None | Keep |
| feedback_daily_briefing_table.md | feedback | Green | None | Keep |
| feedback_human_review_required.md | feedback | Missing `type:` field | Frontmatter has `name:` and `description:` but no `type:` field | Add `type: feedback` |
| feedback_verify_before_describe.md | feedback | Missing `type:` field | Same — no `type:` field | Add `type: feedback` |
| feedback_session_update_before_daily.md | feedback | Green | None | Keep |
| feedback_youtube_transcription.md | feedback | Green | None | Keep |

---

## Stale entries (verify before next session)

| File | Why flagged | What to check |
|---|---|---|
| project_nexwave_rd_obj1_state.md | Describes "Next step: Step 2 — Literature review and architecture research." Vault shows Steps 2 and 3 complete as of 14 April 2026. Sprint 1 Apr described as current; Sprint 2 ends today (25 Apr). Sprint 3 (2026-05-rd-sprint-1, starts 26 Apr) covers synthetic data design and architecture evaluation — the actual current step. | Read nexwave-rd-obj-1.md and the active sprint to confirm current step, then update or replace this memory |
| project_indici_contacts.md | Outreach history last entry is 2026-04-16. Warm-intro fallback trigger date (2026-04-16) has passed. Task rd-20260329-020 still shows `status: in-progress` with no new entries after 16 April. It is 25 April — 9 days since last recorded action. | Check rd-20260329-020.md and email for any replies from Valentia/Indici since 16 April; update outreach history |

---

## Contradictions found

| Memory A | Memory B | Conflict description |
|---|---|---|
| reference_powershell_profile.md | reference_documents_path.md | PS profile memory says profile lives at `C:\Users\reonz\OneDrive\Documents\WindowsPowerShell\...`. Documents path memory says "Always C:\Users\reonz\Documents, never OneDrive — treat this as a hard invariant." The PS profile memory documents this as a legacy exception and the rule applies to new files, so there is no operational conflict — but the blanket "never OneDrive" wording in the Documents rule does not name the exception. A future agent reading only the Documents rule would incorrectly conclude the PS profile path is wrong. Low severity but worth a cross-reference note. |

---

## Index sync issues

| Issue | Detail |
|---|---|
| No unlisted files | All 20 .md files in the directory (excluding MEMORY.md) are in the index. No orphans. |
| No broken links | All 20 links in MEMORY.md resolve to existing files. |
| Index entry lengths | All entries are under 150 characters. |
| Missing `type:` field | `feedback_human_review_required.md` and `feedback_verify_before_describe.md` lack `type:` in frontmatter. Both have `name:` and `description:`. Minor format deviation — does not break anything. |

---

## Missing memory candidates

| Topic | Why it should be saved | Suggested type |
|---|---|---|
| MBIE Q1 claim format and evidence requirements | Vault has detailed notes on what Q1 requires (progress report, cost spreadsheet, GST invoice, PAYE evidence) but no memory entry. Any agent helping with Q1 prep (due 31 May 2026) would benefit from a concise rule about required artefacts and submission steps. | project |
| Buddle Findlay as selected compliance partner | The compliance engagement decision is documented in nexwave-rd.md (week of 23 Apr) but not in memory. Any agent asked about regulatory or compliance questions needs to know Buddle Findlay is the primary partner and Bell Gully is on-hold fallback, and NOT to re-open evaluation of other firms. | project |
| Contract salary discrepancy — corrected contracts required before Q1 | Employment contracts (Ryo + Ting) have stated annual salaries that do not reconcile with actual payroll rates. Helen needs to issue corrected versions before Q1 claim. Tracked in rd-20260420-004. If not in memory, an agent may treat contracts as settled. | project |
| Sprint end = today rule: Sprint 2 ends 2026-04-25, Sprint 3 starts 2026-04-26 | Current sprint boundary is a common point of confusion at session start. Saving this as a time-bounded reference would prevent agents from reading Sprint 2 as current after today. | reference (or omit — time-bounded, low value after 26 Apr) |
| `context/people.md` as canonical scope doc for all team contacts | Helen scope memory references people.md as single source of truth, but no memory explicitly tells agents to check people.md before making assumptions about any person's role (Ting, Helen, Lisa Pritchard, etc.). A general routing rule would reduce drift across sessions. | feedback |

---

_First draft only. Requires Ryo's review before acting on any recommendation._
