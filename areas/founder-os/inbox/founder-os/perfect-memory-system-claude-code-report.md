# The Perfect Memory System for Claude Code: Plan, Design & Build - Reference Report

**Source:** https://www.youtube.com/watch?v=OMkdlwZxSt8
**Analysed via:** Gemini 2.5 Flash
**Speaker:** Mark
**Channel:** MemPalace
**Duration:** 20:51
**Status:** First draft. Requires human review before use as reference.

---

## Overview

A tutorial walkthrough on designing a personalised memory system for Claude Code, aimed at anyone from non-technical users upward. The speaker argues no off-the-shelf memory repo is a perfect fit, then demonstrates a three-step process (Clone, Audit, Extract) using Claude Code itself to analyse existing open-source frameworks and generate a custom architecture. The video ends with a live demo of auto-injecting memory via hooks.

---

## Core Thesis

There is no universal memory system for Claude Code. Effective AI agent memory, like human memory, must be tailored to the individual's role, workflow, and information needs. Rather than adopting an existing repo wholesale, users should treat memory as an evolving "living system": clone existing frameworks, use Claude Code to audit and compare their design patterns, extract what fits, then build a personalised stack that complements (not replaces) Claude Code's native memory.

---

## Transcript Summary

**0:00 - 0:18: Hook**
Animated brain visual. Human brains are similar but not identical; same applies to AI memory needs. "No perfect fit for everybody."

**0:18 - 0:57: The problem**
Claude Code has built-in memory designed for the masses. The open-source ecosystem has many memory frameworks (MemPalace, claudesidian, mem0, beads, kioku, etc.) but none fits everyone. Goal: build one tailored to your day-to-day workflows.

**0:57 - 2:02: Why existing repos fall short**
Each profession has different memory needs: high-volume e-commerce (seasonal patterns), wealth manager (deep relationships), lawyer (precedent recall). The question is "what does my memory system need to look like," not "which repo should I clone."

**2:45 - 3:10: Memory as an infinite game**
Memory is not a one-time setup. "The moment you finish it, the job is to maintain and iterate on it as you evolve, your business evolves, and your day-to-day evolves as well."

**3:10 - 5:42: Demo: Clone, Audit, Extract**
Speaker clones three repos (mempalace, claudesidian, mem0ai/mem0) into Claude Code and prompts subagents to explore each and produce a comparative report. Claude Code launches three background Explore agents and returns:
- A comparison table: Substrate, Unit, Index, Philosophy per framework.
  - MemPalace: ChromaDB + SQLite knowledge graph; vector unit; ANN + graph; structured retrieval.
  - claudesidian: Flat markdown in PARA folders; note unit; fuzzy + tag; human-readable simplicity.
  - mem0: Any of 30 vector stores + SQLite history; entity/fact unit; semantic + graph; managed memory-as-a-service.
- "Consequential design moves" and "patterns worth stealing."

**6:11 - 8:13: Defining your own memory spec**
Speaker inputs a natural language prompt to Claude Code describing desired characteristics: fading memories, some persistent, semantic lookup, lightweight. Claude Code outputs a "lightweight memory spec":
- Stack: SQLite with sqlite-vec extension, small local embedder (bge-small-en or nomic-embed-text via Ollama).
- Schema: one table with id, content, embedding, created_at, last_accessed, access_count, half_life_days, score.
- Three paradigms: two-tier with half-life decay; append-only with lazy cleanup; synthesis rollup.
- "What I deliberately dropped": no graph layer, no LLM-driven UPDATE/DELETE.

**8:13 - 9:53: The memory stack**
Visual layered model:
- ALWAYS ON: Identity (name badge), Critical Context (sticky note).
- ON DEMAND: Working Memory (messy desk).
- SEARCHED: Long-term Knowledge (filing cabinet), Episodic Memory (journal).
- BACKGROUND: Decay (forgetting curve), Promotion (intern to manager).

