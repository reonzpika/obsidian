# ClinicPro Design Research

> Research basis for all decisions in `clinicpro-design-system.md` and `colour-options.md`.
> Date: April 2026. Sources listed at end of each section.
> Do not modify this file — it is a research record, not a living document.

---

## 1. Colour Psychology in Healthcare UI

### Why blue dominates — the mechanism

Blue is entrenched in healthcare for measurable physiological reasons, not arbitrary convention.

**Neurophysiological effect:**
- Blue demonstrably lowers heart rate, blood pressure, and respiratory rate — creating a calming parasympathetic response
- 60% of healthcare apps use blue as primary colour
- 78% of patients prefer "professional, calming" app designs (Journal of Medical Internet Research)
- Blue's prevalence creates learned association: patients now expect blue = healthcare, reinforcing familiarity and trust

**The psychological layer:**
- Trust is the primary mechanism — Adobe studies consistently rank blue highest for trust across industries
- Blue signals professionalism and hygiene, critical for medical contexts
- Cultural consistency: blue reads as calm and stable across age groups and cultural backgrounds

### Teal, green, and blue — differentiated roles in clinical context

Teal + green + blue account for 62% of healthcare website colour choices. They serve distinct functions:

- **Blue (primary):** Primary actions, structural elements, authority, main navigation
- **Green (secondary):** Success states, confirmed actions, approved data, positive outcomes. 22% adoption vs 60% for blue — stands out while remaining clinically credible
- **Teal (accent):** Filtered/clean aesthetic (mimics clinical lighting), patient portals, data clarity panels, secondary information

**Psychological differentiation:**
- Blue is more "mentally stimulating" while calming cardiovascular response
- Green is stabilising, encourages balance and reassurance
- Teal signals cleanliness and precision — useful for technical/data-heavy contexts

### Colours to avoid — evidence-based rationale

**Red / vivid orange / bright yellow:** Elevate anxiety, trigger stress responses, elevate heart rate — physiologically opposite of the desired effect. Reserve red for errors and destructive actions only; never as a brand or accent colour.

**Deep purple / high-saturation colours:** Overwhelming and potentially agitating in clinical environments where cognitive load is already high.

**Sterile white alone:** Paradoxically problematic — creates anxiety and impersonality. Pair white with warm neutrals (soft grays, subtle warm tones).

**Amber as primary:** Amber carries traffic-light/warning associations. If used as brand primary, semantic separation from warning amber must be explicit and rigorously maintained.

### Colour contrast and accessibility

- 300 million people globally have colour blindness — colour cannot be the sole information carrier (WCAG 2.2 success criterion 1.4.1)
- Colour contrast is the #1 web accessibility violation (83.6% of websites fail this)
- Minimum standard: 4.5:1 contrast ratio for normal text (WCAG AA); healthcare should target WCAG AAA (7:1) for clinical data
- Readability increased by 60% with proper colour contrast

**Sources:** Journal of Medical Internet Research; Adobe Colour Trust Studies; UXMatters (2024); Progress Blog; Naskay (2025); WCAG 2.2; Section508.gov

---

## 2. Typography in Healthcare and Professional Software

### Serif vs sans-serif for clinical tools

**Sans-serif is the universal standard for clinical software.** Clear rationale:
- Reduces misreading risk (critical for medication dosages, NHI numbers, clinical data)
- Better screen readability than serif
- Faster scanning under time pressure
- Modern medical institutions use sans-serif for patient-facing and clinical data interfaces

**Serif** (Georgia, Libre Baskerville): Traditional institutional authority. Appropriate for branding/print. NOT recommended for body text on screens or clinical notes.

### Character legibility in clinical contexts

Character distinction matters in medical contexts. Clear letterforms prevent dangerous misreading:
- Distinct characters — avoid "I/l/1" confusion (critical for medication dosages)
- High-contrast letterforms (thick strokes preferred)
- Ample letter spacing reduces eye strain and speeds accurate reading
- Minimum 16px for web UI interfaces (US Health Literacy guidelines)

### Specific font recommendations for clinical/professional software

**Inter** — Research-validated top choice for clinical software
- Humanist sans-serif designed specifically for screen rendering at small sizes
- Outperforms Roboto and Open Sans at 12-16px for readability
- Balances clinical precision with human warmth (humanist approach)
- Specifically praised for rendering on pixel grids
- Excellent WCAG compliance
- "Originally forked from Roboto but optimised for readability at small sizes"

**Roboto** — Acceptable alternative
- Geometric, clinical efficiency, widely recognised as "professional"
- Good for institutional, serious medical contexts
- Slightly condensed appearance conveys efficiency
- Inter outperforms it at small sizes

