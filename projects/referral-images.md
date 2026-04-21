---
id: referral-images
status: active
type: product
repo: clinicpro-saas
stack: [nextjs, typescript, tailwind, vercel, neon, clerk, stripe]
title: "Referral Images"
description: "Referral image tool. Transitioning from free to paid."
phase: "Landing page and paid model rollout"
dashboard: clinicpro-saas
---

## Description
Referral image tool for GPs. Transitioning from free to paid on 6 April 2026. Existing users get 1 free year from signup.

## Pricing
- **$5/month** recurring subscription, cancel anytime
- **No annual plan**
- New users: 1 month free trial, then $5/month
- Existing users (signed up before 6 April 2026): free for 1 year, no credit card until renewal

## Launch Status
- **Launch date:** 6 April 2026 ✓ Launched
- **Customer email sent:** 31 March 2026 (via Resend broadcast)
- **Grandfathering migration:** complete (6 April 2026) — 78 users set to `2027-04-06`
- **Stripe subscription price:** created; test env configured; T5/T6 pending

## Technical Model (post-launch)
- `imageTier === 'premium'` → unlimited (existing users + paying subscribers)
- Month 1 for new users → unlimited (free trial)
- Month 2+ with `imageTier === 'free'` → blocked, must subscribe
- Grace unlock system: **removed**
- Stripe integration: **subscription** (not one-time payment)

## Key Decisions
- One-time $50 payment model scrapped in favour of $5/month subscription
- No annual plan — monthly only, keep it simple
- Existing users grandfathered for 1 year (not forever) — ~60 users × $5/month = $3,600/year revenue starting April 2027
- Landing page improvements deferred to post-launch sprint (2026-04-sprint-1)

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
const all = dv.pages('"tasks/open"')
  .where(p => p.project === "referral-images" && p.status !== "done")
  .sort(p => p.priority === "high" ? 0 : p.priority === "medium" ? 1 : 2);
const groups = {};
const unassigned = [];
for (let p of all) {
  const m = p.milestone ?? "";
  if (m) {
    if (!groups[m]) groups[m] = [];
    groups[m].push(p);
  } else {
    unassigned.push(p);
  }
}
const render = (tasks) => dv.table(
  ['Task', 'Status', 'Priority', 'Due'],
  tasks.map(p => [dv.fileLink(p.file.path, false, p.title || p.file.name), statusSelect(p.file.path), prioritySelect(p.file.path), p.due])
);
for (const [m, tasks] of Object.entries(groups)) {
  dv.paragraph(`**${m}**`);
  render(tasks);
}
if (unassigned.length > 0) {
  if (Object.keys(groups).length > 0) dv.paragraph("**Backlog**");
  render(unassigned);
}
```