**9:53 - 10:29: Multi-signal retrieval**
Combining semantic (meaning), keyword (exact match), and entity (people, places) retrieval via rank fusion before returning results. Claimed reduction from 25,000 to 7,000 tokens for typical retrieval. (See claims section.)

**10:29 - 11:45: Advanced memory concepts**
- Salience: frequently used memories stay sharp; rarely accessed ones fade.
- Promotion: repeated patterns become permanent rules.
- Progressive Disclosure: load identity first, then knowledge, then full history.
- Compaction Survival: re-inject critical memories after context compaction.
- Add-Only: never overwrite; keep both old and new versions.

**11:45 - 13:59: Demo: `memory-architect` skill**
A custom Claude Code skill that interviews the user about their role, technical level, and desired memory layers. Interactive multi-choice UI within the terminal. Speaker selects "Full walkthrough," "Content creator / knowledge worker," "CLI comfortable."

**13:59 - 15:42: Building the custom structure**
Skill recommends Obsidian as visual layer (human browses via app; Claude reads via CLI; same `.md` files). User selects "Obsidian (Recommended)." Skill outputs:
- Recipe: Always On (Identity + Critical Context), On Demand (Working Memory), Searched (Long-term Knowledge + Episodic), Background (Decay + Promotion).
- Creates: `memory/PRIME.md`, `memory/identity.md`, `memory/context.md`, `memory/knowledge/`, `memory/scripts/search.sh`.

**15:42 - 17:59: Memory injection approaches**
Three methods explained:
1. Via CLAUDE.md: simplest, no hooks. Place instructions in CLAUDE.md to read identity and context files at session start.
2. Via Hooks: SessionStart fires `cat _identity.md`; PreCompact fires `cat _context.md`; SessionEnd writes updated context. Deterministic injection.
3. Via Agent Scoping (ClaudeClaw): each specialised agent (comms, content, ops) gets its own vault folder; shared `identity.md` ensures consistent self-awareness across the team.

**17:59 - 19:56: Final build and verification**
Skill generates hooks config in `.claude/settings.json`. Verification: close session, open new one, ask "Who am I and what am I working on?" Claude Code auto-injects primed identity and context without explicit file reads.

**19:57 - 20:44: Close**
Call to action. Skill available in video description. Channel: Early AI-dopters community for advanced content.

---

## Visual Analysis

Key visuals beyond the transcript:

- **Slide: "THE WORLD OF MEMORY"** (0:57): Central purple crystal with ~20 open-source memory project names radiating outward. Establishes the fragmented ecosystem.
- **Slide: "MEMORY IS A FINGERPRINT"** (2:02): Three profession archetypes each linked to a different memory architecture style (hierarchical flowchart, document stacks, network graph).
- **Slide: "Your Memory Stack"** (8:13): Layered pyramid with colour-coded tiers, analogies per layer (name badge, sticky note, messy desk, filing cabinet, journal), and directional arrows showing promotion/decay flow.
- **Slide: "Multi-Signal Retrieval"** (9:53): Three parallel input flows converging at a rank fusion funnel. Token counts 25,000 (crossed out) and 7,000 (circled) shown visually.
- **Slide: "MEMORY CONCEPTS EXPLAINED"** (10:29): Six concept boxes, each with a sketch diagram.
- **Slide: "How Memory Gets Injected"** (15:42): Three-row comparison of injection approaches with hook names, file references, and agent diagrams shown side by side.
- **Live terminal demo** (3:56 onward): Actual Claude Code UI visible; commands pasted, agents launched, markdown tables returned, settings.json written.

---

## All Concepts, Tools, People, and Entities Referenced

