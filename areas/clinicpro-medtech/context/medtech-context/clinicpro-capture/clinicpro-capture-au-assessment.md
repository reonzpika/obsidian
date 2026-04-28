---
title: ClinicPro Capture AU Deal - Red-Team Assessment
type: assessment
audience: internal
project: clinicpro-capture
related: [clinicpro-capture-au-proposal, clinicpro-capture-au-strategy]
author: Dr Ryo Eguchi (red-team review)
date: 2026-04-19
status: draft
meeting: 2026-04-22 Wed with Lawrence Peterson + Alex Cauble-Chantrenne
---

# AU Bundle Deal: Red-Team Assessment

Brutal review of the one-pager and internal strategy, read with fresh eyes. Two perspectives: Lawrence as counter-party, and Ryo's own business blind spots. Then a challenge on pricing, cost model, and strategic posture.

## 0. Summary verdict

**The proposal is well-researched but premature and internally inconsistent.** Three problems:

1. **Sequencing error.** You are sending a priced, structured, 3-year proposal on Monday. Your five biggest commercial unknowns (Q1-Q7 in the strategy doc) only get answered on Wednesday. You are anchoring before you have information. This is the single biggest weakness.
2. **Priority/price mismatch.** Stated priority is "close the deal" with a weak BATNA (would kill AU entirely if it fails). Opening price is AUD 30 with a AUD 20 private floor: 33% negotiation room. That is not a "close fast" opener, it is a "squeeze margin" opener. Pick one.
3. **One-pager is too light for a 3-year white-label, but also commits too much.** A principles memo would protect you; a full term sheet would give you control of drafting; a priced one-pager does neither. It commits a price and structure, but omits the legal hygiene (liability caps, IP, termination, clinical risk) that Medtech's legal will insist on regardless.

Everything below expands on these three and adds the supporting detail.

---

## 1. Lawrence's POV: what he will attack

Reading the one-pager as Lawrence (stretched thin, 2 integration partners already signed, AU G2M pressure, wants simple commercials, 3rd priority slot open):

### 1.1 The 75-practice minimum is the first and loudest pushback

He will say some version of: *"We are launching AU in May. We do not know how many practices will adopt Evolution AU in Year 1, let alone how many will want image capture specifically. Committing AUD 27k/year to you, regardless of whether I sell a single one, is not how we bundle partners."*

- Standard counter: "No minimum Y1, 50 Y2, 100 Y3" (ramp).
- Stronger counter: "Pay-per-active-practice only, no minimum." That is literally how Halo Connect works, which you cite as a structural analogue.
- Your doc says his Y1 practice volume forecast is "awaiting reply." **You are committing to 75 as a floor without knowing his internal number.** If his number is 30-40, you are asking him to pay for 40 practices that do not exist.

**Severity: critical.** This is probably the deal-breaker if Lawrence cannot square it.

### 1.2 "What are the other two partners paying?"

He will not tell you, but he has a number in his head. Your AUD 30 will either:
- Be above the other two (expect hard pushback to $20-25, "we priced them lower").
- Be below the other two (he accepts quickly, you left money on table).

You do not know. You are pricing in the dark. Strategy doc notes this (Q2) but the one-pager commits a number before the question is answered.

### 1.3 Gross-up on WHT

Medtech's treasury will read this as "pay 105.3 to give him 100." He will push:
- **(a)** Shared burden (you eat some of the WHT).
- **(b)** Restructure as services fee (SaaS/support) rather than royalty to avoid WHT classification. This is legitimate; TR 2024/D1 is draft, and the classification depends on how you describe the supply.
- **(c)** "You claim foreign tax credit in NZ; it nets out for you anyway; why do I gross up?"

Your strategy doc flags WHT as critical non-negotiable. Lawrence's legal will flag it as something to negotiate. Budget for a 50/50 split on this or a restructure.

### 1.4 "Powered by ClinicPro attribution + no exclusivity = hostile"

He is bundling you inside Evolution AU, investing in go-to-market, training his support, promoting the feature to his customers. In return, he gets:
- Your brand still visible in-app (minor).
- No exclusivity: you can partner with Bp Premier or Best Practice tomorrow.
- Scope lock in your favour: any future tool requires a new deal.
- Your right to direct AU sales post-term.

