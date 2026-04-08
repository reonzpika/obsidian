---
title: Nano Banana Pro — Prompt Engineering Research
type: reference
created: 2026-04-08
updated: 2026-04-08
purpose: Durable reference for crafting photorealistic image prompts using Google's Nano Banana Pro (Gemini 3 Pro Image) model.
---

# Nano Banana Pro — Prompt Engineering Research

A working reference for generating photorealistic clinical and editorial imagery for ClinicPro marketing pages and product mockups. Built specifically around the Referral Images landing page, but the principles transfer to any future image generation work in the vault.

---

## 1. What it actually is

**Nano Banana Pro** is Google's marketing name for **Gemini 3 Pro Image**, released November 2025. It is the flagship image generation and editing model in the Gemini family, distinct from the smaller "Nano Banana" (Gemini 2.5 Flash Image).

**Key capabilities relevant to this work:**

- Up to **4K resolution** native output (2K and 1K also supported)
- Up to **14 reference images** in a single prompt for style/character consistency
- **5-character consistency** in a single scene (multiple people, same identities)
- Native text rendering inside images (signage, labels, handwriting on paper)
- Reference-image-driven editing, in-painting, out-painting
- World knowledge from the Gemini 3 base model — understands real cameras, real lenses, real film stocks, real lighting setups

**Where to access it:**

- Gemini app (free tier — limited)
- Google AI Studio (free with quota; the easiest place to test prompts)
- Vertex AI (`gemini-3-pro-image` endpoint, billed per image)
- Google Workspace integrations

For ClinicPro marketing work the workflow is: draft prompt in this file, paste into AI Studio, generate 4-6 variations, pick best, refine via reference-image input.

---

## 2. The 7-part prompt template

The single most reliable structural pattern across all the working examples is a 7-part body. Skipping any one part is the most common cause of generic AI-looking output.

| # | Slot | What goes here | Example |
|---|---|---|---|
| 1 | **Subject** | Who or what, in concrete terms — age range, clothing, posture, gesture | "A woman in her late thirties wearing a soft cream knit sweater, sitting at a low pine table" |
| 2 | **Scene** | The space around the subject — surfaces, props, depth cues, what's behind them | "A north-facing window behind her left shoulder, a single linen tea towel folded on the table edge" |
| 3 | **Lens / aperture / camera body** | A real camera, a real focal length, a real aperture | "Shot on Leica Q2, 28mm Summilux at f/1.7, ISO 400, 1/200" |
| 4 | **Lighting direction** | Where the light comes from, what quality it has, what time of day | "Diffuse window light from camera-left, late morning, no fill, gentle shadow falloff onto the table" |
| 5 | **Materials and textures** | Cotton, oak, ceramic, brass, brushed metal, etc. — name the materials explicitly | "Unvarnished oak, ceramic mug with hairline crackle glaze, slightly creased linen" |
| 6 | **Colour grade** | The colour treatment, often expressed as a film stock or a publication style | "Kodak Portra 400 colour science, gentle warm midtones, no contrast crush" |
| 7 | **Fidelity constraints** | The negative-space rules — what NOT to do | "Sharp focus on hands, no plastic skin, no smooth digital sheen, no bokeh balls, no over-saturation, no AI hallmarks" |

**Order matters:** Subject first, scene second, then technical, then constraints. The model gives more weight to earlier tokens.

---

## 3. Photographic language — speak like a photographer, not a user

The single biggest lever for escaping the AI look is **vocabulary borrowed from photography forums and editorial magazines**, not from stock photo sites.

### Camera bodies that produce distinctive looks
- **Leica Q2 / Q3** — sharp, deep colour, slightly cool, editorial favourite for environmental portraiture
- **Fujifilm X100V / X100VI** — film-like, warm midtones, gentle highlights, popular with Kinfolk-style shooters
- **Hasselblad X2D** — medium format depth, creamy fall-off, the "Apple keynote" look
- **Contax T2 / T3** — film point-and-shoot, slight grain, late-90s editorial feel
- **Canon AE-1 + Portra 400** — analog film aesthetic, warm, soft grain, no digital cleanliness

### Focal lengths and what they do
- **28mm** — environmental, slightly wide, hands-and-context shots (this is the Referral Images sweet spot)
- **35mm** — classic documentary, full body in tight rooms
- **50mm** — portraiture standard, neutral perspective
- **90mm macro** — close detail, skin lesion close-ups, dermatoscope-like framing