| Name | Type | Role in video |
|---|---|---|
| Claude Code | Tool | Primary agent being configured |
| MemPalace | Repo | Framework analysed; speaker's own channel |
| claudesidian | Repo | Framework analysed; Claude + Obsidian hybrid |
| mem0 / mem0ai | Repo | Framework analysed; managed memory-as-a-service |
| beads, kioku, memsearch, CPR, supermemory, obsidian-mind, engram, episodic-memory, memory-bank, claude-memory-compiler, memcp, cc-soul, a-mem-mcp, second-brain, Nemp, agentmemory, kioku-lite | Repos | Named in ecosystem slide; not individually analysed |
| ChromaDB | Database | MemPalace substrate |
| SQLite | Database | MemPalace + mem0 + recommended custom stack |
| sqlite-vec | Extension | Recommended for custom vector storage |
| Qdrant | Database | mem0 default vector store |
| bge-small-en | Model | Suggested local embedder |
| nomic-embed-text (Ollama) | Model | Suggested local embedder |
| all-MiniLM-L6-v2 | Model | Suggested local embedder |
| Obsidian | Tool | Recommended visual/human layer for memory |
| ClaudeClaw | System | Speaker's personal Claude Code agent setup |
| memory-architect | Skill | Custom skill to interview and build memory systems |
| GitHub | Platform | Source of repos |
| PARA folders | Method | Organisational framework used by claudesidian |
| Rank fusion | Technique | Combining multiple retrieval signals |
| Half-life decay | Technique | Memory scoring formula based on time and access |
| Hooks (SessionStart, PreCompact, SessionEnd) | Feature | Claude Code event hooks for auto-injection |
| settings.json | File | Claude Code config; hooks are written here |
| PRIME.md | File | Auto-injected identity + context file |

---

## Key Takeaways

1. No off-the-shelf memory system is a perfect fit; build your own by extracting patterns from existing repos.
2. Use Claude Code itself to clone, audit, and compare frameworks: launch subagents, get a comparative report, then define your spec in natural language.
3. Structure memory in layers: Identity and Critical Context always on; Working Memory on demand; Long-term Knowledge and Episodic Memory searched; Decay and Promotion running in background.
4. Multi-signal retrieval (semantic + keyword + entity) narrows context before injection, reducing token usage substantially.
5. Hooks (SessionStart, PreCompact, SessionEnd) are the cleanest injection mechanism: deterministic, automatic, no manual prompting needed.
6. Obsidian works as a human-readable visual layer while Claude reads the same `.md` files via CLI: no duplication.
7. The Add-Only principle prevents silent data loss: keep both old and new versions rather than overwriting.
8. Compaction Survival is underused: re-inject critical context via PreCompact hook to prevent important memory loss during long sessions.
9. For multi-agent setups, give each agent its own vault slice while sharing a common `identity.md`.
10. Treat the memory system as a living, evolving artefact, not a one-time configuration.

---

## Claims Requiring Verification

| Claim | Why it needs checking |
|---|---|
| Multi-signal retrieval reduces tokens from 25,000 to 7,000 | No benchmark cited; depends heavily on content and query type |
| "90% of people don't know about Compaction Survival" | Anecdotal; unverifiable |
| "1-2% of your entire history is typically what you need to recall" | No source; may not hold for knowledge-dense workflows |
| MemPalace uses ChromaDB + SQLite KG | Verify against current repo; architecture may have changed |
| claudesidian is "purely markdown files" | Verify; plugin may have added database features |
| mem0 supports "any of 30 vector stores" | Verify current mem0 docs for supported backends |
| bge-small-en / nomic-embed-text are suitable for production-quality semantic retrieval | Depends on domain; medical or legal text may need larger models |

---

## Open Questions

- What are the latency and cost implications of running local embedders (Ollama) versus cloud embeddings at scale?
- How does the half-life decay formula interact with Claude Code's context compaction? Does compaction reset access counts?
- Is there a performance ceiling on SQLite + sqlite-vec for large memory stores (e.g., 10,000+ entries)?
- How should the `memory-architect` skill be updated as Claude Code's hook API evolves?
- For a medical or clinical workflow, what memory categories would be appropriate (patient context, clinical rules, decision history)?
- How does agent-scoped memory (ClaudeClaw pattern) handle shared state conflicts when two agents update overlapping memory files simultaneously?
- What is the actual token overhead of running `cat PRIME.md` at SessionStart for a 5 KB identity file?
- The video does not cover memory deletion or privacy: how should sensitive memories be expired or redacted?
