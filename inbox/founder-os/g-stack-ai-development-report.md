# Introduction to G Stack - Reference Report

**Source:** https://www.youtube.com/watch?v=wkv2ifxPpF8
**Analysed via:** Gemini 2.5 Flash
**Speaker:** Garry Tan (President and CEO, Y Combinator)
**Channel:** Y Combinator
**Duration:** 21:51
**Status:** First draft. Requires human review before use as reference.

---

## Overview

A Startup School presentation by Garry Tan introducing GStack, an open-source framework that wraps Claude Code with structured "slash command" skills to automate the full software development lifecycle. Aimed at technical founders and solo developers who want to ship faster using AI agents. Includes a live demo of the Office Hours, design-shotgun, and Conductor Pattern workflows.

---

## Core Thesis

The bottleneck in AI-assisted development is not model intelligence -- it is scaffolding. GStack's approach is a "thin harness, fat skills": minimal infrastructure, with opinionated skills that enforce team-level processes (product thinking, design review, bug catching, QA, shipping) around Claude Code. The result is a single developer running what functions as an entire engineering team, achieving 17,000 lines of code per day across 10-15 parallel sessions.

---

## Transcript Summary

**00:00-00:08: Title card**
Animated YC intro, "Startup School: Introduction to G Stack."

**00:08-01:11: Garry's background and the agent era**
- Stanford Computer Systems Engineering; Palantir employee #10; co-founded Posterous (sold to Twitter); built YC's internal Bookface platform.
- "We are in a completely new era of building software: the agent era."
- Claims GStack has more GitHub stars than Ruby on Rails (unverified -- see Claims section).
- Claims he has coded more in the past two months than all of 2013.

**01:11-02:50: The problem with naive AI coding and GStack's philosophy**
- AI models "wander" and produce "plausible-looking code that silently breaks."
- His fix: models are already smart enough; the scaffolding should be "trivially thin."
- GStack = open-source repo that turns Claude Code into an AI engineering team with skills acting as specialist roles (CEO, designer, staff engineer, QA, security, release engineer).

**02:50-07:26: Office Hours demo -- demand validation and business model reframing**
- Demo: new "tax-app" project created from "gstack" template in Conductor IDE.
- Prompt to `/office-hours`: build a tool to collect 1099-INT tax documents from Gmail and bank portals.
- AI ("Garry mode") interrogates demand: "What's the strongest evidence someone actually wants this -- not interested, not on a waitlist, but would be upset if it disappeared?"
- After probing, AI surfaces competitive alternatives: TurboTax 1099 import, Plaid, H&R Block.
- Reframes business model from document aggregator to two-sided marketplace: connect taxpayers with CPAs, charge CPAs for leads.

**07:26-09:27: Browser automation and Codex integration**
- Key insight: GStack Browser runs on the user's machine; AI navigates (screenshots, clicks, form fills, downloads) without storing credentials.
- Tan's hybrid approach: use browser automation to bypass Google OAuth -- open Gmail, let the agent search directly.
- Codex handles "all the crazy bugs." Describes Opus 4.6 as an "ADHD CEO" with "a billion ideas" and Codex as the "autistic CTO" for disciplined execution.

**09:27-11:19: Three approaches, user selects hybrid**
- Approach A: Gmail scanner + smart checklist (MVP, low risk).
- Approach B: Full stack + Gmail + AI browser automation + CPA marketplace (high risk, high reward).
- Approach C: CPA-first, flip go-to-market.
- Tan selects B with a browser-automation twist to skip OAuth.

**11:19-13:43: Adversarial review of design doc**
- AI runs adversarial review on its own design document.
- Finds and fixes 16 issues, raises quality score from 6/10 to 8/10.

**13:43-16:29: Design Shotgun demo**
- `/design-shotgun` generates three UI variants for the "main checklist dashboard":
  - Option A: Dark mode, dense data table.
  - Option B: Light mode, friendly progress cards with status rings.
  - Option C: Split view, CPA requests left, found docs right, visual matching.
