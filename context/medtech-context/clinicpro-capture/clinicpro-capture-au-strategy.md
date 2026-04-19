---
title: ClinicPro Capture AU Deal - Internal Strategy Notes
type: strategy
audience: internal
project: clinicpro-capture
related: clinicpro-capture-au-proposal
author: Dr Ryo Eguchi
date: 2026-04-19
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

## 3. Cost model (revised 19 April 2026 with honest founder-time cost at NZD 145/hr)

**Annual attributable cost of AU deal**: **NZD ~21,300 (~AUD 19,350)**

Composition:
- Cash one-off amortised over 3 years: AU contract legal, AU tax scoping (Helen), AU PIA (DIY), AU privacy policy, Wise setup.
- Founder engineering one-off amortised: 80 hours × NZD 145 = NZD 11,600 total / 3 years.
- Ongoing cash: insurance AU territorial extension, compliance reporting, FX/banking, annual compliance checks.
- Ongoing founder maintenance: 4 hours/month × NZD 145 × 12.

**Change from earlier model (NZD 13,500/yr):** previous model excluded founder time as "opportunity cost, not cash cost." At Ryo's actual billable rate of NZD 145/hr, that is intellectually dishonest and hides the real economics of the deal. Revised model includes founder time at this rate. If Lawrence pushes below AUD 25, founder time is the hidden variable that tips the deal loss-making.

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
| Cash one-off amortised over 3-year term | ~6,336 |
| Founder engineering one-off amortised | ~3,867 |
| Ongoing cash costs | ~4,100 |
| Ongoing founder maintenance | ~6,960 |
| **Total attributable annual cost** | **~21,263 ≈ 21,300** |

**A. One-off costs (3-year term, ÷3 to get per-year)**

