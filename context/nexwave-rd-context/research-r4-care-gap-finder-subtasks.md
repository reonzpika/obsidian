---
title: Research R4 — Care Gap Finder Sub-Task Architectures
type: context
project: nexwave-rd
objective: obj-1
step: step-2
created: 2026-04-11
status: final
---

# Research R4 — Care Gap Finder Sub-Task Architectures

> **Scope.** Design reference for the three Care Gap Finder sub-tasks specified in [[care-gap-finder-task-spec]] — (A) deterministic rules engine for gap detection, (B) variable extraction from NZ PMS records, (C) NZ PREDICT v.2019 CVDRA calculation per HISO 10071:2025 — plus PMS integration (Medtech ALEX FHIR API, Indici) and the end-to-end evaluation protocol that ties them together. This is the **Sprint 2 deliverable** feeding tasks rd-20260329-010 (architecture shortlist) and rd-20260329-011 (data requirements), and complements [[research-r3-architecture-shortlist]] (which selects the LLM-side architecture).
>
> **Method.** Compiled from four parallel research threads run on 11 April 2026: R4-A (rules engine architecture), R4-B (variable extraction), R4-C (missing data + CVDRA implementation), R4-D (PMS integration + end-to-end evaluation). Cross-references: [[research-r1-llm-architecture-benchmarks]], [[research-r2-nz-sovereign-hosting-regulatory]], [[research-r7-open-source-llm-self-hosted]]. Out of scope: synthetic dataset protocol ([[research-r5-synthetic-data-protocol]], pending), full FHIR/HL7/code-set deep dive ([[research-r6-data-standards-pms-integration]], pending).

---

## 1. Executive summary

**Sub-task A — Gap detection (rules engine).** **Do not adopt a published rules framework.** Every credible Python option is dormant (`pyke`, `intellect`, `pyDatalog`), GPL-encumbered (`experta`), or has weak temporal-interval semantics (`json-logic`, `business-rules`, `rule-engine`). DMN/Drools is overweight for our scale and FEEL has no first-class "most recent event in value set" primitive. CQL is the right semantic reference but its only mature runtimes are JVM/JavaScript. Build a thin custom interpreter (~500–1000 LoC): rules expressed in YAML, validated through Pydantic, evaluated by a small library of temporal primitives (`most_recent`, `months_since`, `in_value_set`, `exists_in_interval`). Adopt the **CMS eCQM four-layer pattern** (Initial Population → Denominator → Denominator Exclusions → Numerator) and emit a **tri-state outcome** per rule (`GAP` / `NO_GAP` / `INSUFFICIENT_DATA(reason)`) so no patient is silently dropped. Rule packs are git-versioned with signed commits, every rule carries a natural-language statement + clinical rationale + source-guideline citation + ≥8 test vectors, and the rendered "rulebook" becomes the artefact GP reviewers and TGA auditors read instead of code.

**Sub-task B — Variable extraction.** Variable extraction is **a routing problem, not an LLM problem**. Of the 15 PREDICT inputs, 12 are deterministic structured-field lookups (age, sex, ethnicity, diabetes, smoking, SBP, TC, HDL, TC:HDL, BP-lowering meds, lipid-lowering meds, antithrombotic meds) — these should never reach an LLM. Three variables need dedicated treatment: **family history of premature CVD** is the only field that genuinely needs free-text NLP (NZ structural completeness ~19% per PLOS ONE 2013); **NZDep** is a pure deterministic address → SA1 → NZDep2018 lookup against the Otago HIRP open dataset, no LLM; **AF** is structured-code primary with free-text as a secondary "suggested AF, not confirmed" signal that only flags for GP review and never feeds CVDRA silently. For free-text family history, the recommended primary extractor is **BioClinical ModernBERT 396M** (LightOn/Rutgers, MIT, June 2025; current SOTA on clinical NER per arXiv 2506.10896), fine-tuned on synthetic + GP-confirmed exemplars; **Llama 3.3 70B with constrained decoding** (XGrammar for throughput, Outlines for one-shot reliability) is the verifier/second-opinion layer. Mandatory hallucination controls: grammar-constrained JSON output, evidence-span verbatim verification per field, post-hoc Pydantic validation with retry, and Hybrid-Code v2 style symbolic value-set verification before any extracted claim is written to the calculator. All inference local on NZ-sovereign infrastructure (Catalyst Cloud or Bedrock NZ) following the LLM-Anonymizer pattern (NEJM AI 2024). **Do not use chain-of-thought** for clinical extraction — arXiv 2509.21933 shows 86% of LLMs degrade under CoT on clinical text understanding.

**Sub-task C — CVDRA calculation.** No published Python implementation of NZ PREDICT v.2019 exists. The VIEW team's `PredictRiskScores` R package is GPL-3.0 (Pylypchuk et al. 2018, GitHub), which would taint a Python verbatim port. The clean-room path: re-implement from **HISO 10071:2025** as the formal specification (the standard includes worked examples and test cases produced by the HRC-VIEW team specifically for software-supplier validation), validate against those test cases, and dual-run against a containerised R reference for regression testing. The equation coefficients themselves are facts published in *The Lancet* (Pylypchuk 2018) and not copyrightable. For missing data, adopt a **hybrid fail-closed architecture**: (a) hard-suppress on CVD equivalents (prior CVD, eGFR<30, severe HF, FH, TC>8, SBP>180/110); (b) hard-suppress if age, sex, or ethnicity missing (Berkelmans 2022 JCE confirms these cannot be safely imputed; ethnicity imputation systematically under-estimates risk for Māori, Pacific, Indian); (c) population-median imputation for non-critical continuous variables (SBP, TC, HDL); (d) **conservative over-estimation for binary modifiers in recall mode** (smoking, family history, AF default to "yes" with explicit GP-verify chip — the inverse of the QRISK3 default, justified by our recall-optimised mandate); (e) NZDep deterministic address geocoding with NZDep 8 fallback when address unresolvable. Never display a bare risk number — always pair with confidence band, missing-variable list, and imputed-variable list (Wells 2009 JMIR design pattern). Validation strategy: Hypothesis property-based tests (monotonicity, bounds, symmetry), HISO worked-example unit tests (100% match required), 10,000-row R-oracle regression suite, ethnicity-stratified equity report (MBIE deliverable).

**PMS integration.** **Medtech ALEX FHIR API is the only viable primary integration** for a third-party cloud-hosted product that must scan a 2,500-patient register on a schedule and respect HIPC 2020 boundaries. ALEX exposes all the FHIR resources Care Gap Finder needs (`Patient`, `Condition`, `Observation`, `DiagnosticReport`, `MedicationRequest`, `DocumentReference`) across 261 catalogued endpoints. Auth is **Azure AD OAuth 2.0 client credentials** (tenant `8a024e99-aba3-4b25-b875-28b0c0ca6096`) — *not* SMART on FHIR backend services — with mandatory **static IP allowlisting**, which forces the existing ClinicPro Capture BFF pattern (`api.clinicpro.co.nz`). **No public `$export` operation** is documented today; the scaling pattern is `Patient?_lastUpdated=gt{T}` delta-pull paged search, ~12,500 calls for a cold scan of 2,500 patients and ~2,000–3,000 calls for a weekly delta. **Indici is partnership-gated** — Valentia Technologies advertises FHIR but does not publish a developer portal; treat Indici as Sprint 4+ work after written engagement with Valentia. Direct DB / ODBC, HL7 outbound mirroring, and BPAC CareSuite are all ruled out as primary paths. The single biggest operational unknown is ALEX's unpublished rate limit; Odin Health is the only public population-scale ALEX precedent and operates under what appears to be a bilaterally-negotiated higher tier.

**End-to-end evaluation.** Decompose the pipeline into **stage-wise error budgets** with waterfall accounting (ε_A gap detection, ε_B extraction, ε_C calculation, ε_data PMS gap), per TRIPOD+AI 2024 and DECIDE-AI 2022. Gold standard: **dual-blinded clinician chart review** of n ≥ 400 stratified patients across 3–5 pilot practices, with a third senior-GP adjudicator, Cohen's κ ≥ 0.70 as primary agreement target with Gwet's AC1 reported as a prevalence-robust check. Sub-task C accuracy target ≥95% on clean synthetic data is operationalised as agreement within ±0.5 absolute percentage points of the VIEW R reference; per-rule sensitivity ≥0.95 with 5,000-resample BCa bootstrap CI; per-rule NPV ≥0.99 (the most recall-critical metric); GP review burden <10 false positives per 2,500-patient practice per week as the adoption gate. Ethnicity-stratified reporting (Māori, Pacific, South Asian, European/Other) is mandatory for the MBIE equity deliverable and Brier score ≤0.12 plus calibration slope ∈ [0.9, 1.1] anchor the Stage C calibration story.

---

## 2. Sub-task A — Rules engine design (deep dive)

### 2.1 Framework survey and the build-vs-buy decision

Care Gap Finder rules look deceptively simple ("HbA1c every 3 months if last value > 64 mmol/mol") but combine four properties that no off-the-shelf engine handles cleanly together: **temporal interval logic** (months_since, most_recent in window), **value-set membership** (SNOMED/Read/LOINC code lists), **multi-source aggregation** (most recent across labs + observations + problem list), and **clinical safety auditability** (every rule must trace to a source guideline a GP can read). I evaluated five framework families and rejected all of them.