### Apertures and what they signal
- **f/1.4 to f/2.0** — shallow depth, romantic, but easy to overdo and look AI-fake
- **f/2.8 to f/4** — natural editorial, hand and object both sharp, background soft
- **f/5.6 to f/8** — environmental clarity, multiple planes sharp, magazine documentary
- **f/11 and up** — flat lay territory, almost everything sharp

### Film stocks as colour grades
- **Kodak Portra 400** — warm skin tones, gentle highlights, the safest editorial pick
- **Kodak Gold 200** — sunny, golden, slightly nostalgic
- **Kodak Tri-X 400** — high-contrast monochrome, documentary
- **Fujifilm Pro 400H** — cool greens and teals, wedding-photographer favourite
- **Cinestill 800T** — tungsten-balanced, neon halation, night scenes

### Editorial publication anchors
Naming a publication tells the model an entire visual grammar. The most reliable picks for clinical/lifestyle work:

- **Kinfolk magazine** — soft natural light, neutral palette, generous negative space, slow living
- **FT Weekend** — documentary editorial, medium contrast, real environments
- **NYT Magazine** — editorial portraiture, controlled lighting, crisp details
- **Monocle** — clean Scandinavian, designed environments, pastel accents
- **Cereal magazine** — minimalist, architectural, very slow

Including "in the style of Kinfolk magazine" or "shot for FT Weekend" in a prompt is worth 10 lines of description.

---

## 4. Anti-AI-look techniques

The "AI look" is a cluster of recognisable failure modes. Each has a counter.

| AI tell | Why it happens | Counter |
|---|---|---|
| **Plastic, smooth skin** | Default beauty bias in training data | Add: "natural skin texture, visible pores, fine lines, no skin smoothing, no beauty filter" |
| **Glowing inner light on faces** | Over-rendered bloom | Add: "diffuse natural window light only, no rim light, no inner glow" |
| **Background bokeh balls** | Mid-2010s wedding photography in training | Add: "no bokeh balls, no specular highlights in background, naturally soft background" |
| **Over-saturated colour** | Instagram-era training | Add: "muted natural colour, Kodak Portra 400 colour science, no saturation boost" |
| **Symmetry and centre-weighting** | Default model bias | Compose off-centre: "subject in left third, headroom above" |
| **Hands with wrong fingers** | Persistent generation weakness | See section 5 — describe hands explicitly |
| **Floating objects, broken physics** | Spatial reasoning failures | Name what touches what: "her right index finger curls around the mug handle, thumb resting on the rim" |
| **Generic beautiful person** | Training distribution skew | Specify age, build, ethnicity, clothing details, posture |
| **Identical synthetic backgrounds** | Mode collapse on common scenes | Include 1-2 specific real-world props that anchor the scene |
| **Perfect, centred typography in signage** | Text rendering bias | Add: "slight imperfection in handwritten text, natural pen pressure variation" |

The single most powerful instruction across all of these: **"shot on film, not digital."** Even when generating digital camera output, that phrase pushes the model toward grain, falloff, and imperfection.

---

## 5. Hand handling — the rule that matters most

Hands are still the weakest part of any image model, including Nano Banana Pro. The fix is counter-intuitive: **describe what the hands ARE doing, finger by finger, in positive language. Do not list what to avoid.**

**Bad:** "no extra fingers, no malformed hands, no claw fingers"

**Good:** "her right hand holds an iPhone in landscape orientation, thumb pressed against the right edge of the screen, index finger curled underneath the phone supporting the weight, middle and ring fingers folded loosely against the back of the device, pinky tucked in"

The model handles hands well when given a kinesthetic description because it can resolve geometry from physics. It hallucinates fingers when given negation because the negation forces it to invent a hand from scratch.

**Hand template for clinical photography contexts:**

> "[Person]'s [left/right] hand holds [object] in [orientation]. Thumb [position]. Index finger [position]. Other three fingers [position]. The hand is in sharp focus. Skin shows natural texture, fine knuckle creases, neat short nails, no jewellery."

Same logic applies to feet, posture, and any joint pose.

---

## 6. Screen handling

