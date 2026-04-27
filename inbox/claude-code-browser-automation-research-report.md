# Claude Code + Browser Automation + Research + Obsidian: All Three Combined - Reference Report

**Source:** https://www.youtube.com/watch?v=kU3qYQ7ACMA
**Analysed via:** Gemini 2.5 Flash
**Speaker:** Chase
**Channel:** Chase AI
**Duration:** 15:02
**Status:** First draft. Requires human review before use as reference.

---

## Overview

A 15-minute tutorial demonstrating a combined workflow using Claude Code, Google NotebookLM, Obsidian, and the Claude Code Skill Creator. Chase builds a YouTube research pipeline that searches YouTube via a custom skill, pushes sources into NotebookLM for analysis, generates deliverables (infographics, markdown research notes), and stores all output in Obsidian as persistent memory. The workflow is presented as a flexible template applicable to any data source.

---

## Core Thesis

Combining Claude Code with NotebookLM and Obsidian creates a self-improving personal AI research assistant. NotebookLM handles heavy analysis (offloading token cost from Claude Code), Obsidian provides structured persistent memory that Claude Code can read directly, and the Skill Creator lets users encode multi-tool pipelines into single natural-language-defined commands. The resulting feedback loop (Claude Code acts, output lands in Obsidian, Obsidian informs future Claude Code runs) causes the assistant to become progressively better calibrated to the user's style over time.

---

## Transcript Summary

**0:00 - 0:28 | Introduction**
- Chase previews three prior videos: Claude Code + NotebookLM, Claude Code + Obsidian, Claude Code + Skill Creator.
- Central question: "What's going to happen when we combine all these tools together in a practical yet simple to set up workflow that you can start using today in under 30 minutes?"

**0:28 - 1:33 | Workflow overview: "research on steroids"**
- Describes the workflow as "research on steroids."
- Emphasises flexibility: YouTube is his data source for content research, but any source (PDFs, articles, text) can substitute.
- Quote: "What's important isn't my exact use case... You should be focused on how do I swap the YouTube search for whatever use case I have."

**1:33 - 2:59 | Step-by-step breakdown**
- Claude Code to YouTube: `yt-search` skill using `yt-dlp`.
- YouTube data to NotebookLM: `notebooklm` skill via `notebooklm-py`.
- NotebookLM generates deliverables: podcast, video, infographic, slide deck, flashcards, quizzes, data tables.
- All deliverables returned to Claude Code.
- Sub-skills combined into one "super skill" via Skill Creator.
- All markdown output saved to Obsidian vault.

**2:59 - 4:26 | Obsidian symbiotic relationship**
- Obsidian provides graph view and linked navigation for the user.
- All markdown files in Obsidian are transparent to Claude Code: it can read and build on them.
- Self-improving loop: "The more I run the workflow, the more it gets its analysis in the way I like it... Cloud Code continues to build and build and build over time this corpus of knowledge and evidence for how I like to work."
- Core template is `FLOW -> OBSIDIAN -> IMPROVED SKILLS via SKILL CREATOR`.

**4:26 - 5:22 | Sponsor segment**
- Chase AI Plus (Claude Code Masterclass) and free Chase AI community promoted.

**5:22 - 6:27 | Creating the `yt-search` skill**
- Types `/plugin` in Claude Code terminal, searches for and selects `skill-creator`.
- Skill Creator prompt: search YouTube using `yt-dlp`; return top 20 results with title, channel, subscribers, views, duration, upload date, URL; default 6-month filter with `--months` flag; views-to-subscribers engagement ratio; formatted output with dividers.
- Output confirms: `SKILL.md` created at `.claude/skills/yt-search/SKILL.md`.

**6:27 - 8:42 | NotebookLM integration via `notebooklm-py`**
- No public NotebookLM API; uses `teng-lin/notebooklm-py` (GitHub).
- Install: `pip install notebooklm-py` + `playwright install chromium` (in a separate terminal, not inside Claude Code).
- Auth: `notebooklm login` opens browser for Google account authentication.
- Skill Creator prompt points Claude Code at the GitHub README URL so it can self-teach the library's CLI interface.
- NotebookLM capabilities exposed via skill: create notebooks, add sources, chat, generate audio/video/quizzes/flashcards/infographics/slide decks/data tables, download artefacts.

**8:42 - 11:09 | Creating and executing the `yt-pipeline` super skill**
- Skill Creator prompt combines `yt-search` and `notebooklm` into a single `yt-pipeline` skill.
- Pipeline logic encoded in the prompt: search YouTube for 10 relevant videos, create new NotebookLM notebook, add sources, run analysis, request deliverable (infographic), return markdown research note.
- Live execution: Claude Code checks NotebookLM auth and runs YouTube searches in parallel.
- Runs a second search to increase source variety.
- Highlighted benefit: "these are tokens you're not paying for and Claude Code doesn't have to use" (NotebookLM processing is offloaded to Google).
- Pipeline completes in ~6 minutes. Outputs: `claude-code-mcp-servers-research.md` + `claude-code-mcp-infographic.png`.

