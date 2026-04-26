---
title: Sprint archive integrity check
created: 2026-04-25
type: audit
---

## Summary

16 sprint files in archive. 0 clean (no file has terminal status). 10 files carry `status: active` — the most critical issue. 5 files have end dates in the future (not yet due). 1 file uses `due:` instead of `end:` for the end date field. All 16 files are missing a `title:` frontmatter field (they use `goal:` instead — possible intentional schema variant, but worth standardising). No open tasks reference any sprint ID via a `sprint:` field, so no cross-reference violations.

---

## Archive inventory

| File | ID | Status | Start | End | Goals present |
|---|---|---|---|---|---|
| 2026-03-sprint-1.md | 2026-03-sprint-1 | active | 2026-03-27 | 2026-04-06 (via `due:`) | Yes (Dataview only) |
| 2026-03-sprint-2.md | 2026-03-sprint-2 | done | 2026-03-31 | 2026-04-05 | Yes (Dataview only) |
| 2026-03-rd-sprint-1.md | 2026-03-rd-sprint-1 | active | 2026-03-15 | 2026-03-28 | Yes (retrospective body) |
| 2026-04-sprint-1.md | 2026-04-sprint-1 | active | 2026-04-07 | 2026-04-18 | Yes (Dataview only) |
| 2026-04-gpf-sprint-1.md | 2026-04-gpf-sprint-1 | active | 2026-03-31 | 2026-04-07 | Yes (Dataview only) |
| 2026-04-medtech-sprint-1.md | 2026-04-medtech-sprint-1 | active | 2026-04-15 | 2026-04-21 | Yes (plan ref + Dataview) |
| 2026-04-medtech-sprint-2.md | 2026-04-medtech-sprint-2 | active | 2026-04-21 | 2026-05-16 | Yes (context + Dataview) |
| 2026-04-miozuki-sprint-1.md | 2026-04-miozuki-sprint-1 | done | 2026-04-03 | 2026-04-06 | Yes (Dataview only) |
| 2026-04-miozuki-sprint-2.md | 2026-04-miozuki-sprint-2 | done | 2026-04-04 | 2026-04-10 | Yes (context + progress body) |
| 2026-04-rd-sprint-1.md | 2026-04-rd-sprint-1 | active | 2026-03-29 | 2026-04-11 | Yes (Dataview only) |
| 2026-04-rd-sprint-2.md | 2026-04-rd-sprint-2 | active | 2026-04-12 | 2026-04-25 | Yes (Dataview only) |
| 2026-04-saas-sprint-1.md | 2026-04-saas-sprint-1 | done | 2026-04-15 | 2026-04-21 | Yes (Dataview only) |
| 2026-05-gpf-sprint-1.md | 2026-05-gpf-sprint-1 | active | 2026-04-23 | 2026-05-22 | Yes (Dataview only) |
| 2026-05-rd-sprint-1.md | 2026-05-rd-sprint-1 | active | 2026-04-26 | 2026-05-09 | Yes (Dataview only) |
| 2026-05-rd-sprint-2.md | 2026-05-rd-sprint-2 | active | 2026-05-10 | 2026-05-23 | Yes (Dataview only) |
| 2026-06-rd-sprint-1.md | 2026-06-rd-sprint-1 | active | 2026-05-24 | 2026-06-06 | Yes (Dataview only) |

---

## Schema violations

| File | Missing field | Issue |
|---|---|---|
| All 16 files | `title:` | No file has a `title:` frontmatter field. All use `goal:` instead. Either the schema expectation is wrong, or all files need a `title:` alias added. Flag for schema decision. |
| 2026-03-sprint-1.md | `end:` | Uses `due: 2026-04-06` for the end date instead of `end:`. Other files use `end:`. Inconsistent. |
| 2026-04-miozuki-sprint-1.md | `end:` | No end date field at all (no `end:` and no `due:`). End date is unrecorded. |
| 2026-04-miozuki-sprint-1.md | `dashboard:` | Missing `dashboard:` field. All other files have it. |

---

## Anomalies

| File | Issue | Detail |
|---|---|---|
| 2026-03-sprint-1.md | status: active | End date 2026-04-06 is in the past. Sprint is over but never marked complete. |
| 2026-03-rd-sprint-1.md | status: active | End date 2026-03-28 is in the past. Sprint is over but never marked complete. |
| 2026-04-sprint-1.md | status: active | End date 2026-04-18 is in the past. Sprint is over but never marked complete. |
| 2026-04-gpf-sprint-1.md | status: active | End date 2026-04-07 is in the past. Sprint is over but never marked complete. |
| 2026-04-medtech-sprint-1.md | status: active | End date 2026-04-21 is in the past. Sprint is over but never marked complete. |
| 2026-04-medtech-sprint-2.md | status: active + future end | End date 2026-05-16 is in the future (today: 2026-04-25). Sprint is still running but already archived. Likely archived prematurely or is a planned sprint. |
| 2026-04-rd-sprint-1.md | status: active | End date 2026-04-11 is in the past. Sprint is over but never marked complete. |
| 2026-04-rd-sprint-2.md | status: active | End date 2026-04-25 is today. Sprint ends today, status not yet updated to complete. |
| 2026-05-gpf-sprint-1.md | status: active + future end | End date 2026-05-22 is in the future. Sprint is still running but already in archive. |
| 2026-05-rd-sprint-1.md | status: active + future end | Start date 2026-04-26 is tomorrow; end date 2026-05-09 is in the future. Sprint has not started yet but is already in archive. |
| 2026-05-rd-sprint-2.md | status: active + future end | Start date 2026-05-10 is in the future. Sprint has not started. Should not be in archive. |
| 2026-06-rd-sprint-1.md | status: active + future end | Start date 2026-05-24 is in the future. Sprint has not started. Should not be in archive. |

---

## Open tasks referencing closed sprints

No open task files in `tasks/open/` contain a `sprint:` frontmatter field. No cross-reference violations found.

---

## Non-archive sprint files

None. No sprint files found in `sprints/` outside of `sprints/archive/`.

---

## Notes for review

1. **10 of 16 archive files have `status: active`.** The 4 with past end dates and `status: done` (2026-03-sprint-2, 2026-04-miozuki-sprint-1, 2026-04-miozuki-sprint-2, 2026-04-saas-sprint-1) are the only correctly closed sprints in the archive.

2. **Future-dated sprints in archive.** 2026-05-rd-sprint-1, 2026-05-rd-sprint-2, 2026-06-rd-sprint-1, and 2026-05-gpf-sprint-1 all have future start and/or end dates. These appear to be forward-planned sprint shells placed in archive prematurely. They should either remain in a `sprints/planned/` or `sprints/` folder until active, or the archive policy needs clarifying for pre-planned sprints.

3. **`goal:` vs `title:` field.** The vault CLAUDE.md schema does not define a sprint frontmatter schema explicitly. The `goal:` field appears to be the intentional label. If `title:` is not required for sprints, the schema check expectation in the audit spec may be over-broad. Recommend confirming the canonical sprint schema.

4. **`2026-04-rd-sprint-2` ends today.** Status should be updated to `done` at close of day if work is complete.

---

*All output is a first draft for human review.*
