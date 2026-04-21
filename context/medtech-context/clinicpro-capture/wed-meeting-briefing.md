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

**Your opener:** AUD 30/practice/month · 50-practice floor · 3-year term · AUD 4,000 setup fee.

**Trade rules (pre-decided — do not deviate in room):**

| Scenario | OK? |
|---|---|
| AUD 30 + 40 minimum (Y2+ ramp committed) | Yes |
| AUD 25 + 75 minimum | Yes |
| AUD 25 + 50 minimum | NO — loss-making |
| AUD 22 or below | Walk. Cite cost basis. |

**Break-even reminder:** 54 practices at AUD 30. The 50-practice floor is near-breakeven. Any volume growth above 50 is near-100% margin.


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

## Bring to the meeting

- This doc
- AU proposal one-pager (`clinicpro-capture-au-proposal.md`)
- Commission math (strategy doc §3 table)
- Non-negotiables checklist (strategy doc §6)

---

*For full strategy, cost model, and pricing analysis: `clinicpro-capture-au-strategy.md` and `clinicpro-capture-medtech-integration-strategy.md`.*