**11:09 - 13:23 | Reviewing outputs and Obsidian's role**
- Infographic: "MCP: The Universal Power-Up for AI Coding Agents" displayed in VS Code.
- Research markdown: key takeaways, top 5 MCP servers table, video performance analysis, backlinks to related Obsidian notes.
- Same note shown in Obsidian with knowledge graph connections.
- `CLAUDE.md` described as the "brain within a brain": defines work style, conventions, current priorities.
- Demonstrates live update: prompt to Claude "Can we update claude.md so it better reflects my workstyle, analysis, and output preferences based on our latest conversations."

**13:23 - 15:02 | Conclusion**
- Reiterates self-improving feedback loop with full diagram and blue arrows circling entire workflow.
- Long-term value comes from the growing Obsidian vault continuously calibrating Claude Code.
- Call to action for Chase AI Plus and community.

---

## Visual Analysis

- **Opening icons (0:00 - 0:13):** Sequential appearance of Claude Code (pixelated orange), Notebook LM (three white arcs), Obsidian (purple crystal), Skill Creator (orange starburst) icons on white background.
- **VS Code terminal preview (0:13):** Shows completed pipeline output: "Agent 'Wait and download infographic' completed... Full pipeline complete: 10 Youtube sources analyzed in NotebookLM, Research note saved to research/claude-code-mcp-servers-research.md, Infographic downloaded to research/claude-code-mcp-infographic.png."
- **Workflow diagram (recurring, 0:29 onwards):** Black background. Left: "CLAUDE CODE" (pixelated). Right: "CLAUDE CODE" (pixelated). Centre row: YouTube icon + 3 NotebookLM icons. Below: Obsidian icon. Orange arrows added progressively to show data flow. Blue arrows added to show Obsidian feedback loop encircling the entire workflow.
- **`capstone-video.md` and `CLAUDE.md` (3:12):** VS Code showing video script notes and full personal assistant configuration file with About Me, Vault Structure, Conventions, Preferences, Current Priorities, and Tools sections.
- **Skill Creator terminal (5:23 - 6:27):** VS Code terminal showing `/plugin` and `/skill-creator` invocation, full natural-language prompt, and confirmation of `SKILL.md` creation.
- **notebooklm-py GitHub README (6:38 - 7:49):** Install commands, `notebooklm login`, CLI usage examples, and "Install via CLI or ask Claude Code to do it: `notebooklm skill install`" all visible.
- **Pipeline execution terminal (10:14 - 10:49):** Step-by-step output visible with parallel YouTube search, NotebookLM auth checks, and final completion message with file paths.
- **Generated infographic (11:09 - 11:33):** Colourful PNG in VS Code. Title: "MCP: The Universal Power-Up for AI Coding Agents." Panels: "The Architecture of Autonomous Coding," "The Essential Vibe Coding Stack." Tools visible: Supabase, Context7, Figma, Sentry, Playwright.
- **Research markdown (11:33 - 11:51):** Markdown note with metadata, Related links, Notebook link (to live NotebookLM notebook), Key Takeaways, Top 5 MCP Servers table (Server / Purpose / Why Recommended), Video Performance Analysis.
- **Obsidian graph view (11:51 - 12:02):** Research note shown with knowledge graph connections to other vault notes.
- **CLAUDE.md update (12:02 - 13:23):** Vault folder structure visible (daily-notes, inbox, people, projects, research). Live prompt to update CLAUDE.md shown being processed.

---

## Steps Covered

1. Install `skill-creator` plugin via `/plugin` in Claude Code terminal.
2. Create `yt-search` skill: `/skill-creator` + natural language prompt (yt-dlp backend).
3. Install `notebooklm-py` in a separate terminal: `pip install notebooklm-py`, `playwright install chromium`, `notebooklm login`.
4. Create `notebooklm` skill: `/skill-creator` + GitHub README URL (Claude Code self-teaches the library).
5. Create `yt-pipeline` super skill: single Skill Creator prompt combining both skills into an end-to-end pipeline.
6. Invoke `/yt-pipeline` with a natural-language research query specifying deliverable type.
7. Review outputs (markdown + infographic) in VS Code and Obsidian.
8. Update `CLAUDE.md` by prompting Claude Code to reflect recent conversations.

---

## All Concepts, Tools, People, and Entities Referenced

