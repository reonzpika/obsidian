# How to Make Your Claude Code Skills Self-Improve Overnight (AutoResearch) - Reference Report

**Source:** https://www.youtube.com/watch?v=wQ0duoTeAAU
**Analysed via:** Gemini 2.5 Flash
**Speaker:** Not identified
**Channel:** Not identified
**Duration:** 11:03
**Status:** First draft. Requires human review before use as reference.

---

## Overview

This video demonstrates how to apply Andrej Karpathy's "AutoResearch" concept to Claude Code skills, enabling them to self-improve overnight without human intervention. The target audience is Claude Code power users and builders. It covers two distinct improvement layers: skill activation (YAML trigger description) and skill output quality (binary assertion scoring).

---

## Core Thesis

Claude Code skills can be made to self-improve autonomously for structured, objective output criteria by adapting Karpathy's iterative loop: make a change to `SKILL.md`, run tests against binary true/false assertions, measure a pass rate score, commit if the score improves or reset if it drops, and repeat indefinitely. This eliminates the weeks of manual tweaking typically required to make a new skill reliable, and the loop can run unattended overnight.

---

## Transcript Summary

**00:00 - 00:13: Problem framing**
Skills in Claude Code are powerful but getting them from v1 to reliable "usually takes weeks of tweaking." The speaker has over 20 skills and describes the manual loop (run skill, spot issues, open `SKILL.md`, tweak) as slow and inconsistent.

**00:20 - 00:43: Karpathy's AutoResearch**
Andrej Karpathy (OpenAI founding team, former Tesla AI head) proposed "AutoResearch": give an AI system something to improve and a clear measurement method, then let it loop. If results improve, keep the change; if not, roll it back and try again.

**00:43 - 00:58: Overnight autonomous improvement**
The loop runs while you sleep. Apply this to Claude Code skills for automatic improvement.

**00:58 - 01:58: Karpathy's three files and the loop**
Karpathy's system: `program.md` (baseline instructions), `prepare.py` (fixed data prep), `train.py` (the single file the AI edits). The core `program.md` instructs: tune `train.py`, run experiment, read `val_bpb`, commit if improved, reset if not. Crucially: "NEVER STOP! Do NOT pause to ask the human if you should continue... You are autonomous. If you run out of ideas, think harder."

**02:08 - 02:31: Layer 1 - Skill activation**
For Claude to use a skill, it must determine relevance via the YAML `trigger-description` in `SKILL.md`. Community testing found activation as low as 20% with vague descriptions.

**02:31 - 03:39: Anthropic's built-in loop for skill descriptions**
The upgraded skill-creator skill (Anthropic) already has a built-in loop for trigger optimisation: test queries, check activation accuracy, propose a better description, retest. This is Layer 1 and is available in Skill 2.0.

**03:39 - 04:17: Output quality is a separate problem**
Producing great outputs requires a different approach. A test on a copywriting skill against a `persuasion-toolkit.md` reference file scored 50% pass rate using qualitative assertions. It worked well qualitatively but was not self-improving.

**04:18 - 05:27: The adapted Karpathy loop (Layer 2)**
The video's main contribution: apply the same loop to output quality. Side-by-side comparison:
- Karpathy: read `train.py` -> change value -> run test -> check `val_bpb` -> keep/revert
- This approach: read `SKILL.md` -> change value -> run test -> check pass rate -> keep/revert
Key ingredient: 25 binary assertions x 5 tests for the pass rate.

**05:27 - 06:03: Why binary assertions are essential**
"The word binary is everything here." Subjective tests ("Has a compelling subject line") cannot be automated because two people may disagree. Binary tests ("Does not contain em dashes," "Under 300 words," "Final line is a question") yield consistent true/false results every time, making them automatable.

**06:03 - 07:22: Setting up `evals.json`**
Create an `evals/` folder inside the skill directory. `evals.json` contains:
- `skill_name`
- `evals` array: each entry has `id`, `prompt`, `expected_output`, `assertions`
- Each assertion: `text` (the check) and `type: "binary"`

