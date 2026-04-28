---
title: Vault inconsistency audit
created: 2026-04-25
type: audit
---

## Executive summary

Files checked: 73 open tasks, 115 done tasks, 18 project files, 5 dashboard files.

- Check 1 (broken project refs): 10 issues
- Check 2 (wrong folder): 5 issues
- Check 3 (missing required frontmatter): 0 issues
- Check 4 (invalid field values): 0 issues in open tasks; 1 repo mismatch flagged separately
- Check 5 (orphaned tasks / parked project): 0 issues
- Check 6 (active projects with no open tasks): 4 projects
- Check 7 (milestone label drift): 1 minor inconsistency (quote style only, functionally identical)
- Check 8 (unquoted colons in frontmatter): 2 issues (both in tasks/done, not breaking active views)
- Check 9 (dashboard drift): 0 issues
- Check 10 (inline checkboxes): 0 issues
- Check 11 (project referenced but no file): 1 issue (same root cause as Check 1)

Total distinct issues: 18 across 6 categories.

---

## Check 1: Broken project references

Ten open tasks reference `project: nexwave-rd`, which does not exist as a project file. The valid R&D project IDs are `nexwave-rd-obj-1` and `nexwave-rd-compliance`.

Note: the `nexwave-rd` dashboard Dataview query has a manual carve-out (`t.project === "nexwave-rd"`) that catches these tasks, so they currently appear in the dashboard. However, per-project views in `projects/nexwave-rd-obj-1.md` and `projects/nexwave-rd-compliance.md` will not show these tasks.

| Task file | project: value | Issue |
|---|---|---|
| rd-20260329-013.md | nexwave-rd | No project file with this id; probably nexwave-rd-compliance (objective: capability) |
| rd-20260329-020.md | nexwave-rd | No project file with this id; probably nexwave-rd-obj-1 (objective: obj-1) |
| rd-20260329-021.md | nexwave-rd | No project file with this id; probably nexwave-rd-obj-1 (objective: obj-1) |
| rd-20260329-023.md | nexwave-rd | No project file with this id; probably nexwave-rd-obj-1 (objective: obj-1) |
| rd-20260329-024.md | nexwave-rd | No project file with this id; probably nexwave-rd-obj-1 (objective: obj-1) |
| rd-20260329-025.md | nexwave-rd | No project file with this id; probably nexwave-rd-obj-1 (objective: obj-1) |
| rd-20260329-026.md | nexwave-rd | No project file with this id; probably nexwave-rd-compliance (objective: capability) |
| rd-20260405-001.md | nexwave-rd | No project file with this id; probably nexwave-rd-obj-1 (objective: obj-1) |
| rd-20260419-001.md | nexwave-rd | No project file with this id; probably nexwave-rd-compliance (objective: capability) |
| rd-20260421-003.md | nexwave-rd | No project file with this id; probably nexwave-rd-obj-1 (objective: obj-1) |

Suggested mapping by `objective:` field:
- `objective: obj-1` tasks: change `project:` to `nexwave-rd-obj-1`
- `objective: capability` tasks: change `project:` to `nexwave-rd-compliance`

---

## Check 2: Tasks in wrong folder

Five files in `tasks/done/` have a status value other than `done`.

| Task file | status value | Expected |
|---|---|---|
| tasks/done/rd-20260329-001.md | open | done |
| tasks/done/rd-20260329-017.md | open | done |
| tasks/done/rd-20260421-002.md | open | done |
| tasks/done/saas-20260409-003.md | in-progress | done |
| tasks/done/saas-20260409-006.md | open | done |

These tasks were moved to `tasks/done/` without updating `status:` to `done`, or were moved erroneously while still active. Each file needs either: (a) status corrected to `done` if the task is complete, or (b) the file moved back to `tasks/open/` if still active.

---

## Check 3: Missing required frontmatter

No issues found.

All 73 open task files contain the six required fields: `id`, `title`, `project`, `status`, `priority`, `created`.

All 18 project files contain the five required fields: `id`, `title`, `status`, `type`, `dashboard`.

---

## Check 4: Invalid field values

No invalid values found in open tasks for `status` or `priority`.

No invalid `dashboard` values found in project files.

No malformed or quoted `due:` dates found in open tasks.

**Ancillary finding (not a schema violation, but flag-worthy):**

`tasks/open/saas-20260409-002.md` has `project: referral-images` but `repo: clinicpro-medtech`. The `referral-images` project file declares `repo: clinicpro-saas`. The task `repo:` field overrides the project-level repo, which is intentional per the CLAUDE.md priority order. Flagged for awareness: this task touches the medtech codebase despite living under a saas project.

---

## Check 5: Orphaned tasks (parked project)

No issues found.

No open task references a project with `status: parked`. Parked projects (`cloud9japan`, `eguchi-family`, `gp-community`) have no open tasks.

---

## Check 6: Active projects with no open tasks

Four active projects have zero open tasks referencing their ID.

| Project ID | File | Note |
|---|---|---|
| 12-month-prescription | projects/12-month-prescription.md | No open tasks. Possibly no active work in flight. |
| ahuru | projects/ahuru.md | No open tasks. Possibly parked in practice but not in status. |
| ai-scribe | projects/ai-scribe.md | No open tasks. Possibly no active work in flight. |
| nexwave-rd-obj-1 | projects/nexwave-rd-obj-1.md | Zero direct refs, but 7 obj-1 tasks wrongly use project: nexwave-rd (see Check 1). If those are rerouted, this count becomes 7. |

The `nexwave-rd-obj-1` zero-count is a direct consequence of the Check 1 broken references. Fixing Check 1 resolves this entry.

---

## Check 7: Milestone label drift

No case-drift or prefix-drift detected between tasks in the same project.