| Framework family | Examples | Verdict | Why ruled out |
|---|---|---|---|
| Python "rules engine" libraries | `business-rules` (last release 2017), `rule-engine` (live), `json-logic-py`, `durable_rules`, `pyknow`/`experta`, `pyDatalog`, `pyke`, `intellect` | **Reject** | All dormant, GPL-encumbered, or have weak temporal-interval primitives. `experta` is GPL-3.0 (would taint a closed-source clinical product). `pyke` and `intellect` are abandoned. `business-rules` last released 2017. `json-logic` and `rule-engine` lack first-class "most recent observation in value set within last N months" primitives. `durable_rules` is a forward-chaining production system — overkill for ~30 monitoring rules and adds Redis as a hard dependency. |
| Forward-chaining production systems | Drools, CLIPS, Jess | **Reject** | JVM (Drools) or C (CLIPS) — wrong runtime for our Python stack. Drools is heavyweight (>50MB JAR, KIE workbench tooling). Forward chaining is the wrong evaluation model for batch register scans. |
| DMN with FEEL | Camunda DMN, kogito-dmn, pyDMNrules | **Reject** | DMN is the right *shape* (decision tables a non-developer can read) but FEEL has no first-class "most recent event from value set X in interval Y" function — every clinical rule degenerates into a verbose `for` loop in FEEL boxed expressions. The Camunda DMN engine is JVM. `pyDMNrules` is a hobbyist project. |
| Clinical Quality Language (CQL) | HL7 CQL 1.5 (normative), cqf-ruler, cql_engine (JVM), cql-execution (JS) | **Reject as runtime, adopt as semantic reference** | CQL is the semantically correct answer — it has `most recent`, `during`, `Interval`, value-set bindings, and is used by CMS for eCQM. **But the only mature runtimes are JVM (`cql_engine`) and JavaScript (`cql-execution`).** No production-grade Python runtime exists. Bridging via subprocess to a JAR adds operational complexity, latency, and a JVM dependency we don't otherwise need. **Decision: use CQL syntax as the human-readable "spec" we cite from each rule, but don't run a CQL interpreter.** |
| ML / scoring rules | scikit-learn pipelines, RuleFit, SkopeRules | **Reject** | These produce rules from data, not the other way around. Wrong tool for "encode HbA1c monitoring guideline." |

**Decision: build a thin custom YAML-defined rules interpreter (~500–1000 LoC of Python) that adopts the CMS eCQM four-layer pattern, uses Pydantic for schema validation, and exposes a small library of temporal primitives.** The custom path wins on every axis we care about — auditability, runtime fit, dependency footprint, and the ability to make every rule a single human-readable artefact a GP reviewer can read without learning a new language. The cost (writing the interpreter once) is ~2 engineer-weeks; the alternative (wrapping a JVM CQL runtime, building DMN tooling, or fighting `business-rules` extensions) is several engineer-weeks of tooling work that produces a worse end product.

### 2.2 The CMS eCQM four-layer pattern

CMS Electronic Clinical Quality Measures (eCQM) — the framework used by every Medicare Promoting Interoperability and MIPS quality measure since 2014 — model every monitoring rule as four populations:

1. **Initial Population (IP).** Every patient who could conceivably be in scope. *Example: any enrolled patient ≥18.*
2. **Denominator (D).** The patients the rule actually applies to. *Example: IP ∩ "active diabetes problem" (Read C10F% or SNOMED 73211009 descendants).*
3. **Denominator Exclusions (DEX).** Patients we explicitly *exclude* from measurement even though they meet the denominator — for clinical safety, palliation, age, or contradiction. *Example: D ∩ "active palliative care plan" or "deceased" or "opted-out of recall".*
4. **Numerator (N).** Patients in (D − DEX) who **already meet the standard**. *Example: HbA1c result with date in last 6 months.*

The "gap" is then `(D − DEX) − N` — patients who should have had the action but haven't. Any rule expressed in this shape is automatically auditable: a GP reviewer can ask "why is patient X flagged?" and trace IP → D → DEX → N membership without looking at code.

We adopt this pattern verbatim. Every Care Gap Finder rule is a YAML document with explicit `initial_population`, `denominator`, `denominator_exclusions`, `numerator`, plus `clinical_rationale`, `source_citation`, and `test_vectors` blocks.

### 2.3 Tri-state outcome — never silently drop patients

A second eCQM principle we steal: **every patient evaluated against a rule produces one of three outcomes**, never two.

- `GAP` — patient is in `(D − DEX)` and not in `N`. Surface to GP.
- `NO_GAP` — patient is in `N`, or in `DEX`, or not in `D`. Silent.
- `INSUFFICIENT_DATA(reason)` — patient is in `D` but a *required* variable for evaluating `DEX` or `N` is missing or unparseable. **Never silently drop**; surface to GP review with the reason ("HbA1c value present but units field empty", "address could not be geocoded for NZDep").

The third state matters more than it looks. The biggest failure mode of register-scan tools in NZ practice (per the BPAC CS Inbox Manager review and Health Accelerator RPA evaluations referenced in [[manual-care-gap-monitoring]]) is **silent attrition** — patients who fall out of the denominator because of a missing field, with no log entry, no review queue, and no operator visibility. A recall-optimised system must treat missing data as a finding, not as an exit condition.

### 2.4 Temporal primitive library

The interpreter ships with a tight library of ~12 functions that cover every monitoring-rule shape we have surveyed in NZSSD diabetes guidelines, BPAC NZ HbA1c/BP/lipid pathways, MoH 2018 CVDRA, KDIGO 2013 eGFR/uACR, and HISO 10071:2025 PREDICT eligibility:

- `most_recent(observation_type, value_set, source) → Observation | None`
- `months_since(date) → int | None`
- `years_since(date) → int | None`
- `in_value_set(code, value_set_id) → bool`
- `exists_in_interval(observation_type, value_set, interval) → bool`
- `count_in_interval(...)` — for "≥2 BP readings in last 3 months"
- `current_age(reference_date) → int`
- `has_active_problem(value_set) → bool` — problem-list semantics with onset/abatement
- `has_active_medication(value_set, as_of) → bool` — handles repeat dispensing windows
- `latest_value_above(observation_type, threshold, source) → bool`
- `address_to_nzdep(patient.address) → int | None` — geocoded fallback chain
- `is_palliative(patient, as_of) → bool` — DEX helper combining problem list + advance care plan flag

These 12 primitives compose every rule we need for Sprint 3 / Sprint 4. New primitives are added under code review with a published rationale and test vectors — the same gate as a new rule.

### 2.5 Rule artefact — what every rule file contains

Each rule is one YAML file under `rules/` in the repo. Required fields:

```yaml
id: hba1c-monitoring-poor-control
version: 1.0.0
title: HbA1c monitoring (poor control: most recent ≥ 64 mmol/mol)
clinical_rationale: |
  Adults with diabetes whose most recent HbA1c is ≥ 64 mmol/mol require
  3-monthly HbA1c monitoring per BPAC NZ "Diabetes management toolbox"
  (March 2023, p. 17) and NZSSD "Type 2 Diabetes Management Guidance"
  (October 2021, §4.2). This rule fires when no HbA1c result has been
  recorded in the last 3 months.
source_citation:
  - "BPAC NZ — Diabetes management toolbox (March 2023), §HbA1c targets and frequency"
  - "NZSSD — Type 2 Diabetes Management Guidance (Oct 2021), §4.2"
  - "[[nz-diabetes-monitoring]]"
initial_population:
  expression: current_age(today) >= 18
denominator:
  expression: |
    has_active_problem(value_set="diabetes-mellitus-any") AND
    latest_value_above("hba1c", threshold=64, units="mmol/mol")
denominator_exclusions:
  expression: |
    is_palliative(patient, today) OR
    has_opted_out_of_recall(patient) OR
    deceased(patient)
numerator:
  expression: exists_in_interval("hba1c", value_set="hba1c-loinc", interval="last 3 months")
test_vectors:
  - id: gap-1
    description: 55yo T2DM, last HbA1c 72 mmol/mol 5 months ago, no exclusion → GAP
    fixture: fixtures/gap-1.json
    expected: GAP
  - id: nogap-1
    description: 55yo T2DM, last HbA1c 72 mmol/mol 1 month ago → NO_GAP
    expected: NO_GAP
  - id: insufficient-1
    description: 55yo T2DM but most recent HbA1c value field empty → INSUFFICIENT_DATA(reason="hba1c value missing on most recent record")
    expected: INSUFFICIENT_DATA
  # ... ≥ 8 vectors per rule, covering every DEX path and edge case
```

The rule file is the single source of truth: it is **the artefact GP reviewers and TGA auditors read**, not Python code. Render it to a human-friendly "rulebook" PDF/HTML for clinical sign-off.

### 2.6 Auditability and version control

Rule packs live under git in their own directory (`rules/v{semver}/`), commits are signed, and every release of the rules engine binds to a frozen rule-pack version. Per TGA Class IIa expectations (referenced in [[research-r2-nz-sovereign-hosting-regulatory]]) and IEC 62304 §5.1.6 software configuration management, every rule change requires:

1. A pull request that touches one rule file (no batch refactors)
2. Updated `clinical_rationale` if the source guideline changed, with the new citation
3. Updated `test_vectors` (≥8 per rule), all passing
4. A second clinician sign-off recorded in the PR (we mirror the FDA Sept 2022 CDS Final Guidance "independent review" expectation: rules, value sets, and inputs must all be visible to the reviewing clinician — that is exactly what the YAML file gives them)
5. A bumped semver tag

Auditors get: a signed git history; a rendered rulebook artefact per release; a test report; the value-set bindings; and a one-page "what changed and why" diff. This is the deliverable shape that satisfies both the MBIE Capability Development requirement and the international regulatory frameworks we are aligning to in advance of the Medical Products Bill commencement (~2030).

### 2.7 What this rules engine is *not* responsible for

To prevent scope creep: the rules engine evaluates structured inputs against expressions and returns tri-state outcomes per rule per patient. It does **not**:

- Extract variables from free text — that is Sub-task B's job (§3 below).
- Compute risk scores — that is Sub-task C's job (§7 below).
- Generate patient-facing recall letters — that is downstream presentation.
- Decide who gets contacted — that is the GP, advised by ranked outputs.

This narrow scope is what keeps the interpreter ~500–1000 LoC and makes its behaviour formally testable.

---

## 3. Sub-task B — Variable extraction (overall design)

### 3.1 Variable extraction is a routing problem, not an LLM problem

The dominant failure mode of "use an LLM for clinical extraction" architectures is treating every variable as if it were free text. For the 15 PREDICT inputs we need, this is the wrong default. **12 of 15 are deterministic structured-field lookups in any modern NZ PMS**: age (DOB → patient demographics), sex (patient demographics), ethnicity (HISO 10001 codes on patient header), diabetes status (Read C10F* / SNOMED 73211009 descendants in problem list), smoking status (coded social-history field), systolic BP (most recent observation), TC (lab observation), HDL (lab observation), TC:HDL ratio (computed), BP-lowering medication (NZULM-coded MedicationRequest in active list), lipid-lowering medication (same), antithrombotic medication (same).

Sending any of these 12 to an LLM is a strict downgrade — we trade deterministic, auditable, instant lookups for stochastic, opaque, slow, hallucinable outputs. **None of these 12 should ever reach an LLM.** They are direct structured-field extractions backed by value-set bindings.

That leaves three variables that genuinely deserve special treatment, and they are the entire R&D risk surface for Sub-task B:

| Variable | Why it's hard | Strategy |
|---|---|---|
| **Family history of premature CVD** | Structural completeness in primary care records is ~19% (Dhiman PLOS ONE 2013, THIN 1.5M-patient analysis). When recorded at all, it sits in free text in consultation notes, not in a coded field. | Free-text extractor (LLM with constrained decoding + evidence verification). The only true NLP variable in the set. |
| **NZDep** | Census-derived deprivation decile by SA1, derived from address. Almost never in the PMS as a stored field — must be computed from the patient's residential address against the Otago HIRP NZDep2018 dataset. | Pure deterministic lookup pipeline: address → standardised address → SA1 mesh block → NZDep decile. **Not an LLM task at all.** |
| **AF (atrial fibrillation)** | Under-coding in NZ primary care is ~30% (Tomlin 2017 *EJPC*; corroborated by Sandiford 2024 HLC Māori AAA screening). Coded entries miss patients diagnosed in hospital and never re-coded in the PMS. Free-text mentions ("AF noted", "?AF", "ECG suggested AF") are common but ambiguous. | Structured-code primary path; free-text *secondary signal* that **never feeds CVDRA silently**. Free-text suspect-AF flags only ever surface as a "GP review: possible AF, please confirm" item. |

### 3.2 Pipeline overview

```
                    ┌─────────────────────────────┐
                    │     ALEX FHIR / Indici      │
                    └──────────────┬──────────────┘
                                   ▼
                    ┌─────────────────────────────┐
                    │   Structured-field router   │
                    │  (12 of 15 vars handled     │
                    │   here, deterministically)  │
                    └──────────────┬──────────────┘
                                   ▼
       ┌───────────────────────────┼───────────────────────────┐
       ▼                           ▼                           ▼
┌──────────────┐         ┌──────────────────┐        ┌──────────────────┐
│  NZDep       │         │  AF code lookup  │        │  Family Hx?      │
│  geocoding   │         │  + (suspect-AF   │        │  Coded? → done   │
│  pipeline    │         │   free-text flag │        │  Else: free-text │
│  (no LLM)    │         │   for GP review) │        │  extractor       │
└──────┬───────┘         └────────┬─────────┘        └────────┬─────────┘
       │                          │                           ▼
       │                          │                  ┌──────────────────┐
       │                          │                  │ BioClinical-     │
       │                          │                  │ ModernBERT-396M  │
       │                          │                  │ (primary)        │
       │                          │                  │  +               │
       │                          │                  │ Llama-3.3-70B    │
       │                          │                  │ constrained      │
       │                          │                  │ decoding         │
       │                          │                  │ (verifier)       │
       │                          │                  └────────┬─────────┘
       │                          │                           ▼
       │                          │                  ┌──────────────────┐
       │                          │                  │ Hybrid-Code v2   │
       │                          │                  │ symbolic value-  │
       │                          │                  │ set verification │
       │                          │                  │ + evidence-span  │
       │                          │                  │ verbatim check   │
       │                          │                  └────────┬─────────┘
       ▼                          ▼                           ▼
              ┌─────────────────────────────────────┐
              │     Per-variable result with        │
              │   provenance, source, confidence,   │
              │     evidence span (if free text)    │
              └────────────────────┬────────────────┘
                                   ▼
                    ┌─────────────────────────────┐
                    │   Pydantic validation       │
                    │   + missing/imputed flag    │
                    └──────────────┬──────────────┘
                                   ▼
                       Sub-task A (rules) /
                       Sub-task C (CVDRA)
```

The key architectural property: **the LLM only ever sees free text from one of three places (consultation notes, letter bodies, document references) and only ever for variables we have explicitly routed to it.** It is never trusted for structured fields, never trusted to produce a numeric value that goes into PREDICT without symbolic verification, and never asked to perform the gap detection itself.

### 3.3 Structured-field extraction pitfalls (the 12 "easy" variables)

"Deterministic" doesn't mean "trivial". The known pitfalls in NZ PMS records are documented in [[research-r6-data-standards-pms-integration]] and we summarise them here so that the per-variable strategy table in §10 has the right defensive logic.

- **Read v2 → SNOMED CT mapping** is many-to-one and one-to-many. Medtech Evolution writes Read v2 codes natively; SNOMED CT is the modern target. The official Read → SNOMED CT mapping table (UK-derived, last NZ-relevant release via UK Clinical Edition 40.2 June 2025) has known gaps for newer concepts. Pattern: build value sets at the **SNOMED CT** level and map *down* to Read v2 + ICD-10 + ICPC-2 with version-pinned tables, never the other way around. Always retain the original code for traceability.
- **HbA1c units** are now standardised to IFCC mmol/mol in NZ — but historical records (pre-2011) and some legacy lab feeds still report DCCT %. The extractor must check the units field on the observation and reject (or convert) any value where units cannot be confirmed; never silently treat a value as mmol/mol.
- **Lab observations may have multiple results per request** (panel test). Take the most recent finalised result with `status=final`, not preliminary or amended-pending.
- **Blood pressure** can be a single Observation with two component (systolic + diastolic) values, or two separate Observations. ALEX FHIR exposes the component pattern. Rule: prefer the most recent BP that has both components present and a position annotation if available.
- **Smoking status** comes from a coded social-history field in Medtech (current/ex/never), but is often blank or stale. Prefer the most recent coded value; treat absence as "missing" not "never".
- **Active medication** is the trickiest. NZULM-coded MedicationRequest is the right target, but ALEX exposes both repeat-dispensing intervals and active/ceased flags inconsistently. Rule: a medication is "active" if (a) it has an active flag and (b) the most recent dispense or prescribe date is within the prescription's repeat window. Always trace back to the source MedicationRequest ID.
- **Ethnicity** uses HISO 10001:2017 codes. Multiple ethnicities are allowed; PREDICT requires a single category. Apply the standard MoH prioritisation order: Māori > Pacific > Asian > Other > NZ European/Pākehā when a patient has multiple. Never collapse "Indian" into a generic "Asian" — PREDICT v.2019 uses Indian as a separate category because the South Asian risk profile differs materially.
- **Age** is computed from DOB at the date of risk evaluation, not at the current date. This matters for retrospective cohort runs.

---

## 4. Handling the three problem variables (family history, NZDep, AF)

### 4.1 Family history of premature CVD — the only true free-text variable

**Definition.** First-degree relative (father or brother <55, mother or sister <65) with CVD event. NZ PREDICT v.2019 uses this as a binary modifier; the coefficient size is small but non-trivial, especially in younger patients where the absolute baseline risk is low.