Example assertions: "First line is a standalone sentence," "Contains at least one specific number or statistic," "Final line is not a question," "Total word count is under 300," "Does not contain any em dashes," "Does not contain the words synergy, leverage, or paradigm."

You can ask Claude Code to auto-generate `evals.json` from your `SKILL.md`.

**07:51 - 08:34: The improvement prompt**
Prompt to Claude Code: "Use the skill-creator skill to run a self-improvement loop on my copywriting skill. Use the test prompts and assertions in `./claude/skills/mkt-copywriting/evals/evals.json`... For each cycle: run all test prompts through the skill, grade each assertion pass/fail, calculate pass rate. If any assertions fail, propose and make ONE change to SKILL.md. Re-run all tests. If score improved, keep and git commit. If dropped or same, git reset. Log each iteration. Do not stop to ask me. I may be asleep. Keep looping until I interrupt you or you hit a perfect score."

**08:34 - 09:22: Example loop output (copywriting skill)**
- Iteration 1 baseline: 23/24 (95.8%). Failure: `EVAL1.A3` - "end with a question" rule in `tone-of-voice.md` conflicted with the skill's rule.
- Claude's fix: Added explicit override to `SKILL.md`: "LinkedIn posts must not end with a question. Close with declarative statement, CTA, or punchy fragment."
- Iteration 2: 24/24 (100%). Change committed.

**09:22 - 10:31: Summary of two layers and limitations**
- Layer 1 (skill-creator): improves activation via YAML description refinement
- Layer 2 (adapted Karpathy): improves output quality for structured/format elements
- Limitations: binary loop does not handle tone of voice, creative quality, or whether reference files are being used correctly. These still need human judgment, assisted by the skill-creator's side-by-side dashboard for A/B testing reference files.

**10:31 - 11:03: Agentic OS product pitch**
The speaker promotes "Agentic OS": a self-maintaining business OS built on Claude Code, 18 production skills (marketing, strategy, ops, visuals), brand memory, self-learning loop, Telegram phone access. Three-layer architecture: Agent Identity, Skills Pack, Brand Context.

---

## Visual Analysis

Key visuals that add meaning beyond the transcript:

- **Skill loop diagram (04:24)**: Side-by-side comparison of Karpathy's loop and the adapted skills loop. Yellow box highlights "25 BINARY assertions x 5 tests" as the measurement layer. Identical git commit/reset logic in both.
- **Binary vs subjective slide (05:33)**: Red box labels subjective tests ("Has a compelling subject line") as non-automatable. Green boxes show three binary examples. Yellow footer: "Two strangers get the same answer every time."
- **`evals.json` in VS Code (06:21-07:22)**: Full JSON structure shown. Assertions are read out with their text and `type: "binary"` fields visible.
- **Self-improvement loop log (08:34-09:22)**: Iteration table showing baseline 95.8% score, the specific failing assertion, Claude's proposed fix, and the 100% result after one iteration. The added rule text is highlighted.
- **Karpathy's NEVER STOP instruction (01:42-01:58)**: Full text shown on screen: "The human might be asleep, or gone from a computer and expects you to continue working indefinitely... If you run out of ideas, think harder."
- **Agentic OS README and 3-layer diagram (10:32-10:52)**: Architecture diagram shows Agent Identity, Skills Pack, and Brand Context feeding into a Content Matrix.

---

## All Concepts, Tools, People, and Entities Referenced