From his seat, he is subsidising your AU market entry and getting very little commitment back. He will push for **one or more** of:
- Category exclusivity in AU (image capture only, for the 3-year term).
- ROFR on future ClinicPro AU offerings.
- Non-compete on direct AU sales during term + 12-month tail.
- Removing the "Powered by" attribution (full white-label, no vendor brand visible).

Your strategy doc treats "no exclusivity" as non-negotiable #5. That is a hill to die on, but prepare for it to be a real fight, not a line item.

### 1.5 Quarterly in advance

He will counter with quarterly in arrears based on active practices. Standard bundle economics. Your strategy doc's "cash flow hedge" is exactly what he will resist. Expected landing: monthly in arrears true-up, minimum paid quarterly in advance.

### 1.6 "Compliance milestones TBD" will not pass procurement

His vendor security team will want specifics before bundling:
- Data residency attestation (you have it: Sydney).
- Pentest evidence (CREST ANZ NZ test: subject to AU acceptance).
- PIA (not yet done).
- ISO 27001 or SIG Lite or CAIQ.
- Incident response plan.
- Data breach notification SLAs.

"TBD in contract" signals you are not ready. He may say: *"Come back when you have the artefacts."* That loses you the May/June window. You need the PIA and privacy policy drafts in hand before Wed, or at least credible timelines.

### 1.7 Training scope is too thin

Two 1-hour online sessions + handover docs + one Q&A round to support a white-label image capture product across an unknown number of AU practices is thin. His support team will need:
- Runbook / playbook.
- Escalation matrix with named ClinicPro contacts.
- Shared ticketing or email integration.
- Weekly sync for the first 60-90 days.
- Quarterly product updates.

He will push for extended training + ongoing support SLAs. Budget for that.

### 1.8 Missing commercial hygiene

His legal will immediately ask for terms not in the one-pager:
- Liability cap (essential: clinical images, patient data, NDB).
- IP ownership (your code, his licence scope).
- Data portability / exit obligations.
- Service level agreement (uptime, latency, breach notification windows).
- Termination for cause / convenience.
- Change of control clauses.
- Escrow (source code release if you cease operating).
- Audit rights.

Your strategy doc says "accept Medtech's template on standard language." That is a gift to Medtech. Their template will be drafted in their favour. You need your own redlines prepared.

### 1.9 Launch timeline mismatch

He says May-June. You have:
- Contract negotiation (2-3 weeks minimum after Wed).
- AU regionalisation engineering (60-120 hrs founder time).
- PIA (6-8 hrs founder time + optional review).
- Privacy policy + IRP.
- Insurance territorial extension.
- Possible AU pentest.

Realistically, you ship mid to late June. If he needs May, you either (a) miss the window or (b) ship half-ready. If you miss the window, the other two signed partners are the G2M story and you join Phase 2 with reduced marketing priority.

### 1.10 No pilot or proof period

Standard in AU bundled partner deals: 3-6 month pilot at reduced commitment, then conversion to full term. He will propose this, and it is arguably better for both of you than a hard 3-year with a minimum.

---

## 2. Ryo's business POV: blind spots

What you are not seeing, or hand-waving.

### 2.1 Founder time is the biggest cost in the deal and it is not in the cost model

Strategy doc line 82: "AU regionalisation engineering (~80 hours): Ryo writing it himself. Cash cost zero. Opportunity cost ~2 weeks of founder time (flagged for deal-level decision)."

At a realistic founder rate (NZD 300-500/hr for a clinician-founder doing specialist work), 80-120 hours = **NZD 24-60k**. This is larger than the entire one-off cash budget. But it is discounted to "zero cost" in the pricing model because it is not cash.

If you booked founder time honestly, break-even at AUD 30 moves from ~52 practices to ~80-100 in Year 1. Your 75 minimum becomes borderline. At AUD 25, you need 100-120 practices to break even in Y1-2 on honest cost.

**This is load-bearing.** Re-run break-even with founder time costed.

### 2.2 Ongoing engineering is under-budgeted

"1 hour/month of AU-specific maintenance" is optimistic. Real AU ongoing work:
- AU sandbox credential rotation and testing.
- AU-specific bug reports from Medtech tier-1 (will be frequent in first 6 months).
- AU feature requests Lawrence will absolutely make (because he is paying).
- IHI/HI Service monitoring.
- AU privacy law monitoring (OAIC guidance changes).
- AU compliance reporting cycles.