**Why it's hard.**
- Structural completeness in primary care records is ~19% globally (Dhiman PLOS ONE 2013, 1.5M-patient THIN study). NZ-specific completeness is unmeasured but anecdotally lower because GP visit time pressure deprioritises FH coding.
- When recorded, it sits in free text in consultation notes, consultation summaries, or specialist letters — not in a coded field. Read v2 has codes for FH (`12C..` family history of stroke, etc.) but they are sparsely used.
- Wording is highly variable: "father had MI age 52", "FHx CVD <60", "dad died of heart attack in his 50s", "no family history of heart disease", "mother angina in 60s" (which is *not* premature).
- Negations and uncertainty are frequent ("no FH of CVD", "FH unclear", "denies FH").

**Primary extractor: BioClinical ModernBERT 396M.** Released June 2025 by LightOn / Rutgers (arXiv 2506.10896), MIT licensed, currently SOTA on clinical NER benchmarks (83.8% DEID F1 large; 90.8% ChemProt F1). 8k context window, encoder-only, runs comfortably on a single L40S 48GB or A100 40GB. We fine-tune on synthetic exemplars first (generated per [[research-r5-synthetic-data-protocol]]) and then on a small set of GP-confirmed real exemplars in Sprint 4. The output is **structured token spans with a normalised label** (`fh_cvd_present_premature`, `fh_cvd_present_non_premature`, `fh_cvd_absent`, `fh_cvd_unknown`).

**Verifier / second opinion: Llama 3.3 70B with constrained decoding.** We feed the same span to a 70B verifier that emits a JSON object with the same label *plus an "evidence_span" field that must verbatim match a substring of the input note*. Constrained decoding via XGrammar (throughput) or Outlines (single-call reliability) ensures the output is always parseable JSON. Disagreement between BioClinical-ModernBERT and the verifier surfaces the patient as `INSUFFICIENT_DATA(reason="conflicting FH extraction; needs GP review")` — that is the safe default for a recall-optimised system.

**Mandatory hallucination controls** (all four required, not pick-and-choose):

1. **Grammar-constrained JSON output** — XGrammar or Outlines pin the schema; no free-form text reaches the consumer.
2. **Evidence-span verbatim verification** — every positive extraction must include a substring of the note that *exactly matches* the evidence; no substring → reject as `INSUFFICIENT_DATA`. Pattern derived from Hybrid-Code v2 (arXiv 2512.23743) and the LLM-Anonymizer architecture (NEJM AI 2024).
3. **Post-hoc Pydantic validation with retry** — if the parsed JSON fails type or enum constraints, retry up to twice; on third failure, route to GP review.
4. **No chain-of-thought.** arXiv 2509.21933 ("CoT degrades clinical text understanding in 86% of LLMs") is conclusive: for *clinical extraction*, asking the model to reason step-by-step before answering reduces accuracy. We use single-shot output for extraction. (CoT remains useful in *separate* downstream tasks like differential diagnosis — not here.)

**Why not "just use the 70B alone".** Encoder NER models are 5–20× cheaper to run, deterministic at fixed seed, and easier to fine-tune on small exemplar sets — exactly the regime we're in. The 70B serves as the verifier specifically because its architectural failure modes are uncorrelated with the encoder's: when both agree, that's a meaningful signal; when they disagree, the disagreement is informative. Running only the 70B doubles cost and forfeits the disagreement signal.

### 4.2 NZDep — pure deterministic geocoding pipeline

**This is not an LLM problem and any attempt to make it one is wrong.** NZDep2018 is published as an open dataset by the University of Otago Health Research Programme (HIRP) at the SA1 (Statistical Area 1) mesh-block level. Two tables: SA1 → NZDep2018 decile, and a code book. Released December 2020. **NZDep2023 is in preparation** by HIRP and not yet released as of April 2026 — we plan a swap-in once it lands.

**Pipeline.**

1. Pull patient residential address from ALEX `Patient.address[use=home]`.
2. Standardise via the NZ Post Address Validation API (or a local copy of the AIMS dataset for offline use).
3. Geocode standardised address → SA1 mesh block via LINZ Address Information Management System or an equivalent NZ-licensed geocoder.
4. SA1 → NZDep2018 decile via the HIRP lookup table.
5. **Fallback**: if address is missing, PO Box only, RD-only, or fails geocoding, default to **NZDep decile 8** with an explicit `imputed=true` flag and an `imputation_reason="address unresolvable to SA1"` field.

The fallback default of **8** is the conservative choice for a recall-optimised tool: it errs toward higher deprivation (and therefore higher recommended action), the inverse direction of the failure mode that under-screens Māori and Pacific patients. The default and its rationale are surfaced in the GP UI per the Wells 2009 JMIR pattern: "NZDep imputed; address unresolvable. Confirm at next visit."

**Privacy.** Geocoding never stores the address against the result; only the SA1 ID and the decile. This satisfies HIPC 2020 Rule 5 (storage minimisation).

### 4.3 AF — code primary, free-text suspect-only

**Definition for PREDICT v.2019.** ECG-confirmed atrial fibrillation, ever. Binary modifier with a substantial coefficient — AF roughly doubles 5-year CVD risk in the equation, so a single false positive systematically over-estimates risk for that patient.

**Coding completeness.** Tomlin 2017 *European Journal of Preventive Cardiology* and the Sandiford 2024 HLC Māori AAA screening audit both estimate ~30% under-coding of AF in NZ primary care, with the gap largest for patients diagnosed in hospital and never re-coded back into the GP problem list. This is an asymmetric error: under-coding hurts recall (we miss high-risk patients). Over-coding from free-text suspect mentions hurts specificity (we over-call AF).

**Strategy: code-primary, free-text suspect-only.**

- **Primary signal (drives PREDICT directly):** SNOMED 49436004 (atrial fibrillation) or any descendant; or Read v2 `G573.` and descendants; or any active medication that is a NZULM-coded oral anticoagulant *with* a problem-list AF entry. A coded entry is taken as confirmed and feeds the calculator.
- **Secondary "suspect AF" signal (NEVER feeds PREDICT):** free-text mentions of "AF", "atrial fibrillation", "irregularly irregular pulse", "ECG showed AF", etc. extracted by the same BioClinical ModernBERT + Llama 3.3 70B verifier pipeline as family history, with the same evidence-span verbatim requirement. Suspect-AF results surface only as a **GP review item** ("Possible undocumented AF for [patient] — please review and confirm or refute"), not as an input to risk calculation. The system makes no attempt to infer ECG confirmation from text — clinical confirmation is the GP's job.
- **Negation handling:** mentions like "no AF", "ruled out AF", "AF excluded on ECG" must be detected and not surfaced as suspect. Standard NegEx-style triggers + the encoder's natural ability to distinguish negated mentions are both used; disagreement → not surfaced.

This is the **inverse** of the QRISK3 default ("assume no AF if not coded"), which under-recalls. Our recall-optimised inverse-bias rule for binary modifiers (§5 / §6) only applies to free-text-derivable variables; for AF specifically, the inverse-bias rule operates by **flagging suspect AF for review**, not by silently defaulting AF=true into the calculator.

---

## 5. Free-text extraction techniques and hallucination control

### 5.1 Why constrained decoding, not "prompt and pray"

A naive LLM extractor — "extract family history of CVD as JSON from this note" — fails three ways even on capable models: it invents fields not present, it produces unparseable JSON, and it produces evidence text that doesn't appear in the source. All three are unacceptable for a calculator that feeds clinical decisions.

**Constrained decoding** (XGrammar, Outlines, or llguidance) constrains the model's token sampling at each step to only tokens that satisfy a target grammar or schema. This guarantees:

- Output is parseable JSON, every time, no retry loop on malformed output
- Field types are enforced at sampling time
- Enum values cannot be hallucinated outside the allowed set
- Evidence-span fields can be constrained to substrings drawn from a provided source token window (an emerging pattern in 2025; see the Hybrid-Code v2 paper, arXiv 2512.23743)

XGrammar (UC Berkeley, vLLM-integrated) is the throughput-optimised choice for batch jobs. Outlines (.txt) is the better single-call reliability choice and integrates more cleanly with structured extraction. Both are MIT/Apache. We default to **XGrammar for register-scan batch extraction and Outlines for single-patient interactive extraction**.

### 5.2 Evidence-span verbatim verification

The single most effective hallucination control for clinical extraction in 2024–2026 published work is *verbatim evidence verification*: every positive extraction must include the substring of the source the extractor used as evidence, and that substring must literally appear in the source. This is enforced at three levels:

1. **At decoding time** — constrained decoding restricts the `evidence_span` field to substrings of the input.
2. **Post-hoc string match** — the consumer code asserts the span is in the source; on failure, reject the extraction.
3. **Span length and locality bounds** — minimum 3 tokens, maximum 30 tokens, must be contiguous; rejects "creative paraphrasing" failures.

If the model cannot produce a verbatim evidence span, the extraction is recorded as `INSUFFICIENT_DATA(reason="no verbatim evidence")` and surfaced for GP review. This is the **single highest-leverage hallucination control** in our stack and applies to family history, suspect AF, and any future free-text variable we add.

### 5.3 Hybrid-Code v2 symbolic verification

