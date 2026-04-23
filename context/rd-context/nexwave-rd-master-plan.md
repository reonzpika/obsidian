---
title: "NexWave R&D Master Plan"
type: reference
project: nexwave-rd
created: 2026-04-23
updated: 2026-04-23
---

# NexWave R&D — Master Plan
_Last updated: 23 April 2026_

---

## Programme at a Glance

- **What:** NexWave Health builds AI tools for NZ general practice — Inbox Helper (inbox triage) and Care Gap Finder (patient population scanning). AI assists only; GP decides everything.
- **Funded by:** MBIE R&D grant CONT-109091-N2RD-NSIWKC. Total Obj 1 budget: $177,396. Compliance budget: $18,000 (Feb 2026–Jul 2027).
- **Obj 1 deliverable deadline:** End of June 2026. Architecture selected, synthetic data evaluated, accuracy targets hit.
- **Q1 MBIE claim deadline:** 31 May 2026. Internal labour costs claimable only after PAYE condition confirmed approved in Forge.
- **Architecture decision:** C3 primary (rules engine + BioClinical ModernBERT 396M / Llama 3.1 8B LoRA hybrid); C1 (Bedrock Claude Haiku 4.5 / Sonnet 4.6) as parallel reference for Sprint 3 bake-off.

---

## Where We Are — 23 April 2026

### Objective 1: Foundation AI Architecture

| Step | Name | Status | Notes |
|------|------|--------|-------|
| 1 | Define the problems | Complete (5 Apr) | Inbox Helper and Care Gap Finder specs finalised and filed. GP review underway — 1 reviewer done (Nick Buist), 1-2 more needed before spec synthesis. |
| 2 | Literature review and architecture research | Complete (14 Apr) | Seven research reports (r1–r7) and sprint-2-summary filed. Key finding: fine-tuned 8B beats zero-shot 120B at 300–500-item scale; CoT degrades 86% of clinical LLMs. |
| 3 | Shortlist architecture candidates | Complete (14 Apr) | Four candidates evaluated. Decision: C3 primary, C1 parallel reference. Data requirements and synthetic dataset schema v0.1 (provisional) filed. |
| 4 | Evaluate candidates on synthetic data | Not started | Requires synthetic dataset (400 items) to exist first. Blocked until dataset generated. Sprint 3 bake-off window: 26 Apr–9 May. |
| 5 | Make the architecture decision | Not started | Follows Step 4 bake-off results. Document for MBIE must include evidence from Step 4, sovereignty rationale, and data requirements for real GP data. |

### Compliance Track

- **Bell Gully (Laura Hardcastle):** Proposal received 16 Apr. Phase 1: $2,500–$4,000 + GST (SaMD classification under current law + Medical Products Bill pipeline). Three AI-output questions answered and drafted; reply pending Ryo sign-off (rd-20260420-002). Decision due 27 Apr.
- **Buddle Findlay (Catherine Miller):** Proposal received 17 Apr. $9,000–$12,000 + GST + 3.5% (full 5-area compliance overview). On hold pending Elevate Medtech quote and Bell Gully decision.
- **Elevate Medtech (Anne Arndt):** Away until 29 Apr. Re-engage with scoped brief on return. Provides SaMD technical pathway advice (IEC 62304, ISO 13485) — complements legal advice, does not replace it.
- **Aesculytics (Dr Arindam Bose):** No response after 5+ days. Deprioritised.

### Programme Admin

| Item | Status |
|------|--------|
| PAYE evidence | Submitted to Forge portal 20 Apr. Awaiting confirmation of approval before Q1 claim proceeds. |
| Ting employment contract | Hourly rate corrected to $58.33/hr in Google Doc (15 Apr). Re-signature from Ting still pending. PAYE submission blocked until signed. |
| Ryo employment contract | Annual salary figure in contract ($140,160/yr) does not match payroll rate ($124,800/yr). Helen to issue corrected version — task rd-20260420-004, due 14 May. |
| R&D bank account | Not yet opened. Due 15 May. Required so Helen can segregate R&D spend in Xero for MBIE cost reports. |
| Q1 claim records | Lisa Pritchard (MBIE) replied 19 Apr with guidance: any time-tracking format accepted; claim submitted via Forge portal. Template received. Records not yet set up — task rd-20260421-001, due 14 May. |
| GST invoice template | Not yet set up (rd-20260329-013, overdue). Required for MBIE quarterly claims. |

### Blockers (right now)