**Minor inconsistency:** within `clinicpro-capture-au-bundle`, the milestone value `AU bundle deal` appears both quoted (`"AU bundle deal"`) and unquoted across different task files. Dataview resolves quoted and unquoted YAML strings to the same value, so this does not break grouping in practice. Listed for tidiness.

| Task file | Milestone as written |
|---|---|
| medtech-20260418-002.md | "AU bundle deal" (quoted) |
| medtech-20260418-003.md | "AU bundle deal" (quoted) |
| medtech-20260418-004.md | "AU bundle deal" (quoted) |
| medtech-20260418-007.md | "AU bundle deal" (quoted) |
| medtech-20260418-008.md | "AU bundle deal" (quoted) |
| medtech-20260418-009.md | "AU bundle deal" (quoted) |
| medtech-20260422-001.md | AU bundle deal (unquoted) |
| medtech-20260423-002.md | AU bundle deal (unquoted) |
| medtech-20260424-002.md | "AU bundle deal" (quoted) |

Recommendation: standardise to unquoted (consistent with other milestone values in the vault).

---

## Check 8: Unquoted colons in frontmatter values

Two files in `tasks/done/` have `title:` values containing `: ` without quotes. These are in the done folder and do not affect active Dataview queries, but they violate the YAML quoting rule and would cause Dataview to silently drop those notes if the rule applies to done-folder queries.

| File | Problematic line |
|---|---|
| tasks/done/rd-20260403-001.md | `title: Inbox Helper — task specification: input types, urgency taxonomy, output schema, success criteria` |
| tasks/done/rd-20260403-002.md | `title: Care Gap Finder — task specification: clinical rules, data requirements, success criteria` |

Fix: wrap the `title:` value in double quotes in each file.

No violations found in `tasks/open/` or `projects/`.

---

## Check 9: Dashboard drift

No issues found.

All 18 project files declare a `dashboard:` value that corresponds to an existing file in `dashboards/`. The four active dashboard files are `clinicpro-saas`, `clinicpro-medtech`, `nexwave-rd`, and `other-projects`. All projects route to one of these.

Note: `gp-fellowship` is listed as a valid dashboard value in `CLAUDE.md` but no `dashboards/gp-fellowship.md` file exists. The `fellowship-application` project correctly uses `dashboard: other-projects` rather than `gp-fellowship`. The CLAUDE.md valid-values list appears stale. Not a current breakage but worth pruning from CLAUDE.md.

---

## Check 10: Inline checkboxes (disallowed)

No issues found.

No `- [ ]` or `- [x]` patterns found in any file under `tasks/` or `projects/`.

---

## Check 11: Projects referenced by tasks but with no project file

One unique `project:` value in `tasks/open/` has no corresponding project file.

| project: value | Task count | Issue |
|---|---|---|
| nexwave-rd | 10 | No `projects/nexwave-rd.md` exists. Same root as Check 1. |

This is the same set of tasks identified in Check 1. Resolving Check 1 resolves this check.

---

## Priority fixes

Listed by impact on active Dataview queries and task visibility.

1. **Fix 10 broken project references (rd tasks referencing project: nexwave-rd)**
   Map by `objective:` field: `obj-1` tasks to `nexwave-rd-obj-1`; `capability` tasks to `nexwave-rd-compliance`. Files: `rd-20260329-013`, `020`, `021`, `023`, `024`, `025`, `026`, `rd-20260405-001`, `rd-20260419-001`, `rd-20260421-003`. Once fixed, these tasks will appear in the correct per-project task tables and the `nexwave-rd-obj-1` zero-count (Check 6) is resolved.

2. **Resolve 5 misplaced files in tasks/done/ with non-done status**
   For each of `rd-20260329-001`, `rd-20260329-017`, `rd-20260421-002`, `saas-20260409-003`, `saas-20260409-006`: determine whether the task is actually complete (update `status: done`) or still active (move back to `tasks/open/` and use Templater correctly next time).

3. **Investigate zero-task active projects: 12-month-prescription, ahuru, ai-scribe**
   After fixing Check 1, `nexwave-rd-obj-1` will gain tasks. The other three projects (`12-month-prescription`, `ahuru`, `ai-scribe`) have no tasks at all. Either: (a) create tasks if work is genuinely planned, or (b) change `status:` to `parked` to reflect reality. Stale `active` status inflates the active project count and misleads home dashboard queries.

4. **Fix unquoted colon titles in two done tasks**
   `tasks/done/rd-20260403-001.md` and `rd-20260403-002.md`: wrap the `title:` value in double quotes. Low risk (done folder), but cleans up the YAML rule violation before it proliferates.

5. **Prune gp-fellowship from CLAUDE.md valid dashboard list**
   `CLAUDE.md` lists `gp-fellowship` as a valid `dashboard:` value, but no such dashboard file exists and no project uses it. Remove it from the allowed-values list to avoid future confusion. File: `C:\Users\reonz\cursor\obsidian\CLAUDE.md`.

---

## Assumptions

- `repo:` is not a strictly required field per CLAUDE.md schema (it lists it in the schema but the required-fields list in Check 3 only names `id`, `title`, `project`, `status`, `priority`, `created`). Tasks missing `repo:` are not flagged as required-field violations.
- The `nexwave-rd` dashboard query carve-out (`t.project === "nexwave-rd"`) is intentional and currently functional. The Check 1 finding is about per-project view visibility, not dashboard visibility.
- `milestone:` quote-style inconsistency (Check 7) is functionally harmless in Dataview. Flagged for tidiness only.
- Inline body content in task files (steps, notes under the frontmatter) is not subject to the no-inline-checkbox rule for existing structured content like ordered lists. Check 10 searched specifically for `- [ ]` and `- [x]` Markdown task syntax only.

All output is a first draft for human review.
