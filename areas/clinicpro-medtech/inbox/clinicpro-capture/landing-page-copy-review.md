---
title: Capture landing page copy review
created: 2026-04-25
---

All output is a first draft for human review. No section should be treated as final without Ryo's explicit sign-off.

---

## Source material used

- Landing page source: `app/(marketing)/medtech/_components/` (nine component files read in full)
- Champion email: `docs/marketing/phase-1/champion-email-v1.md`
- Project file: `obsidian/projects/clinicpro-capture.md`
- Phase 1 plan: `docs/superpowers/plans/2026-04-15-capture-marketing-phase1.md`

**URL note:** The live landing page route is `capture.clinicpro.co.nz/medtech` (or `capture.clinicpro.co.nz` depending on routing config). The plan specifies `/medtech/capture` but the built components live at `app/(marketing)/medtech/`. Verify the deployed URL matches what the champion email footer cites (`capture.clinicpro.co.nz`).

---

## Consistency issues

| Claim | Landing page | Champion email | Verdict |
|---|---|---|---|
| Product name | "ClinicPro Capture" throughout | "ClinicPro Capture" | Consistent |
| Core mechanism | "commits photos from your phone straight to the patient's Medtech record" | "Look up the patient by NHI, take the photo, tap upload. It lands directly in their Medtech Inbox Scan via the ALEX API" | Consistent in substance; landing page omits "NHI lookup" from the hero |
| Setup time / simplicity | "No install. Phone browser." implied via How it works | "Phone browser, no install" explicit | Consistent |
| Medtech variants | "Works whether your Medtech is on-premise or cloud" in hero; full list in pricing inclusions | Not stated in email | No conflict; email doesn't need it |
| Champion offer: "3 months free" | NOT present anywhere on the landing page | "3 months of Capture, on me" — explicit offer | **Gap: email makes a specific offer that the landing page does not mention.** If a champion's practice manager clicks through after receiving the email, they will see no reference to the offer. They may doubt the email is legitimate, or feel the offer has vanished. |
| CTA mechanism | "Book a 15-minute demo" via mailto to ryo@clinicpro.co.nz | "Reply with your PM's name and email" — reply-based, not mailto | Different paths. Not a conflict for v1 (email is GP-to-GP; page is for PMs). But the PM experience if they click the URL is: land on page, see "Book a demo", open an email client. The email did not mention a mailto link. No active conflict, but the handoff is not smooth. |
| Pricing | Annual per practice, NZ$299/$799/$1,500/contact; pricing visible on page | Not mentioned in email | No conflict. Email correctly avoids pricing; page carries it. |
| Audience signal | "For Medtech Evolution practices" (header); "For Medtech Evolution practices" (eyebrow) | Explicitly for Medtech practices who use referral-images | Consistent |
| ALEX API mention | Named in HowItWorks ("Capture queries Medtech via the ALEX API"); in MedtechBadge | Named in email ("ALEX API") | Consistent. Email notes this may be too technical for some readers. Same caveat applies to the landing page. |
| Founder identity | "Dr. Ryo Eguchi" with photo and credentials | "Ryo" signed as "Dr Ryo Eguchi, MBChB, FRNZCGP" | Minor inconsistency: landing page uses "Dr. Ryo Eguchi" (with period) and email uses "Dr Ryo Eguchi" (without). Standardise. |
| Trust line | "Built by a practising NZ GP. ALEX API integration. Medtech partnership agreement." | "I'm trialling it with a small group of NZ practices before the Medtech partnership goes live" | Both reference the Medtech partnership as not-yet-final. Consistent in substance. |
| Phase / soft-launch positioning | Page reads as generally available (no soft-launch framing) | "Small group of NZ practices... before the Medtech partnership goes live" signals exclusivity | Framing mismatch. Email implies a privileged early-access position. Landing page looks like a regular commercial product page. A PM who clicks through from the email loses the "you're early" framing entirely. |

---

## Copy improvements

