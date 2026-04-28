# AI Memory Systems for Claude Code: Reference Report

**Source:** https://youtu.be/UHVFcUzAGlM
**Analysed via:** Gemini 2.5 Flash (direct YouTube URL, April 2026)
**Status:** First draft. Requires human review before use as reference.

---

## Overview

The video surveys the landscape of AI memory tools for Claude Code and argues they are not competing products but distinct levels of a memory stack, each suited to a specific scale and use case. The speaker frames the choice as a decision about two variables:

1. **Where memory lives:** the storage mechanism and file structure (markdown, vector database, local, cloud).
2. **How the AI retrieves it:** the retrieval stage (always-loaded, searched, auto-injected, or called on demand).

Six levels are defined, each building on the previous. Levels 1, 2, and 3 share compatible folder structures and can be stacked.

---

## Core Thesis

Most users are overwhelmed because they treat these tools as alternatives rather than a progression. The right question is not "which tool is best" but "what level do I actually need?" Start at Level 1. Move up only when a specific pain point emerges.

---

## Level 1: What Ships with Claude Code

**Timestamp:** ~1:38 to ~3:40

### CLAUDE.md

A plain markdown file. Always loaded into every session. Functions as a persistent system prompt.

**Three scope levels:**
- User-level (global): `~/.claude/CLAUDE.md` -- loaded in every session everywhere.
- Workspace root: `/projects/CLAUDE.md` -- shared across sub-projects in that workspace.
- Individual project: `marketing-automation/CLAUDE.md` -- only loaded within that specific project.

Local `CLAUDE.md` files override parent files for conflicting rules.

**Context rot problem:** Loading more than ~200 lines into `CLAUDE.md` degrades recall accuracy. The speaker shows a bar chart: recall accuracy drops significantly beyond 200 lines due to context window limits. The fix is to keep `CLAUDE.md` as an index and reference separate files for detailed content.

### Auto-memory

A native Claude Code feature. Claude automatically saves notes across sessions: task context, debugging insights, architecture notes, decisions. It creates a `memory_index.md` as an index pointing to separate markdown files. Claude decides what is worth saving rather than dumping everything.

**Folder structure (auto-memory):**
```
.claude/
  memory/
    memory_index.md        # index file, always loaded
    feedback_*.md          # individual memory entries
    project_*.md
```

**KAIROS (unreleased, leaked):** Anthropic is reportedly developing an always-on background daemon called KAIROS. It watches projects, decides what to remember, and consolidates old notes automatically. Sourced from a Reddit post titled "Five mechanisms of KAIROS, the unreleased always-on Claude Code background agent." Not yet available as of recording.

---

## Level 2: Reliable Memory With Hooks

**Timestamp:** ~6:20 to ~17:00

