# AutoResearch Clearly Explained - Reference Report

**Source:** https://www.youtube.com/watch?v=uBWuKh1nZ2Y
**Analysed via:** Gemini 2.5 Flash
**Speaker:** David Ondrej
**Channel:** David Ondrej
**Duration:** 20:00
**Status:** First draft. Requires human review before use as reference.

---

## Overview

David Ondrej explains AutoResearch, an open-source framework by Andrej Karpathy that enables AI agents to autonomously run experiments, evaluate results, and iteratively improve code or any measurable process. The video targets developers and technical founders who want to apply autonomous optimisation loops beyond machine learning. It includes a live demo building an AutoResearch loop from scratch using Claude Code and Puppeteer.

---

## Core Thesis

AutoResearch represents a paradigm shift: execution becomes automated, so the scarce skill is no longer doing the work but defining what "better" means. The framework lets an AI agent run hundreds of experiments overnight against an objective metric, keeping improvements and discarding failures via git, without human oversight. Karpathy's central claim is that any process with a clear scalar metric can be autoresearched, and that recursive self-improvement loops will be adopted by all major LLM frontier labs.

---

## Transcript Summary

**0:00 - 1:32: Introduction and background**
- AutoResearch lets AI autonomously improve code: run experiment, evaluate, keep or discard, repeat.
- Fixed time budget per experiment (e.g. 5 min) makes runs comparable and prevents cheating by training longer.
- Karpathy: "All LLM frontier labs will do this. It's the final boss battle."
- Garry Tan: "The bottleneck isn't compute. It's your program.md."
- Karpathy developed it after an AI agent optimised his GPT-2 training script better than months of manual work.

**1:32 - 2:58: The loop and file architecture**
- Three files: `program.md` (human-defined goal), `train.py` (agent can edit), `prepare.py` (evaluation script, locked).
- The agent cannot touch `prepare.py` to prevent gaming the metric.
- Loop: Hypothesis -> Modify `train.py` -> Train (fixed time) -> Evaluate -> git commit or git reset -> repeat.

**2:58 - 5:36: Broad implications**
- Tobi Lutke (Shopify CEO): +19% score on a 0.8B LLM after 8 hours and 37 experiments.
- Patrick Collison (Stripe CEO): used a similar loop for weather forecasting model training.
- Biggest misconception: AutoResearch is not only for ML. Anything measurable can be autoresearched.
- Karpathy: "Any metric you care about that is reasonably efficient to evaluate can be autoresearched."

**5:36 - 7:02: Sponsorship (Oxylabs)**
- Oxylabs Web Scraper API and AI Studio for live web data in agent workflows.
- Oxylabs MCP integrates with Cursor/Claude Code for plain-English scraping.

**7:02 - 10:56: Use cases and failure modes**
- Trading: agent tweaks buy/sell rules, backtests, scores by Sharpe ratio.
- Marketing: agent modifies copy/creatives, measures conversions; Eric Siu predicts 36,500+ experiments/year vs. the current 30.
- Code optimisation: point at any codebase with benchmarks, e.g. fine-tune open-source models to run on-device.
- Prompt engineering: agent rewrites system prompts, scores by task success rate.
- Failure modes: subjective domains (brand design, UX feel) where "better" cannot be reduced to a single number. A bad metric produces confidently wrong results.

**10:56 - 11:20: Karpathy's vision**
- Envisions thousands of AI agents on thousands of machines, analogous to SETI@home.
- "The goal is not to emulate a single PhD student. It's to emulate a research community of them."

**11:20 - 19:53: Live demo (see Steps Covered)**

---

## Steps Covered (Demo)

1. Clone `karpathy/autoresearch` repo into `/original`.
2. Create `/website` folder; use Claude Code + Express to build an intentionally unoptimised portfolio site.
3. Write `benchmark.mjs` using Puppeteer to measure page load time (the objective metric).
4. Establish baseline: 50.9 ms load time.
5. Adapt Karpathy's `program.md` to describe the goal (minimise load time) and list candidate optimisations.
6. Start the autonomous loop inside Claude Code.
7. Experiment 1: slight regression; Claude reverts.
8. Experiment 2: remove Google Fonts import. Result: 33.8 ms (34.5% improvement). Committed.
9. Experiment 3: remove `lodash.js`, inline debounce, defer `app.js`. Result: 28.8 ms (14.8% further improvement). Committed.
10. Experiment 4: add gzip compression middleware. Result: 25.5 ms (11.5% further improvement). Committed.
11. Experiment 5: inline critical CSS/JS. Regression; reverted.
12. Final result: 25.5 ms from 51.6 ms baseline, roughly 50% improvement in under 5 minutes of real time.

---

## Visual Analysis

- Intro animation: descending step-graph with green commits and grey discarded experiments; visually communicates the ratchet-improvement pattern.
- The loop diagram (Hypothesis -> Modify -> Train -> Evaluate -> Keep/Discard) recurs throughout as a visual anchor; speaker traces it with a red line each time.
- Locked folder icon for `prepare.py` vs. pencil icon for `train.py`: clear visual metaphor for access rules.
- Bar chart: 7 minutes vs. 7 days compute analogy, illustrating fixed time budget fairness.
- Arena image with twelve armoured figures representing frontier LLM labs converging on recursive self-improvement.
- Live coding in Cursor: green/red diff highlights during each experiment iteration; terminal load-time output shown clearly at each step.
- YouTube Studio subscriber stat (74.8% not subscribed) used mid-video as a direct CTA with humorous dog-fish graphic.