| Section | Original | Suggested | Why |
|---|---|---|---|
| Hero H1 | "The Medtech Evolution Capture problem. / Solved." | "Clinical photos into Medtech. No desktop. No camera roll." | Original headline names the solution category ("Capture") before explaining the problem. Readers who don't already know the problem may not connect. The suggested version states the outcome in one sentence and implies the problem. Also: original is 9 words across two lines; suggested is 10 words but reads as one complete claim. |
| Hero H1 (alternative if keeping problem framing) | "The Medtech Evolution Capture problem. / Solved." | "Every Medtech practice has the same photo problem. / Capture solves it." | This was the locked copy from the Phase 1 plan (2026-04-15 conversation). The built headline diverged from it. Revert if design intent is to lead with the problem. |
| Hero subheadline | "ClinicPro Capture commits photos from your phone straight to the patient's Medtech record. Right size, right format, right folder. No manual resize. No rejected referrals. Works whether your Medtech is on-premise or cloud." | No major rewrite needed. Consider adding "No install." as a fourth micro-claim after "No rejected referrals." to address the friction question immediately. | "No install" appears in the How It Works section but not the hero. GPs and PMs will ask "does this need IT?" before they scroll. |
| Hero trust line | "Built by a practising NZ GP. ALEX API integration. Medtech partnership agreement." | "Built by a practising NZ GP. ALEX API integration. Medtech partnership agreement in final stages." | The phase 1 plan locked the phrase as "in final stages." The built version drops those words. Omitting them makes the line read as if the partnership is complete when it is not. Regulatory accuracy matters here. |
| PainFix row 2 fix body | "Referral-ready format. Accepted by every NZ referral system." | "Referral-ready TIFF format. Accepted by HealthLink, ERMS, and ALEX SR." | "Every NZ referral system" is a strong universal claim that could be challenged. The named systems (HealthLink, ERMS, ALEX SR) are specific and defensible. Also aligns with the row 3 fix body which already names these systems. |
| PainFix row 2 fix body (format claim detail) | "Referral-ready format." | "Converted to the format HealthLink and ERMS require." | The plan specifies "JPEG-in-TIFF" as the output format. The landing page drops this specificity. Technical readers (PHO IT leads, practice managers with IT backgrounds) will ask "what format?" Naming it is more credible than an abstract claim. |
| TrustSection compliance callout | "Built by a practising NZ GP. Built to meet the rules that govern clinical software in New Zealand. HIPC 2020. Privacy Act 2020 s11. HISO 10029." | No rewrite needed for NZ. **For AU:** replace "in New Zealand" with "in New Zealand and Australia" and add "Australian Privacy Act 1988" to the list. | The page currently names NZ-only frameworks. AU practices will not see their regulatory context reflected. |
| TrustSection card: "HIPC and Privacy Act compliance" | "ClinicPro acts as agent of your practice under Privacy Act 2020 s11." | No change for NZ. **For AU:** add a parallel sentence for the Australian Privacy Act 1988, APP 11 (data security obligations) and the Notifiable Data Breaches scheme. | NZ-only framing currently. |
| HowItWorks step 2 | "Look up the patient by NHI." | "Look up the patient. Search by NHI or name." | NHI is a NZ-specific identifier. AU uses Medicare/IHI. The current copy will be confusing to AU users. Even within NZ, adding "or name" widens perceived accessibility. |
| HowItWorks step 2 note | "Live patient lookup, no double-entry." | Keep. | Strong benefit claim. Accurate. |
| PricingSection inclusions item 7 | "Photos never saved to the phone camera roll." | "Photos never saved to the phone. Camera roll, iCloud, and Google Photos stay clean." | More specific. Addresses both iOS and Android storage vectors. Aligns with the TrustSection card wording. |
| PricingSection inclusions item 3 | "Guided onboarding and ALEX connection." | "Guided setup included. We connect to your Medtech ALEX facility on the onboarding call." | "Guided onboarding and ALEX connection" is abstract. The improved version explains what it means in practice: a call where the ALEX connection is established. This is a genuine selling point (removes IT burden from the practice) and should be stated explicitly. |
| PricingSection: no concierge trial line | (absent) | Add below inclusions: "Running a trial? Email ryo@clinicpro.co.nz. We set it up directly with your team so it's wired correctly before you evaluate." | The phase 1 plan specifies a concierge trial line. It is missing from the built PricingSection. No self-serve trial exists; PMs who want to trial need to know how. Without this line, the only path is "Book a demo" which may undersell the trial option. |
| FAQSection Q7 | "Is there a free trial?" answer is absent from the built FAQ (the plan specified it, the built FAQ omits it) | Add: "Yes. Email ryo@clinicpro.co.nz to arrange one. Trials are set up with you directly on a Zoom so everything is connected correctly before you evaluate." | The built FAQ has no trial question. The plan specified it as Q7. Its absence leaves PMs without an obvious answer to the most common objection. |
| FinalCTASection sign-off | "Yours, / Ryo Eguchi. / Built in Auckland, NZ. NexWave Solutions Limited." | Keep for NZ. For AU: add "(serving NZ and AU)" or a separate AU-specific footer variant. | Footer currently anchors to Auckland/NZ. For AU practices this reads as a foreign vendor. |
| DEMO_MAILTO subject | `Capture%20demo%20%E2%80%94%20%5Bpractice%20name%5D` (contains an em dash via %E2%80%94) | `Capture%20demo%20%3A%20%5Bpractice%20name%5D` (colon instead) | The global formatting rule prohibits em dashes. The mailto subject line encodes an em dash. Replace with a colon. |

---

## Missing elements