**Source articles:**
- Pawel Huryn (The Product Compass Newsletter): "How to Give Claude Code Memory"
- John Connelly: "How I Finally Sorted My Claude Code Memory" (Substack, issue #98)

### Structured memory folder

Root at `.claude/memory/`. Manual setup, then Claude maintains it.

```
.claude/memory/
  memory.md              # master index, always loaded
  general.md             # cross-project facts
  domain/
    <topic>.md           # domain-specific knowledge files
  tools/
    <tool>.md            # tool configuration and usage notes
  product/               # product-specific notes
  project/               # project-specific notes
```

Rules embedded in `CLAUDE.md`:
- Keep `memory.md` as a current index.
- Read `memory.md` at session start.
- Write to domain and tools files when relevant context is encountered.

### SessionStart hook

A bash or Python script placed in `~/.claude/hooks/` and registered in `settings.json`. Fires at the start of every new session and every sub-agent. Automatically injects the global memory index into context, ensuring consistent baseline regardless of which project or sub-agent is running.

**Benefit:** removes reliance on Claude remembering to read the memory index. The hook forces it.

### Reorganise memory command

A periodic maintenance ritual. Run `reorganize memory` in plan mode. Claude then:
- Deletes empty stub files.
- Trims stale session notes.
- Annotates unresolved threads.
- Adds cross-references between related files.
- Seeds global memory with new reusable facts.
- Updates all indexes.

### Additional benefits

- Domain files can be shared with teammates (team-level shared context).
- Global vs project memory separation is explicit and portable.

### When to use Level 2

When you have been using Claude Code for a while and want more reliable context loading. Most users, according to the speaker, stop at Level 2.

---

## Level 3: Memory by Meaning, Not Keywords

**Timestamp:** ~17:36 to ~23:46

**Problem Level 2 solves at small scale but not large:** keyword-based file search breaks down as the number of memory files grows. You can have the answer in your notes but Claude cannot find it if the exact keywords do not match.

**Solution:** semantic search -- retrieval by meaning using vector embeddings.

### memsearch

A Claude Code plugin. Ports OpenClaw's memory architecture into Claude Code.

**OpenClaw's architecture (the source pattern):**
- Long-term memory: `memory.md`
- Short-term memory: `daily/` folder
- Background process (optional): `dreaming/` folder for consolidation

**memsearch implementation:**
- Chunks documents into semantic vectors.
- Hybrid search: dense vector search + BM25 sparse search + RRF (Reciprocal Rank Fusion) reranking.
- Smart deduplication.
- Live sync as files change.
- Conversations are auto-summarised and stored.
- Recall happens via semantic search without polluting the main context window.

**Hook used:** `UserPromptSubmit` -- fires on every user message. Injects the top 3 semantic matches from memory files directly into Claude's context before Claude processes the prompt.

**Installation:** Add the plugin via Claude Code plugin manager. Configure in `settings.local.json`:
```json
{
  "memsearch@memsearch-plugins": true,
  "hooks": {
    "UserPromptSubmit": [...]
  }
}
```

**Folder compatibility:** memsearch works with the same `.claude/memory/` structure as Level 2. The two levels are additive.

### claude-mem (alternative to memsearch)

A separate plugin with more features:
- Captures and compresses everything Claude does.
- Dashboard for browsing memory.
- Team collaboration support.
- MCP-based: Claude actively calls the search tool rather than automatic injection.

**Tradeoff:** More featured but requires Claude to decide when to call the memory tool (an extra round-trip). memsearch is automatic via hook.

### When to use Level 3

- You have been using Claude Code for more than a month.
- You have a meaningful number of memory files.
- Claude cannot find answers you know are in your notes.

---

## Level 4: Searching Conversations Verbatim

**Timestamp:** ~23:46 to ~28:28

**Problem Levels 1-3 do not solve:** summarised and embedded memory loses exact wording. You cannot retrieve the precise text of a past decision or conversation.

**Solution:** store content verbatim, indexed for fast lookup.

### MemPalace

A framework for exact word-for-word recall.

**Architecture metaphor:** Wings, Rooms, Closets, Drawers. A hierarchical namespace for organising memory entries.

**Technical implementation:**
- Content is stored verbatim (not summarised).
- An index file written in AAAK (a symbolic language) acts as a pointer system. LLMs scan the index quickly to find which "drawer" holds the answer.
- Two databases running locally:
  - **SQLite:** stores entities and relationships.
  - **ChromaDB:** stores searchable vector chunks for semantic lookup within the verbatim store.
- Background hooks silently index and store information during normal use.
- All data stays on the local machine.

**When to use Level 4:**
- You need the exact wording of a past architectural decision.
- You need to retrieve a verbatim code snippet or conversation excerpt.
- Summarised recall is insufficient for your use case.

---

## Level 5: A Knowledge Base That Builds Itself

**Timestamp:** ~28:28 to ~34:55

**Problem Levels 1-4 do not solve:** managing a large, interconnected body of knowledge across many topics over time. Deep research with linked subtopics.

**Solution:** a living wiki with a strict read/write ownership model.

### Karpathy's LLM Wiki

A pattern, not a specific tool. Named after Andrej Karpathy.

**Core principle -- ownership separation:**
```
raw/     # User owns. Claude reads but NEVER writes.
          # Contains: articles, reports, transcripts, PDFs, raw notes.
wiki/    # Claude owns. Claude reads and writes.
          # Contains: index, concept summaries, decision logs, cross-references.
```

**How it works:**
1. User drops source material into `raw/`.
2. Claude reads `raw/`, extracts knowledge, and writes structured entries into `wiki/`.
3. Claude maintains cross-references and updates `wiki/index.md` automatically.
4. Over time, `wiki/` becomes a searchable, interconnected knowledge base.

**Format:** all plain markdown. Readable by humans, portable, no vendor lock-in.

**Visualisation:** use Obsidian to render the knowledge graph from the markdown wikilinks.

**When to use Level 5:** deep research on a topic where you want to accumulate and connect knowledge across many sources over weeks or months.

### Recall.ai (hosted alternative)

Essentially Karpathy's wiki pattern as a service.

**Tradeoffs:**
- Pro: no setup, managed for you.
- Con: you do not own the data. Built for consumption (reading), not operational memory (acting). Has pricing.

### LightRAG (enterprise alternative)

Open-source, research-grade knowledge graph system.

**Features:** heavy entity extraction, dual-level retrieval (local and global graph traversal), full graph database backend.

**Tradeoff:** enterprise-appropriate but completely over-engineered for individual use. The speaker explicitly calls it overkill for most users.

---

## Level 6: One Memory Across Every AI Tool

**Timestamp:** ~28:28 to ~39:27 (overlaps with Level 5 intro)

**Problem Levels 1-5 do not solve:** memory is locked to Claude Code. When you switch to ChatGPT, a phone AI app, or a future tool, context is lost.

**Solution:** a single shared memory database that any AI tool can read and write.

### Open Brain

Created by Nate B. Jones. Described as "infrastructure for thinking."

**Architecture:**
- **Database:** PostgreSQL via Supabase. Stores "thoughts": text, vector embedding, tags, categories, timestamp.
- **Vector search:** `pgvector` extension on PostgreSQL enables semantic search.
- **Gateway:** Supabase Edge Functions act as a front door. Any AI tool calls the same Edge Function endpoint to read or write memory.
- **Clients:** Claude Code desktop, ChatGPT phone app, any future AI tool -- all connect to the same database via the Edge Function.

**Benefits:**
- Same memory, same brain, any device, any model.
- Maximum portability and future-proofing.
- You own the data completely.
- Cost: under $1/month on Supabase free tier.

**Drawbacks:**
- Setup time: ~45 minutes following the setup guide.
- Requires understanding of PostgreSQL and Supabase.
- Latency: every memory read/write is an external database call.

**Setup guide:** provided by Nate Jones (GitHub repo: Open Brain).

### Mem0.ai (hosted alternative)

A well-funded, production-ready cross-tool memory layer.

**Tradeoffs:**
- Pro: production-ready, minimal setup, works across tools immediately.
- Con: you do not own the data. SaaS pricing. No local option.

---

## All Tools Referenced

| Tool | Type | Local/Cloud | Cost | Data ownership | Primary use case |
|------|------|------------|------|----------------|-----------------|
| CLAUDE.md | Native feature | Local | Included | Full | Session rules and context |
| Auto-memory | Native feature | Local | Included | Full | Automatic cross-session notes |
| KAIROS | Unreleased native | Local | TBD | Full | Always-on background memory daemon |
| memsearch | Claude Code plugin | Local | Free | Full | Semantic search over memory files |
| claude-mem | Claude Code plugin (MCP) | Local | Free | Full | Full session compression with dashboard |
| OpenClaw | Separate framework | Local | Free | Full | Agent memory architecture (long/short/dreaming) |
| MemPalace | Framework | Local | Free | Full | Verbatim recall via symbolic index + SQLite + ChromaDB |
| Karpathy LLM Wiki | Pattern (no tool) | Local | Free | Full | Self-building knowledge base in markdown |
| Obsidian | Visualisation | Local | Free/paid | Full | Knowledge graph visualisation of wiki |
| Open Brain | Self-hosted infra | Cloud (Supabase) | Under $1/mo | Full | Cross-tool shared memory via PostgreSQL |
| LightRAG | Open-source framework | Local/self-hosted | Free | Full | Enterprise knowledge graph (heavy setup) |
| Recall.ai | Hosted service | Cloud | Paid | None | Managed Karpathy-style wiki |
| Mem0.ai | Hosted service | Cloud | Paid | None | Cross-tool memory layer (managed) |

---

## Stacking Compatibility

The speaker explicitly addresses which levels can coexist:

- **Levels 1 + 2 + 3** stack cleanly out of the box. They share the same folder structure (`.claude/memory/`). memsearch reads the same files that Levels 1 and 2 write. No conflict.
- **Level 4 (MemPalace)** is independent. It runs its own SQLite and ChromaDB alongside the markdown stack. Can coexist but is a separate system.
- **Level 5 (LLM Wiki)** is independent. Uses `raw/` and `wiki/` folders. No overlap with the memory stack.
- **Level 6 (Open Brain)** is independent. External database. Any level can write to it; it does not replace local memory.

---

## Decision Framework

The speaker provides a flowchart:

```
I just started Claude Code
  → Level 1 (CLAUDE.md + auto-memory). 10 minutes to set up. Start here.

I've been using it for a while and want reliable loading
  → Level 2 (Structured memory + SessionStart hook). Most users stop here.

I'm losing old decisions across months of work (summarised recall is fine)
  → Level 3 (memsearch). Semantic search over growing file base.

I need the exact wording of past decisions or conversations
  → Level 4 (MemPalace). Verbatim recall via pointer index.

I need deep research on interconnected topics across many sources
  → Level 5 (Karpathy LLM Wiki). Self-building knowledge base.

I want one brain across Claude Code, ChatGPT, phone apps, and future tools
  → Level 6 (Open Brain or Mem0). Portable, cross-tool memory.
```

---

## Speaker's Personal Position

The speaker states they are personally implementing up to Level 3 within their "Agentic OS" project. They are not implementing Levels 4, 5, or 6 at the time of recording.

---

## Visual Summary

Key on-screen content not captured in audio:

- **Recall accuracy bar chart:** shows accuracy drops sharply beyond ~200 lines of context loaded. Cited as justification for the index-not-content approach to `CLAUDE.md`.
- **OpenClaw architecture diagram:** three-tier: long-term (`memory.md`), short-term (`daily/`), background (`dreaming/`).
- **memsearch architecture diagram:** markdown files to vector store to hybrid search (dense + BM25 + RRF).
- **MemPalace UI screenshots:** shows verbatim content stored in "drawer" system, browsable.
- **Open Brain architecture diagram:** Supabase PostgreSQL at centre, Supabase Edge Functions as gateway, Claude Code desktop and ChatGPT phone as clients connecting to the same database.
- **Level 6 decision flowchart:** visual summary of all 6 levels with decision path shown as a tree.

---

## Claims That Require Verification

1. **KAIROS:** sourced from a Reddit post claiming a leak. Unverified. No official Anthropic announcement referenced.
2. **Recall accuracy drops at 200 lines:** the bar chart is shown but no source or study is cited. Treat as an approximation, not a measured figure.
3. **Open Brain cost under $1/month:** depends on Supabase pricing and usage volume. Supabase free tier limits apply; pricing may have changed.
4. **memsearch plugin availability:** referenced as installable via Claude Code plugin manager. Verify current availability and version compatibility.
5. **claude-mem dashboard and team features:** described but not demonstrated. Verify feature set matches current release.
6. **LightRAG classification as "enterprise-grade":** subjective framing by the speaker. Evaluate independently based on actual use case complexity.

---

## Open Questions Not Addressed in the Video

- How do Levels 3-6 handle sensitive or private data (clinical, legal, financial)?
- What are the actual latency figures for Level 6 (Open Brain) on typical memory queries?
- Can Levels 3 and 4 coexist without indexing conflicts (memsearch + MemPalace on the same files)?
- How does KAIROS (if real) interact with externally-built Level 2/3 systems?
- What happens to memsearch indexes when `memory/` files are reorganised or renamed?
- Is there a meaningful performance ceiling for memsearch before a proper vector database is needed?