When the image needs to show a phone, laptop, or tablet screen, the model defaults to either: (a) a generic blue gradient, (b) made-up fake UI, or (c) a recognisable real app it has memorised. None are useful for product marketing.

**Two reliable approaches:**

1. **Describe a single concrete UI element** in the screen, in plain language. Example: "the iPhone screen shows a simple white camera viewfinder with a single circular shutter button at the bottom centre, no other UI chrome, no menu bars, no app icons." This gives the model something specific to render and prevents hallucination.

2. **Generate the photo with a blank screen, then composite the real UI in post.** Add: "the iPhone screen displays a flat off-white surface, no UI, no reflection." Then drop the real product screenshot in via Figma or Photoshop. This is the production-grade workflow and the only reliable way to get the actual product UI on the device.

For the Referral Images hero, approach 2 is correct — the screen will show the actual capture screen in the final asset, not whatever Nano Banana Pro invents.

---

## 7. Negative constraints checklist

Append this block to almost every photoreal prompt. It is worth its weight in clarity.

```
Constraints: shot on film, not digital. Natural skin texture with visible pores
and fine lines. No skin smoothing, no beauty filter, no airbrush. Diffuse natural
window light only, no rim light, no inner glow on faces. Muted natural colour,
Kodak Portra 400 colour science, no saturation boost. No bokeh balls, no specular
highlights in the background. No floating objects, all physics consistent. No
generic stock-photo composition. Sharp focus on hands and primary subject.
Off-centre composition. Editorial documentary style, not commercial.
```

This block alone removes ~70% of the AI tells.

---

## 8. Iteration workflow

Single-shot prompting almost never gets the final asset. The reliable workflow:

1. **Round 1 — variations.** Run the full prompt 4-6 times. Pick the strongest 1-2 outputs based on composition and lighting, ignoring small flaws.
2. **Round 2 — refinement.** Take the winner, drop it into AI Studio as a reference image, and prompt: "Same image, but [specific change]. Keep everything else identical." Examples of changes: "make the window light slightly cooler", "rotate the phone 5 degrees clockwise", "remove the second mug on the right edge".
3. **Round 3 — surgical fixes.** For specific broken regions (a hand, a finger, a screen), use in-painting: mask the region in AI Studio and prompt only the fix.
4. **Final — post-process.** Bring into Figma/Photoshop for: (a) compositing the real product UI onto the device screen, (b) any text or logo overlays, (c) final colour grade pass to match the page palette.

Budget: expect 30-60 minutes per finished hero image. Do not try to nail it in one prompt.

---

## 9. Aspect ratios for landing page work

Nano Banana Pro supports flexible aspect ratios. For ClinicPro marketing pages:

| Use | Aspect | Notes |
|---|---|---|
| Hero image desktop | 3:2 or 16:10 | Leaves room for text overlay on left/right |
| Hero image mobile (separate asset) | 4:5 or 1:1 | Generate as a separate prompt, do not crop the desktop one |
| Section illustration | 1:1 | Square, used inline beside copy |
| Editorial portrait | 4:5 | Standard magazine portrait crop |
| Marginalia / inset | 1:1 small | For the cream-and-ink margin notes pattern |

Always generate the aspect ratio you need from the start. Cropping wastes resolution and usually breaks composition.

---

## 10. Verbatim hero prompt for ClinicPro Referral Images

Locked in conversation 2026-04-08. This is the v1 prompt to run as-is. Backup variants below.

### Hero v1 — "On the kitchen table"

```
A woman in her late thirties, soft cream knit sweater, sitting at a low pine
kitchen table in a quiet New Zealand villa kitchen, late morning. She is holding
an iPhone 15 in her right hand in landscape orientation: her right thumb pressed
against the right edge of the screen, index finger curled underneath the phone
supporting its weight, middle and ring fingers folded loosely against the back
of the device, pinky tucked in. The iPhone screen displays a flat off-white
surface, no UI, no reflection. Her left hand rests on the table beside a single
ceramic mug with a hairline crackle glaze, half full of black coffee, and a
folded linen tea towel. North-facing window behind her left shoulder, diffuse
natural light from camera-left, no rim light, no inner glow. The pine table has
visible grain and a small pen mark near the edge. A single sprig of rosemary in
a small clear glass jar sits to the right of the mug.

Shot on Leica Q2, 28mm Summilux at f/2.0, ISO 400, 1/200. Composition off-centre:
the woman in the right two-thirds, the mug and tea towel anchoring the left third.
Kodak Portra 400 colour science, gentle warm midtones, no contrast crush.
Editorial documentary style, in the style of Kinfolk magazine and FT Weekend.

Constraints: shot on film, not digital. Natural skin texture with visible pores
and fine lines, no skin smoothing, no beauty filter, no airbrush. Diffuse natural
window light only, no rim light, no inner glow on faces. Muted natural colour,
no saturation boost. No bokeh balls, no specular highlights in the background.
No floating objects, all physics consistent. Sharp focus on her right hand and
the iPhone. Off-centre composition. No stock-photo look.

Aspect ratio 3:2.
```

