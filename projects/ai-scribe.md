---
id: ai-scribe
status: active
type: product
repo: clinicpro-saas
stack: [nextjs, typescript, tailwind, vercel, neon, clerk]
---

## Description
AI-powered clinical scribe tool for NZ general practice. Active development. Landing page live at `/ai-scribe`.

## Positioning (decided 2026-04-09)

Three pillars, in order of presentation:

1. **Cognitive load, not time** — The measurable benefit is cognitive, not speed. NASA Task Load Index (JAMIA Open 2025): mental demand −6.9 pts (p<.001). Researchers noted "decreased cognitive burden occurred more often than decreased documentation time." Clinician quote: "I'm not worried that I will forget some important detail." PMC12492056 (263 physicians, 6 health systems, 2025): cognitive task load −2.64/10 after 30 days.

2. **Multi-problem consults** — Most scribes trained on single-problem American specialty visits. NZ GP reality: 15-minute slots, 4+ active problems. Market leader (Heidi) independently documented to "conflate or misequence elements when patients present with four or more active conditions." ClinicPro structures notes around an issues list — each complaint keeps its own history, exam, and plan.

3. **NZ GP provenance as trust** — Built by a practising Auckland GP facing the same RNZCGP standards, Medtech/MyPractice quirks, NZ Formulary, and polypharmacy consults. Supporting signal, not primary headline.

Do NOT lead with time savings. Do NOT name Heidi directly. Market-behaviour framing only.

## Landing page assets (as of 2026-04-09)

| Asset | Path | Notes |
|---|---|---|
| Hero image | `public/generated/ai-scribe-hero.jpg` | Nano Banana Pro generated, 2924 KB |
| Hero prompt | `scripts/prompts/ai-scribe-hero.prompt.md` | Fujifilm X100V / Classic Chrome / venetian blind light |
| Consultation screenshot | `public/images/landing-page/ClinicProConsultation.jpg` | § 01 (post pull-quote) |
| Generate note screenshot | `public/images/landing-page/ClinicProGenerateNote.jpg` | § 02 (pre 4-step card) |
| Profile photo | `public/images/landing-page/DrRyoEguchiProfilePicMain.jpg` | 48px circle, § 05 |
| Referral photos | `public/images/referral-images/referral_images_hero_image_3.png` | § 04 referral callout |

## Image generation infrastructure

`scripts/gen-image.mjs` — Node 20 ESM script, no deps. Calls laozhang.ai API (Nano Banana Pro / Gemini 3 Pro Image).

Usage:
```
node --env-file=.env scripts/gen-image.mjs \
  --prompt scripts/prompts/ai-scribe-hero.prompt.md \
  --out public/generated/ai-scribe-hero.jpg \
  --model gemini-3-pro-image-preview \
  --aspect 16:9 --size 2K
```

API format (laozhang.ai): `generationConfig: { responseModalities: ['IMAGE'], imageConfig: { aspectRatio, imageSize } }`. Response: `candidates[0].content.parts[n].inlineData.data` (camelCase).

**Step 1 status (09 April 2026):** Complete. Landing page fully rewritten with cognitive load / multi-problem / NZ provenance positioning, letter grammar visual system, editorial hero image, and product screenshots.

## Tasks

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
const pages = dv.pages('"tasks/open"')
  .where(p => p.project === "ai-scribe" && p.status !== "done")
  .sort(p => p.priority === "high" ? 0 : p.priority === "medium" ? 1 : 2);
const headers = ['Task', 'Status', 'Priority', 'Due'];
dv.table(headers, pages.map(p => [
  dv.fileLink(p.file.path, false, p.title || p.file.name),
  statusSelect(p.file.path), prioritySelect(p.file.path), p.due
]));
scheduleDashboardColumnSort(dv, headers);
```
