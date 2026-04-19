---
title: ClinicPro Capture AU Deal - Internal Strategy Notes
type: strategy
audience: internal
project: clinicpro-capture
related: clinicpro-capture-au-proposal
author: Dr Ryo Eguchi
date: 2026-04-18
status: active
meeting: 2026-04-22 Wed with Lawrence Peterson + Alex Cauble-Chantrenne
---

# AU Bundle Deal: Internal Strategy Notes

Comprehensive background, cost model, negotiation tactics, and pre-meeting checklist for Wednesday 22 April 2026 meeting with Lawrence Peterson (GM Integration, Medtech Global) and Alex Cauble-Chantrenne (NZ Partnership).

## 1. Strategic context

- **NexWave Health R&D is the primary founder bet.** ClinicPro Capture is secondary: cash generator plus PMS partnership foothold for future tools.
- **AU market entry via Medtech is channel-only.** No direct AU sales planned. Partnership with PMS is crucial for selling clinical tools into AU given no local presence.
- **Wed meeting will discuss NZ commission AND AU bundle together.** Alex was CC'd on Lawrence's earlier AU emails. Expect attempted deal linkage.

## 2. Deal framing

**Lawrence's 12 April proposal** (verbatim extract):
> "Two core integration partners 'white labelled' into the Aus product for G2M in May. I would like to think I have one more, being ClinicPro, but at this time thinking just a limited feature set. Medtech Purchase of licenses... image capture and post feature as a starting point by May/June."

**Signals to read:**
- White-label (not co-brand) is the default Medtech offer.
- Image capture + post ONLY. No other features.
- Tight timeline (May/June). Pressure tactic AND real.
- You are 3rd priority after two already-signed partners.
- Houston may build equivalent. Competitive time pressure implied.
- Lawrence is "stretched thin". Wants simple clean commercials.

## 3. Cost model (verified via research 18 April 2026, revised for Ryo's scope decisions)

**Annual attributable cost of AU deal**: NZD ~13,500 (~AUD 12,300)

Composition:
- Fixed ongoing: insurance AU territorial extension, engineering maintenance (AU share), compliance reporting time, FX/banking, annual compliance checks
- One-off amortised over 3 years: AU contract legal, AU tax scoping (Helen), AU PIA (DIY), AU privacy policy, Wise setup
- Per-practice onboarding (first 24 months only): AUD ~11.30 per practice per month

