---
title: Wednesday Meeting Briefing
type: briefing
audience: internal
date: 2026-04-22
attendees: Lawrence Peterson (AU), Alex Cauble-Chantrenne (NZ), Ryo
project: clinicpro-capture
---

# Wed 22 April: Lawrence + Alex — Meeting Briefing

**Two separate deals. Two commercial logics. Do not link.**

---

## Deal 1: AU Bundle (Lawrence)

**Your opener:** AUD 30/practice/month · 50-practice floor · 3-year term.

**Setup fee:** removed from one-pager. Raise verbally after the technical questions (domain, auth, update control). Say: "There'll be a setup fee in the term sheet to cover AU engineering. Amount depends on a few technical decisions we need to walk through. Won't be large, but this isn't a flip-a-switch deployment." Firm number goes in the term sheet once scope is known.

**Trade rules (pre-decided — do not deviate in room):**

| Scenario | OK? |
|---|---|
| AUD 30 + 40 minimum (Y2+ ramp committed) | Yes |
| AUD 25 + 75 minimum | Yes |
| AUD 25 + 50 minimum | NO — loss-making |
| AUD 22 or below | Walk. Cite cost basis. |

**Break-even reminder:** 54 practices at AUD 30. The 50-practice floor is near-breakeven. Any volume growth above 50 is near-100% margin.

### If Lawrence tables high volume and pushes price down

Annual revenue / margin at central cost (AUD 19,350/year):

| Price/month | 50 practices  | 100 practices       | 150 practices        | 200 practices        | 300 practices        | Min for +10k profit |
| ----------- | ------------- | ------------------- | -------------------- | -------------------- | -------------------- | ------------------- |
| AUD 30      | 18k / -1.4k   | 36k / +16.7k (46%)  | 54k / +34.7k (64%)   | 72k / +52.7k (73%)   | 108k / +88.7k (82%)  | 82                  |
| AUD 25      | 15k / -4.4k   | 30k / +10.7k (36%)  | 45k / +25.7k (57%)   | 60k / +40.7k (68%)   | 90k / +70.7k (79%)   | 98                  |
| AUD 22      | 13.2k / -6.2k | 26.4k / +7.1k (27%) | 39.6k / +20.3k (51%) | 52.8k / +33.5k (63%) | 79.2k / +59.9k (76%) | 112                 |
| AUD 20      | 12k / -7.4k   | 24k / +4.7k (19%)   | 36k / +16.7k (46%)   | 48k / +28.7k (60%)   | 72k / +52.7k (73%)   | 123                 |
| AUD 18      | 10.8k / loss  | 21.6k / +2.3k (10%) | 32.4k / +13.1k (40%) | 43.2k / +23.9k (55%) | 64.8k / +45.5k (70%) | 136                 |
| AUD 15      | 9k / //loss   | 18k / loss          | 27k / +7.7k (28%)    | 36k / +16.7k (46%)   | 54k / +34.7k (64%)   | 164                 |

**Floor by volume (absolute minimums — protect against high-cost scenario):**
- 50 practices: AUD 30 (no room to move)
- 100 practices: AUD 25
- 150 practices: AUD 22
- 200 practices: AUD 22 (AUD 20 is the true floor but risky if costs blow out)
- 300 practices: AUD 18

**Framing for volume discount ask:** "AUD 30 is already wholesale. If you can confirm the volume commitment in writing, I can move to AUD 25. Below that the unit economics don't work at our cost base."


what I said to him in the email:
- **AUD 30** per active practice per month
- **50 active practices per year minimum**, so **AUD 18,000/year** as the floor
- **3-year initial term**
- Scope as you flagged: **image capture and ALEX `/DocumentReference` POST**
- Launch target **May to June 2026** to line up with AU G2M
- **Sydney AWS hosting**, AU data residency covered

---

## Deal 2: NZ Integration Contract (Alex)

**Your opener:** 15% flat commission on gross revenue, NZ + AU direct sales.

**Trade rules:**