| Name | Type | Role in video |
|---|---|---|
| Claude Code | AI tool | Central orchestrator; runs skills and saves output |
| NotebookLM | AI tool (Google) | Analysis engine; generates structured deliverables |
| Obsidian | Knowledge base | Persistent memory and self-improvement feedback layer |
| Skill Creator | Claude Code feature | Natural-language skill definition and composition |
| yt-dlp | CLI tool | YouTube search and metadata backend |
| notebooklm-py (teng-lin) | Python library | Unofficial NotebookLM API via browser automation |
| Playwright | Web automation library | Required by notebooklm-py for browser-based auth |
| VS Code | IDE | Development environment shown throughout |
| YouTube | Platform | Data source for demo pipeline |
| MCP (video uses "Meta-Cognitive Protocol") | Protocol/concept | Subject of demo research; shown in infographic |
| Supabase | Backend service | Listed in infographic as essential vibe coding stack tool |
| Context7 | Tool | Listed in infographic as essential vibe coding stack tool |
| Figma | Design tool | Listed in infographic |
| Sentry | Error tracking | Listed in infographic |
| Shadcn | UI component library | Listed in infographic |
| PostHog | Product analytics | Listed in infographic |
| CLAUDE.md | Vault file | Personal assistant configuration for Claude Code |
| yt-search skill | Custom Claude Code skill | YouTube search and metadata retrieval |
| notebooklm skill | Custom Claude Code skill | NotebookLM interaction via notebooklm-py |
| yt-pipeline skill | Custom Claude Code super skill | End-to-end YouTube research pipeline |
| Kenny Liao (3.2x) | Person | Mentioned as engagement outlier in research output |
| Matt Kuda (6.6x) | Person | Mentioned as engagement outlier in research output |
| Chase AI Plus | Product | Speaker's paid Claude Code masterclass |
| Chase AI Community | Resource | Speaker's free community |

---

## Key Takeaways

- Combining Claude Code, NotebookLM, Obsidian, and Skill Creator creates a workflow that is significantly more capable than any single tool alone.
- The Skill Creator allows complex multi-tool pipelines to be defined in plain language and invoked as a single command.
- NotebookLM offloads heavy analysis from Claude Code, reducing token cost and enabling richer deliverables (infographics, audio, slide decks).
- Obsidian functions as Claude Code's readable persistent memory: every markdown output accumulates into a structured knowledge base the AI can act on.
- `CLAUDE.md` is the explicit control layer; the broader vault provides implicit style calibration through accumulated examples.
- The feedback loop is the core value: each run deposits more evidence of the user's preferences, making subsequent runs more accurately tailored.
- The workflow template is data-source-agnostic: swap YouTube for PDFs, articles, or any other source without changing the architecture.
- Pointing the Skill Creator at a GitHub README is sufficient to teach Claude Code how to use an external library.

---

## Claims Requiring Verification

| Claim | Timestamp | Note |
|---|---|---|
| Setup completable "in under 30 minutes" | 0:28 | Optimistic; assumes familiarity with Claude Code, Python, and the tools involved |
| Pipeline completes in ~6 minutes for 10 sources | 10:49 | Will vary with NotebookLM load, complexity of analysis, and deliverable type |
| Slide deck generation can take "up to 15 minutes" | ~11:03 | NotebookLM generation times vary; check current docs |
| notebooklm-py is reliable and maintained | Throughout | Unofficial library against a web UI; fragile to Google endpoint changes |
| NotebookLM processing is "tokens you're not paying for" | ~10:43 | Accurate for the current free tier; check whether Google has added quotas or costs |
| "MCP" expanded as "Meta-Cognitive Protocol" in infographic | Visual analysis | Gemini's reading; actual expansion in video is likely Model Context Protocol |

---

## Open Questions

- What is the failure mode when notebooklm-py's browser-based auth (Playwright) breaks? No error handling is shown.
- How does the pipeline behave if a NotebookLM notebook with the same name already exists?
- Is `teng-lin/notebooklm-py` actively maintained? What is the break risk if Google changes internal endpoints?
- What are the actual token savings from offloading to NotebookLM versus Claude Code processing the same sources directly?
- The "self-improving loop" is described qualitatively. Does Claude Code read the entire vault on each invocation, or only `CLAUDE.md`? What is the practical mechanism?
- How does performance scale as the Obsidian vault grows? Is there a context bloat risk?
- What happens to NotebookLM notebooks over time? Is there a cleanup strategy, or do they accumulate indefinitely?
- Is the infographic output format (PNG) always available in NotebookLM, or is it tier-dependent?
- How does this workflow handle private or age-restricted YouTube videos?
- What are the data privacy implications of sending research queries through both Google (NotebookLM) and Anthropic (Claude Code)?