- Tan picks Option B (5 stars). AI offers next steps: iterate, finalise to HTML/CSS, save to plan.

**16:09-19:36: The Sprint Process and GStack stat slide**
- Slide: "58K+ GitHub stars, 28 slash commands, 17K LOC/day (Garry)."
- Sprint cycle: `/office-hours` -> `/autoplan` -> `/design-*` -> Claude Code build -> `/review` -> `/qa` -> `/ship` -> `/retro` + `/learn` + `/document-release` -> next sprint.
- `/plan-ceo-review`: should we build this? `/plan-eng-review`: can we ship this safely?
- Browser automation: Playwright + Chromium CLI wrapper enables headed and headless automation, regression tests, CSS updates.
- "Tests verify you built what you planned. Reviews verify you planned the right thing."

**19:36-21:04: The Conductor Pattern**
- 10-15 parallel Claude Code sessions, each in an isolated git worktree.
- Productivity claim (March 2026): 3 simultaneous projects, 15 concurrent sessions, 17,000 LOC/day, 35% of shipped code is tests, 600K+ lines in 60 days part-time.
- Workflow: click "+" in Conductor, name a worktree per to-do item, run `/office-hours`, let it run, get notified, keep 20 going at once.
- No to-do list needed -- each worktree IS the to-do item.

**21:04-21:40: Review before build + call to action**
- "The most expensive bugs are the ones you implement on purpose."
- Real example: agent skipped ahead and introduced 19 bugs before a single line of code was written; caught by `/plan-ceo-review` and `/plan-eng-review`.
- Call to action: "The barrier to building just collapsed. What are you going to build? Go make something people want."

---

## Visual Analysis

- **00:00:** Animated white-grid-on-black YC intro sequence, title card appears.
- **00:08:** Garry Tan at round wooden table with MacBook Pro, red acoustic-foam wall behind him. Lower-third: "Garry Tan, President and CEO, Y Combinator."
- **02:50:** Screen recording of Conductor IDE: file explorer sidebar, code editor, terminal. Quick-start template picker visible ("Empty," "Next.js," "gstack (NEW)"). Project named "tax-app."
- **03:41-11:19:** Terminal output showing AI "Thinking" blocks, multi-choice prompts, and Tan's typed responses. Right sidebar shows `.claude.md`, `.context`, `.git`.
- **13:43:** Browser tab opens showing "Design Exploration" -- three side-by-side HTML/CSS mockups with "Pick" radio buttons and star ratings below each option.
  - Option A: Dark mode with dense bank-document table.
  - Option B: Light mode, per-bank status cards, progress ring "5 of 8 documents collected."
  - Option C: Light mode, two-column split with connecting lines between CPA requests and found docs.
- **16:09:** Full-screen stat slide: "What is GStack?" with role list and headline numbers.
- **16:29:** Full-screen sprint-cycle diagram.
- **19:36:** Full-screen Conductor Pattern diagram: session flow from 1 to 15+, with Garry's March 2026 numbers bottom-left and workflow description bottom-right.
- **21:04:** Full-screen "Review Before You Build" slide with three review stages.

---

## Skills and Commands Reference

| Skill | Stage | What it does |
|---|---|---|
| `/office-hours` | Think | 6 forcing questions: demand, competition, model, approach |
| `/autoplan` | Plan | Automates CEO, engineering, and design reviews |
| `/plan-ceo-review` | Plan | Should we build this? |
| `/plan-eng-review` | Plan | Can we ship this safely? |
| `/design-shotgun` | Design | Generates 3 UI variants per screen, star-rated picker |
| `/review` | Review | Staff-level adversarial bug catch on generated code |
| `/qa` | Test | Browser regression tests via Playwright/Chromium |
| `/ship` | Ship | PR, CI, deploy |
| `/retro` + `/learn` + `/document-release` | Retrospective | Feeds learnings into next sprint |

---

## All Concepts, Tools, People, and Entities Referenced

