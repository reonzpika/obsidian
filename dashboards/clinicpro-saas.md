# Dashboard — ClinicPro SaaS

Products: AI Scribe, Referral Images, 12-Month Prescription.

---

## Projects

```dataviewjs
const active = dv.pages('"projects"')
  .where(p => p.dashboard == "clinicpro-saas" && p.status != "parked")
  .sort(p => p.title ?? p.file.name);
for (let p of active) {
  const badge = p.status == "production" ? "🟢" : "🔵";
  const taskCount = dv.pages('"tasks/open"').where(t => t.project === p.id && t.status !== "done").length;
  const phase = p.phase ? `\n  _${p.phase}_` : "";
  dv.paragraph(`${badge} [[${p.file.name}|${p.title ?? p.file.name}]] · ${p.description ?? ""} · **${taskCount} open**${phase}`);
}
const parked = dv.pages('"projects"').where(p => p.dashboard == "clinicpro-saas" && p.status == "parked");
if (parked.length > 0) {
  dv.paragraph("💤 **Parked:** " + parked.map(p => `[[${p.file.name}|${p.title ?? p.file.name}]]`).join(" · "));
}
```

---

## Quick Links

| | |
|--|--|
| **Products** | [[ai-scribe]] · [[referral-images]] · [[12-month-prescription]] |
| **Context docs** | [Design System](context/clinicpro-context/clinicpro-design-system.md) · [Design Research](context/clinicpro-context/design-research.md) · [Colour Options](context/clinicpro-context/colour-options.md) · [Regulatory Compliance](context/clinicpro-context/regulatory-compliance.md) |
| **Repo map** | [[repos]] |
| **Finance & accounting** | Helen Yu (accountant, all entities) — see [people.md](../context/people.md#helen-yu) for scope |

---

## Weekly Progress Log

### Week of 2026-04-14

- GP profile photo regenerated (saas-20260409-008 closed): two editorial images via Nano Banana Pro with reference-image refinement — v1d (desk/office, lived-in background) replaces `DrRyoEguchiProfilePicMain.jpg` for homepage hero + all avatar uses; alt-v2a (consultation room, candid off-camera gaze) saved as `DrRyoEguchiProfilePicClinic.jpg` for FounderSection + product pages
- AI Scribe § 05 "Why I built this" redesigned: single-column text to two-column editorial layout with clinic portrait (left 2/5) and story text (right 3/5); copy edit removed "and iterate when something breaks"
- Referral Images page: founder trust strip added between § 03 "Honest about everything" and § 04 "Privacy by design"
- Full homepage visual redesign: hero staggered entrance animation, dark forest green evidence section with animated counters, bouncy FAQ accordion, signature easing applied across all marketing transitions
- `FounderSection.tsx` and `clinicpro-landing.ts` updated to reference clinic image; shared marketing primitives extracted to `src/shared/components/marketing/letter-grammar.tsx`
- `app/layout.tsx` updated: Newsreader, Caveat, JetBrains Mono loaded globally; `tailwind.config.ts` updated; `app/globals.css` `--primary` migrated to forest green

### Week of 2026-04-07

- AI Scribe landing page fully rewritten: three-pillar positioning, research citations embedded
- `scripts/gen-image.mjs` created: Nano Banana Pro image generation script
- Referral Images landing page redesigned: dark navy hero replaced with light cream editorial hero, asymmetric headline-led layout, forest green CTAs
- Colour palette decision finalised: Option 1 Native (forest green nz-green-700 + amber accent)
- ClinicPro design system created: `context/clinicpro-context/clinicpro-design-system.md`

### Week of 2026-04-06

- Referral Images launched 6 April 2026 on $5/month subscription model
- Grandfathering migration applied: 78 pre-launch users set to `grandfatheredUntil = 2027-04-06`
- Stripe checkout converted to subscription mode; paywall UI added to capture and desktop pages
- Local test environment stable: NexWave test keys + CLI; production deploy confirmed complete
