> [!info]+
> `= dateformat(date(today), "d MMMM yyyy")` · `= link("daily/" + dateformat(date(today), "yyyy-MM-dd"), "Today's Note")` · [[dashboards/portfolio-map|🗺 Portfolio Map]] · [[#Quick Links|↓ Quick Links]]
>
> [[clinicpro-saas|ClinicPro SaaS]] · [[clinicpro-medtech|ClinicPro Medtech]] · [[nexwave-rd|Nexwave R&D]] · [[other-projects|Other Projects]] · Partnerships

---

### [[clinicpro-saas|ClinicPro SaaS]]

```dataviewjs
const active = dv.pages('"projects"')
  .where(p => p.dashboard == "clinicpro-saas" && p.status != "parked")
  .sort(p => p.title ?? p.file.name);
for (let p of active) {
  const badge = p.status == "production" ? "🟢" : "🔵";
  const phase = p.phase ? ` · _${p.phase}_` : "";
  dv.paragraph(`${badge} [[${p.file.name}|${p.title ?? p.file.name}]] · ${p.description ?? ""}${phase}`);
}
const parked = dv.pages('"projects"').where(p => p.dashboard == "clinicpro-saas" && p.status == "parked");
if (parked.length > 0) {
  dv.paragraph("💤 **Parked:** " + parked.map(p => `[[${p.file.name}|${p.title ?? p.file.name}]]`).join(" · "));
}
```

### [[clinicpro-medtech|ClinicPro Medtech]]

```dataviewjs
const active = dv.pages('"projects"')
  .where(p => p.dashboard == "clinicpro-medtech" && p.status != "parked")
  .sort(p => p.title ?? p.file.name);
for (let p of active) {
  const badge = p.status == "production" ? "🟢" : "🔵";
  const phase = p.phase ? ` · _${p.phase}_` : "";
  dv.paragraph(`${badge} [[${p.file.name}|${p.title ?? p.file.name}]] · ${p.description ?? ""}${phase}`);
}
const parked = dv.pages('"projects"').where(p => p.dashboard == "clinicpro-medtech" && p.status == "parked");
if (parked.length > 0) {
  dv.paragraph("💤 **Parked:** " + parked.map(p => `[[${p.file.name}|${p.title ?? p.file.name}]]`).join(" · "));
}
```

### [[nexwave-rd|Nexwave R&D]]

```dataviewjs
const active = dv.pages('"projects"')
  .where(p => p.dashboard == "nexwave-rd" && p.status != "parked")
  .sort(p => p.title ?? p.file.name);
for (let p of active) {
  const badge = p.status == "production" ? "🟢" : "🔵";
  const phase = p.phase ? ` · _${p.phase}_` : "";
  dv.paragraph(`${badge} [[${p.file.name}|${p.title ?? p.file.name}]] · ${p.description ?? ""}${phase}`);
}
```

### [[other-projects|Other Projects]]

```dataviewjs
const active = dv.pages('"projects"')
  .where(p => p.dashboard == "other-projects" && p.status != "parked")
  .sort(p => p.title ?? p.file.name);
for (let p of active) {
  const badge = p.status == "production" ? "🟢" : "🔵";
  const phase = p.phase ? ` · _${p.phase}_` : "";
  dv.paragraph(`${badge} [[${p.file.name}|${p.title ?? p.file.name}]] · ${p.description ?? ""}${phase}`);
}
const parked = dv.pages('"projects"').where(p => p.dashboard == "other-projects" && p.status == "parked");
if (parked.length > 0) {
  dv.paragraph("💤 **Parked:** " + parked.map(p => `[[${p.file.name}|${p.title ?? p.file.name}]]`).join(" · "));
}
```

### Partnerships

```dataviewjs
const active = dv.pages('"projects"')
  .where(p => p.dashboard == "partnerships" && p.status != "parked")
  .sort(p => p.title ?? p.file.name);
for (let p of active) {
  const badge = p.status == "production" ? "🟢" : "🔵";
  const phase = p.phase ? ` · _${p.phase}_` : "";
  dv.paragraph(`${badge} [[${p.file.name}|${p.title ?? p.file.name}]] · ${p.description ?? ""}${phase}`);
}
```

---

## Reviews

```dataviewjs
const weekly = dv.pages('"reviews/weekly"').sort(p => p.file.name, 'desc').slice(0, 4);
const monthly = dv.pages('"reviews/monthly"').sort(p => p.file.name, 'desc').slice(0, 2);
if (weekly.length > 0)
  dv.paragraph("**Weekly:** " + weekly.map(p => `[[reviews/weekly/${p.file.name}|${p.title ?? p.file.name}]]`).join(" · "));
if (monthly.length > 0)
  dv.paragraph("**Monthly:** " + monthly.map(p => `[[reviews/monthly/${p.file.name}|${p.title ?? p.file.name}]]`).join(" · "));
```

---

## Quick Links

**Dev**
- [GitHub](https://github.com/reonzpika?tab=repositories)
- [Cursor Dashboard](https://cursor.com/dashboard)
- [OpenAI Usage](https://platform.openai.com/settings/organization/usage)
- [Domains Direct](https://secure.domainsdirect.nz/?login)
- [Vercel](https://vercel.com/nexwave-solutions-projects)
- [Neon DB](https://console.neon.tech)
- [Stripe](https://dashboard.stripe.com/)
- [Clerk](https://dashboard.clerk.com/apps)

**AI**
- [Claude](https://claude.ai/settings/general)
- [NotebookLM](https://notebooklm.google.com/notebook)
- [Perplexity](https://www.perplexity.ai/)
- [Yingtu](https://yingtu.ai/en)
- [Laozhang API](https://api.laozhang.ai/token)

**Google**
- [Calendar](https://calendar.google.com/calendar/u/0/r)
- [Gmail](https://mail.google.com/mail/u/0/#inbox)
- [Drive](https://drive.google.com/drive/u/0/home)