| Scenario | OK? |
|---|---|
| 15% — hold | Default |
| 20% — fallback maximum | Acceptable |
| Above 20% | Walk |
| Any flat per-facility fee | Refuse |

---

## If they link the deals

Refuse in room. "Two separate contracts, two commercial logics."

Only engage a written trade proposal (48 hours to respond):
- Concede NZ fee tiers → if AU minimum drops to 40 or Year 1 minimum waived
- Concede NZ rate (accept <15%) → if AU price increases or term shortens
- NOT acceptable: concede both in one trade

---

## Walk-away conditions

- AU: below AUD 20/practice OR below 40-practice minimum at AUD 30
- NZ: above 20% commission OR any flat per-facility fee
- Either: exclusivity clause on ClinicPro's side

---

## Questions — Lawrence (AU)

Get answers to these before leaving the room.

**Commercial:**
1. Who approves this deal internally, and what is your realistic timeline to signed contract?
2. What is your internal practice volume forecast for AU Year 1?
3. What vendor security requirements does Medtech AU impose? ISO 27001, SIG Lite, CAIQ, or self-attestation? Will NZ CREST ANZ pentest be accepted as AU compliance evidence?
4. Preferred tax treatment: services fee or royalty? Gross-up clause acceptable?

**Technical (needed before engineering can start):**

5. Domain: will Medtech white-label this on their own domain (e.g. capture.medtech.com.au), or is a ClinicPro subdomain acceptable?
6. Auth: do AU GPs authenticate via Medtech's existing SSO, or ClinicPro's own auth?
7. Update control: does Medtech review and approve product releases before they go live to AU practices, or does ClinicPro ship on its own cadence?

---

## Questions — Alex (NZ)

1. Where did the team land on fee model? Moving to % commission or still pushing flat fee?
2. 6-month PIA/pentest timeline from go-live: confirmed?
3. Quarterly reporting cadence acceptable?

---

## Key non-negotiables (do not give in room)

1. Net AUD 30/practice after tax (gross-up or services-fee restructure — method flexible)
2. NZ CREST ANZ pentest accepted as AU pentest evidence (saves ~AUD 15k/year)
3. Scope locked to image capture + ALEX post only
4. No exclusivity on ClinicPro side
5. Double-dipping carve-out: bundled AU practices excluded from NZ commission scope

---

## Meeting checklist

### Before

- [x] This briefing open and reviewed
- [ ] Trade rules memorised (AU and NZ)
- [ ] AU proposal one-pager on hand

### During — Lawrence (AU)

- [x] Asked: decision authority and timeline to signed contract
- [ ] **Is this G2M medtech evolution? or something completely new?**
- [ ] **Asked: Y1 practice volume forecast**
- [ ] **Asked: happy with the per practice cost (AUD 30)?**
- [ ] **Asked: minimum year commitment - happy with 3 years?**
- [ ] **Asked: security requirements - same as the Medtech NZ ALEX partnership?**
- [ ] Asked: tax treatment preference (services fee or royalty?) - defer for the second meeting. first meeting is going over the major points to head to the closing phase. 
- [ ] Asked: domain (their domain vs ClinicPro subdomain) - defer
- [ ] Asked: update control (approval process vs auto-deploy)
- [ ] Raised: setup fee, whether they want **UI customisation, and auth model** (bundle after confirming commercial terms)

### During — Alex (NZ)

- [ ] Asked: fee model landing (% commission or still flat fee?)
- [ ] Asked: 3-month PIA/pentest timeline confirmed
- [ ] Asked: quarterly reporting cadence acceptable

### During — both

- [ ] Confirmed two-contract structure with both
- [ ] Refused deal linkage (if raised)
- [ ] Did not deviate from trade rules

### After

- [ ] Send follow-up email confirming key points and any agreement in principle
- [ ] Scope setup fee based on technical answers (domain, auth, update control)
- [ ] If agreed in principle: draft term sheet within 5 working days

---

*For full strategy, cost model, and pricing analysis: `clinicpro-capture-au-strategy.md` and `clinicpro-capture-medtech-integration-strategy.md`.*
