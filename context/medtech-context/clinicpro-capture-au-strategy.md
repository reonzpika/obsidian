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

## 3. Cost model (verified via research 18 April 2026)

**Annual attributable cost of AU deal**: NZD ~21,500 (~AUD 19,500)

Composition:
- Fixed ongoing: insurance AU territorial extension, engineering maintenance (AU share), compliance reporting time, FX/banking, annual tax check
- One-off amortised over 3 years: AU contract legal, tax scoping, PIA extension, privacy policy + DPA + IRP, AU regionalisation engineering, Wise setup
- Per-practice onboarding (first 24 months only): AUD ~11.30 per practice per month

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
| One-off costs amortised over 3-year term | ~14,370 |
| Ongoing annual costs | ~7,100 |
| **Total attributable annual cost** | **~21,470 ≈ 21,500** |

**A. One-off costs (3-year term, ÷3 to get per-year)**

| Line | One-off NZD | /year | Source / reasoning | Confidence |
|---|---|---|---|---|
| AU contract legal | 15,000 | 5,000 | NZ mid-tier firm (Hudson Gavin Martin, Kindrik Partners, Duncan Cotterill) partner rate NZD 500-800/hr, senior associate 400-550/hr. Counterparty-drafted B2B license, 3-year term, $50-150k/yr deal value. Research estimated 16-27 hours total (read, issues memo, negotiation, WHT clause, finalisation). Mid-point $15k. | Medium-high |
| AU tax scoping | 3,000 | 1,000 | One-off international tax advisor consultation: PE risk, royalty WHT treatment, NZ-AU DTA application, GST position. 4-8 hours at NZD 350-500/hr partner (Baker Tilly Staples Rodway, BDO NZ, Grant Thornton). Mid-point $3k. | Medium |
| AU PIA extension | 6,000 | 2,000 | Extension of existing NZ PIA to APP framework (not fresh AU PIA). Re-map APPs 1-13, add APP 8 cross-border, NDB process, AU controller-processor structure. 2-4 consulting days at AU senior privacy rate AUD 2,000-2,800/day = NZD 4,400-12,300. Mid-point $6k. Providers: Privacy 108, Salinger/Helios, IIS Partners. | Medium |
| AU privacy policy + DPA + IRP | 3,500 | 1,200 | AU-facing privacy policy (Sprintlaw AUD 700-2,500 fixed fee) + Data Processing Agreement (Sprintlaw AUD 700-2,000) + Incident Response Plan (AUD 1,500-4,000 or free via OAIC template). Using Sprintlaw-style fixed fee total ~AUD 3,000 = NZD 3,500. | High |
| AU regionalisation engineering | 15,000 | 5,000 | 60-120h work: NHI→IHI identifier swap, AU facility ID format, date/terminology, AU ALEX environment credentials and testing, AU privacy copy. Central 80h at NZ senior contractor NZD 180/hr = NZD 14,400. Rounded to $15k. | Medium |
| Wise setup + misc | 500 | 170 | Wise Business setup NZD 40 + AU invoicing admin + onboarding misc. Rounded to $500. | High |
| **One-off subtotal** | **43,000** | **14,370** | | |

**B. Ongoing annual costs**

| Line | NZD/year | Source / reasoning | Confidence |
|---|---|---|---|
| Insurance AU territorial extension | 1,500 | NZ baseline combined tech liability (PI + cyber) NZD 2,500-8,000/yr. AU territorial extension adds +15-30% (source: Kindrik Partners tech insurance guide, broker benchmarks from Delta Insurance via Apollo/Gallagher). NZD 500-2,500 delta, central $1,500. | Medium |
| Pentest (AU scope) | 0 | CREST Australia New Zealand operates jointly. NZ pentest by CREST ANZ-approved firm (Insomnia Security, Aura, Lateral Security) accepted for AU partner procurement. **Subject to written confirmation from Medtech AU.** If separate AU pentest required, budget AUD 6,000-20,000 annually. | High (subject to confirmation) |
| Engineering maintenance (AU-specific portion) | 3,000 | 4-10 hours/month steady-state. Most shared with NZ code path. 25% attributed to AU-specific work = ~1 hour/month × 12 × NZD 250/hr (opportunity cost) = $3,000. | Low-Medium |
| Compliance reporting time | 1,800 | Quarterly usage/SLA/security reports to Medtech. 2-4 hours/quarter at NZD 150-200/hr opportunity cost = 8-16 hours/year. Mid-point $1,800. | Low-Medium (depends on Medtech requirements) |
| Infrastructure overage | 0 | Below 500 AU practices, combined NZ+AU workload stays within existing Vercel/Supabase/Lightsail tiers. At 500+ practices, incremental ~USD 98/mo = NZD 2,000/year kicks in. **Assumes Year 1-2 scale below 500.** | High |
| Banking / FX | 300 | Wise Business on AUD 50k annual volume: 0.4-0.7% FX margin + small fees = NZD 200-400/yr. Mid-point $300. | High |
| Annual AU compliance checks | 500 | Annual tax advisor check-in, privacy policy refresh, minor admin. $300-500. | Medium |
| **Ongoing subtotal** | **7,100** | | |

### 3.2 What is NOT in the cost model (and why)

