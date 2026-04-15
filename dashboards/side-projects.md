---
id: side-projects
status: active
type: side-project
---

# Side Projects

Personal and family projects outside of ClinicPro and Nexwave R&D. Maintained by Ryo and Ting.

---

## Projects

| Project            | Owner | Status        | Notes                                 |
| ------------------ | ----- | ------------- | ------------------------------------- |
| [[linkedin-agent]] | Ryo   | 🟢 Production | Automated. Low maintenance.           |
| [[gp-community]]   | Ryo   | 💤 Parked     | Parked indefinitely.                  |
| [[cloud9japan]]    | Ryo   | 💤 Parked     | Mum's business. Horse Messe complete. |
| [[ahuru]]          | Ting  | 🟡 Active     | Ting's ecommerce SEO project.         |
| [[miozuki]]        | Ting  | 🟡 Active     | —                                     |
| [[eguchi-family]]  | Ryo   | 💤 Parked     | Family AI site.                       |

---

## Weekly Progress Log

### Week of 2026-04-14

**miozuki**
- Two-track collaboration workflow shipped: Ting works direct on master, Ryo on feature branches with Vercel previews. `.vscode/tasks.json` (dev server auto-start), `.vscode/settings.json` (one-click auto-push commit), `Ctrl+Alt+P` publish shortcut, `TING-GUIDE.md`, `CLAUDE.md` workflow note, `docs/ting-laptop-setup.md` checklist
- In-person setup on Ting's laptop completed 15 Apr — miozuki-20260415-001 closed
- Site audit cycle run: first audit results filed, audit scripts added to repo, Instagram proxy, Klaviyo subscribe + email popup a11y + contact form fixes shipped
- LCP image perf pass: priority + responsive `sizes` added; audit re-run against fixes
- Nano Banana Pro research context imported to miozuki repo

**linkedin**
- Major agent refactor: full cutover to skill-driven flow across Researcher → Architect → Strategist → Analyst → Picker → Planner → Image Architect (Phases 1–8 commits)
- **Anthropic API dependency eliminated** — `agents/_llm.py` deleted, `langchain-anthropic` + `langchain-core` removed, `config/model_config.json` deleted. Engine now runs on Claude Code subscription only (zero per-post API spend)
- Strategist deterministic guardrails extracted to standalone module with 14 tests
- All 7 agent prompts extracted to `agents/*.md` — editable independently of agent wiring
- MBIE N2RD LinkedIn-safe context added; loaded in Architect for Pillar 2
- `@playwright/cli` installed; new `linkedin-selector-repair` skill — selector fixes via shell loop, ~5 min instead of half-day
- Comprehensive audit (10 workflows) at `temporary/audit/`; 7 critical + 28 significant fixes shipped: first_comment retry on `schedule_post`, per-comment failure tolerance in `executor_run` (≥4/6 threshold), two-phase result merging, session cookie expiry pre-check, em-dash check extended to Golden Hour comments, scheduling registry pruning + hash-based task names, debug instrumentation purged
- New scripts: `auth_preflight.py` (cron-safe session check), `append_performance_history.py`
- Test suite rationalised — Redis + legacy phases removed; all 7 phases pass without API
- linkedin-20260415-001 in-progress (graph.state cause cleared; awaits live verification post session-refresh); new linkedin-20260415-002 created for verification + daily auth-preflight cron

---

## Open Tasks

