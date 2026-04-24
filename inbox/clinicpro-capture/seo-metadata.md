# SEO Metadata Spec: ClinicPro Capture

**Product:** ClinicPro Capture (mobile PWA, NZ GP practices, Medtech Evolution PMS)
**Prepared:** 2026-04-24
**Status:** Draft — supersedes 2026-04-23 draft below

---

## SEO Priorities for Capture Launch

**Target intents (NZ first):**
Search volume for this niche is low. The audience is small and specific: practice managers, head nurses, and GP owners running Medtech Evolution. Priority intents are navigational (`medtech evolution clinical photos`), pain-point-driven (`photograph wound medtech record`), and competitor-aware (`medtech photo documentation`). Do not chase broad GP practice software terms -- CPCs are high and you will not rank against incumbents.

**Paid vs organic:**
Organic is largely futile at launch in a market this small. The decision-makers are not actively searching; they are talking to peers. Organic SEO earns long-term trust and captures the rare inbound searcher, but it is not a primary growth lever here. Invest in referral mechanics (the refer-a-practice page), LinkedIn, and Medtech partner channels first. A narrow Google Ads campaign targeting `medtech evolution` and `medtech GP practice` brand terms is worth testing at low spend once the refer page is live.

**Quick-win technical SEO for Next.js at launch:**
Add a `sitemap.xml` using `next-sitemap`. Configure it to include both `/medtech/capture` and `/medtech/refer`, set `changefreq: monthly`, and submit to Google Search Console on day one. This costs one hour and ensures Google indexes the pages immediately rather than waiting for discovery.

---

## Page 1: Main Landing Page

**URL:** `https://clinicpro.co.nz/medtech/capture`
**Slug:** `/medtech/capture` -- keep as given, descriptive and product-aligned.

### Keywords

**Primary:** `medtech evolution clinical photography`
Rationale: Combines the PMS name (high specificity, low competition) with the core use case. Anyone searching this term is exactly the target buyer.

**Secondary:**
- `medtech evolution photo documentation` -- same intent, slightly broader phrasing
- `GP practice clinical image capture NZ` -- geographic qualifier, pain-point framing
- `wound photo PMS integration` -- clinical workflow term, resonates with nurses
- `ACC injury photo GP practice` -- specific NZ clinical context, differentiates from generic tools
- `medtech evolution PWA` -- technical buyers (practice managers who evaluated other tools)
- `ClinicPro Capture` -- brand term, own it from day one

### `<title>` Tag

```html
<title>ClinicPro Capture | Clinical Photos in Medtech Evolution</title>
```

Character count: 57. Includes primary keyword and brand.

### `<meta name="description">`

```html
<meta name="description" content="Photograph wounds, rashes, and ACC injuries on your phone. One tap sends the image directly into your patient's Medtech Evolution record. Get early access today." />
```

Character count: 158. Leads with the clinical action, names the PMS, includes CTA.

### `<meta name="keywords">`

```html
<meta name="keywords" content="medtech evolution clinical photography, GP practice photo documentation, wound photo PMS integration, ACC injury photo, ClinicPro Capture, clinical image capture NZ, medtech evolution PWA" />
```

### Open Graph Tags

```html
<meta property="og:type" content="website" />
<meta property="og:title" content="ClinicPro Capture | Clinical Photos in Medtech Evolution" />
<meta property="og:description" content="One tap sends clinical photos directly into your patient's Medtech Evolution record. Built for NZ GP practices by a practising GP." />
<meta property="og:url" content="https://clinicpro.co.nz/medtech/capture" />
<meta property="og:image" content="https://clinicpro.co.nz/og/capture-hero.png" />
<meta property="og:image:alt" content="ClinicPro Capture app on a phone showing a wound photo being saved to a Medtech Evolution patient record" />
<meta property="og:site_name" content="ClinicPro" />
```

**OG image guidance:** Show a phone with the Capture UI visible, alongside a Medtech Evolution patient record screen. Dimensions: 1200x630px. This image is shared when a practice manager posts the link in a WhatsApp, Slack, or email thread -- make it legible at small sizes.

### Twitter Card Tags

```html
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="ClinicPro Capture | Clinical Photos in Medtech Evolution" />
<meta name="twitter:description" content="One tap. Clinical photo lands in the patient's Medtech record. Built for NZ GP practices. Get early access." />
<meta name="twitter:image" content="https://clinicpro.co.nz/og/capture-hero.png" />
```

### Canonical URL

```html
<link rel="canonical" href="https://clinicpro.co.nz/medtech/capture" />
```