- **Indici sandbox silent.** Valentia has not responded to 5+ contact attempts since 4 Apr across LinkedIn, email, and web form. Phone escalation to NZ office (07 929 2090) was planned by 17 Apr — status unclear. Goal A (sandbox environments connected) is a named Obj 1 deliverable and is at risk. May need proactive flag to Lisa Pritchard at MBIE.
- **GP reviewer count below threshold.** 1 review done (Nick Buist, 21 Apr). Need at least 1 more (target 2–3) before rd-20260421-003 (spec synthesis) can proceed. Gareth Roberts (Comprehensive Care PHO) outreach sent 9 Apr, no response. Heidi Bubendorfer (RNZCGP) is the next escalation channel — not yet activated.
- **Bell Gully decision pending.** Three AI-output questions answered but not yet sent. Decision required by 27 Apr. Delay pushes compliance engagement into May and risks missing the sprint window before the Q1 MBIE narrative is written.
- **Ting contract re-signature outstanding.** PAYE submission is technically in Forge but contract discrepancy (Ting's rate: $58.33/hr vs stated $102,194/yr salary) must be resolved before the Q1 claim is defensible at audit.
- **Synthetic dataset not started.** Schema is at v0.1 provisional (pending GP review). Core question unresolved: generate now with Nick's findings baked in, or wait for second review? Sprint 3 bake-off starts 26 Apr — dataset must exist by then to hit the 23 May accuracy testing deadline.

---

## The Next 6 Weeks (23 Apr – 31 May 2026)

**Week of 23 April (Sprint 2 close)**
- Ryo (Thu–Sun): Send Bell Gully response (rd-20260420-002, due 27 Apr). Log Nick Buist findings in nexwave-rd dashboard (rd-20260420-003). Review Lisa MBIE Q1 claim guidance (rd-20260421-001). Decide on synthetic dataset timing.
- Ting (weekdays): Phone Valentia NZ office to escalate Indici sandbox access. Begin synthetic dataset generation if Ryo gives go-ahead on provisional schema.
- Milestone: R&D Sprint 2 ends 25 Apr. Bell Gully holding reply due 27 Apr.

**Week of 28 April (Sprint 3 opens)**
- Ryo (weekend): Escalate GP reviewer outreach to Heidi Bubendorfer (RNZCGP) if no second reviewer confirmed. Re-engage Elevate Medtech (Anne Arndt back 29 Apr) with scoped brief. Make compliance engagement decision (Bell Gully + Elevate Medtech in parallel, or sequence).
- Ting (weekdays): Continue synthetic dataset generation (rd-20260329-023). Target 400-item corpus with 14 QA gates passing. Begin Medtech sandbox documentation (rd-20260329-021).
- Milestone: Elevate Medtech quote expected by end of week. Compliance engagement decision by 30 Apr.

**Week of 5 May**
- Ryo (weekend): Synthesise GP review findings once second reviewer done (rd-20260421-003). Update Inbox Helper and Care Gap Finder specs. Research PHO/capitation funding-linked care gaps (Nick Buist finding — confirm scope before finalising Care Gap Finder spec).
- Ting (weekdays): Run Sprint 3 architecture bake-off on synthetic dataset. Test C3 (rules engine + ModernBERT/Llama 3.1 8B) and C1 (Bedrock Claude Haiku 4.5/Sonnet 4.6 reference) against the 400-item corpus. Log all results.
- Milestone: Synthetic dataset complete (target end of this week). Bake-off running.

**Week of 12 May**
- Ryo (weekend): Set up Q1 timesheets for Ryo and Ting (12 Mar–31 Mar 2026) using Lisa's Forge template (rd-20260421-001, due 14 May). Email Helen to issue corrected employment contracts for both Ryo and Ting (rd-20260420-004, due 14 May). Open R&D bank account and notify Helen (rd-20260419-001, due 15 May).
- Ting (weekdays): Finish bake-off runs. Triage accuracy testing on synthetic dataset — target ≥90% (rd-20260329-025). CVDRA prototype accuracy testing — target ≥95% (rd-20260329-024). Log all experiment results.
- Milestone: R&D accuracy testing sprint ends 23 May. Employment contract fix due 14 May. R&D bank account due 15 May.

**Week of 19 May**
- Ryo (weekend): Draft architecture decision document for MBIE (Step 5). Incorporate bake-off results, sovereignty rationale, and data requirements for Obj 2. Confirm PAYE condition approved in Forge.
- Ting (weekdays): Support architecture decision write-up with experiment logs. Confirm all Q1 MBIE claim records are complete and accurate.
- Milestone: Accuracy testing sprint ends 23 May. Architecture decision draft complete by end of week.

**Week of 26 May (claim week)**
- Ryo (weekend): Review and finalise Q1 MBIE claim submission. Confirm all deliverable documents are filed in nexwave-rd/docs/. Set up GST invoice template if not done (rd-20260329-013).
- Ting (weekdays): Compile Q1 time records and cost documentation. Submit Q1 grant claim via Forge portal (rd-20260329-026).
- Milestone: Q1 MBIE claim submitted by 31 May 2026.

---

## To June 2026 — The Big Picture

### What Objective 1 requires to be "done"

| Deliverable | What gets it there |
|-------------|-------------------|
| Medtech and Indici sandbox environments connected | Medtech ALEX FHIR access is in progress. Indici (Valentia) requires phone escalation — currently at risk. |
| Architecture selected with documented evidence | Sprint 3 bake-off results feed directly into the Step 5 decision document. Must include sovereignty analysis and accuracy data. |
| Data requirements documented | Done. Filed as sprint-2-data-requirements.md. |
| Triage prototype hitting ≥90% accuracy on synthetic data | Requires synthetic dataset complete + Step 4 bake-off run. Sprint 3 window 26 Apr–9 May; testing sprint ends 23 May. |
| CVDRA prototype hitting ≥95% accuracy on synthetic data | Same dependencies as triage. CVDRA subtasks include one free-text variable (family history of premature CVD) that requires LLM extraction. |

### Objectives 2–4: the runway

**Objective 2 — Real patient data (estimated start: July 2026).** Proof-of-concept on de-identified real GP data. Triggers the Privacy Act 2020 and HIPC obligations. Requires a PIA drafted internally and reviewed by legal counsel before any real data enters the system. Bell Gully (legal) and Buddle Findlay (privacy/health law) engagements feed directly into this. Sandbox environments must be live.

**Objective 3 — Trial in practices (estimated start: late 2026).** Live tool running inside GP practices with real workflows. Requires HISO compliance, PHO contract review, ALEX FHIR API licence formal review, and MCNZ AI guidance (March 2026) baked into tool design. PHO relationships (Comprehensive Care, Health HB) established through Obj 1 GP reviewer network are the commercial entry path.

**Objective 4 — Commercialisation (2027).** Full formal assessment: IP protection, licensing agreements, Fair Trading Act marketing compliance, SaMD registration path (if Medical Products Bill passes). Combined Bell Gully + Buddle Findlay engagement expected. This objective is 12+ months away; design decisions made now (assist-only posture, audit trail, sovereignty) must leave room for the compliance path.

---

## Deadlines — Cannot Miss

| Date | Item | Owner | Status |
|------|------|--------|--------|
| 25 Apr 2026 | R&D Sprint 2 ends | Ryo | Active |
| 27 Apr 2026 | Bell Gully holding reply deadline | Ryo | Drafted, not sent |
| 29 Apr 2026 | Elevate Medtech back (Anne Arndt) | Elevate | Awaiting |
| 30 Apr 2026 | Compliance engagement decision (Bell Gully + Elevate) | Ryo | Open |
| 14 May 2026 | Lisa MBIE Q1 claim guidance reviewed + claim records set up | Ryo | Open |
| 14 May 2026 | Employment contracts corrected (Ryo + Ting) and re-signed | Ryo / Helen | Open |
| 15 May 2026 | R&D bank account open and Helen notified | Ryo | Open |
| 23 May 2026 | R&D accuracy testing sprint ends | Ryo / Ting | Not started |
| 31 May 2026 | Q1 MBIE claim submitted via Forge portal | Ryo / Ting | Not started |
| End June 2026 | Obj 1 all deliverables due (sandbox, architecture, prototypes) | Both | In progress |

---

## Open Risks

- **Indici sandbox.** Valentia has been silent for 3+ weeks. If they do not respond to a phone escalation, Goal A (Indici sandbox connected) cannot be completed by June 2026. This is a named Obj 1 deliverable — may require proactive disclosure to Lisa Pritchard at MBIE and a contingency plan.
- **GP reviewer shortfall.** Only 1 of 2–3 required reviewers has responded. The spec synthesis task (rd-20260421-003) is blocked. If the second reviewer is not secured by early May, synthetic dataset taxonomy may need to be finalised on Nick's findings alone — reducing the MBIE evidence base for Step 1.
- **Synthetic dataset timing.** Schema is provisional pending GP review. If generation starts now (provisional) and the taxonomy shifts significantly after the second review, a targeted relabel is needed. If generation waits, the Sprint 3 bake-off window (26 Apr–9 May) is compressed. This is the most time-critical decision of the week.
- **PAYE condition not yet confirmed approved.** Forge submission was made 20 Apr. If MBIE does not approve the PAYE condition before 31 May, internal labour costs cannot be claimed in Q1. Monitor Forge actively.
- **Employment contract salary discrepancies.** Both Ryo and Ting contracts have stated annual salaries that do not match payroll rates. If not corrected before Q1 claim, the audit trail is inconsistent. Helen needs clear direction; task due 14 May.
- **Architecture bake-off not complete before Q1 narrative.** The Q1 MBIE claim report is written in the Forge portal. If the Sprint 3 bake-off is not complete before the claim is submitted (31 May), the architecture narrative will be forward-looking rather than evidenced. Sprint 3 must finish by 23 May to leave 8 days for claim prep.
- **Compliance engagement decision delay.** The longer Bell Gully and Elevate Medtech engagement is deferred, the less time legal advice has to inform the architecture decision document. Bell Gully Phase 1 takes time once instructed. Decide by 30 Apr or the advice arrives after the Q1 report is drafted.
- **Medical Products Bill uncertainty.** Bell Gully view: introduction this parliamentary term is increasingly unlikely given election proximity. SaMD classification under the current Medicines Act 1981 is unclear for assist-only clinical AI. Design must assume the bill passes eventually and maintain a defensible assist-only posture throughout Obj 1.