```dataviewjs
const mb = app.plugins.getPlugin('obsidian-meta-bind-plugin')?.api;
const lifecycle = this.component;
const statusOpts = [
  { name: 'option', value: ['open'] },
  { name: 'option', value: ['in-progress'] },
  { name: 'option', value: ['blocked'] },
  { name: 'option', value: ['done'] }
];
const priorityOpts = [
  { name: 'option', value: ['high'] },
  { name: 'option', value: ['medium'] },
  { name: 'option', value: ['low'] }
];
const ownerOpts = [
  { name: 'option', value: ['ryo'] },
  { name: 'option', value: ['ting'] },
  { name: 'option', value: ['both'] }
];
function statusSelect(filePath) {
  const el = dv.el('span', '');
  const field = mb.createInputFieldMountable(filePath, {
    renderChildType: 'inline',
    declaration: { inputFieldType: 'inlineSelect', bindTarget: mb.parseBindTarget('status', filePath), arguments: [{ name: 'class', value: ['vault-dash-select'] }, { name: 'class', value: ['vault-dash-select--status'] }, ...statusOpts] }
  });
  mb.wrapInMDRC(field, el, lifecycle);
  return el;
}
function prioritySelect(filePath) {
  const el = dv.el('span', '');
  const field = mb.createInputFieldMountable(filePath, {
    renderChildType: 'inline',
    declaration: { inputFieldType: 'inlineSelect', bindTarget: mb.parseBindTarget('priority', filePath), arguments: [{ name: 'class', value: ['vault-dash-select'] }, { name: 'class', value: ['vault-dash-select--priority'] }, ...priorityOpts] }
  });
  mb.wrapInMDRC(field, el, lifecycle);
  return el;
}
function scheduleDashboardColumnSort(dv, headerNames) {
  const bind = (table) => {
    if (table.dataset.vaultDashSortBound) return;
    const thead = table.querySelector('thead');
    const tbody = table.tBodies[0] ?? table.querySelector('tbody');
    if (!thead || !tbody || tbody.rows.length === 0) return;
    table.dataset.vaultDashSortBound = '1';
    const ths = thead.querySelectorAll('th');
    const stripArrows = (s) => String(s).replace(/\s*[\u25B2\u25BC]\s*$/, '').trim();
    const state = { col: -1, dir: 'asc' };
    ths.forEach((th) => { th.dataset.sortLabel = stripArrows(th.textContent); });
    ths.forEach((th, colIndex) => {
      th.style.cursor = 'pointer';
      th.title = 'Sort column';
      th.classList.add('vault-dash-sortable-th');
      th.addEventListener('click', (ev) => {
        ev.preventDefault(); ev.stopPropagation();
        const nextDir = state.col === colIndex && state.dir === 'asc' ? 'desc' : 'asc';
        state.col = colIndex; state.dir = nextDir;
        const headerName = headerNames[colIndex] ?? '';
        const sortKey = (row) => {
          const cell = row.cells[colIndex];
          if (!cell) return '';
          if (/due/i.test(headerName)) {
            const raw = cell.innerText?.trim() ?? '';
            const L = dv.luxon.DateTime;
            const iso = L.fromISO(raw);
            if (iso.isValid) return iso.toMillis();
            const fmts = ['MMMM d, yyyy', 'd MMMM yyyy', 'yyyy-MM-dd', 'dd/MM/yyyy', 'd/MM/yyyy'];
            for (const f of fmts) { const d = L.fromFormat(raw, f, { locale: 'en-NZ' }); if (d.isValid) return d.toMillis(); }
            const ms = Date.parse(raw);
            if (!isNaN(ms)) return ms;
            return raw.toLowerCase();
          }
          const sel = cell.querySelector('select');
          if (sel) { const opt = sel.options[sel.selectedIndex]; return (opt?.textContent ?? opt?.innerText ?? sel.value ?? '').trim().toLowerCase(); }
          return (cell.innerText?.trim() ?? '').toLowerCase();
        };
        const tb = table.tBodies[0] ?? table.querySelector('tbody');
        if (!tb) return;
        const rows = Array.from(tb.rows);
        rows.sort((a, b) => { const ka = sortKey(a), kb = sortKey(b); let cmp = (typeof ka === 'number' && typeof kb === 'number') ? ka - kb : String(ka).localeCompare(String(kb), undefined, { numeric: true, sensitivity: 'base' }); return nextDir === 'asc' ? cmp : -cmp; });
        rows.forEach((r) => tb.appendChild(r));
        ths.forEach((h, i) => { const base = h.dataset.sortLabel || stripArrows(h.textContent); h.textContent = base + (i === colIndex ? (nextDir === 'asc' ? ' ▲' : ' ▼') : ''); });
      });
    });
  };
  const tryBind = () => { const table = dv.container.querySelector('table'); if (!table) return false; const tbody = table.tBodies[0] ?? table.querySelector('tbody'); if (!tbody || tbody.rows.length === 0) return false; bind(table); return true; };
  if (tryBind()) return;
  const obs = new MutationObserver(() => { if (tryBind()) obs.disconnect(); });
  obs.observe(dv.container, { childList: true, subtree: true });
  setTimeout(() => obs.disconnect(), 8000);
}
const sideProjects = ["gp-community", "cloud9japan", "linkedin-agent", "ahuru", "miozuki", "eguchi-family"];
const pages = dv.pages('"tasks/open"')
  .where(p => sideProjects.includes(p.project) && p.status !== "done")
  .sort(p => p.priority === "high" ? 0 : p.priority === "medium" ? 1 : 2);
const headers = ['Task', 'Project', 'Owner', 'Status', 'Priority', 'Due'];
dv.table(headers, pages.map(p => [
  dv.fileLink(p.file.path, false, p.title || p.file.name),
  p.project, p.owner, statusSelect(p.file.path), prioritySelect(p.file.path), p.due
]));
scheduleDashboardColumnSort(dv, headers);
```