Realistic: 3-5 hours/month. At NZD 250-500/hr opportunity cost: NZD 9-30k/year, not 3k.

### 2.3 Insurance line is a placeholder, not a quote

NZD 1,500/year for AU territorial extension assumes you resolve the clinical/medical software exclusion with the underwriter. You have no quote. Worst case at real clinical-software premiums: NZD 4-6k/year for the extension alone, with a combined base policy approaching NZD 10k/year. Get the quote before you send the one-pager.

### 2.4 Pentest "confirmed subject to Medtech AU confirmation" is a deal-shaped risk

If Medtech AU demands a separate AU-scope pentest, that is AUD 15-20k you are not pricing. It also sits on the founder's critical path before go-live. Confirm this in writing before signing, not after.

### 2.5 ISO 27001 risk is under-played

Strategy doc says "almost certainly not required for this tier." That is a guess. If Medtech AU procurement says yes, you are looking at:
- AUD 15-30k initial.
- AUD 4-10k/year maintenance.
- 6-12 month implementation.
- Effectively kills the May/June window.

Ask Lawrence directly Wednesday, document the answer. If he cannot confirm, assume worst case and price for it.

### 2.6 The 75-practice minimum was anchored on cost recovery, not deal probability

Strategy doc derives 75 from break-even + margin targets. It does not estimate P(Lawrence accepts 75). Given:
- Only 2 other partners signed.
- AU product launching May.
- Unknown Y1 practice forecast.

P(Lawrence accepts 75 minimum) is probably <40%. Cost-derived floors are only useful if the counter-party's reality supports them. **You may need to drop to 40-50 or remove the hard minimum entirely.**

### 2.7 Market benchmarks are cherry-picked to justify AUD 30

Strategy doc section 7a lists Cubiko ($50 retail), Halo Connect ($20-50), Epic App Orchard (15-30% revenue share). These bracket AUD 30. But:
- Cubiko is a mature multi-feature product, not a single-feature capture tool. Not a like-for-like.
- Halo Connect low-end is $20-25. Your structural analogue supports a number *below* your opener, not above.
- Epic is a different market scale entirely.

Honest read: AUD 20-30 is the defensible range. $30 is top-of-range for an unproven single-feature product in a new market. The strategy doc frames it as "conservative." It is not conservative.

### 2.8 Liability and clinical risk are completely absent

You are a practising GP. Capture handles clinical images routed to patient records. Missing from both docs:
- Clinical risk assessment (wrong-patient image assignment, failed commits, image integrity).
- Liability cap proposal (essential before signing anything).
- Practitioner-level audit trail and evidence retention.
- Clinical incident response pathway (separate from data breach IRP).
- Professional indemnity alignment (Capture's PI insurance vs the GP's own indemnifier).

This is unusual for you to miss. Medtech AU procurement will ask. Have an answer ready.

### 2.9 "Relationship capital" is carrying too much weight

The argument "Medtech is THE long-term partner, close fast, accept margin pressure" assumes:
- Medtech stays strategically aligned for 5+ years.
- Lawrence stays in his role.
- No M&A event changes their partner roster.
- They actually bundle more ClinicPro tools later (not a given: strategy doc admits "any features beyond image capture and ALEX post are out of scope").

If any of these fail, you took a near-term haircut for nothing. Pricing the deal on relationship capital is fine; pricing it entirely on relationship capital is not.

### 2.10 Alex's presence on Wednesday is not neutral

Alex is CC'd on Lawrence's AU emails. He drafted your NZ partnership (which currently has fee-model issues you are contesting). On Wednesday, he may:
- Tag-team with Lawrence on deal linkage ("accept AUD 22 in AU, we give you 15% commission in NZ").
- Push Medtech-favourable positions on both deals simultaneously.
- Use NZ concessions as leverage on AU and vice versa.

Your strategy says "refuse linkage." Easy to say in a strategy doc. Harder when two senior Medtech people are jointly proposing an integrated package that is *slightly* better combined than either deal standalone. Have a pre-agreed rule: *we respond to linked offers by unbundling them and responding to each commercial logic independently, at the end of the meeting, in writing, not in the room.*

### 2.11 Your BATNA is weaker than the strategy doc admits

