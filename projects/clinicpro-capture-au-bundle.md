---
id: clinicpro-capture-au-bundle
status: active
type: partnership
repo: clinicpro-medtech
title: "ClinicPro Capture: AU Bundle Deal"
description: "Medtech Global purchases Capture licences to bundle into Evolution AU G2M launch. Lawrence Peterson lead."
phase: "Term sheet on hold pending WHT resolution; Lawrence reviewing practice minimum"
dashboard: clinicpro-medtech
---

## Overview

Medtech Global purchases ClinicPro Capture licences as a value-add bundle for the Evolution AU G2M launch. Per-licence fee model. Lawrence Peterson (Medtech Global) is the main contact.

Kept strictly separate from the Medtech NZ integration contract ([[clinicpro-capture-integration]]). Medtech may attempt to link the two contracts; refuse linkage.

**Execution sprint**: [[2026-04-medtech-sprint-2]] (21 Apr - 16 May 2026)
**Strategy and pricing analysis**: [[clinicpro-capture-au-strategy]]
**External proposal one-pager**: [[clinicpro-capture-au-proposal]]
**Product context**: [[clinicpro-capture]]

## 22 April 2026 meeting outcomes

**Lawrence (AU):** Strong interest, deal likely. AUD 30 not objected to. 50-practice minimum flagged as too high; Lawrence taking to boss — expected response within days. Floor is 40 at AUD 30 (per trade rules). Product confirmed as entirely new G2M software (Medtech AU revamp). Same ALEX backend, not all APIs accessible; capture API available. White-label confirmed. Medtech handling all marketing. Setup fee acknowledged verbally in room, no cost given. Competitor image vendor slow on issue response; Lawrence prefers ClinicPro. Lawrence raised a management dashboard (tenancy/licence model) — confirmed as out-of-bundle scope, separate one-off build engagement (task medtech-20260422-001). Auth, update control, security requirements, domain, tax treatment not discussed — carry to next meeting.

## AU bundle — Lawrence Peterson (Medtech Global)

**Proposal received 12 April 2026:** Lawrence proposes Medtech purchases ClinicPro Capture licenses to bundle as a value-add for AU G2M in May. Scope: image capture + post only as starting point. Two other integration partners already confirmed for AU launch.

**Terms sent to Lawrence 19 April 2026** (CC Alex, existing thread 19cfe204467d0370):

- AUD 30 per active practice per month
- 50 active practices per year minimum → AUD 18,000/year floor
- 3-year initial term
- Scope: image capture and ALEX /DocumentReference POST
- Launch target May–June 2026 to align with Evolution AU G2M
- Sydney AWS hosting, AU data residency covered

## Legal approach (decided 23 April 2026)

- **Method:** self-draft with AI assistance, review-only legal engagement. No lawyer drafting from scratch.
- **Rationale:** AUD $14,400-$18,000/year deal value makes full-drafting engagement disproportionate.
- **Legal firms contacted:** HGM (Andrew Dentice, andrew.dentice@hgmlegal.com) and Kindrik Partners (Averill Dickson, averill.dickson@kindrik.co.nz). Duncan Cotterill (Ron Arieli, ron.arieli@duncancotterill.com, +64 21 254 3575) replied unsolicited via the firm's general Auckland inbox. All three confirmed capacity same day (23 Apr).
- **Status (24 Apr):** All three firms on hold pending WHT resolution and term sheet finalisation. Evaluating Sprintlaw NZ for fixed-fee contract structure review (~$900 NZD, no calls required). WHT is a tax question requiring a separate specialist opinion — ask Helen first. Hold replies sent to all three firms. See task medtech-20260423-002.

**AU term sheet v1 status (23 April 2026):** Drafted. `clinicpro-medtech/docs/commercial/au-bundle-term-sheet-v1.md`. AUD $30/practice/month, 40-50 practice floor ($14,400-$18,000/year), 3-year term. 8 open questions. Do not send to Lawrence until Q5 (WHT/Helen) is resolved.

## Open questions

| # | Question | Status |
|---|---|---|
| Q2 | Does Lawrence accept AUD 30/practice/month — minimum practice number? | AUD 30 not objected to. 50-practice minimum flagged as too high. Lawrence taking to boss. Floor is 40 at AUD 30. |
| Q5 | WHT treatment on AU-NZ SaaS payments under NZ-AU DTA | ATO draft ruling TR 2024/D1 (Jan 2024): SaaS payments likely qualify as royalties under Art. 12, 5% WHT, withheld by Medtech (AU payer) before remitting to ClinicPro. Contract must address this explicitly: either gross-up clause (Medtech pays WHT on top, ClinicPro receives full AUD 30) or stated net rate (ClinicPro receives AUD 28.50). Professional tax opinion required — Art. 7 business profits exemption does not override Art. 12 royalty treatment. Next: ask Helen (or her referral) for targeted opinion. Hold term sheet until resolved. |
| Q6 | Management dashboard scope — what does Lawrence need it to do? | Raised 22 Apr. Cannot price or commit until scope received from Lawrence in writing. Separate one-off invoice. Task medtech-20260422-001. |
| Q8 | Update control: Medtech approval vs ClinicPro auto-deploy | Not discussed 22 Apr. Needed for setup fee scoping. |

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
  .where(p => p.project === "clinicpro-capture-au-bundle" && p.status !== "done")
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