| Line | One-off NZD | /year | Source / reasoning | Confidence |
|---|---|---|---|---|
| AU contract legal | 15,000 | 5,000 | NZ mid-tier firm (Hudson Gavin Martin, Kindrik Partners, Duncan Cotterill) partner rate NZD 500-800/hr. Counterparty-drafted B2B license, 3-year term, $50-150k/yr deal value. 16-27 hours total. Covers read + issues memo + markup + WHT clause + negotiation + finalisation. | Medium-high |
| AU tax scoping (Helen) | 1,500 | 500 | Helen (Ryo's NZ accountant) billable rate NZD 200-250/hr × 4-6 hours to confirm WHT treatment under TR 2024/D1, NZ-AU DTA, GST B2B exemption, PE confirmation, and WHT gross-up wording for lawyer. If Helen refers to AU specialist, cost could be $3k. | Medium |
| AU PIA (DIY + external review) | 1,000 | 333 | DIY PIA using OAIC free template (6-8 hours Ryo's time, no cash cost). Budget $1k for external review from Privacy 108 or Salinger if Medtech AU pushes back on self-conducted PIA. | Medium |
| AU-facing privacy policy | 1,000 | 333 | Adapted from NZ privacy policy with APP alignment. Sprintlaw AU fixed fee AUD 700-2,500 or DIY. DPA typically included in main contract (no separate cost). IRP via free OAIC template. | High |
| Wise setup + misc | 500 | 170 | Wise Business setup NZD 40 + AU invoicing admin + onboarding misc. | High |
| **One-off subtotal** | **19,000** | **6,336** | | |

**Founder engineering (now in model, previously excluded):**

| Line | One-off NZD | /year | Source / reasoning |
|---|---|---|---|
| AU regionalisation engineering (80h × NZD 145) | 11,600 | 3,867 | NHI → IHI identifier swap, AU facility ID handling, AU-specific terminology, separate AU ALEX sandbox credentials, AU privacy copy. Rate is Ryo's actual billable rate. |

**B. Ongoing annual costs**

| Line | NZD/year | Source / reasoning | Confidence |
|---|---|---|---|
| Insurance AU territorial extension | 1,500 | Ryo currently has NO insurance. Combined tech liability policy (PI + cyber) needs to be purchased before signing AU contract, ~NZD 2,500-4,500/yr base. AU territorial extension adds 15-30% (NZD 500-2,500). Base NOT attributed to AU (needed for NZ anyway); extension IS AU-incremental. Mid-point $1,500. Must resolve clinical/medical exclusion with underwriter. | Medium |
| Pentest (AU scope) | 0 | CREST Australia New Zealand operates jointly. NZ CREST ANZ pentest accepted for AU partner procurement. **Subject to Medtech AU written confirmation.** Budget AUD 6,000-20,000 contingency if separate AU pentest demanded. | High (subject to confirmation) |
| Founder engineering maintenance | 6,960 | ~4 hours/month of AU-specific maintenance × 12 × NZD 145/hr. Includes AU sandbox credential rotation, AU-specific bug reports from Medtech tier-1, AU feature requests, IHI/HI Service monitoring, AU privacy law monitoring. | Low-Medium |
| Compliance reporting time | 1,800 | Quarterly usage/SLA/security reports to Medtech. 2-4 hours/quarter at NZD 150-200/hr. | Low-Medium (depends on Medtech requirements) |
| Infrastructure overage | 0 | Below 500 AU practices, combined NZ+AU workload stays within existing Vercel/Supabase/Lightsail tiers. At 500+ practices, incremental ~USD 98/mo = NZD 2,000/year kicks in. | High |
| Banking / FX | 300 | Wise Business on AUD 50k annual volume. | High |
| Annual AU compliance checks | 500 | Annual privacy policy refresh, OAIC guidance monitoring, minor admin. | Medium |
| **Ongoing subtotal** | **11,060** | | |

### 3.2 What is NOT in the cost model (and why)

1. **NZ partnership costs** (NZ PIA, NZ pentest, NZ contract legal). Exist regardless of AU deal.
2. **Base infrastructure** (Vercel Pro, Supabase Pro, Lightsail). Already paid for NZ. Zero incremental cost up to 500 AU practices.
3. **Base insurance policy** (~NZD 2,500-4,500/yr combined PI + cyber). Ryo currently has none, but needs it for NZ partnership anyway. Medtech AU forces the timing, not the attribution. Must be purchased before signing AU contract.
4. **Royalty withholding tax (5% of revenue)**. Cash flow drag, not a cost. Reclaimable as NZ foreign tax credit. Net-zero to profitability, *if* we negotiate gross-up or restructure as services fee to minimise exposure.
5. **Founder time on deal management** (negotiation, relationship, reporting). Real opportunity cost, not cash cost. Handled via annual minimum and margin structure.

### 3.3 Confidence caveat

Most numbers are benchmarks from research, not actual quotes. Realistic variance +/- 30%. Get real quotes on the two largest line items before signing:

1. **AU contract legal** (biggest one-off: $15k at risk). Indicative quotes from Hudson Gavin Martin AND Kindrik Partners.
2. **Combined PI + cyber insurance with AU extension** (biggest recurring annual: ~$4,000 total, ~$1,500 AU-attributable). Broker quote from Apollo Insurance Brokers or Gallagher NZ. Must resolve clinical / medical software exclusion with underwriter.

### 3.4 Low / central / high sensitivity

| Scenario | Cash one-off NZD | Founder eng. one-off NZD | Ongoing NZD/yr | Total NZD/yr |
|---|---|---|---|---|
| Low-cost (Sprintlaw fixed fees, insurance exclusion resolved cheap, no AU pentest demand, lighter maintenance load) | 12,000 | 8,000 | 8,000 | ~14,700 |
| **Central (used in model)** | 19,000 | 11,600 | 11,060 | **~21,263** |
| High-cost (top-tier legal, AU pentest required, ISO 27001 demanded, heavy AU support requests, higher insurance uplift) | 45,000 | 20,000 | 25,000 | ~46,700 |

**What shifts the scenario**: answers Lawrence gives Wed on security requirements, pentest reuse, and volume forecast. Each answer moves the cost model by thousands.

**Implications for floor pricing at 50 practices:**
- Low-cost scenario: floor ≈ AUD 22/practice/month.
- Central: AUD 30/practice/month is breakeven.
- High-cost: AUD 65/practice/month needed.

AUD 30 with 50-practice minimum is breakeven central-case. Upside is entirely in volume growth above minimum: every practice above 50 at AUD 30 is near-100% margin in steady state.

## 4. Break-even analysis at AUD 30 per practice per month

Annual cost NZD ~21,300 = AUD ~19,350 (central case, honest founder time).

| Price | Break-even practices/year |
|---|---|
| AUD 30/month | ~54 |
| AUD 25/month | ~65 |
| AUD 22/month | ~73 |

**Margin at different volumes at AUD 30/month:**

| Practices | Annual revenue (AUD) | Annual margin (AUD) |
|---|---|---|
| 50 | 18,000 | -1,350 (slight loss) |
| 75 | 27,000 | +7,650 (28%) |
| 100 | 36,000 | +16,650 (46%) |
| 150 | 54,000 | +34,650 (64%) |
| 300 | 108,000 | +88,650 (82%) |

**Important caveat:** this is steady-state annual math. Year 1 includes the full cash one-off spend (~NZD 19,000 legal + tax + PIA + privacy + Wise) hitting in the first 12 months. Actual Y1 cash outlay is front-loaded. Steady-state economics from Y2 onwards are what matter for the 3-year deal.

**3-year totals at 50-practice flat minimum × AUD 30:**

| Scenario | 3-yr revenue (AUD) | 3-yr cost (AUD) | 3-yr net (AUD) |
|---|---|---|---|
| Flat at 50 all 3 years | 54,000 | ~58,000 | -4,000 (loss) |
| Ramp 50 → 75 → 100 | 81,000 | ~58,000 | +23,000 |
| Ramp 50 → 100 → 150 | 108,000 | ~58,000 | +50,000 |

50-practice floor makes the deal break-even on minimum performance, profitable on any growth. Acceptable risk posture given weak BATNA and strategic value.

## 5. Pricing strategy

- **Opening ask** (in proposal to Medtech): **AUD 30** per practice per month.
- **Public floor** (as stated internally and defended publicly): AUD 25 per practice per month.
- **Private soft floor** (with non-price concessions): AUD 20 per practice per month.
- **Likely landing zone** after negotiation: AUD 25-30 per practice per month.

**Framing to Lawrence**: do NOT anchor on "% of NZ retail." Anchor on cost + value + AU market benchmarks. Cubiko QuickCheck retails at AUD 50/practice/month direct; $30 as wholesale to PMS bundle sits in the expected 50-60% band. Halo Connect (Best Practice's partner API) uses the identical structural model Medtech is proposing.

**Framing to Lawrence**: do NOT anchor on "% of NZ retail." Anchor on cost + margin. Your number is defensible on unit economics, not relative discount. Stronger negotiation posture.

## 6. Minimum license commitment strategy

**Opening ask (in one-pager): flat 50 practices per year across all 3 years = AUD 18,000/year minimum.** 3-year minimum total: AUD 54,000.

**Why 50, not 75**: closing speed and deal probability. Lawrence has 2 other partners already signed and his AU Y1 practice volume is unknown. 75 was anchored on cost recovery at margin; 50 is anchored on deal probability with breakeven-at-floor economics. We give up ~AUD 6,000/year of guaranteed margin at floor in exchange for substantially higher P(close).

**Why flat, not incrementing**: simplicity. Flat minimums are easier for Lawrence to approve internally and remove ramp-schedule complexity. Upside is NOT capped: per-active-practice fees apply fully when practices exceed 50.

**Revenue scenarios under 50 flat minimum at AUD 30:**

| Scenario | Y1 practices | Y2 practices | Y3 practices | 3-year revenue (AUD) |
|---|---|---|---|---|
| Minimum floor only | 50 | 50 | 50 | 54,000 |
| Modest ramp | 50 | 75 | 100 | 81,000 |
| Target ramp | 50 | 100 | 150 | 108,000 |
| Over-delivery | 75 | 150 | 250 | 162,000 |

Minimum establishes downside protection at breakeven. Profit comes from volume growth.

**Hard floor (absolute walk-away)**: if Lawrence cannot commit to **40 practices/year minimum at AUD 30**, deal does not work (even honest-cost break-even is 54 at this price). Below that, either price has to move up or walk.

**Price/volume trade rules** (pre-decided for Wednesday):
- Hold AUD 30 at 50 minimum: default.
- AUD 30 at 40 minimum: acceptable only if Lawrence confirms Y2+ growth path.
- AUD 25 at 75 minimum: acceptable trade (AUD 22,500 revenue at floor, ~AUD 3,150 margin).
- AUD 25 at 50 minimum: **do NOT accept**. AUD 15,000 revenue at floor = ~AUD 4,000/year loss.

**Payment structure**: monthly invoicing in arrears, 30-day terms, minimum floor applied. Signals cashflow confidence, avoids "quarterly in advance" BATNA tell.

**Setup fee**: AUD 4,000 on contract execution, offsets Year 1 minimum. Covers AU onboarding, compliance setup, and initial Medtech support enablement (runbook, escalation matrix, shared ticketing, training). Included in one-pager.

## 7. Non-negotiable contract clauses

Trimmed for closing speed. Only four hard non-negotiables:

1. **Tax treatment resolved to ClinicPro receiving net AUD 30/practice**. Method negotiable: either WHT gross-up, OR restructure deal as services fee (not royalty) to avoid WHT classification under TR 2024/D1, OR shared burden as last resort. Let Medtech's treasury propose preferred structure; we care about the net outcome, not the mechanism. **Do not raise in one-pager. Discuss in meeting or term sheet.**
2. **Pentest reuse confirmed in writing**. NZ CREST ANZ pentest acceptable as AU compliance evidence. Saves ~AUD 15k/year.
3. **Scope locked to image capture and ALEX post**. Future ClinicPro tools require separate commercial agreements.
4. **No exclusivity on ClinicPro's side**. Freedom to partner with Bp Premier or other AU PMS later.

**Dropped from non-negotiables (acceptable concessions):**
- **"Powered by ClinicPro" attribution**. Acceptable to drop if it smooths Medtech approval. Not worth fighting for.
- **Quarterly in advance payment**. Monthly in arrears is fine. Signals cashflow confidence rather than need.

**Standard contract language (accept Medtech's template unless it harms us materially)**: force majeure, late payment interest, acceleration on material breach, governing law (accept AU), dispute resolution, confidentiality.

**Items to raise at term sheet stage (not one-pager, not meeting)**: liability cap, IP ownership, termination for cause/convenience, SLA, data portability, change of control, clinical risk pathway, practitioner-level audit, professional indemnity alignment.

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
- Medtech is the priority long-term integration partner for ClinicPro (5+ year horizon, multiple future tools).
- AU bundle deal is **guaranteed distribution**. NZ partnership is channel access where ClinicPro still has to acquire customers.
- **Priority inversion: AU bundle > NZ commission.** If forced to trade in a linked offer on Wednesday, concede NZ terms to protect AU economics, not vice versa.
- Relationship capital matters more than squeezing this single deal.
- Close fast, keep simple.

**Timeline goal**: agreement in principle from Wednesday meeting, contract signed by mid-May 2026 (3-4 weeks from Wed).

**BATNA framing**: if Lawrence pushes price hard, reference emerging AU PMS vendors (Bp Premier, Best Practice, MedicalDirector, Zedmed) as option to go direct later. **Never admit you'd kill AU entirely if this fails** (which is the truth). Do 2 hours of discovery calls with these vendors between Monday and Wednesday so the BATNA is real, not pure bluff.

**Pre-decided price/volume trade rules** (locked before meeting):
- Default: AUD 30 at 50 minimum (one-pager opener).
- If Lawrence pushes volume: AUD 30 at 40 minimum acceptable if Y2+ ramp committed.
- If Lawrence pushes price: AUD 25 acceptable only if minimum moves up to 75+ to protect Y1 economics.
- AUD 25 at 50 minimum = loss position, DO NOT accept.
- AUD 22 or below: walk, cite cost basis.

**Pre-decided linkage trade rule** (if Alex/Lawrence propose integrated NZ+AU offer):
- Acknowledge linkage in room, defer written response to 48 hours post-meeting.
- Acceptable trade: concede on NZ per-facility fee tiers (accept Alex's current draft) IF Medtech drops AU minimum to 40 OR accepts no minimum for Year 1.
- Acceptable trade: concede on NZ commission rate (accept <15% if still in commission model) IF AU price bumps or term shortens.
- **NOT acceptable**: concede on BOTH NZ fee model AND AU price in a single linked trade.

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
1. **First 5 minutes:** what is your approval path for a deal of this size, and realistic execution timeline from handshake to signed contract? This sets everything else.
2. What vendor security requirements does Medtech AU impose on bundled partners? ISO 27001, SIG Lite, CAIQ, self-attestation? Will NZ CREST ANZ pentest be accepted?
3. What practice volume forecast does Medtech have for AU Year 1? Push him on internal number. Sets minimum licence negotiation.
4. Does My Health Record integration sit within Capture scope, or stays Medtech-side?
5. Can Medtech confirm ABN and GST registration in writing? (GST B2B exemption hinges on this.)
6. What is Medtech treasury's preferred approach to cross-border tax treatment? Gross-up on royalty or restructure as services fee?
7. What is the proposed governing law for the AU contract (Victoria, NSW, other)?

**For Alex (NZ):**
1. Where did the Medtech team land on NZ fee structure? Flat 15% commission, or still per-facility tiers?
2. What is your timeline for the pentest and PIA on NZ side? (Impacts shared-cost attribution.)
3. Will Medtech NZ commission any differently on existing customers vs Medtech-referred customers?

## 10. Pre-meeting checklist (before Wed 22 April)

**Must do before Monday send:**
- [ ] Send email to Lawrence, CC Alex, Monday AM. Email only, no PDF attachment. Body carries headline terms (price, minimum, term, scope, launch, data residency, infrastructure cost answer). Frame as direct response to Lawrence's 12 April question.

**Must do between Monday and Wednesday:**
- [ ] 2 hours of discovery calls with Bp Premier / Best Practice / MedicalDirector partner teams. Convert BATNA from bluff to real.
- [ ] Get pre-quote indications from 2 NZ law firms (Hudson Gavin Martin, Kindrik Partners) for AU contract review scope. In parallel with the above.
- [ ] Email broker (Apollo Insurance or Gallagher NZ) to flag need for AU territorial extension on PI + cyber policies. Ask about medical device / clinical software exclusions.
- [ ] Call Helen to book phone consultation on TR 2024/D1 royalty classification and services fee restructure option.

**Bring to Wednesday meeting:**
- [ ] One-pager (comprehensive version) as Ryo's own reference and potential handout if Lawrence asks for detail.
- [ ] Cost model showing break-even at AUD 30 × 50 practices.
- [ ] Price/volume trade rules (section 6) and linkage trade rules (section 7b).
- [ ] Lawrence decision authority question prepared as first agenda item.

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

*Last updated: 2026-04-19. Revised cost model includes honest founder time at NZD 145/hr. Minimum licence reduced to 50 practices to improve P(close). Non-negotiables trimmed. AU > NZ priority inversion added to linkage framework. Revalidate cost model annually.*