- **Champion offer on the landing page.** The email offers 3 months free. A PM who clicks through sees no trace of this offer. Either add a soft-launch/champion banner (e.g. "If you were referred by a ClinicPro GP, ask us about our champion offer") or add a `/champion` path that carries the offer. Without this, the email-to-landing-page funnel has a dead drop.
- **Concierge trial copy in PricingSection.** The plan specified a plain-text trial line beneath the inclusions. It was not built. PMs currently have no path to trial without "Book a demo", which undersells the trial.
- **FAQ Q7 (free trial).** Missing from built FAQ. Specified in the plan.
- **Social proof / testimonials.** The SoundFamiliarSection uses two community quotes from the GPs for GPs Facebook group (problem validation), not product testimonials. There are no customer quotes from actual Capture users because there are no paying customers yet. This is expected pre-launch. The case-study template (Task 5) addresses this. Flag: the page needs at least one testimonial before champion email results start landing, or the social proof section will remain purely problem-validation rather than solution-validation.
- **Loom embed.** The `loom-embed-slot` div in HeroSection is blank (expected: Task 5 not yet complete). The hero right column currently renders an empty 16:9 box. Before sending the champion email, this must be filled or the empty box will look like a broken page.
- **AU-specific pricing.** Pricing is in NZ$. AU practices need AU$ pricing or at minimum a note that AU pricing is available on request. The AU white-label deployment plan (Lawrence Peterson) implies separate pricing will apply, but this is not reflected on the page.
- **Privacy policy / terms link.** The TrustSection makes strong compliance claims (Privacy Act 2020 s11, HIPC 2020, HISO 10029, Data Processing Agreement per practice). There is no link to a privacy policy or DPA request path. A PHO IT lead evaluating the product will ask for these before approving. Add "Privacy policy" and "Request a DPA" links to the footer.
- **"Medtech partnership agreement" status.** The trust line says "Medtech partnership agreement" (omitting "in final stages" per the lock). The plan and the email both note it is not yet signed. Until it is signed, the copy must reflect the pre-signed state. This is a compliance and credibility risk if misread as "signed partnership".

---

## AU-readiness notes

- **NHI (NZ-specific identifier).** HowItWorks step 2 says "Look up the patient by NHI." NHI is the NZ National Health Index. AU uses Medicare number and/or IHI (Individual Healthcare Identifier). For AU, this step copy must change or the lookup must support AU identifiers. Mark as an engineering dependency, not just a copy change.
- **Regulatory frameworks.** TrustSection names HIPC 2020, Privacy Act 2020 s11, and HISO 10029. These are NZ-only. AU equivalents: Australian Privacy Act 1988 (APPs, particularly APP 11), Notifiable Data Breaches scheme, My Health Records Act 2012 (if any MHR integration is contemplated). Add AU frameworks for the AU white-label deployment.
- **Currency.** All prices shown in NZ$. AU white-label will need AU$ pricing. The current page has no currency-switching mechanism.
- **"Enrolled patients" pricing metric.** PHO enrolled patient count is a NZ primary care concept tied to the NZ PHO model. AU general practice does not use the same enrolled-patient metric. AU pricing may need a different base metric (e.g. full-time GP equivalent, or practice size band). This is a commercial decision, not just copy. Flag to Lawrence Peterson.
- **"Inbox Scan" terminology.** Inbox Scan is a Medtech Evolution concept. It will be meaningful to AU Medtech practices. No change needed if the AU product is Medtech-only. Confirm that the AU bundle (Lawrence Peterson) is Medtech Evolution, not a different PMS.
- **Auckland location signals.** The hero marginalia ("Auckland, NZ"), the FounderSection byline ("Auckland, NZ"), and the FinalCTASection footer ("Built in Auckland, NZ") all anchor the product to NZ. These are fine for NZ marketing. For AU white-label, remove or neutralise Auckland references so the product reads as regionally appropriate.
- **Spelling.** The page uses "programme" (zero instances found) and "organisation" (zero instances found) — spelling appears neutral/abbreviated in current copy (e.g. "practising" is correct NZ/AU spelling). No AU-specific spell check issues found. Verify full rendered page before AU launch.
- **"NZ GP" in founder attribution.** FounderSection byline: "Practising GP & Founder. Auckland, NZ." For AU white-label, replace with a neutral description or omit the geographic anchor.

---

## Assumptions

1. **The live deployed URL is `capture.clinicpro.co.nz/medtech`.** The Vercel project for `capture.clinicpro.co.nz` serves the `clinicpro-medtech` repo, and the landing page is the `(marketing)/medtech/page.tsx` component. The champion email footer cites `capture.clinicpro.co.nz` with no path. **Could not verify the exact routing config without checking Vercel or `next.config.ts` redirects.** If the URL is `capture.clinicpro.co.nz/medtech`, the email footer link may need a path appended.

2. **`app/(marketing)/medtech/page.tsx` contained workspace notes, not the live page scaffold.** The component files in `_components/` are the actual page content and were treated as the source of truth for this review. The `page.tsx` file showed "obsidian claude.md" notes, which appear to be an accidental save. Verify `page.tsx` imports and mounts the components correctly before treating the page as live.

3. **No live URL access.** This review is based entirely on source code. Some presentation issues (spacing, motion, responsive layout) can only be verified by viewing the rendered page. CTA click paths (mailto open, anchor scroll) were assessed from code logic, not live interaction.

4. **"Medtech partnership agreement" is not yet signed.** This is explicitly stated in the project file and the phase 1 plan. The trust line on the landing page omits "in final stages." This review treats the un-signed state as current and flags the omission as a risk.

5. **No paying Capture customers exist at time of this review.** Social proof analysis is based on this assumption. If any early practices are live, their quotes should be prioritised for the SoundFamiliarSection or a new testimonial section.