"Weak BATNA: kill AU entirely if deal fails." But the doc then lists BATNA framing as "reference emerging AU PMS vendors, option to go direct later." These are incompatible stances.

If you genuinely would kill AU, Lawrence can extract almost anything. If you genuinely have alternative AU PMS conversations, bluff holds.

**Action:** before Wednesday, do 2-3 hours of discovery on Bp Premier / Best Practice / Medical Director / Zedmed partner programmes. Even preliminary outreach gives you real BATNA, not bluff BATNA. Lawrence will sense the difference.

### 2.12 One-pager vs term sheet

At this deal size (3-year, ~AUD 80-250k lifetime value, regulated clinical software, cross-border, white-label), a one-pager is too light to control drafting. Lawrence's legal will receive it and say: *"Great, we will send over our partner agreement template." You then spend 8-12 weeks redlining their template.*

Alternative posture: **you provide a full term sheet (5-8 pages) at or shortly after Wednesday, covering pricing, term, support, IP, liability, termination, data handling.** This keeps you in control of the drafting cadence. The one-pager is fine for the 30-minute commercial discussion; the term sheet is what you follow up with.

---

## 3. Pricing challenge

### 3.1 Top-down vs bottom-up

Your pricing was built bottom-up: cost + margin = AUD 30. The more defensible approach is top-down market:

- Medtech AU bundle budget per practice: AUD 118-355/month (your figure).
- Two partners already signed. Assume they absorb 50-70% of budget. Remaining budget for partner #3: **AUD 35-180/month, mid-range ~AUD 60-90.**
- Your AUD 30 fits easily. But you do not know his two partners' prices. You are pricing in the dark.

Also: your NZ retail ($799 median ≈ AUD 730/year ≈ AUD 60/month) provides a useful anchor. AUD 30 to Medtech AU is 50% of NZ retail. At 3-year scale, that is a very fair wholesale rate.

**Conclusion:** AUD 30 is plausibly defensible, but you are *guessing*. You will only know after Wednesday.

### 3.2 Opener vs close-fast mismatch

Stated priority: close the deal. Weak BATNA. Stated opener: AUD 30 with AUD 20 private floor = 33% room.

This is a **margin-optimising opener, not a deal-closing opener.** Pick:
- **Option A (close fast):** open AUD 25, floor AUD 20. Signals readiness, closes in 1-2 rounds.
- **Option B (margin-first):** open AUD 30, floor AUD 22. Signals you expect to negotiate. Adds 1-2 weeks to close.

Your priority stack supports A. Your current opener is B. The two are inconsistent.

### 3.3 Price is premature

Do not put a price in the Monday proposal. Send a **principles memo** (term, structure, support, scope, minimum structure without number, data residency) and hold price until after Wednesday. This lets Lawrence's answers to Q1-Q7 inform your number.

Example language for Monday: *"Commercial terms to be finalised following our Wednesday discussion and subject to Medtech's volume forecast, security requirements, and governing law position. Working range AUD 25-35 per practice per month with annual minimum structure."*

This holds your anchor (working range), signals you are flexible, and does not commit to the exact number before you have information.

---

## 4. Cost model honest re-examination

Revised cost model including founder time at realistic opportunity cost:

| Line | Current model | Honest model |
|---|---|---|
| One-off amortised over 3yr | 6,336 NZD/yr | 6,336 NZD/yr |
| Founder engineering (80h @ NZD 400) | 0 (excluded) | 32,000 NZD one-off → 10,667 NZD/yr |
| Ongoing engineering | 3,000 NZD/yr | 9,000 NZD/yr (3-5h/mo) |
| Insurance (placeholder) | 1,500 NZD/yr | 3,000 NZD/yr (conservative) |
| Compliance reporting | 1,800 NZD/yr | 3,000 NZD/yr (4-6h/qtr) |
| Banking/FX/admin | 800 NZD/yr | 800 NZD/yr |
| Pentest contingency (risked) | 0 | 5,000 NZD/yr (50% × $10k) |
| **Total NZD/yr** | **~13,500** | **~37,800** |
| **Total AUD/yr** | **~12,300** | **~34,400** |

At AUD 30 × 75 practices × 12 months = AUD 27,000 minimum revenue. Against AUD 34,400 honest cost, **Year 1 at minimum volume is loss-making on honest accounting.**