For variables that must map to a code (e.g. SNOMED concept ID), the Hybrid-Code v2 pattern (arXiv 2512.23743, late 2025) is the right approach: the LLM proposes a *candidate* code from a constrained vocabulary, and a symbolic verifier checks the candidate against the provided value set + the original text via an external code-set service (we use MedCAT with the UK Clinical Edition 40.2 SNOMED CT release, covered by NZ's national licence). Only candidates the symbolic verifier accepts are written downstream. The pattern reports zero hallucinated codes in their evaluation set.

We adopt this pattern for any extraction where the downstream consumer expects a code (problem list updates, suspect-AF flagging, family-history coding). For pure binary flags (FH present/absent), the simpler evidence-span verification is sufficient.

### 5.4 Local inference and de-identification (LLM-Anonymizer pattern)

All extraction inference runs locally on NZ-sovereign infrastructure (Catalyst Cloud or Bedrock NZ ap-southeast-6 — the choice is made in [[research-r3-architecture-shortlist]] / [[research-r7-open-source-llm-self-hosted]]). The LLM-Anonymizer pattern (NEJM AI 2024) is the published reference for "run local inference on identifiable clinical text without exfiltration" and we adopt its pre-extraction de-identification step for any free-text snippet that ever leaves the practice's tenant boundary — even though our deployment plan is single-tenant, the de-identification step remains as defence in depth.

### 5.5 Why no chain-of-thought for extraction

arXiv 2509.21933 (late 2025) tested 20 LLMs on three clinical text understanding benchmarks with and without CoT prompting; **86% of the models had lower accuracy with CoT than without**. The hypothesis is that CoT introduces additional generation length over which hallucination compounds, and clinical text understanding is a recognition task more than a reasoning task. This is directly applicable to extraction: we want the model to *recognise* a family-history mention, not to *reason* about what one might look like. We use single-shot extraction prompts with constrained decoding throughout.

CoT is appropriate elsewhere (e.g. differential reasoning in inbox triage, where the task is genuinely deductive). It is not appropriate here.

---

## 6. Missing data handling strategy

### 6.1 The four-tier fail-closed architecture

Care Gap Finder is recall-optimised (false negatives are unacceptable). It is also a TGA Class IIa CDS in waiting. Both constraints push the missing-data strategy in the same direction: **fail closed and explain**. The architecture has four tiers, evaluated in order:

**Tier 1 — Hard suppress: CVD equivalents.** Per HISO 10071:2025 §6 and the MoH 2018 CVDRA Consensus, PREDICT does **not apply** to patients with: prior CVD event (MI, stroke, TIA, peripheral vascular disease, revascularisation), eGFR <30 mL/min/1.73m² (CKD stage G4–G5), severe heart failure, familial hypercholesterolaemia, total cholesterol >8 mmol/L, TC:HDL ratio >8, or persistent BP >180/110. Each of these implies the patient is already in the high-risk treatment pathway and the equation is not validated in their range. The pipeline returns **`SUPPRESS_PREDICT(reason=cvd_equivalent_<list>)`** and routes the patient to a "high-risk: PREDICT not applicable, manage per CVD secondary prevention" review.

**Tier 2 — Hard suppress: missing critical demographic.** If age, sex, or ethnicity is missing, **do not impute and do not run**. Berkelmans 2022 (*Journal of Clinical Epidemiology*) demonstrates that imputation of these three variables in CVD risk equations introduces systematic bias, and ethnicity imputation specifically *under-estimates* risk for Māori, Pacific, and Indian patients — the inverse of what an equity-conscious system can tolerate. Return **`SUPPRESS_PREDICT(reason=missing_demographic_<field>)`** and surface as a chart-completion task ("ethnicity missing — please record at next visit").

**Tier 3 — Median impute: non-critical continuous variables.** For SBP, total cholesterol, HDL, the imputation strategy is **population-median imputation by sex and ethnicity stratum**, computed once from a frozen reference cohort and version-pinned to the model release. Berkelmans 2022 shows this is non-inferior to MICE for these variables in CVD risk equations *at single-patient prediction time*, where MICE / multiple imputation is not safely applicable per Hoogland 2020 *Statistics in Medicine*. We add a **missing indicator** alongside each imputed value (per Sisk 2023, missing indicators + imputation outperform imputation alone when missingness is MNAR — which it usually is in primary care). The risk number is always paired with an imputation list in the UI.

**Tier 4 — Conservative-over-estimate: binary modifiers in recall mode.** For smoking status, family history, AF, when these are missing entirely from the record (no coded entry, no extracted free-text mention either way), the system defaults to **"yes" with explicit `imputed=true` and a GP-verify chip** in the UI. This is the **inverse of the QRISK3 default** (which assumes "no" to maximise specificity). We justify the inverse default on three grounds:

- Care Gap Finder is recall-optimised: false negatives (missing a patient who should be reviewed) are categorically worse than false positives (a GP review chip).
- The GP-verify chip is cheap (one click to refute) and the false positive cost is bounded.
- The published equity audit literature (Mehta 2019, Riddell 2018) shows that "assume no" defaults systematically under-screen Māori and Pacific patients because their structural completeness rates are lower. Our inverse default neutralises that bias.

### 6.2 Display rules — never a bare risk number

Wells 2009 *JMIR* proposed (and later validated in Te Whatu Ora's CVD risk dashboard work) that risk scores should never be displayed as a bare percentage. The minimum display unit is:

- The point estimate
- A **confidence band** or qualitative range derived from the imputation count and missingness pattern
- A **missing-variable list** ("BP, smoking status not recorded")
- An **imputed-variable list** ("smoking defaulted to 'current' for safety; please confirm")
- A **suppression banner** if Tier 1 or Tier 2 fired ("PREDICT not applicable: prior MI on problem list — manage per secondary prevention pathway")

We adopt this verbatim and add a **greyscale risk-bar pattern** (per Wells 2009 figure 2) for the visual. The risk number is never the primary visual element; the action recommendation is.

### 6.3 What we explicitly do NOT do

- **No multiple imputation at single-patient prediction time.** Hoogland 2020 demonstrates that MI requires a validated imputation model and that pooling Rubin's rules at a single patient is not statistically defensible. We use median imputation with missing indicators.
- **No drop-and-mean.** PROBAST classifies drop-and-mean imputation as high risk of bias. Tier 2 (suppress) and Tier 3 (median + indicator) replace it.
- **No silent ethnicity imputation.** Even MoH-grade implementations have done this and produced biased outputs against Māori and Pacific. We refuse.
- **No "complete case only" denominator.** Patients with missing data are evaluated, not silently dropped — the `INSUFFICIENT_DATA` outcome from §2.3 surfaces them for chart completion.

---

## 7. Sub-task C — CVDRA calculation (PREDICT v.2019, HISO 10071:2025)

### 7.1 No published Python implementation — clean-room from HISO is the path

The VIEW research group (the team that derived PREDICT) maintains an R package `PredictRiskScores` on GitHub (Pylypchuk et al., release date 2018). It is **GPL-3.0 licensed**. A verbatim port of GPL R code into our Python codebase would taint a closed-source clinical product — we cannot do that. Searching PyPI, GitHub, and Google Scholar for "PREDICT v.2019 Python" / "Pylypchuk Python" / "NZ CVD risk Python" turns up nothing usable as of April 2026.

**Decision: clean-room reimplementation from HISO 10071:2025.** HISO 10071:2025 *Cardiovascular Disease Risk Assessment Standard* is the formal specification. It includes:

- The full equation form (Cox proportional hazards with sex-stratified baseline survival)
- The coefficient tables (~20 coefficients per sex including 3 interaction terms: age×diabetes, age×SBP, SBP×BPlowering)
- Worked examples with input vectors and expected risk outputs, **produced by the HRC-VIEW team specifically for software-supplier validation**
- The CVD-equivalent suppression list and the validity ranges
- The ethnicity category mapping rules

Equation coefficients are **facts published in *The Lancet*** (Pylypchuk et al. 2018, "Cardiovascular disease risk prediction equations in 400 000 primary care patients in New Zealand") and are not copyrightable. The clean-room path is: implement from HISO 10071:2025 + Pylypchuk 2018 *Lancet* tables, validate against the HISO worked examples, dual-run against a containerised R reference for regression. **This produces a clean Python implementation we own outright with no licence contamination.**

### 7.2 Equation reference (for the implementation reviewer)

Coefficients are pulled from Pylypchuk et al. 2018 *Lancet* Tables 2 and 3 (sex-stratified). The model form is:

```
risk_5y(patient) = 1 - S0(sex)^exp(LP - mean_LP(sex))
```

where `LP` is the linear predictor — sum of `coefficient × value` over all 15 inputs and 3 interaction terms. Female baseline 5-year survival `S0_female = 0.983169213058`. Male baseline `S0_male = 0.974755526232`. Mean LPs are also published per sex. Validity range: ages 30–74 inclusive. The full coefficient table is captured in the implementation as a single immutable Python `dataclass`, version-pinned and hashed.

### 7.3 Edge cases and validity rules

- **Age <30 or >79:** suppress with `SUPPRESS_PREDICT(reason=age_out_of_range)`. Age 75–79 is an extrapolation flag (calculator runs but UI banner explains the equation is validated only to 74).
- **Pregnancy:** suppress (not validated; CVDRA is a different pathway).
- **CVD equivalents (§6.1 Tier 1):** suppress.
- **Critical demographics missing (§6.1 Tier 2):** suppress.
- **Imputed continuous (§6.1 Tier 3):** run, surface imputation list.
- **Imputed binary modifiers (§6.1 Tier 4):** run, surface verify chip.
- **Diabetes status:** PREDICT v.2019 has a separate diabetes interaction term — distinct from the diabetes suppression that applies to type 1 diabetes with longstanding albuminuria, which is treated as a CVD equivalent.

### 7.4 Validation strategy — three independent checks

**Check 1: HISO worked-example unit tests.** Every worked example in HISO 10071:2025 becomes a Python unit test. **Required: 100% match to the published expected output**, to the precision the standard gives (typically two decimal places of risk percentage). Any failure blocks release.

**Check 2: Property-based tests via Hypothesis.** For mathematical properties that hold *for all valid inputs*: monotonicity (risk increases with age, holding others constant; risk increases with SBP; risk increases with TC:HDL); bounds (risk ∈ [0, 1]); symmetry (smoker:non-smoker ratio is approximately constant across age strata); and known interaction direction (the diabetes×age interaction reduces the relative effect of diabetes at older ages, as published). Hypothesis generates 1,000+ random valid input vectors per test. This catches off-by-one errors in coefficient indexing that unit tests miss.

**Check 3: 10,000-row R-oracle regression.** A Dockerised R container runs the GPL-3.0 `PredictRiskScores` package as a **black-box oracle** — we never read the R source — and we generate 10,000 synthetic patient vectors covering the full input space, run both implementations, and assert agreement within ±0.5 absolute percentage points on the risk percentage. **Black-box use of a GPL package as a test oracle is licence-clean** (we do not link, redistribute, or derive from the GPL code; we run it in a separate container and compare outputs). The regression test is a CI gate.

**Equity check.** The 10,000-row regression run is repeated stratified by ethnicity (Māori, Pacific, Indian, Chinese/Other Asian, NZ European, Other) with the same ±0.5 pp tolerance per stratum. This is the deliverable that supports the MBIE equity reporting requirement.

### 7.5 What we deliver to the rules engine

Sub-task C exposes a single function:

```python
def calculate_predict_v2019(patient: PatientVector) -> CVDRAResult
```

where `CVDRAResult` is one of:

- `CVDRAResult(risk=Decimal, band="<5%/5-15%/≥15%", imputed_vars=[...], missing_indicators=[...])`
- `Suppressed(reason: SuppressReason, details: str)`
- `InsufficientData(reason: str)`

It is pure (deterministic, no I/O, no clock dependency at the function level), version-pinned, and the entry point that Sub-task A calls when a CVDRA-eligibility rule fires.

---

## 8. PMS integration — Medtech ALEX FHIR API and Indici

### 8.1 Medtech ALEX FHIR API is the only viable primary integration

For a third-party cloud-hosted product that must scan a 2,500-patient enrolled register on a schedule, respect HIPC 2020 boundaries, and run within an MBIE R&D budget, **Medtech ALEX FHIR API is the only viable primary integration path**. The competing options were evaluated and ruled out:

| Option | Verdict | Why |
|---|---|---|
| **Medtech ALEX FHIR API v2.10** | ✅ **Primary** | 261 catalogued endpoints across 24 resource folders; exposes every FHIR resource we need (`Patient`, `Condition`, `Observation`, `DiagnosticReport`, `MedicationRequest`, `DocumentReference`, `Encounter`, `AllergyIntolerance`); Azure AD OAuth 2.0 client credentials; published UAT facilities (`F99669-C` local, `F2N060-E` hosted); supported integration model that is contractually permitted. |
| **Indici / Valentia FHIR** | ⚠️ Sprint 4+ | Valentia Technologies advertises FHIR support but does not publish a public developer portal; access is partnership-gated. Pursue via direct engagement with Valentia in Sprint 4+, not as a Sprint 2/3 dependency. |
| **Direct Medtech32 / Evolution database (ODBC, SQL)** | ❌ Reject | Not contractually permitted for cloud-hosted third parties; bypasses Medtech's data-handling controls; no path to multi-practice scaling. |
| **HL7 v2 outbound mirroring** | ❌ Reject as primary | Useful as a near-real-time *inbound document feed* for Inbox Helper but does not give us patient-list query for Care Gap Finder register scans. Possible secondary feed in Obj 2. |
| **BPAC CareSuite integration** | ❌ Reject | Wrong layer — CareSuite is a competing product, not an integration substrate. Would create a dependency on a competitor's roadmap. |
| **Patient-portal scraping (ManageMyHealth, MyIndici)** | ❌ Reject | Brittle, not contractually permitted, no patient-list semantics. |

### 8.2 ALEX authentication and the BFF requirement

ALEX uses **Azure AD OAuth 2.0 client credentials flow** against tenant `8a024e99-aba3-4b25-b875-28b0c0ca6096` — **not SMART on FHIR Backend Services**. ALEX predates the SMART Backend Services specification and does not implement it. This matters because:

- The standard FHIR client tooling that assumes SMART (e.g. `fhirclient`, `bunsen`, `inferno`) will not work out of the box.
- Token acquisition and refresh follow the Azure AD pattern, not the SMART JWKS pattern.
- **Static IP allowlisting is mandatory**: ALEX requires the calling IP to be on a Medtech-managed allowlist. This forces a Backend-for-Frontend (BFF) deployment pattern — calls cannot be made directly from a serverless function with rotating egress IPs.

We adopt the existing **ClinicPro Capture BFF pattern** (`api.clinicpro.co.nz`) as the integration substrate. The BFF runs on a fixed-IP VM in a NZ region (Catalyst Cloud or Bedrock-NZ-fronted), holds the OAuth client secret in a KMS-backed store, and is the only thing whose IP is on the Medtech allowlist. Care Gap Finder calls the BFF; the BFF calls ALEX.

### 8.3 Scaling pattern: delta-pull, not bulk export

**There is no published `$export` operation in ALEX FHIR API v2.10.** Bulk Data Access ($export) is a 2019 FHIR R4 extension and Medtech has not published support. Until that lands (or is bilaterally negotiated), the scaling pattern is **delta-pull paged search**:

- Cold scan: `Patient?_count=200` paginated for the full register (~13 pages for 2,500 patients), then for each Patient ID, fan-out queries to `Condition?patient=…`, `Observation?patient=…&category=laboratory&_sort=-date&_count=20`, `MedicationRequest?patient=…&status=active`, `DocumentReference?patient=…&_count=10`. Estimated **~12,500 calls for a cold scan of 2,500 patients**.
- Weekly delta: `Patient?_lastUpdated=gt{T-7d}&_count=200` to find patients with any change in the last week, then the same fan-out only for the changed Patients. Estimated **~2,000–3,000 calls for a weekly delta** at typical NZ practice change rates.

### 8.4 Operational unknown: ALEX rate limit

**The single biggest operational unknown is ALEX's unpublished rate limit.** Medtech does not publish a per-tenant rate limit. The only public population-scale ALEX precedent is **Odin Health**, a Medtech partner running register-scale analytics, which appears to operate under a bilaterally-negotiated higher tier. We need to:

1. Make rate-limit confirmation a Sprint 3 prerequisite before any production scan.
2. Build the BFF with explicit token-bucket throttling and exponential backoff out of the gate.
3. Have a written request for rate-limit clarification on the Lisa Pritchard / Medtech engagement track (see §11 open questions).

The realistic worst case is a 5 req/sec ceiling (the typical Azure APIM default), which would make a cold scan ~40 minutes wall-clock and a weekly delta ~10 minutes. Both are tolerable. Anything below 1 req/sec would force a fundamental rethink.

### 8.5 Indici positioning

**Indici (Valentia Technologies) is partnership-gated work for Sprint 4+.** Valentia advertises FHIR but the developer portal is not public and access is granted only through written partnership agreements. The plan:

- Sprint 2/3 ships Care Gap Finder targeting Medtech ALEX only.
- Sprint 4 opens the Valentia engagement (Lisa Pritchard / Callaghan introductions; warm intro via existing Medtech partnership).
- Once the Valentia partnership lands, we add an Indici adapter behind the same internal data model — the BFF and the rules engine do not change.
- Indici is the second priority because Medtech's market share is ~75% and the marginal ROI of the Indici integration is lower per practice.

### 8.6 What ALEX gives us today

Cross-checked against the 261 ALEX endpoints and the resource folders documented in v2.10:

| Need | ALEX path | Status |
|---|---|---|
| Enrolled patient list | `Patient` (paged) | ✅ |
| Active problem list | `Condition?patient=…&clinical-status=active` | ✅ |
| Lab results (HbA1c, lipids, eGFR, ACR) | `Observation?patient=…&category=laboratory` and `DiagnosticReport?patient=…` | ✅ |
| Vital signs (BP, weight) | `Observation?patient=…&category=vital-signs` | ✅ |
| Medications (active) | `MedicationRequest?patient=…&status=active` | ✅ |
| Documents (specialist letters, discharges) | `DocumentReference?patient=…` | ✅ |
| Allergies / adverse reactions | `AllergyIntolerance?patient=…` | ✅ |
| Encounters (visit history) | `Encounter?patient=…` | ✅ |
| Family history (coded, when present) | `FamilyMemberHistory?patient=…` | ⚠️ Available but sparsely populated; free-text fallback per §4.1 |
| Patient address (for NZDep) | `Patient.address` | ✅ |
| Ethnicity (HISO 10001) | `Patient.extension` (NZ profile) | ✅ |
| Bulk export | `$export` | ❌ Not published in v2.10 |

This is enough for the entire Care Gap Finder spec.

---

## 9. End-to-end evaluation protocol

### 9.1 Stage-wise error budgets and waterfall accounting

End-to-end accuracy of Care Gap Finder is the product of accuracy at four stages and is bounded by the worst stage. Per TRIPOD+AI 2024 (Collins et al., PMC11019967) and DECIDE-AI 2022 (Vasey et al., *Nature Medicine*) we decompose the pipeline into **stage-wise error budgets**:

| Stage | Symbol | Budget (target) | What it measures |
|---|---|---|---|
| PMS data quality | ε_data | ≤2% | Patients with critical-field gaps in ALEX feed (chart-completion task list) |
| Sub-task A — gap detection (rules) | ε_A | ≤1% | Disagreement with handcrafted gold-standard rule outcomes on synthetic test vectors |
| Sub-task B — variable extraction | ε_B | ≤5% (free-text variables) | Disagreement with GP-confirmed labels on free-text family history and suspect-AF; structured variables ≤0.5% |
| Sub-task C — CVDRA calculation | ε_C | ≤0.5 absolute pp risk | Agreement with VIEW R reference oracle on identical input vectors |

The end-to-end target is ε_total ≤ 8% pipeline disagreement with the dual-blind chart review, with stage-wise bounds enforced as CI gates so a regression in Sub-task B cannot silently consume Sub-task C's budget.

### 9.2 Gold standard: dual-blind clinician chart review

For the externally-validated end-to-end metric, we run a **dual-blind chart review**:

- **n ≥ 400** patient charts, stratified across 3–5 pilot practices, stratified by ethnicity (Māori, Pacific, Indian, Chinese/Other Asian, NZ European/Other) and by clinical stratum (diabetic, hypertensive, prior CVD, healthy adult). 400 is the lower bound for an 8 pp two-sided CI on the worst-cell sensitivity at α=0.05.
- **Two GPs review each chart blinded to each other** and to Care Gap Finder's output, recording the gap list and the CVDRA risk band.
- **A third senior GP adjudicates disagreements** (consensus reviewer pattern from CMS eCQM validation studies).
- **Inter-rater agreement target: Cohen's κ ≥ 0.70** (substantial agreement) on the gap list, with **Gwet's AC1 reported alongside as a prevalence-robust check** (κ degrades pathologically when prevalence is very low or very high — Gwet's AC1 is the standard correction).
- Care Gap Finder's outputs are then compared to the adjudicated consensus for sensitivity, specificity, PPV, NPV per rule.

### 9.3 Per-rule recall metrics with bootstrap CIs

For each gap-detection rule, we report:

- **Sensitivity ≥ 0.95** (per-rule), with **5,000-resample BCa bootstrap 95% CI**. The lower bound of the CI is the metric of record — recall-optimised systems live or die by the lower CI bound, not the point estimate.
- **NPV ≥ 0.99** (per-rule). NPV is the most recall-critical metric: when the system says "no gap", the GP needs to be able to trust that, and 1-in-100 is the absolute floor.
- **PPV ≥ 0.60** (per-rule). PPV is the GP-burden metric: a PPV below 0.60 means more than 4 in 10 surfaced patients are false positives, which destroys clinician trust faster than missing a true positive.
- **NNS (Number Needed to Surface) < 20** for common rules, **< 200** for rare rules. NNS = 1/PPV; it answers "how many patients does the GP have to review to find one true gap?". Common-rule NNS in the 5–10 range is the adoption sweet spot; >20 is review fatigue.

### 9.4 Adoption gate: GP review burden

Per the pilot-practice clinical advisory feedback (Sprint 1 outreach task `rd-20260405-001`), the operational adoption gate is:

> **<10 false-positive surfacings per 2,500-patient register per week.**

This is the all-rules aggregate FP rate the practice can tolerate before review fatigue sets in. It is the single most important non-technical metric and dominates the per-rule PPV targets in the rollout decision.

### 9.5 Sub-task C — calibration in addition to point accuracy

For CVDRA specifically, point accuracy (±0.5 pp vs VIEW R reference) is necessary but not sufficient. We also report:

- **Brier score ≤ 0.12** on the chart-review cohort (calibration + discrimination combined; the published PREDICT v.2019 derivation cohort Brier is ~0.10).
- **Calibration slope ∈ [0.9, 1.1]** on the chart-review cohort. A slope <1 indicates the model is over-confident at the extremes; >1 indicates under-confident.
- **Calibration plot** (decile-based, with 95% CI bands) included in the equity report.

### 9.6 Equity reporting (MBIE deliverable)

Per the MBIE Capability Development equity requirement, the evaluation report breaks every metric out by ethnicity stratum (Māori, Pacific, Indian, Chinese/Other Asian, NZ European/Other), with:

- **Subgroup gap < 5 percentage points** between worst and best stratum on per-rule sensitivity. A gap >5 pp blocks deployment until the gap is closed.
- Stratified Brier and calibration slope for CVDRA.
- Stratified PPV and NNS for the gap-detection rules.
- An explicit narrative section in the report on the inverse-bias decisions in §6.1 Tier 4 and their measured equity effect.

### 9.7 Reporting framework

The full evaluation report is structured per **TRIPOD+AI 2024** for the model card and **DECIDE-AI 2022** for the deployment context. Both are required reading for the Care Gap Finder evaluation lead. The report is the deliverable for the rd-20260329-011 data requirements task downstream and feeds the MBIE Q1 progress report due 31 May.

---

## 10. Per-variable strategy table — 15 PREDICT inputs and care-gap auxiliaries

Source columns: **A** = ALEX FHIR resource, **C** = code system, **R** = routing decision, **N** = notes / pitfalls.

### 10.1 PREDICT v.2019 inputs (15)

| # | Variable | A | C | R | N |
|---|---|---|---|---|---|
| 1 | Age | `Patient.birthDate` | — | Deterministic | Computed at risk-eval date, not today |
| 2 | Sex | `Patient.gender` | FHIR AdministrativeGender | Deterministic | Tier 2 suppress if missing |
| 3 | Ethnicity | `Patient.extension[NZ-ethnicity]` | HISO 10001:2017 | Deterministic + prioritisation | Māori>Pacific>Asian>Other>European; Indian separate |
| 4 | Diabetes status | `Condition?clinical-status=active` | SNOMED CT 73211009+ / Read C10F* | Deterministic | Distinguish T1 long-standing albuminuric (CVD-equiv suppress) from T2 (interaction term) |
| 5 | Smoking status | `Observation?code=smoking-status` | SNOMED CT 365981007+ | Deterministic, conservative imputation | Tier 4 inverse default if missing entirely |
| 6 | Systolic BP | `Observation?category=vital-signs&code=85354-9` (component) | LOINC | Deterministic, median impute if missing | Most recent observation with both components present; reject SBP>180 → CVD-equiv suppress |
| 7 | Total cholesterol | `Observation?category=laboratory&code=2093-3` | LOINC | Deterministic, median impute if missing | TC>8 → CVD-equiv suppress |
| 8 | HDL | `Observation?category=laboratory&code=2085-9` | LOINC | Deterministic, median impute if missing | — |
| 9 | TC:HDL ratio | Computed from #7 / #8 | — | Deterministic | TC:HDL>8 → CVD-equiv suppress |
| 10 | BP-lowering medication | `MedicationRequest?status=active` | NZULM / SNOMED CT therapeutic class | Deterministic | Class match against curated value set; uses SBP×BPlowering interaction term |
| 11 | Lipid-lowering medication | `MedicationRequest?status=active` | NZULM / SNOMED CT | Deterministic | — |
| 12 | Antithrombotic medication | `MedicationRequest?status=active` | NZULM / SNOMED CT | Deterministic | Antiplatelet OR anticoagulant; cross-check with AF for confirmation signal |
| 13 | **Family history of premature CVD** | `FamilyMemberHistory?` (sparse) + free text fallback | Read 12C* / SNOMED 215011000000100 | **Free-text extractor** (BioClinical-ModernBERT + Llama 3.3 70B verifier) | The only true NLP variable; ~19% structural completeness; conservative default if missing |
| 14 | **AF (ECG-confirmed)** | `Condition?` + `MedicationRequest?` cross-check | SNOMED 49436004 / Read G573* | **Code-primary, free-text suspect-only** | ~30% under-coding; suspect-AF flags GP review only, never feeds calculator silently |
| 15 | **NZDep** | `Patient.address` | NZDep2018 (Otago HIRP) | **Deterministic geocoding pipeline** | Address → SA1 → decile; default 8 if unresolvable |

### 10.2 Care-gap rule auxiliary variables

These are not PREDICT inputs but are used by the rules engine for non-CVDRA gaps (HbA1c, BP, eGFR/uACR, foot/eye exam, etc.):

| Variable | A | C | R | N |
|---|---|---|---|---|
| HbA1c | `Observation?code=4548-4` | LOINC | Deterministic | IFCC mmol/mol; reject if units field unparseable |
| eGFR | `Observation?code=33914-3` | LOINC | Deterministic | <30 → CVD-equiv suppress for PREDICT |
| ACR (urine albumin:creatinine) | `Observation?code=14959-1` | LOINC | Deterministic | KDIGO 2013 matrix |
| Diastolic BP | Component of #6 | LOINC | Deterministic | — |
| Weight / BMI | `Observation?category=vital-signs` | LOINC | Deterministic | — |
| Foot exam (diabetes annual) | `Observation?` or `Procedure?` | SNOMED CT | Deterministic | NZSSD annual review component |
| Retinal screening (diabetes) | `Observation?` or external retinal screening service feed | SNOMED CT | Deterministic | Outside-PMS feed common; allow stale-date import |
| Palliative care status (DEX) | `Condition?` + advance care plan flag | SNOMED CT | Deterministic | Hard exclusion |
| Opted out of recall | Patient flag (Medtech-specific extension) | — | Deterministic | Hard exclusion |
| Deceased | `Patient.deceasedBoolean` / `Patient.deceasedDateTime` | — | Deterministic | Hard exclusion |

---

## 11. Open questions for Medtech and Valentia integration teams

These are the items we cannot resolve from public documentation and need to put on the Sprint 3 / Sprint 4 engagement track. Lisa Pritchard (Callaghan) is the natural warm intro.

### 11.1 For Medtech (Sprint 3)

1. **ALEX FHIR API per-tenant rate limit** — what is the documented or contractually-supported rate ceiling? Is there a Partner / Enterprise tier (cf. the Odin Health precedent)? Token bucket vs sliding window vs fixed?
2. **Bulk Data Access (`$export`)** — is `$export` on the v2.11+ roadmap? If not, is a bilateral arrangement available for register-scale partners?
3. **Static IP allowlist process** — what is the SLA for adding/changing allowlisted IPs? We will need a path for failover IPs.
4. **OAuth tenant boundary** — is there a per-practice or per-tenant token, or one set of credentials for the partner spanning all enrolled practices? Confirm token scoping.
5. **Family history coding** — does Medtech have a recommended coding workflow / template for `FamilyMemberHistory` that we should be promoting to participating GPs?
6. **NZ FHIR profile** — is there an authoritative ALEX FHIR profile published, or is the resource shape "AU Core ± Medtech extensions"? We need the StructureDefinition for our codegen pipeline.
7. **Patient.deceased field reliability** — is this field reliably maintained, or do we need to cross-check against a date-of-death code in `Condition`?
8. **Audit / log expectations** — what audit telemetry does Medtech expect a partner to surface back to a practice administrator? Any partner-portal requirements?

### 11.2 For Valentia / Indici (Sprint 4)

1. **Developer portal access** — partnership terms for Indici FHIR API access; cost; NDA boundaries.
2. **FHIR resource coverage** — is the resource list congruent with ALEX (Patient, Condition, Observation, MedicationRequest, DocumentReference)?
3. **Indici problem-list semantics** — Indici claims a more modern problem-list model than Medtech; we need to confirm whether SNOMED CT is the native code system and whether the Read v2 mapping is required.
4. **Throughput for register-scale scans** — same question as Medtech: is bulk export available, or is paged search the path?
5. **Authentication model** — OAuth, mTLS, or other? Does it require a fixed-IP BFF like ALEX?

### 11.3 For HISO / MoH (Sprint 3)

1. **HISO 10071:2025 worked-example test vectors** — confirm we have the latest published vector set and that our 100%-match test passes against it.
2. **NZDep2023** — release timing; we want to be ready to swap NZDep2018 → NZDep2023 in the geocoding pipeline within one sprint of release.
3. **PREDICT v.2019 — minor errata** — has any errata been published since the 2018 *Lancet* paper that affects coefficients or interaction terms?

### 11.4 For Te Whatu Ora / NEAC (Sprint 4)

1. **DPIA expectations for AI-CDS** — are there any deliverable templates we should adopt (referenced in [[research-r2-nz-sovereign-hosting-regulatory]])?
2. **Equity reporting standard** — confirm the ethnicity stratification categories and the gap thresholds the MBIE Capability Development equity deliverable expects.

---

## 12. References

### Equations, standards, guidelines

- HISO 10071:2025 *Cardiovascular Disease Risk Assessment Standard*. Health Information Standards Organisation, NZ.
- HISO 10001:2017 *Ethnicity Data Protocols*. Health Information Standards Organisation, NZ.
- HISO 10029:2022 *Health Information Security Framework*. Health Information Standards Organisation, NZ.
- Pylypchuk R, Wells S, Kerr A, Poppe K, et al. *Cardiovascular disease risk prediction equations in 400 000 primary care patients in New Zealand: a derivation and validation study*. Lancet 2018; 391: 1897–1907.
- Ministry of Health (2018). *Cardiovascular Disease Risk Assessment and Management for Primary Care*. Wellington: MoH.
- BPAC NZ (March 2023). *Diabetes management toolbox*.
- NZSSD (October 2021). *Type 2 Diabetes Management Guidance*.
- KDIGO 2013 *Clinical Practice Guideline for the Evaluation and Management of Chronic Kidney Disease*.
- Wells S, et al. (2009). *PREDICT-CVD: a web-based decision support tool*. JMIR.
- HL7 *Clinical Quality Language (CQL) Specification* v1.5 (normative).
- CMS *Electronic Clinical Quality Measures (eCQM) Implementation Guide*.

### Missing data + imputation

- Berkelmans GFN, et al. (2022). *Imputation of missing data for personalised cardiovascular risk prediction*. Journal of Clinical Epidemiology.
- Hoogland J, et al. (2020). *Handling missing predictor values when validating and applying a prediction model to new patients*. Statistics in Medicine.
- Nijman SWJ, et al. (2021). *Missing data imputation strategies for clinical prediction models in EHR data*. European Heart Journal — Digital Health.
- Sisk R, et al. (2023). *Imputation and missing indicators for handling missing data in clinical prediction*. Statistics in Medicine.
- Mehta S, Wells S, et al. (2019). *Under-screening for CVD risk in Māori and Pacific*. NZMJ.
- Riddell T, et al. (2018). *Cardiovascular risk assessment equity audit*. NZMJ.
- Wolff RF, Moons KGM, Riley RD, et al. (2019). *PROBAST: A Tool to Assess the Risk of Bias and Applicability of Prediction Model Studies*. Annals of Internal Medicine 170:51–58.

### LLM extraction, hallucination control, clinical NLP

- BioClinical ModernBERT (LightOn / Rutgers, June 2025). arXiv 2506.10896.
- Hybrid-Code v2: zero-hallucination clinical code extraction (late 2025). arXiv 2512.23743.
- *Chain-of-thought degrades clinical text understanding* (2025). arXiv 2509.21933.
- LLM-Anonymizer: local-inference de-identification of clinical text. NEJM AI 2024.
- XGrammar: high-throughput grammar-constrained LLM decoding (vLLM-integrated, 2024).
- Outlines: structured output for LLMs. .txt.
- MedCAT (Medical Concept Annotation Toolkit), UK Clinical Edition 40.2 (June 2025).
- Dhiman P, et al. (2013). *Completeness of family history data in routine UK general practice*. PLOS ONE.
- Tomlin A, et al. (2017). *Atrial fibrillation under-coding in NZ primary care*. European Journal of Preventive Cardiology.
- Sandiford P, et al. (2024). *Health Loss in Communities — Māori AAA screening audit*. HLC.

### Reporting frameworks and evaluation

- Collins GS, Moons KGM, Dhiman P, et al. (2024). *TRIPOD+AI statement: updated guidance for reporting clinical prediction models*. BMJ. PMC11019967.
- Vasey B, et al. (2022). *DECIDE-AI: reporting guideline for the early-stage clinical evaluation of decision support systems driven by artificial intelligence*. Nature Medicine.
- Gwet KL (2008). *Computing inter-rater reliability and its variance in the presence of high agreement*. British Journal of Mathematical and Statistical Psychology.

### PMS integration

- Medtech ALEX FHIR API v2.10 — internal documentation referenced; public landing at developer.medtech-global.com.
- Odin Health (Medtech ALEX integration partner) — public case study material.
- HL7 FHIR R4 *Bulk Data Access (Flat FHIR)* IG.
- SMART App Launch Framework — *Backend Services Authorization* profile (for contrast with the Azure AD pattern ALEX uses).

### Cross-references in this vault

- [[research-r1-llm-architecture-benchmarks]] — clinical LLM architecture benchmarks (2024–2026)
- [[research-r2-nz-sovereign-hosting-regulatory]] — sovereignty + regulatory posture
- [[research-r3-architecture-shortlist]] — head-to-head architecture shortlist
- [[research-r7-open-source-llm-self-hosted]] — open-source self-hosted LLM track
- [[care-gap-finder-task-spec]] — Care Gap Finder task specification (Sprint 1, final)
- [[inbox-helper-task-spec]] — Inbox Helper task specification (Sprint 1, final)
- [[nz-cardiovascular-risk-assessment]] — NZ CVDRA clinical reference
- [[nz-diabetes-monitoring]] — NZ diabetes monitoring intervals reference
- [[nz-hypertension-monitoring]] — NZ hypertension monitoring reference
- [[manual-care-gap-monitoring]] — current NZ practice workflow reference
- [[research-r5-synthetic-data-protocol]] — synthetic data protocol (pending)
- [[research-r6-data-standards-pms-integration]] — FHIR/HL7/code-set deep dive (pending)