**Scope decisions reducing cost from initial $21,500 estimate:**
- AU tax scoping handled by Helen (NZ accountant) at her billable rate — cheaper than specialist firm but not free.
- AU regionalisation engineering (~80 hours) done by Ryo himself. Cash cost $0, opportunity cost ~2 weeks of founder time.
- AU PIA done DIY using OAIC free template (6-8 hours of Ryo's time). Budget $1k for external review if Medtech AU pushes back.
- Privacy policy adapted from NZ version at low cost; DPA typically in main contract; IRP via free OAIC template.

**Infrastructure is effectively free** up to 500 AU practices (existing Sydney-region stack already covers it). Above 500, modest Lightsail bandwidth overage kicks in.

**Not required** based on research:
- Separate AU pentest: NZ CREST ANZ pentest is accepted in AU.
- ISO 27001: almost certainly not required for this tier of Medtech partner.
- TGA medical device registration: Capture is EXCLUDED as pure image pass-through with no analysis.
- AU GST registration: not needed for B2B supply to GST-registered Medtech AU.
- AU permanent establishment: no risk given no AU physical presence or dependent agent.

### 3.1 Detailed line-item breakdown

**Summary**

| Category | NZD/year |
|---|---|
| One-off costs amortised over 3-year term | ~6,336 |
| Ongoing annual costs | ~7,100 |
| **Total attributable annual cost** | **~13,436 ≈ 13,500** |

**A. One-off costs (3-year term, ÷3 to get per-year)**

| Line | One-off NZD | /year | Source / reasoning | Confidence |
|---|---|---|---|---|
| AU contract legal | 15,000 | 5,000 | NZ mid-tier firm (Hudson Gavin Martin, Kindrik Partners, Duncan Cotterill) partner rate NZD 500-800/hr. Counterparty-drafted B2B license, 3-year term, $50-150k/yr deal value. 16-27 hours total. Covers read + issues memo + markup + WHT clause + negotiation + finalisation. | Medium-high |
| AU tax scoping (Helen) | 1,500 | 500 | Helen (Ryo's NZ accountant) billable rate NZD 200-250/hr × 4-6 hours to confirm WHT treatment under TR 2024/D1, NZ-AU DTA, GST B2B exemption, PE confirmation, and WHT gross-up wording for lawyer. If Helen refers to AU specialist, cost could be $3k. | Medium |
| AU PIA (DIY + external review) | 1,000 | 333 | DIY PIA using OAIC free template (6-8 hours Ryo's time, no cash cost). Budget $1k for external review from Privacy 108 or Salinger if Medtech AU pushes back on self-conducted PIA. | Medium |
| AU-facing privacy policy | 1,000 | 333 | Adapted from NZ privacy policy with APP alignment. Sprintlaw AU fixed fee AUD 700-2,500 or DIY. DPA typically included in main contract (no separate cost). IRP via free OAIC template. | High |
| Wise setup + misc | 500 | 170 | Wise Business setup NZD 40 + AU invoicing admin + onboarding misc. | High |
| **One-off subtotal** | **19,000** | **6,336** | | |

**Removed from model (Ryo doing himself):**
- **AU regionalisation engineering** (~80 hours): Ryo writing it himself. Cash cost zero. Opportunity cost ~2 weeks of founder time (trade-off against NexWave R&D pace, flagged for deal-level decision).

**B. Ongoing annual costs**

| Line | NZD/year | Source / reasoning | Confidence |
|---|---|---|---|
| Insurance AU territorial extension | 1,500 | Ryo currently has NO insurance. Combined tech liability policy (PI + cyber) needs to be purchased before signing AU contract, ~NZD 2,500-4,500/yr base. AU territorial extension adds 15-30% (NZD 500-2,500). Base NOT attributed to AU (needed for NZ anyway); extension IS AU-incremental. Mid-point $1,500. Must resolve clinical/medical exclusion with underwriter. | Medium |
| Pentest (AU scope) | 0 | CREST Australia New Zealand operates jointly. NZ CREST ANZ pentest accepted for AU partner procurement. **Subject to Medtech AU written confirmation.** Budget AUD 6,000-20,000 contingency if separate AU pentest demanded. | High (subject to confirmation) |
| Engineering maintenance (AU-specific portion) | 3,000 | ~1 hour/month of AU-specific maintenance × 12 × NZD 250/hr opportunity cost. Most maintenance shared with NZ code path. | Low-Medium |
| Compliance reporting time | 1,800 | Quarterly usage/SLA/security reports to Medtech. 2-4 hours/quarter at NZD 150-200/hr opportunity cost. | Low-Medium (depends on Medtech requirements) |
| Infrastructure overage | 0 | Below 500 AU practices, combined NZ+AU workload stays within existing Vercel/Supabase/Lightsail tiers. At 500+ practices, incremental ~USD 98/mo = NZD 2,000/year kicks in. | High |
| Banking / FX | 300 | Wise Business on AUD 50k annual volume. | High |
| Annual AU compliance checks | 500 | Annual privacy policy refresh, OAIC guidance monitoring, minor admin. | Medium |
| **Ongoing subtotal** | **7,100** | | |

### 3.2 What is NOT in the cost model (and why)

1. **NZ partnership costs** (NZ PIA, NZ pentest, NZ contract legal). Exist regardless of AU deal.
2. **Base infrastructure** (Vercel Pro, Supabase Pro, Lightsail). Already paid for NZ. Zero incremental cost up to 500 AU practices.
3. **Base insurance policy** (~NZD 2,500-4,500/yr combined PI + cyber). Ryo currently has none, but needs it for NZ partnership anyway. Medtech AU forces the timing, not the attribution. Must be purchased before signing AU contract.
4. **Founder engineering time on AU regionalisation** (~80 hours). Cash cost zero. Opportunity cost ~2 weeks of founder time impacting NexWave R&D pace. Real but not cash.
5. **Royalty withholding tax (5% of revenue)**. Cash flow drag, not a cost. Reclaimable as NZ foreign tax credit. Net-zero to profitability. Address via gross-up clause.
6. **Founder time on deal management** (negotiation, relationship, reporting). Real opportunity cost, not cash cost. Handled via annual minimum and margin structure.

### 3.3 Confidence caveat

Most numbers are benchmarks from research, not actual quotes. Realistic variance +/- 30%. Get real quotes on the two largest line items before signing:

1. **AU contract legal** (biggest one-off: $15k at risk). Indicative quotes from Hudson Gavin Martin AND Kindrik Partners.
2. **Combined PI + cyber insurance with AU extension** (biggest recurring annual: ~$4,000 total, ~$1,500 AU-attributable). Broker quote from Apollo Insurance Brokers or Gallagher NZ. Must resolve clinical / medical software exclusion with underwriter.

### 3.4 Low / central / high sensitivity

| Scenario | One-off NZD | Ongoing NZD | Total/yr NZD |
|---|---|---|---|
| Low-cost (Sprintlaw fixed fees hold, insurance already held, no AU pentest demand) | 12,000 | 5,000 | ~9,000 |
| **Central (used in model)** | 17,500 | 7,100 | **~12,936** |
| High-cost (top-tier legal, AU pentest required, ISO 27001 demanded, higher insurance uplift) | 45,000 | 22,000 | ~37,000 |

**What shifts the scenario**: answers Lawrence gives Wed on questions 1-7 (security requirements, pentest reuse, MHR scope, WHT gross-up position). Each answer moves the cost model by thousands.

**Implications for floor pricing at 150 practices:**
- Low-cost scenario: floor could drop to AUD ~12/practice/month.
- Central: AUD ~17/practice/month.
- High-cost: AUD ~28/practice/month.

Opening at AUD 30 holds up comfortably in central AND high scenarios. Leaves comfortable negotiation room.

## 4. Break-even analysis at AUD 30 per practice per month

Annual fixed cost NZD ~12,936 = AUD ~11,760. Per-practice onboarding AUD 11.30/month in years 1-2.

| Scenario | Break-even practices |
|---|---|
| Years 1-2 (including onboarding cost) | ~52 |
| Year 3+ steady state (onboarding drops off) | ~33 |

**Margin at different volumes at AUD 30/month:**

| Practices | Yr 1-2 annual margin (AUD) | Yr 3+ annual margin (AUD) |
|---|---|---|
| 50 | -540 (slight loss) | +6,240 (35%) |
| 100 | +10,680 (30%) | +24,240 (67%) |
| 150 | +21,906 (41%) | +42,240 (78%) |
| 300 | +55,548 (51%) | +96,240 (89%) |
| 500 | +100,440 (56%) | +168,240 (93%) |

Revised model significantly improves margins at every scale vs the original $21,500/yr cost basis.

## 5. Pricing strategy

- **Opening ask** (in proposal to Medtech): **AUD 30** per practice per month.
- **Public floor** (as stated internally and defended publicly): AUD 25 per practice per month.
- **Private soft floor** (with non-price concessions): AUD 20 per practice per month.
- **Likely landing zone** after negotiation: AUD 25-30 per practice per month.

**Framing to Lawrence**: do NOT anchor on "% of NZ retail." Anchor on cost + value + AU market benchmarks. Cubiko QuickCheck retails at AUD 50/practice/month direct; $30 as wholesale to PMS bundle sits in the expected 50-60% band. Halo Connect (Best Practice's partner API) uses the identical structural model Medtech is proposing.

**Framing to Lawrence**: do NOT anchor on "% of NZ retail." Anchor on cost + margin. Your number is defensible on unit economics, not relative discount. Stronger negotiation posture.

## 6. Minimum license commitment strategy

**Proposal** (opening ask, in one-pager): **flat 75 practices per year across all 3 years = AUD 27,000/year minimum**. 3-year minimum total: AUD 81,000.

**Why flat, not incrementing**: simplicity. Aligned with priority of closing fast. Flat minimums are easier for Lawrence to approve internally and remove ramp-schedule complexity. Upside is NOT capped — per-active-practice fees apply fully when practices exceed 75.

**Revenue scenarios under flat minimum:**

| Scenario | Year 1 practices | Year 2 practices | Year 3 practices | 3-year revenue (AUD) |
|---|---|---|---|---|
| Minimum floor only | 75 | 75 | 75 | 81,000 |
| Ramp as hoped | 75 | 150 | 250 | 162,000 |
| Over-delivery | 100 | 200 | 400 | 252,000 |

Upside captured fully whether Medtech under-delivers, hits target, or accelerates. Minimum only establishes downside protection floor.

**Hard floor** (absolute walk-away): if Lawrence cannot commit to 75 practices per year in any year, deal does not work economically.

**Payment structure**: annual minimum billed quarterly in advance, equal instalments (25%/quarter = AUD 6,750/quarter). Per-active-practice excess invoiced quarterly in arrears. Net 30 terms.

**Setup fee**: AUD 4,000 at contract execution, offsets Year 1 minimum. Covers PIA, privacy policy adaptation, IRP, onboarding admin. Reduced from earlier $15k given engineering work is founder-absorbed.

## 7. Non-negotiable contract clauses

Reduced to six essentials for simplicity (aligned with priority of closing fast):

1. **WHT gross-up clause**. AU royalty withholding tax under NZ-AU DTA is 5% (draft ruling TR 2024/D1 treats software bundle payments as royalties). Without gross-up, ClinicPro loses 5% of every payment. **Critical.**
2. **Pentest reuse confirmed in writing**. NZ CREST ANZ pentest acceptable as AU compliance evidence. Saves ~AUD 15k/year.
3. **Scope locked to image capture and ALEX post**. Future ClinicPro tools require separate commercial agreements.
4. **"Powered by ClinicPro" attribution** in about/help panel. Minimum brand presence.
5. **No exclusivity on ClinicPro's side**. Freedom to partner with Bp Premier or other AU PMS later.
6. **30-day payment terms, quarterly in advance**. Protects cash flow.

**Standard contract language (do not fight for explicit clauses, accept Medtech's template)**: force majeure, late payment interest, acceleration on material breach, governing law (accept AU), dispute resolution, confidentiality.

**Simplification rationale**: originally identified 14 clauses. Dropped eight for closing speed. The six retained are load-bearing; losing any one of them compromises the deal economics materially. Everything else is in the contract template as standard language and can be accepted without negotiation.

## 7a. Market benchmark validation

Research (18 April 2026) confirmed AUD 30 is inside AU industry bundle pricing norms:

**Medtech Evolution AU unit economics** (source: ITQlick, Jan 2026):
- List price AUD 240 per license per month
- Typical practice (~7 licenses) = AUD 1,680 per month revenue
- Estimated central gross profit per practice per month: ~AUD 1,180
- Industry rule: bundled partner COGS absorb 10-25% of gross profit
- Medtech's rational bundling budget per practice: **AUD 118-355 per month**
- AUD 30 is only 2.5% of central gross profit. Very affordable for Medtech.

**Direct AU comparable — Cubiko QuickCheck**:
- Direct retail AUD 50 per practice per month
- Single-module add-on integrated with Best Practice
- Closest analogue in scope and depth to Capture
- At typical wholesale discount of 40-50%, wholesale equivalent = **AUD 25-30/practice/month**

**Structural fit — Halo Connect (Best Practice partner API)**:
- Uses identical "set fee per practice per month, tiered by usage" model Medtech is proposing
- Top tier estimated at AUD 20-50/practice/month
- AUD 30 sits squarely in the band

**Global analogue** (Epic App Orchard historical):
- 15-30% revenue share on partner apps
- On a AUD 200 retail product, Epic took AUD 30-60. AUD 30 on a narrower-scope tool is consistent.

**Bottom line**: AUD 30 is defensible as opener. Market supports it. Lawrence's rational pushback band is AUD 22-28. Our floor of AUD 25 is well inside defensible territory.

## 7b. Revised strategy framework (19 April 2026)

**Ryo's priorities (confirmed)**:
1. Getting the deal (weak BATNA: kill AU entirely if this fails)
2. Maximising margin
3. Cash flow (NexWave R&D has runway, AU cash is bonus)

**Strategic context**:
- Medtech is THE long-term integration partner for ClinicPro (5+ year horizon, multiple future tools)
- Relationship capital matters more than squeezing this single deal
- Close fast, keep simple

**Timeline goal**: contract signed by end April 2026 (10 days from Wed meeting).

**BATNA bluff**: if Lawrence pushes price hard, reference emerging AU PMS vendors and option to go direct later. **Never admit you'd kill AU entirely if this fails** (which is the truth).

## 8. Strategic risks to manage

**Risk: Deal linkage NZ to AU.** Medtech will try to trade "NZ commission increase for AU per-practice decrease." Refuse. Two separate deals, two separate commercial logics. Repeat as needed.

**Risk: White-label brand capture.** Full white-label means every future ClinicPro AU tool is a new Medtech negotiation. Gatekeeper risk. Mitigation: scope lock + right to direct AU sales post-term + no exclusivity.

**Risk: Houston competitive pressure.** Unclear if real or speculative. Push for first-mover timing advantage, not product exclusivity.

**Risk: Medtech AU security posture unknown.** If ISO 27001 required, deal economics change by ~AUD 25-50k over 3 years. Ask Lawrence Wed.

**Risk: Alex's NZ partnership clauses.** His draft includes flat fee per Active Facility ($10-60/month tier). Your counter is 10/15% commission. If Alex settles on flat 15% of gross revenue, that is good NZ outcome. AU deal must NOT be used as trade-off.

**Risk: Royalty WHT classification.** TR 2024/D1 is still draft. Worst case: ATO classifies entire payment as royalty, 5% withheld. Best case: apportioned. Needs advisor sign-off before signing.

**Risk: Concession creep.** Lawrence's "move at speed" pressure can be used to extract concessions. Trade speed for better terms, don't cave to deadline without reciprocation.

## 9. Questions to bring to Wed meeting

**For Lawrence (AU):**
1. What vendor security requirements does Medtech AU impose on bundled partners? ISO 27001, SIG Lite, CAIQ, self-attestation?
2. Who are the two already-signed AU partners? Understand benchmarks and relative positioning.
3. What practice volume forecast does Medtech have for AU Year 1? Push him on internal number. This sets annual minimum negotiation.
4. Does My Health Record integration sit within Capture scope, or stays Medtech-side?
5. Can Medtech confirm ABN and GST registration in writing? (GST B2B exemption hinges on this.)
6. What is Medtech's position on gross-up for AU royalty withholding tax?
7. What is the proposed governing law for the AU contract (Victoria, NSW, other)?

**For Alex (NZ):**
1. Where did the Medtech team land on NZ fee structure? Flat 15% commission, or still per-facility tiers?
2. What is your timeline for the pentest and PIA on NZ side? (Impacts shared-cost attribution.)
3. Will Medtech NZ commission any differently on existing customers vs Medtech-referred customers?

## 10. Pre-meeting checklist (before Wed 22 April)

- [ ] Send AU bundle proposal (one-pager) to Lawrence, CC Alex. Tuesday AM latest.
- [ ] Get pre-quote indications from 2 NZ law firms (Hudson Gavin Martin, Kindrik Partners) for AU contract review scope.
- [ ] Email broker (Apollo Insurance or Gallagher NZ) to flag need for AU territorial extension on PI + cyber policies. Ask about medical device / clinical software exclusions.
- [ ] Phone consultation with a NZ international tax advisor (Baker Tilly Staples Rodway, BDO NZ) on TR 2024/D1 royalty classification. Confirm before any signing.
- [ ] Print cost model showing break-even curve at AUD 30.
- [ ] Print NZ retail tier comparison table ($299/$799/$1,500 tiers → AUD equivalents).
- [ ] Print the AU proposal one-pager for handover.

## 11. Post-Wed actions

Depending on outcome:

**If Lawrence accepts proposal in principle:**
- Create task: draft AU term sheet within 5 working days.
- Engage NZ commercial lawyer for contract drafting and review.
- Commission AU PIA extension (Privacy 108 or Salinger/Helios).
- Get written confirmation from Medtech AU that CREST ANZ NZ pentest is accepted.

**If Lawrence pushes significantly below floor:**
- Restate cost basis clearly.
- Walk if below AUD 20/practice or if annual minimums below hard floor.
- Keep door open: "happy to revisit in 6 months when AU G2M is clearer."

**If deal is linked to NZ concessions:**
- Refuse linkage in meeting. Keep commercial logics separate.
- Restate NZ counter (10/15% commission) independently.

## 12. Key resources for Wed

- Email thread "AU market for Capture app" with Lawrence (Gmail, last message 13 April)
- Existing NZ partnership draft from Alex Cauble-Chantrenne (received 13 April)
- Main project file: `projects/clinicpro-capture.md`
- External proposal: `projects/clinicpro-capture-au-proposal.md`
- Two other partners: ask Lawrence directly, research not yet available

---

*Last updated: 2026-04-18. Numbers based on research completed this date. Revalidate cost model annually.*
