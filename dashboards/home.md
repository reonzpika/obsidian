> [!info]+
> `= dateformat(date(today), "d MMMM yyyy")` · `= link("daily/" + dateformat(date(today), "yyyy-MM-dd"), "Today's Note")` · [[clinicpro-saas|ClinicPro SaaS]] · [[clinicpro-medtech|ClinicPro Medtech]] · [[nexwave-rd|Nexwave R&D]] · [[gp-fellowship|GP Fellowship]] · [[side-projects|Side Projects]] · Partnerships
> [[dashboards/portfolio-map|🗺 Portfolio Map]] · [[#Quick Links|↓ Quick Links]]

---

### [[clinicpro-saas|ClinicPro SaaS]] · `./clinicpro-saas`
`$= dv.pages('"tasks/open"').where(t => (dv.page("projects/" + t.project)?.dashboard == "clinicpro-saas" || dv.page("sprints/active/" + t.sprint)?.dashboard == "clinicpro-saas")).length + " open"`

> [!note]- Projects & Sprints
>
> #### Projects
>
> ```dataviewjs
> const active = dv.pages('"projects"')
>   .where(p => p.dashboard == "clinicpro-saas" && p.status != "parked")
>   .sort(p => p.title ?? p.file.name);
> for (let p of active) {
>   const badge = p.status == "production" ? "🟢" : "🔵";
>   dv.paragraph(`${badge} [[${p.file.name}|${p.title ?? p.file.name}]] · ${p.description ?? ""}`);
> }
> const parked = dv.pages('"projects"')
>   .where(p => p.dashboard == "clinicpro-saas" && p.status == "parked");
> if (parked.length > 0) {
>   dv.paragraph("**Parked**");
>   for (let p of parked) {
>     dv.paragraph(`💤 [[${p.file.name}|${p.title ?? p.file.name}]] · ${p.description ?? ""}`);
>   }
> }
> ```
>
> #### Active Sprints
>
> ```dataviewjs
> const sprints = dv.pages('"sprints/active"')
>   .where(s => s.dashboard == "clinicpro-saas" && s.status == "active")
>   .sort(s => s.start, "desc");
> if (sprints.length === 0) {
>   dv.paragraph("_No active sprints._");
> } else {
>   for (let s of sprints) {
>     const n = dv.pages('"tasks/open"').where(t => t.sprint === s.id).length;
>     dv.paragraph(`[[${s.file.name}|${s.id}]] · ${s.goal ?? ""} · **${n} open**`);
>   }
> }
> ```

### [[clinicpro-medtech|ClinicPro Medtech]] · `./clinicpro-medtech`
`$= dv.pages('"tasks/open"').where(t => (dv.page("projects/" + t.project)?.dashboard == "clinicpro-medtech" || dv.page("sprints/active/" + t.sprint)?.dashboard == "clinicpro-medtech")).length + " open"`

> [!note]- Projects & Sprints
>
> #### Projects
>
> ```dataviewjs
> const active = dv.pages('"projects"')
>   .where(p => p.dashboard == "clinicpro-medtech" && p.status != "parked")
>   .sort(p => p.title ?? p.file.name);
> for (let p of active) {
>   const badge = p.status == "production" ? "🟢" : "🔵";
>   dv.paragraph(`${badge} [[${p.file.name}|${p.title ?? p.file.name}]] · ${p.description ?? ""}`);
> }
> const parked = dv.pages('"projects"')
>   .where(p => p.dashboard == "clinicpro-medtech" && p.status == "parked");
> if (parked.length > 0) {
>   dv.paragraph("**Parked**");
>   for (let p of parked) {
>     dv.paragraph(`💤 [[${p.file.name}|${p.title ?? p.file.name}]] · ${p.description ?? ""}`);
>   }
> }
> ```
>
> #### Active Sprints
>
> ```dataviewjs
> const sprints = dv.pages('"sprints/active"')
>   .where(s => s.dashboard == "clinicpro-medtech" && s.status == "active")
>   .sort(s => s.start, "desc");
> if (sprints.length === 0) {
>   dv.paragraph("_No active sprints._");
> } else {
>   for (let s of sprints) {
>     const n = dv.pages('"tasks/open"').where(t => t.sprint === s.id).length;
>     dv.paragraph(`[[${s.file.name}|${s.id}]] · ${s.goal ?? ""} · **${n} open**`);
>   }
> }
> ```

### [[nexwave-rd|Nexwave R&D]] · `./nexwave-rd`
`$= dv.pages('"tasks/open"').where(t => (dv.page("projects/" + t.project)?.dashboard == "nexwave-rd" || dv.page("sprints/active/" + t.sprint)?.dashboard == "nexwave-rd")).length + " open"`

> [!note]- Projects & Sprints
>
> #### Projects
>
> ```dataviewjs
> const active = dv.pages('"projects"')
>   .where(p => p.dashboard == "nexwave-rd" && p.status != "parked")
>   .sort(p => p.title ?? p.file.name);
> for (let p of active) {
>   const badge = p.status == "production" ? "🟢" : "🔵";
>   dv.paragraph(`${badge} [[${p.file.name}|${p.title ?? p.file.name}]] · ${p.description ?? ""}`);
> }
> const parked = dv.pages('"projects"')
>   .where(p => p.dashboard == "nexwave-rd" && p.status == "parked");
> if (parked.length > 0) {
>   dv.paragraph("**Parked**");
>   for (let p of parked) {
>     dv.paragraph(`💤 [[${p.file.name}|${p.title ?? p.file.name}]] · ${p.description ?? ""}`);
>   }
> }
> ```
>
> #### Active Sprints
>
> ```dataviewjs
> const sprints = dv.pages('"sprints/active"')
>   .where(s => s.dashboard == "nexwave-rd" && s.status == "active")
>   .sort(s => s.start, "desc");
> if (sprints.length === 0) {
>   dv.paragraph("_No active sprints._");
> } else {
>   for (let s of sprints) {
>     const n = dv.pages('"tasks/open"').where(t => t.sprint === s.id).length;
>     dv.paragraph(`[[${s.file.name}|${s.id}]] · ${s.goal ?? ""} · **${n} open**`);
>   }
> }
> ```

### [[gp-fellowship|GP Fellowship]]
`$= dv.pages('"tasks/open"').where(t => (dv.page("projects/" + t.project)?.dashboard == "gp-fellowship" || dv.page("sprints/active/" + t.sprint)?.dashboard == "gp-fellowship")).length + " open"`

> [!note]- Projects & Sprints
>
> #### Projects
>
> ```dataviewjs
> const active = dv.pages('"projects"')
>   .where(p => p.dashboard == "gp-fellowship" && p.status != "parked")
>   .sort(p => p.title ?? p.file.name);
> for (let p of active) {
>   const badge = p.status == "production" ? "🟢" : "🔵";
>   dv.paragraph(`${badge} [[${p.file.name}|${p.title ?? p.file.name}]] · ${p.description ?? ""}`);
> }
> const parked = dv.pages('"projects"')
>   .where(p => p.dashboard == "gp-fellowship" && p.status == "parked");
> if (parked.length > 0) {
>   dv.paragraph("**Parked**");
>   for (let p of parked) {
>     dv.paragraph(`💤 [[${p.file.name}|${p.title ?? p.file.name}]] · ${p.description ?? ""}`);
>   }
> }
> ```
>
> #### Active Sprints
>
> ```dataviewjs
> const sprints = dv.pages('"sprints/active"')
>   .where(s => s.dashboard == "gp-fellowship" && s.status == "active")
>   .sort(s => s.start, "desc");
> if (sprints.length === 0) {
>   dv.paragraph("_No active sprints._");
> } else {
>   for (let s of sprints) {
>     const n = dv.pages('"tasks/open"').where(t => t.sprint === s.id).length;
>     dv.paragraph(`[[${s.file.name}|${s.id}]] · ${s.goal ?? ""} · **${n} open**`);
>   }
> }
> ```

### [[side-projects|Side Projects]]
`$= dv.pages('"tasks/open"').where(t => (dv.page("projects/" + t.project)?.dashboard == "side-projects" || dv.page("sprints/active/" + t.sprint)?.dashboard == "side-projects")).length + " open"`

> [!note]- Projects & Sprints
>
> #### Projects
>
> ```dataviewjs
> const active = dv.pages('"projects"')
>   .where(p => p.dashboard == "side-projects" && p.status != "parked")
>   .sort(p => p.title ?? p.file.name);
> for (let p of active) {
>   const badge = p.status == "production" ? "🟢" : "🔵";
>   dv.paragraph(`${badge} [[${p.file.name}|${p.title ?? p.file.name}]] · ${p.description ?? ""}`);
> }
> const parked = dv.pages('"projects"')
>   .where(p => p.dashboard == "side-projects" && p.status == "parked");
> if (parked.length > 0) {
>   dv.paragraph("**Parked**");
>   for (let p of parked) {
>     dv.paragraph(`💤 [[${p.file.name}|${p.title ?? p.file.name}]] · ${p.description ?? ""}`);
>   }
> }
> ```
>
> #### Active Sprints
>
> ```dataviewjs
> const sprints = dv.pages('"sprints/active"')
>   .where(s => s.dashboard == "side-projects" && s.status == "active")
>   .sort(s => s.start, "desc");
> if (sprints.length === 0) {
>   dv.paragraph("_No active sprints._");
> } else {
>   for (let s of sprints) {
>     const n = dv.pages('"tasks/open"').where(t => t.sprint === s.id).length;
>     dv.paragraph(`[[${s.file.name}|${s.id}]] · ${s.goal ?? ""} · **${n} open**`);
>   }
> }
> ```

### Partnerships
`$= dv.pages('"tasks/open"').where(t => (dv.page("projects/" + t.project)?.dashboard == "partnerships" || dv.page("sprints/active/" + t.sprint)?.dashboard == "partnerships")).length + " open"`

> [!note]- Projects & Sprints
>
> #### Projects
>
> ```dataviewjs
> const active = dv.pages('"projects"')
>   .where(p => p.dashboard == "partnerships" && p.status != "parked")
>   .sort(p => p.title ?? p.file.name);
> for (let p of active) {
>   const badge = p.status == "production" ? "🟢" : "🔵";
>   dv.paragraph(`${badge} [[${p.file.name}|${p.title ?? p.file.name}]] · ${p.description ?? ""}`);
> }
> const parked = dv.pages('"projects"')
>   .where(p => p.dashboard == "partnerships" && p.status == "parked");
> if (parked.length > 0) {
>   dv.paragraph("**Parked**");
>   for (let p of parked) {
>     dv.paragraph(`💤 [[${p.file.name}|${p.title ?? p.file.name}]] · ${p.description ?? ""}`);
>   }
> }
> ```
>
> #### Active Sprints
>
> ```dataviewjs
> const sprints = dv.pages('"sprints/active"')
>   .where(s => s.dashboard == "partnerships" && s.status == "active")
>   .sort(s => s.start, "desc");
> if (sprints.length === 0) {
>   dv.paragraph("_No active sprints._");
> } else {
>   for (let s of sprints) {
>     const n = dv.pages('"tasks/open"').where(t => t.sprint === s.id).length;
>     dv.paragraph(`[[${s.file.name}|${s.id}]] · ${s.goal ?? ""} · **${n} open**`);
>   }
> }
> ```

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