| Item | Type | Notes |
|------|------|-------|
| Claude Code | Platform | AI coding assistant, primary tool |
| Skills | Concept | Modular, reusable AI functions in Claude Code |
| Andrej Karpathy | Person | OpenAI founding team, former Tesla AI head; proposed AutoResearch |
| AutoResearch | Concept | Autonomous AI self-improvement via iterative change/test/commit loop |
| `program.md` | File (Karpathy) | Baseline instructions for the AI agent |
| `prepare.py` | File (Karpathy) | Fixed data preparation, not modified by agent |
| `train.py` | File (Karpathy) | GPT model, optimizer, training loop; the file the AI edits |
| `val_bpb` | Metric (Karpathy) | Validation bits per byte; lower = better |
| `SKILL.md` | File (Claude Code) | Defines a skill including YAML trigger description |
| YAML trigger description | Concept | `trigger-description` field in SKILL.md; determines when Claude activates the skill |
| Skill-creator skill | Tool (Anthropic) | Built-in Claude Code skill for improving skill descriptions |
| `improve_description.py` | Script (Agentic OS) | Improves skill descriptions based on eval results |
| `run_loop.py` | Script (Agentic OS) | Combines eval and description improvement in a loop |
| `evals.json` | File | JSON file with test prompts and binary assertions for a skill |
| Binary assertions | Concept | True/false checks on skill output; required for automation |
| Pass rate | Metric | Overall score from binary assertions; replaces `val_bpb` |
| `persuasion-toolkit.md` | Reference file | Persuasive writing techniques; used as skill context |
| `tone-of-voice.md` | Reference file | Brand tone rules; caused assertion conflict in the example |
| Agentic OS | Product | Self-maintaining business OS built on Claude Code |
| Telegram | Integration | Phone access to Agentic OS |
| VS Code | Tool | Code editor used in all demonstrations |
| Google Workspace APIs | APIs | Drive, Gmail, Calendar; shown in early terminal commands |
| Skool | Platform | Example community for which landing page copy was tested |
| Muon + AdamW | Optimizers | Used in Karpathy's `train.py` |

---

## Key Takeaways

- Self-improvement in Claude Code skills operates on two distinct layers: trigger activation (YAML description) and output quality (binary assertions). They need separate approaches.
- Binary true/false assertions are the non-negotiable ingredient for automation. Subjective quality criteria cannot drive an autonomous loop.
- Karpathy's NEVER STOP instruction is the architectural key: the loop must be instructed explicitly to work without human confirmation prompts.
- Git commit/reset is the mechanism for keeping improvements and discarding regressions. The loop relies on a clean git history.
- Claude Code can generate an `evals.json` automatically from `SKILL.md`, lowering the setup cost.
- The loop resolves conflicts between reference files (e.g., `tone-of-voice.md` vs `SKILL.md`) by adding explicit overrides to `SKILL.md` rather than modifying reference files.
- The binary loop does not handle creative quality, tone of voice, or correct use of context files. Human review remains required for these dimensions.
- For newly created skills with lower baseline scores, the loop would run many more iterations than the 2-iteration example shown.

---

## Claims Requiring Verification

- Skill activation as low as 20% with vague trigger descriptions: specific statistic from "community testing" with no cited source. Needs independent verification.
- Agentic OS has 18 production skills: product claim, unverifiable from this video.
- "Gets sharper every time you use it": marketing claim for Agentic OS with no metrics or benchmarks provided.
- Speaker's claim that skills take "weeks of tweaking" from v1 to reliable: personal experience, not generalisable without data.

---

## Steps Covered

1. Understand Karpathy's AutoResearch loop (change, test, measure, commit/revert, repeat)
2. Identify the two improvement layers in Claude Code skills
3. Use skill-creator's built-in loop to optimise YAML trigger descriptions (Layer 1)
4. Create `evals/` folder and `evals.json` with binary assertions inside a skill (Layer 2)
5. Prompt Claude Code to run the self-improvement loop using the evals file
6. Review the loop log: iteration scores, failing assertions, proposed changes, commit/reset decisions
7. Manually review qualitative dimensions (tone, creativity, reference file use) that binary loops cannot handle

---

## Open Questions

- What is the API token cost of running 25 assertions x 5 tests x N iterations overnight at scale across multiple skills?
- How does Claude Code handle assertion conflicts when two assertions in `evals.json` push the skill in opposite directions?
- What prevents runaway drift if the loop commits a change that improves binary scores but degrades qualitative output quality?
- Are there published benchmarks on activation rate improvements from Layer 1 (skill-creator loop)?
- How does the loop perform on skills with fewer structural constraints (e.g., research or analysis skills vs copywriting)?
- What git branching strategy is recommended when running overnight loops that auto-commit?