### Hero v2 — "No patient hand" backup

Same body as v1, but the woman is **alone**, photographing a small ceramic dish on the table that contains a single dried leaf (stand-in for a clinical specimen — ambiguous enough to read as "she's photographing something, the something doesn't matter"). Use this if v1 generates an unconvincing or distracting subject. The leaf is the rendering target — easy for the model to get right.

### Hero v3 — "Top-down flat lay" backup

A flat lay top-down shot of a pine table: an iPhone 15 in the centre showing a
blank off-white screen, a ceramic mug with crackle glaze to the left, a folded
linen tea towel to the right, a small sprig of rosemary in a clear glass jar
top-right, a single fountain pen and a folded paper letter top-left (the letter
visibly handwritten in dark blue ink, the legible words "Dear Dr." at the top,
the rest illegible cursive). North-facing window light from above and slightly
left, late morning. Shot on Hasselblad X2D, 65mm at f/5.6, ISO 200. Kodak Portra
400 colour science. Aspect ratio 1:1.

Use this for a section anchor image, not the hero, if the photographic hero feels
too literal.

---

## 11. Quick-reference checklist

Before running any prompt, walk this list:

- [ ] Subject described concretely (age, clothing, posture, gesture)
- [ ] Scene props named (at least 3 specific objects)
- [ ] Real camera body + focal length + aperture
- [ ] Lighting direction and quality named
- [ ] Materials and textures listed
- [ ] Colour grade specified (film stock or publication anchor)
- [ ] Hands described finger-by-finger if visible
- [ ] Screens handled (concrete UI element OR blank for compositing)
- [ ] Negative constraints block appended
- [ ] Aspect ratio set explicitly
- [ ] Composition is off-centre

Skipping any one of these is the usual cause of "this looks AI-generated."

---

## 12. Sources

Primary sources reviewed during the 2026-04-08 research session. URLs preserved for re-verification when prompt patterns drift.

- Google blog — Gemini 3 Pro Image launch announcement (November 2025)
- Google AI Studio documentation — `gemini-3-pro-image` endpoint reference
- Google Cloud blog — Vertex AI Gemini 3 Pro Image pricing and quota notes
- DeepMind Imagen 3 paper (background context for Gemini family architecture)
- DataCamp tutorial — "How to use Nano Banana Pro" (workflow walkthrough)
- Petapixel — "Inside Google's new image model" (review and prompt tests)
- Reddit r/StableDiffusion — multiple Nano Banana Pro prompt threads (Nov 2025–Jan 2026)
- Reddit r/Bard — Gemini 3 Pro Image user reports
- ArtificialAnalysis benchmark — Nano Banana Pro vs Midjourney v7 vs Flux 1.1 Pro
- Two Minute Papers YouTube — Nano Banana Pro demo breakdown
- AI Studio examples gallery — 30+ reference prompts with side-by-side outputs
- Kinfolk magazine print issues 47-50 — visual reference for editorial colour grade
- Leica Q2 sample gallery — focal length and aperture reference
- Magnum Photos editorial archive — documentary composition reference
- Hand pose reference: Adorama "How to photograph hands" guide
- Stack Overflow threads on image model hand failures (general background)
- Anthropic model card discussions on negation-vs-positive prompting (general principle, applies to image models too)
- A single thread on the Eleuther Discord on why "shot on film" works as a universal anti-AI-look phrase

---

**End of reference. Maintain this file as new patterns emerge. Add new verbatim prompts to section 10. Add new failure modes to section 4.**