### H1 Recommendation

```
Clinical Photos in Medtech Evolution, Straight from Your Phone
```

Rationale: Leads with the outcome, names the PMS, anchors the mobile use case. Reads naturally for a nurse or practice manager scanning the page.

---

## Page 2: Refer-a-Practice Page

**URL:** `https://clinicpro.co.nz/medtech/refer`
**Slug:** `/medtech/refer` -- keep as given, short and action-oriented.

### Keywords

**Primary:** `refer GP practice ClinicPro`
Rationale: This page has a narrow job -- convert champion users into referrers. It will not rank for broad terms. SEO here serves navigational and direct-link traffic from existing users who want to share the page.

**Secondary:**
- `ClinicPro Capture referral` -- brand plus action term
- `medtech evolution practice referral` -- PMS-specific, for any organic discovery
- `GP practice software referral NZ` -- geographic plus category
- `ClinicPro early access` -- awareness term for practices in evaluation mode
- `NZ GP practice clinical photo tool` -- descriptive fallback

### `<title>` Tag

```html
<title>Refer a Practice | ClinicPro Capture Early Access</title>
```

Character count: 51. Action-first, brand present, signals exclusivity.

### `<meta name="description">`

```html
<meta name="description" content="Know a GP practice on Medtech Evolution? Refer them to ClinicPro Capture and get them three months free. Takes 60 seconds. Help your colleagues work smarter." />
```

Character count: 157. Names the PMS, states the incentive, includes implicit CTA.

### `<meta name="keywords">`

```html
<meta name="keywords" content="refer GP practice ClinicPro, ClinicPro Capture referral, medtech evolution practice referral, GP practice software referral NZ, ClinicPro early access, NZ GP clinical photo tool" />
```

### Open Graph Tags

```html
<meta property="og:type" content="website" />
<meta property="og:title" content="Refer a Practice to ClinicPro Capture" />
<meta property="og:description" content="Know a practice on Medtech Evolution? Refer them and get them three months free. Help your colleagues document clinical images the easy way." />
<meta property="og:url" content="https://clinicpro.co.nz/medtech/refer" />
<meta property="og:image" content="https://clinicpro.co.nz/og/refer-hero.png" />
<meta property="og:image:alt" content="ClinicPro Capture referral page with a prompt to share with other NZ GP practices on Medtech Evolution" />
<meta property="og:site_name" content="ClinicPro" />
```

**OG image guidance:** Clean graphic with the message "Get your colleagues 3 months free" plus the ClinicPro Capture logo. Optimise for WhatsApp and email preview sizes. High contrast, no small text. Dimensions: 1200x630px.

### Twitter Card Tags

```html
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Refer a Practice to ClinicPro Capture" />
<meta name="twitter:description" content="Know a Medtech Evolution practice? Refer them in 60 seconds and get them three months free access." />
<meta name="twitter:image" content="https://clinicpro.co.nz/og/refer-hero.png" />
```

### Canonical URL

```html
<link rel="canonical" href="https://clinicpro.co.nz/medtech/refer" />
```

### H1 Recommendation

```
Help a Colleague. Refer a Practice to ClinicPro Capture.
```

Rationale: Peer-to-peer framing. "Colleague" resonates in GP culture. Clear action, clear product name.

---

## Implementation Notes

- **OG images:** Place at `public/og/capture-hero.png` and `public/og/refer-hero.png`. Set `metadataBase: new URL('https://clinicpro.co.nz')` in `app/layout.tsx` so Next.js resolves relative OG image paths to absolute URLs.
- **Title template:** Use Next.js `title.template` in `app/layout.tsx` to avoid repeating the brand suffix in every page:
  ```ts
  title: {
    template: '%s | ClinicPro',
    default: 'ClinicPro Capture — Clinical Photos for Medtech Evolution',
  }
  ```
- **Structured data:** Add `SoftwareApplication` schema to the `/medtech/capture` page and `Organization` schema to the root layout. These improve SERP rich result eligibility and E-E-A-T signals. `Person` schema for Dr Ryo Eguchi as founder also supports E-E-A-T in a health context.
- **Australia expansion:** When the AU bundle deal closes, create separate localised pages (e.g. `/medtech/au/capture`). Do not reuse NZ pages with AU content -- Google treats them as duplicates and keyword intent differs across Medtech Global vs Medtech Evolution branding.
- **Search Console:** Verify domain on day one. Submit `sitemap.xml`. Monitor impressions for `medtech evolution` brand terms weekly for the first month.
- **`/medtech/refer` indexing:** Current default is index/follow. If you prefer the refer page to be invitation-only and not discoverable via search, add `<meta name="robots" content="noindex, follow" />`. Leave as-is if organic discovery of the referral mechanic is acceptable.

