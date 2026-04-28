# LLM workspace guide — NexWave / ClinicPro

Read this **before** editing files when the user shares Obsidian context, tasks, or dashboards.

## What each place is for

| Location | Purpose | Code? |
|----------|---------|--------|
| **Obsidian vault** (`…/Cursor/obsidian/`) | Tasks, projects, sprints, dashboards, strategy notes (`context/`) | **No application code.** No Next.js routes, no API handlers, no migrations for product apps. |
| **clinicpro-saas** | ClinicPro web app (www.clinicpro.co.nz) | **Yes** — primary codebase for SaaS work. |
| **clinicpro-medtech** | ClinicPro Capture PWA + Medtech integration | **Yes** — includes `lightsail-bff/` where relevant. |
| **nexwave-rd** | MBIE R&D programme (isolated from commercial repos) | **Yes** — experiments, scripts, R&D docs **only** here. |

The vault holds **what to do** (`tasks/open/*.md` with `repo` + `project` in frontmatter). Product repos hold **how it is built**.

## Hard rule: do not implement in the vault

If the user pastes a task, dashboard, or note from Obsidian:

1. **Read the task file’s `repo` field** — that names the git repo where implementation belongs.
2. **Open and work in that repo’s root**, not under `obsidian/`.
3. **Obsidian changes** are limited to: task status, due dates, notes in the task body, `projects/`, `context/` — unless the user explicitly asks for vault-only work.

If you start adding routes, components, or server logic under `obsidian/`, you are in the **wrong tree**.

## How to choose the repo (deterministic)

1. **From a task file:** use frontmatter `repo:` (`clinicpro-saas` | `clinicpro-medtech` | `nexwave-rd`).
2. **From task id prefix:** `saas-*` → clinicpro-saas; `medtech-*` → clinicpro-medtech; `rd-*` → nexwave-rd.
3. **From `project` file** in `projects/*.md`: check that file’s `repo` field.
4. **If `repo` is missing or ambiguous:** ask the user which repo to use **before** writing code.

## Paths (Ryo’s machine)

Adjust if the user’s base path differs; structure is stable.

| `repo` field | Typical folder |
|--------------|----------------|
| `clinicpro-saas` | `C:\Users\reonz\Cursor\clinicpro-saas` |
| `clinicpro-medtech` | `C:\Users\reonz\Cursor\clinicpro-medtech` |
| `nexwave-rd` | `C:\Users\reonz\Cursor\nexwave-rd` |
| Vault | `C:\Users\reonz\Cursor\obsidian` |

## Where knowledge lives

- **Repo:** `README`, `docs/`, ADRs, comments next to code — versioned with the product; use when **implementing**.
- **Vault:** `system/repos.md` (route map), `system/stack.md`, people, planning — use when **scoping or prioritising**; not a substitute for repo docs.

When you need product structure (routes, folders), prefer **`system/repos.md`** in the vault **plus** the target repo’s tree — not the vault for code.

## R&D isolation

`nexwave-rd` work must **not** import or copy commercial ClinicPro code into grant deliverables unless the user explicitly allows it. Keep MBIE-related changes in **nexwave-rd** and Obsidian `rd-*` tasks.

## Short checklist before coding

- [ ] Confirmed target **repo** (from task or user).
- [ ] Terminal / file operations use that repo’s root (or a path inside it).
- [ ] No new “app” code under `obsidian/` unless the task is vault maintenance only.