**Source Sans Pro** — Purpose-built for information clarity
- Designed for legibility in professional contexts
- Open apertures reduce eye strain
- "Information clarity takes priority" — explicitly mentioned in medical typography research

**Open Sans** — Decent, used widely
- Sophisticated, modern
- Inferior to Inter for clinical UI but acceptable for marketing copy

**Merriweather** — Only recommended serif for clinical use
- "Designed specifically for comfortable screen reading over extended periods"
- If a serif heading font is required, this is the safest clinical choice

### Display fonts for marketing (not in-app clinical UI)

Condensed display fonts (e.g. Oswald) are appropriate for large marketing headings where visual hierarchy matters. **Not appropriate for in-app clinical UI** — condensed letterforms are harder to scan under time pressure at smaller sizes.

### Geometric vs humanist sans-serif

- **Geometric** (Roboto, Montserrat): Clinically precise, neutral, unconcerned with aesthetics. Feels institutional.
- **Humanist** (Inter, Open Sans): Warm, thoughtful, designed-for-humans. Feels modern trustworthy.
- **For clinical tools:** Lean geometric when emphasising precision and safety. Humanist when emphasising patient comfort and modern trustworthiness. Inter sits at the ideal intersection.

### Technical typography standards for clinical contexts

| Parameter | Standard |
|-----------|----------|
| Minimum body font size | 16px |
| Line height | 1.5–1.6x font size (`leading-relaxed`) |
| Letter spacing | Generous — never tight for body text |
| Preferred weights | 400 (body), 500 (labels), 600 (emphasis), 700 (headings) |
| Avoid | Light (300) weights — poor legibility in clinical lighting |
| Avoid | Condensed fonts for body/data text |

**Sources:** Letter Hend; FontAlternatives; Digital Arcane; What Font Is; Dogtown Media; PubMed PMC (readability in EHR); CJNI (EHR usability); Mockplus; Designshack

---

## 3. GP Workflow UX Psychology

### Cognitive load in clinical settings

**Critical finding:** For every 8 hours of scheduled patient time, office-based physicians spend 5+ hours in EHR systems. This creates a two-front cognitive burden: patient interaction + system navigation simultaneously.

**Actionable principles:**
1. **Progressive disclosure** — surface only what's needed for the current decision point. Clinical decision-making is sequential (triage → examination → diagnosis → action), not parallel.
2. **Task-aligned hierarchy** — clinicians scan for actionable information in ~5-second intervals during consultations. Critical alerts must be spatially prominent without scrolling.
3. **Minimal clicks** — 2-3 clicks maximum for common actions. Reducing clicks significantly reduces cognitive load.
4. **Predictability and transparency** — clinicians reject systems that automate or default unexpectedly. Every automatic action must be transparent: show what changed, why, and give immediate override control.

### Gaze patterns during consultations

GPs operate under divided attention — maintaining eye contact with patients while managing digital systems. This is not a "fully focused on screen" interaction:

- Clinicians use "rapid glance-and-verify" patterns (5–10 second screen bursts) interspersed with patient observation
- Prolonged screen focus (>20 seconds) breaks patient rapport
- Critical information must be retrievable in a single visual field — no navigation or scrolling required
- Interruption resilience is essential — consultations are constantly interrupted

### What clinicians complain about most (EHR research)

1. **Workflow misalignment** — systems don't match how doctors actually work. Mental model mismatch creates friction.
2. **Alert quality** — inadequate, absent, or ambiguous alerts. Alert fatigue from false positives causes clinicians to ignore genuine alerts.
3. **Interoperability gaps** — hunting for data from other systems breaks the consultation workflow.
4. **Unpredictable automation** — auto-populated fields without explicit clinician action are cited as safety risks.

**Safety link:** Poor EHR usability directly correlates with missed safety catches. Systems with poor UX are less likely to flag harmful medication errors or drug interactions.

### Mobile vs desktop in clinical practice

**Major shift:** Smartphones and tablets are now preferred over desktop at point-of-care. 73% of clinicians say mobile is easier, 70% say faster than finding a desktop.

| Mobile use case | Desktop use case |
|-----------------|-----------------|
| Quick reference during consultation | Full consultation notes |
| Drug lookup, dose checking | Medication reconciliation |
| Image capture (clinical photos) | Complex patient record review |
| Rest home visits (no desktop available) | Administrative tasks |

**Design implication:** Design for complementary use — mobile for in-consultation quick reference, desktop for post-consultation documentation. Not one-or-the-other.

**Impact figures:**
- 84% increased job satisfaction with tablet use
- 51% reduction in time at hospital/clinic
- 65% improved care quality perception (self-reported)

### Trust signals for clinicians (vs consumer apps)

Clinicians evaluate trust differently from consumers. Polished consumer apps with gamification or playful tone read as NOT SERIOUS to medical professionals.

