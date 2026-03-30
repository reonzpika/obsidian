# Follow-Up Review Prompt — NexWave AI Agent System v2

Use this prompt when sending the v2 document back to the agents who reviewed v1.

---

## Prompt

This is a follow-up to a review you completed on the NexWave AI Agent System design. You provided critical feedback on v1. This is v2, updated in response to that feedback and a clarifying discussion with the operator.

Your job is the same: find problems, not validate. Be direct.

---

## What changed in v2 (and why)

Before you read the document, here is a summary of what was updated and the reasoning. This saves you re-reviewing things that haven't changed.

**1. Purpose reframed around agent automation**
The operator clarified his goal: not just visibility, but reducing "supervise every step" to "review at defined checkpoints." The document now opens with this explicitly, including an honest ceiling table showing what agents handle vs what always requires the operator.

**2. Mechanical approval triggers added**
v1 relied on "when in doubt, surface it" as the primary control. v2 replaces this with a file-pattern table: `package.json`, lockfiles, `middleware.ts`, `vercel.json`, `*.env*`, DB migration files, Stripe/Clerk/auth files, BFF files. These are checked against the diff, not left to agent interpretation. "When in doubt" is now explicitly labelled as backup only.

**3. Two spec types introduced**
Implementation spec (execution allowed) vs Spike spec (time-boxed investigation, output is report + revised spec, no production code). Default to Spike when significant unknowns exist.

**4. Git containment model added**
New section: agents work on feature branches only, PRs are mandatory, no agent merges to `main`, no direct deploys. Branch naming convention defined.

**5. Handoff transport made explicit**
Ryo pastes the spec content directly into the Paperclip trigger message. The `obsidian/inbox/` file is an archive copy only. Execution agents never read the Obsidian directory.

**6. Checkpoint-based review model**
Four explicit checkpoints where the operator reviews before execution proceeds: code diff/PR, UI check, QA report, pre-deployment. CEO agent does not proceed past a checkpoint without sign-off.

**7. MBIE isolation hardened**
Replaced policy language with a six-row isolation checklist: separate API keys, no shared codebase access, separate Paperclip company, separate cost tracking, exportable audit trail, context isolation in prompt templates.

**8. Single system of record clarified**
Obsidian is authoritative. Paperclip is ephemeral execution state. When they conflict, Obsidian wins.

**9. Agent rosters defined per company**
Each execution company now has a defined roster: CEO (orchestration), Developer (implementation), QA (test writing and running). HQ has one CEO only, no access to repo directories.

**10. Fallback documented**
If Paperclip breaks, the fallback is pasting the spec directly into a Claude Code session. Same output, zero orchestration overhead.

---

## The updated document

[PASTE THE FULL CONTENTS OF agent-system.md v2 HERE]

---

## What to focus on in this review

This is a targeted re-review, not a full pass from scratch. Focus your energy here:

**1. Did the fixes actually fix the problems?**
For each critical issue you raised in v1, does v2 address it adequately? Be specific if the fix is incomplete or introduces a new problem.

**2. New issues introduced by v2**
Changes sometimes create new problems. Look especially at:
- The checkpoint model — is 4 checkpoints the right number? Are they at the right moments? Could an agent stall between checkpoints in a way that blocks progress?
- The mechanical approval triggers — are there obvious gaps in the file-pattern list? Files that should be on the list but aren't?
- The two spec types — does the spike/implementation distinction hold up in practice? What happens when a spike reveals that implementation is also needed immediately?
- The agent roster (CEO + Developer + QA) — is this the right structure for a solo founder's needs? Is a separate QA agent realistic at this stage?

**3. The Paperclip value question**
v1 feedback from all three reviewers questioned whether Paperclip justified its overhead. The operator answered this directly: his goal is agent automation — replacing "supervise every step" with "review at checkpoints." Does v2's design now credibly deliver this? Or is there still a gap between the vision and what the architecture actually provides?

**4. Anything still missing**
Open questions from v1 that v2 did not answer: break-glass policy when the operator is unavailable, secrets management across companies, what happens when a spec is wrong mid-execution. v2 carries these as open questions. Do you have concrete recommendations for any of them?

---

## Format

**Fixes that landed** — which v1 issues are now resolved (brief, one line each)

**Fixes that are incomplete** — v1 issues that were addressed but not fully solved

**New issues from v2** — problems the changes introduced

**Still missing** — things not in v1 or v2 that should be

**Verdict** — has v2 moved from "not ready" to "ready to pilot"? Be specific about what the remaining blockers are, if any.

Keep it tight. If something is fixed, say so and move on. Focus your detail on what's still wrong.