| Entity | Type | Relevance |
|---|---|---|
| Garry Tan | Person | Speaker, YC CEO, GStack creator |
| Y Combinator | Organisation | Accelerator, employer, "office hours" model source |
| GStack | Tool | Open-source AI dev framework (central topic) |
| Conductor | Tool | IDE integrating GStack with worktree management |
| Claude Code / Opus 4.6 | AI model | Underlying model GStack wraps |
| Codex | Tool | Used for bug review and disciplined execution |
| Playwright | Library | Browser automation, wrapped into GStack CLI |
| Chromium | Runtime | Browser for headed/headless automation |
| Ruby on Rails | Framework | Star-count comparison |
| Palantir | Company | Garry's early employer |
| Posterous | Product | Garry's prior startup (sold to Twitter), used as rebuild benchmark |
| Bookface | Product | YC internal platform Garry built |
| 1099-INT | Tax form | Demo use case |
| Gmail | Service | Document search in demo |
| TurboTax | Competitor | Mentioned in competitive analysis |
| H&R Block | Competitor | Mentioned in competitive analysis |
| Plaid | Service | Bank connection alternative, mentioned in competitive analysis |
| Andrej Karpathy | Person | Mentioned as claiming he no longer manually writes code |
| Boris Cherny | Person | Mentioned alongside Karpathy |

---

## Key Takeaways

1. GStack's value is process enforcement, not raw AI capability -- the model is already capable enough; the scaffolding was the bottleneck.
2. `/office-hours` runs before any code is written and frequently reframes the business model, not just the technical design.
3. Browser automation without credential storage ("user logs in, AI navigates") is a privacy-preserving pattern worth noting for any app touching financial or health data.
4. The adversarial self-review pattern (AI critiques its own design doc, scores it, fixes issues) is a transferable technique independent of GStack.
5. The Conductor Pattern -- one worktree per to-do item, 10-15 parallel sessions -- is the key productivity multiplier, not any single skill.
6. "Tests verify you built what you planned. Reviews verify you planned the right thing." -- plan-level review before code is the key risk reduction.
7. Spending $4K/month on Claude "fast mode" is presented as clearly ROI-positive at this output level.
8. GStack is open source; the sprint process and slash-command pattern are replicable in any Claude Code setup.

---

## Claims Requiring Verification

| Timestamp | Claim | Status |
|---|---|---|
| 01:03 | "More GitHub stars than Ruby on Rails" | Unverified. Rails has ~54K stars. GStack star count needs current check (Gemini training data is stale). |
| 16:15 | "70,000+ stars now" | Unverified. Check github.com/garrytan/gstack directly. |
| 01:43 | Posterous rebuild: "took two years, $10M, 10 engineers originally" | Unverified. |
| 16:26 | "~$4K/month on fast mode" | Plausible at 15 concurrent Opus 4.6 sessions; verify current Claude pricing. |
| 19:53 | "17,000 LOC/day, 600K+ lines in 60 days, part-time" | High claim; no independent verification. Possible at scale but unconfirmed. |
| Throughout | Productivity comparisons to 2013 coding output | Self-reported; anecdotal. |

Note: Gemini's knowledge cutoff may predate current GStack star counts. Verify directly on GitHub before citing.

---

## Open Questions

- What is the actual current GitHub star count for GStack? (The video's own numbers conflict across slides.)
- How much of the Office Hours question tree is fixed vs. dynamically adapted per project type?
- Does the Playwright/Chromium browser CLI work reliably on sites with aggressive bot detection (bank portals, financial institutions)?
- What are the actual costs at various usage levels? ($4K/month is for Garry's extreme usage -- what does a more typical founder pay?)
- Is Conductor available publicly, or only to YC-affiliated founders?
- How does GStack handle the "supply chain attacks" concern Tan mentions? What specific mitigations are in place?
- How do the `/review` and `/plan-eng-review` skills differ in practice -- one catches code bugs, one catches design bugs, but where exactly is the boundary?
- For a non-technical founder, how much does understanding the underlying Claude Code model matter to get value from GStack?