You only reach honest break-even at AUD 30 × 100 practices. If Lawrence commits to 50-60 practices Year 1, you lose money Year 1 at AUD 30. At AUD 25, break-even is 115 practices.

**Action:** rebuild the cost table with founder time at a defensible rate before Wednesday. Your minimum of 75 practices may be too low even at AUD 30 if you cost yourself honestly.

---

## 5. Strategic posture challenges

### 5.1 "Medtech is THE long-term partner"

Reduce to: Medtech is **a** high-priority long-term partner. Do not price the deal as if Medtech is irreplaceable. Start discovery with Bp Premier, Best Practice, MedicalDirector before Wednesday.

### 5.2 "Refuse deal linkage"

Useful as an internal rule, but **expect Lawrence and Alex to propose linkage anyway**. Pre-commit a response pattern: acknowledge the offer, request both deals in writing separately, defer response to 48 hours post-meeting. Do not respond to linked proposals in the room.

### 5.3 "Never admit you would kill AU"

Your behaviour will leak BATNA signals regardless. Specifically: hard quarterly-in-advance, aggressive WHT gross-up, 3-year lock, 75 practice floor. These all signal cashflow certainty is important to you, which signals financial pressure. Lawrence will read the signals.

**Counter:** reduce at least one of those demands (quarterly in advance is the easiest to concede). Signals confidence, not need.

### 5.4 Alex's NZ draft is leverage against you

His current NZ draft (per-facility tiered fee) is worse for you than your counter (15% commission). If Alex arrives Wednesday with a "yes on commission in NZ if you concede on AU," you face a genuinely hard trade. Pre-decide the trade rule: *NZ commission ≥ 12% with no AU concession, or NZ commission ≥ 15% with at most AUD 2/practice concession on AU.* Write this down before Wednesday.

### 5.5 Lawrence's decision authority is unconfirmed

Does he have sign-off for a 3-year commitment at this value? Or does it go to ELT/Board? If sign-off takes 4-6 weeks, your May/June window is dead regardless. **Ask him in the first 5 minutes of the meeting:** *"What is your approval path for a deal of this size, and what is the realistic execution timeline?"*

---

## 6. Recommended adjustments before Monday send

In priority order:

1. **Do not send the priced proposal on Monday.** Send a principles memo instead. Hold price until post-Wednesday.
2. **Rebuild cost model with honest founder time.** Reconfirm break-even.
3. **Drop 75-practice minimum to soft ramp structure**: 40 Y1, 60 Y2, 80 Y3, or similar. Matches Lawrence's likely counter and preserves upside.
4. **Prepare the term sheet (5-8 pages) to follow the one-pager.** Covers liability cap, IP, termination, SLA, clinical risk, data portability. Hold for delivery after Wed.
5. **Prepare non-linkage response script** for the Alex/Lawrence tag-team risk.
6. **Prepare linkage trade rule** (pre-decided, not improvised in room).
7. **Do discovery on 1-2 alternative AU PMS vendors** before Wednesday. Converts BATNA from bluff to real.
8. **Get real quotes on insurance + AU contract legal** before the Wednesday meeting. Both are sent as tasks but timing is tight.
9. **Confirm Lawrence's decision authority** as first meeting question.
10. **Reframe pricing anchor** in your head from "cost + margin" to "market range AUD 22-35, targeting middle after Wed information".

## 7. What is actually strong in the current docs

So this is not all red ink:

- Market benchmark section (7a) is solid research and gives Lawrence-facing defensibility.
- WHT treatment and gross-up framing is correct and ahead of where most startup founders would be.
- Cost model's scope exclusions (TGA, ISO, GST, PE) are well-reasoned and each referenced.
- Strategy doc's risk register is comprehensive and honest about uncertainty.
- The 3-year term structure is right for this type of bundle.
- Alex/Lawrence meeting tactics are correctly identified as a risk even if mitigation is under-developed.
- Support model structure (Medtech tier-1, ClinicPro technical) matches industry convention.

Foundations are strong. Execution sequencing, founder-time accounting, and negotiation preparation are where the gaps sit.

---

*Prepared 2026-04-19 as a brutal final-check ahead of Wednesday 22 April meeting. Use alongside, not instead of, the strategy doc. Revalidate assumptions with Lawrence's answers Wednesday before committing any price or structure in writing.*