---

## All Concepts, Tools, People, and Entities Referenced

| Name | What it is / why mentioned |
|---|---|
| AutoResearch | Open-source autonomous experiment loop framework by Karpathy |
| Andrej Karpathy | AI researcher, OpenAI co-founder, Tesla Autopilot, created AutoResearch |
| `program.md` | Human-written goal/constraints file; most important input |
| `train.py` | The one file the agent modifies |
| `prepare.py` | Locked evaluation/metric script |
| Fixed time budget | Per-experiment time cap for fair comparison |
| Recursive self-improvement | AI system iteratively improving its own capabilities |
| Garry Tan | Quoted: "The bottleneck isn't compute. It's your program.md." |
| Tobi Lutke | Shopify CEO; +19% LLM score in 8 hours via AutoResearch |
| Patrick Collison | Stripe CEO; weather forecasting model via similar loop |
| Eric Siu | Quoted: marketing teams will run 36,500+ experiments/year with agents |
| Harrison Chase | LangChain founder; quoted on agent context and system prompts |
| LangChain | Framework for LLM-powered applications |
| GPT-2 | OpenAI model used as Karpathy's original optimisation target |
| Sharpe ratio | Risk-adjusted return metric; used as trading use-case example |
| SETI@home | Distributed computing analogy for Karpathy's multi-agent research vision |
| Cursor | AI-native IDE used in the demo |
| Claude Code | Coding agent used inside Cursor for the demo loop |
| Express | Node.js web framework used to build demo website |
| Puppeteer | Headless Chrome library used to build the benchmark script |
| `lodash.js` | JavaScript utility lib; removed in Experiment 3 |
| Google Fonts | External font service; removed in Experiment 2 |
| gzip compression | Added in Experiment 4; delivered 11.5% load time improvement |
| `benchmark.mjs` | Demo equivalent of `prepare.py`; measures page load time |
| `results.tsv` | AutoResearch experiment log file |
| Oxylabs | Sponsor; web scraping API and AI Studio |
| Oxylabs MCP | Oxylabs integration for Cursor/Claude Code |
| n8n | Workflow automation tool; mentioned in Oxylabs segment |
| GitHub | Hosts the `karpathy/autoresearch` repo |
| Vibe coding | Term coined by Karpathy |

---

## Key Takeaways

- Any process with one measurable scalar metric, one editable file, and automated evaluation can be autoresearched.
- The 3 required conditions: clear objective metric, fully automated evaluation (no human in the loop), single editable file.
- Failure mode: subjective outcomes (brand feel, UX quality) cannot be reduced to a number, so the agent cannot learn.
- A wrong metric is worse than no metric: the agent will confidently optimise the wrong thing.
- The bottleneck shifts from execution to metric design. "Knowing what to measure" is the new scarce skill.
- Fixed time budget per experiment is essential for fair comparison across iterations.
- Real demo result: 50% page load improvement in under 5 minutes of real time, 5 autonomous experiments.
- Karpathy's vision: thousands of AI agents running in parallel, analogous to a distributed research community, not a single PhD student.
- This framework applies to trading (Sharpe ratio), marketing (conversion rate), code speed (load time), and prompt engineering (task success rate).

---

## Claims Requiring Verification

| Claim | Flag |
|---|---|
| 100 experiments overnight at 5 min each | Approximation; depends on hardware and task |
| Tobi Lutke: +19% score on 0.8B model, 8 hours, 37 experiments | Specific benchmark not named; verify source tweet |
| Patrick Collison: weather forecasting model via Claude | General statement; no specific metrics given |
| Marketing teams will run 36,500+ experiments/year | Eric Siu prediction; not a measured statistic |
| Claude Sonnet 4.6 quality models on iPhones in 3-4 months | Speaker prediction; check current on-device model landscape (post-August 2025 cutoff) |
| Oxylabs 2,000 free scraped results | Verify current free tier on Oxylabs site |
| Oxylabs 20% discount code DAVID | Verify validity and expiry |
| Karpathy: 650 experiments over 2 days on depth-12 model transferring to depth-24 | Mentioned verbally; verify on Karpathy's GitHub/Twitter |

---

## Open Questions

- What are the token costs for a typical overnight AutoResearch run (hundreds of experiments)? Relevant for budgeting API spend.
- How does the agent avoid repeating discarded experiments? Does it read `results.tsv` to build a memory of what failed?
- What security controls prevent an autonomous agent from introducing vulnerabilities in production code?
- How do you define a single scalar metric for multi-objective problems (e.g. speed AND accuracy AND cost)?
- What is the practical limit of the "one editable file" constraint for large real-world codebases with many interdependencies?
- Are there established leaderboards or shared benchmarks for AutoResearch applications outside LLM training?
- How does AutoResearch interact with non-deterministic outcomes (e.g. marketing A/B tests that need statistical significance before committing)?