**What builds trust:**
1. **Explainability** — show WHY something is flagged, with confidence level and source reference
2. **Absence of flashiness** — cluttered interfaces and excessive interactive feedback reduce trust scores in clinical software
3. **Consistency and predictability** — same buttons, same places, same workflow every time
4. **Data source credibility** — "where is this from? is it current? is it reputable?"
5. **No automation without consent** — full transparency + control = trust
6. **Professional tone** — clear, specific, jargon-appropriate, action-oriented. Never casual.

**Sources:** Asahi Technologies; Design Bootcamp (Medium); PMC eye-tracking studies; AMA (EHR usability challenges); PMC usability challenges (2025); PMC EHR patient harm contribution

---

## 4. NZ and Australia Cultural Context

### Colour preferences and professional associations

**Australia:**
- 85% of leading healthcare companies use blue — industry standard, not distinctive
- Green (secondary): only 22% adoption, calming and health-associated but less common in clinical software
- Neutral palettes preferred: blues, greys, whites — professional standard
- Bright/loud colours feel out of place in medical settings

**New Zealand:**
- Nature/green associations: NZ design leans into native bush and natural greens — culturally resonant
- Māori cultural integration: Te Reo Māori and Tikanga concepts increasingly standard in professional NZ software
  - **Whakawhanaungatanga** (building relationships/trust through connection) — should inform interface tone
  - **Manaakitanga** (hospitality/care/respect) — make users feel respected, not rushed
  - Māori colour tradition: earth tones, greens, blacks — connection to land
- NZ Government digital design standard specifies interactive/active blue for clickable elements — a local standard worth following for credibility with NZ organisations

### Trust signals and formality

**New Zealand:**
- Trust based on integrity, not status — Kiwi professionals trust software that is honest about limitations and shows genuine care for their workflow
- Inform, don't command — use "softeners": "Consider reviewing..." not "ERROR: Review now"
- Meritocracy over hierarchy — treat GPs as experts: show reasoning, offer recommendations, let them decide
- Openness and collaboration — share information fully, avoid feature gatekeeping
- Cultural inclusivity — including Te Reo Māori terms and Māori health concepts (holistic, whānau-centred) matters for trust

**Australia:**
- Trust through competence — prioritise demonstrated expertise and evidence-based credentials
- Straightforward communication — direct, no-nonsense, no flowery language
- Practical focus — "does it work?" matters more than "does it look good?" Show proven workflow improvements
- Speed signals professionalism — slow software reads as broken or unreliable
- Authentic imagery — real clinic spaces and actual staff, not stock photography

### Tone and messaging by market

**NZ:** Warm professionalism. Collaborative framing. "Let's review this" not "You must do this." Avoid corporate-speak — Kiwis distrust marketing jargon. Acknowledge Māori health concepts where relevant.

**AU:** Direct, clear, action-oriented. Lead with clinical evidence and credentials. Brief, to-the-point. Emphasise practical benefits and workflow improvement.

**Both markets shared:** Avoid exclamation marks in clinical context. Avoid flowery or emotional language. Avoid stock photography. Lead with what the tool does, not how innovative it is.

**Sources:** Cultural Atlas / SBS (NZ Business Culture); Ministry of Education NZ Design System; PMC (Māori-centred relational health model); Sprypt (visual trust signals); Curogram (patient trust through digital communication); Global Health Education (AU communication styles)

---

## 5. Summary: Key Decisions the Research Informs

| Question | Research verdict |
|----------|-----------------|
| Blue as primary? | Valid but not original — 60% adoption means no differentiation |
| Green viable? | Yes — 22% adoption, health associations, NZ resonance. Use deep shades only |
| Teal viable? | Yes — clinical precision signal. Common enough that it doesn't fully differentiate |
| Indigo viable? | Yes — spectrally adjacent to blue (residual trust), completely unused in healthcare |
| Slate as primary viable? | Yes, with disciplined execution — premium editorial, requires perfect typography/spacing |
| Amber as primary viable? | Risky — semantic separation from warning amber required; most original but hardest to implement |
| Purple? | No — overwhelming in high-cognitive-load clinical contexts |
| Pastel? | No — signals unserious |
| Best body font? | Inter — research-validated for screen readability at small sizes in clinical contexts |
| Display font for marketing? | Strong condensed sans-serif acceptable at large sizes (Oswald viable) |
| Condensed for body/UI text? | No — harder to scan under time pressure |
| Light font weights (300)? | No — poor legibility in clinical lighting |
| Animations? | Purposeful only — clinicians find excessive animation untrustworthy |
| Mobile vs desktop priority? | Both — mobile for consultation, desktop for documentation. Not one-or-the-other |
| NZ/AU shared approach? | Blue OR deep green + neutral palette. Direct tone. No jargon. Speed matters |