1. **NZ partnership costs** (NZ PIA, NZ pentest, NZ contract legal). These exist regardless of the AU deal. Not incremental.
2. **Base infrastructure** (Vercel Pro $20 USD, Supabase Pro $25 USD, Lightsail $12 USD per month). Already paid for NZ operation. Zero incremental cost to add AU up to 500 practices.
3. **Royalty withholding tax (5% of revenue)**. Cash flow drag, not a cost. WHT deducted at source by Medtech AU is reclaimable as NZ foreign tax credit. Net-zero to profitability. Address via gross-up clause in contract.
4. **Ryo's founder time on deal management** (negotiation, relationship, strategic decisions). Real opportunity cost but not a cash cost. Handled via annual minimum and margin structure, not inflated into the cost model.

### 3.3 Confidence caveat

Most numbers are **benchmarks from research**, not actual quotes. Realistic variance is +/- 30%. Before signing, get real quotes on the three largest line items:

1. **AU contract legal** (biggest one-off: $15k at risk). Indicative quotes from Hudson Gavin Martin AND Kindrik Partners.
2. **AU regionalisation engineering** ($15k at risk). Scope with actual developer or self-estimate honestly.
3. **Insurance AU territorial extension** (biggest recurring: $1,500/yr). Broker quote from Apollo Insurance Brokers or Gallagher NZ.

### 3.4 Low / central / high sensitivity

| Scenario | One-off NZD | Annual NZD | Total/yr NZD |
|---|---|---|---|
| **Low-cost** (Sprintlaw-style fixed fees hold, no AU pentest, low insurance uplift) | 28,000 | 5,000 | ~14,300 |
| **Central (used in model)** | 43,000 | 7,100 | **~21,500** |
| **High-cost** (top-tier legal, higher engineering hours, AU pentest required, higher insurance uplift) | 68,000 | 22,000 | ~44,700 |

**What shifts the scenario**: the answers Lawrence gives on Wed to questions 1-7 (vendor security requirements, pentest reuse acceptance, MHR scope, WHT gross-up position). Each answer can move the cost model by thousands.

**Implications for floor pricing at 150 practices:**
- Low-cost scenario: floor could drop to AUD ~16/practice/month.
- Central: AUD 20-25/practice/month.
- High-cost: AUD 30+/practice/month.

This is why the proposal opens at AUD 30: it covers the central scenario comfortably and holds up under the high scenario.

## 4. Break-even analysis at AUD 30 per practice per month

| Scenario | Break-even practices |
|---|---|
| Years 1-2 (including onboarding cost) | ~87 |
| Year 3+ steady state | ~54 |

**Margin at different volumes at AUD 30/month:**

| Practices | Yr 1-2 annual margin (AUD) | Yr 3+ annual margin (AUD) |
|---|---|---|
| 100 | -3,000 (loss) | +16,500 (45%) |
| 150 | +14,000 (26%) | +34,500 (64%) |
| 300 | +60,000 (55%) | +88,500 (82%) |
| 500 | +120,000 (67%) | +160,000 (89%) |

## 5. Pricing strategy

- **Opening ask** (in proposal to Medtech): **AUD 30** per practice per month.
- **Walk-away floor**: AUD 20 per practice per month (~37% of NZ medium-tier retail).
- **Likely landing zone** after negotiation: AUD 22-27 per practice per month.

**Framing to Lawrence**: do NOT anchor on "% of NZ retail." Anchor on cost + margin. Your number is defensible on unit economics, not relative discount. Stronger negotiation posture.

## 6. Minimum license commitment strategy

**Proposal** (opening ask): 150 / 250 / 400 practices = AUD 54k / 90k / 144k.

**Expect pushback.** Lawrence will argue Medtech cannot guarantee rollout volume. Reasonable landing zone:

| Year | Opening ask | Likely landing |
|---|---|---|
| 1 | 150 practices / AUD 54k | 100-120 practices / AUD 36-43k |
| 2 | 250 practices / AUD 90k | 175-200 practices / AUD 63-72k |
| 3 | 400 practices / AUD 144k | 275-325 practices / AUD 99-117k |

**Hard floor minimums** (below these, economics do not work):

- Year 1: AUD 25,000 minimum. Covers fixed cost with thin margin.
- Year 2: AUD 45,000 minimum.
- Year 3: AUD 75,000 minimum.

If Medtech cannot commit to the hard floor, walk away.

## 7. Non-negotiable contract clauses

Identified through research, must appear in final contract:

1. **WHT gross-up clause**. AU royalty withholding tax under NZ-AU DTA is 5% (draft ruling TR 2024/D1 treats software bundle payments as royalties). Without gross-up, Ryo loses 5% of every payment. Critical.
2. **Pentest reuse confirmed in writing**. NZ CREST ANZ pentest acceptable as AU compliance evidence. Saves ~AUD 15k/year.
3. **Scope locked to image capture and ALEX post**. Future ClinicPro tools (Inbox Helper, Care Gap Finder) require separate commercial agreements.
4. **"Powered by ClinicPro" attribution** in about/help panel. Minimum brand presence.
5. **No exclusivity on ClinicPro's side**. Freedom to partner with Bp Premier or other AU PMS later. Medtech can claim to be an AU partner but cannot bind ClinicPro to exclusivity.
6. **Right to direct AU sales post-term**. Exit optionality. If partnership ends, ClinicPro can sell direct.
7. **Active practice definition favourable**. "1 user + 1 successful capture per month" (not heavy usage thresholds that let Medtech stall practices into non-payment).
8. **Governing law accepted AU**, but NZ-qualified lawyer with ANZ experience handles review. Not a problem.
9. **Annual CPI pricing review**. Protects margin over 3 years from inflation.

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