---

## Prior Draft: 2026-04-23

The following was the original metadata draft produced before the product URL structure was finalised. Retained for reference.

---

### Global keyword strategy (2026-04-23 draft)

Five high-priority target terms with NZ search intent.

| Term | Monthly intent | Rationale |
|---|---|---|
| `Medtech Evolution clinical photos` | Informational / problem-aware | Direct match to the exact pain point GPs search when they hit the format rejection issue. High specificity, low competition. |
| `ALEX FHIR API integration NZ` | Navigational / technical | Medtech practice managers and IT coordinators researching how ALEX works. Signals credibility to the buyer who controls purchasing decisions. |
| `clinical photo NZ referral rejected` | Informational / frustrated | Mirrors verbatim language from GPs for GPs Facebook group. Strong purchase intent once landed: they already have the problem. |
| `Medtech Evolution Inbox Scan` | Navigational | GPs and nurses searching for the specific folder path. Anyone who knows this term already uses Medtech Evolution and will recognise the product immediately. |
| `NZ GP clinical imaging PMS` | Informational / discovery | Broader discovery term for GPs exploring practice tools. NZ-specific qualifier filters for target audience. Useful for long-tail content strategy. |

### Page-by-page metadata (2026-04-23 draft)

#### Landing page: `/medtech`

URL: `capture.clinicpro.co.nz/medtech`

**SEO title** (55 chars)
```
ClinicPro Capture -- Clinical Photos for Medtech Evolution
```

**Meta description** (152 chars)
```
Commit clinical photos from your phone directly to a patient's Medtech Evolution Inbox Scan via the ALEX FHIR API. Right format, right folder. Built by a NZ GP.
```

**OG title**
```
ClinicPro Capture -- Clinical Photos for Medtech Evolution
```

**OG description** (160 chars)
```
Stop resizing images and getting referrals rejected. Capture commits photos from your phone straight to the patient record. For NZ Medtech Evolution practices.
```

**Primary keyword:** `Medtech Evolution clinical photos`

**Secondary keywords:**
- `ALEX FHIR API Medtech`
- `clinical photo NZ referral`
- `Medtech Evolution Inbox Scan`
- `NZ GP photo upload PMS`
- `Medtech Evolution ERMS HealthLink`

**Structured data recommendation:**
`SoftwareApplication` (applicationCategory: MedicalApplication, operatingSystem: Any modern mobile browser, offers: structured with pricing tiers). Supplement with `FAQPage` schema for the FAQ accordion (8 questions already present in FAQSection.tsx). `Person` schema for Dr Ryo Eguchi as the founder attribution.

#### Refer-a-practice page: `/refer-a-practice`

URL: `capture.clinicpro.co.nz/refer-a-practice`

**SEO title** (55 chars)
```
Refer a Practice -- ClinicPro Capture for Medtech Evolution
```

**Meta description** (153 chars)
```
Know a Medtech Evolution practice that needs ClinicPro Capture? Refer them and earn NZ$200 credit or 3 months free when they become a paying customer.
```

**OG title**
```
Refer a Medtech Practice -- Earn NZ$200 Credit or 3 Months Free
```

**OG description** (155 chars)
```
Introduce a Medtech Evolution practice to ClinicPro Capture. When they subscribe, you choose: NZ$200 credit on your subscription or 3 months of Capture free.
```

**Primary keyword:** `ClinicPro Capture referral`

**Secondary keywords:**
- `Medtech Evolution software referral`
- `NZ GP practice referral programme`
- `clinical imaging software NZ`
- `refer a medical practice NZ`

#### Root layout metadata (global defaults, 2026-04-23 draft)

Recommended replacements for placeholder strings in `app/layout.tsx`:

**Title template:**
```ts
title: {
  template: '%s | ClinicPro Capture',
  default: 'ClinicPro Capture -- Clinical Photos for Medtech Evolution',
}
```

**Default description:**
```
Mobile web app that commits clinical photos from your phone to Medtech Evolution via the ALEX FHIR API. Built for NZ general practice. No installation required.
```

**Additional recommended global tags:**
```ts
metadataBase: new URL('https://capture.clinicpro.co.nz'),
openGraph: {
  siteName: 'ClinicPro Capture',
  locale: 'en_NZ',
  type: 'website',
},
twitter: {
  card: 'summary_large_image',
},
```
