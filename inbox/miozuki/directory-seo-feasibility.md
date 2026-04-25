---
title: "Miozuki: Directory Site SEO Feasibility"
created: 2026-04-25
status: draft
tags: [miozuki, seo, research, strategy]
---

# Miozuki: Directory Site SEO Feasibility

First draft for human review. All findings require Ryo's review before acting on any recommendation.

---

## 1. What Is Ranking in the NZ Jewellery and Lifestyle Space

### Sites currently ranking

The NZ jewellery search landscape is dominated by three types:

**Curated editorial lists (strongest SEO performers)**
- Urban List NZ (`theurbanlist.com/new-zealand/a-list/jewellers-nz`) ranks for "best jewellers NZ" and "best jewellers Auckland." Authority comes from a well-established lifestyle brand with broad NZ content, high domain authority, and strong editorial backlinks. Not monetised through listings directly; monetised through advertising and sponsored content.
- Neat Places (`neatplaces.co.nz`) ranks similarly for NZ-specific lifestyle and shopping queries. Editorial, brand-driven, not a transactional directory.

**Trade / association directory**
- JWNZ (`jwnz.co.nz`) ranks for trade queries and "find a jeweller NZ." Old site, outdated design, ranks on domain age and inbound links from member sites. Primarily trade-facing, not consumer SEO. Limited commercial threat.

**No dedicated consumer-facing ethical jewellery or moissanite directory exists in NZ.** The moissanite NZ search results are entirely retailer sites (Raphana, Holloway, NZ Jewellers, Agape, Miozuki itself). The query "ethical jewellers NZ" similarly returns individual retailer pages, not a curated directory. This is a gap.

**Wedding directory space is crowded**
The NZ wedding vendor space has multiple established players: WeddingWise, My Wedding Guide, Getting Hitched, NZ Bride, Bride & Groom Magazine, Wild Hearts, Wezoree. This space is genuinely competitive. Entering here as a new domain competes with sites that have been building authority for 5-15 years.

### What makes them rank
- Domain age and accumulated backlinks (Urban List, Neat Places, JWNZ)
- Editorial curation and brand trust, not volume of listings
- Topical authority: sites that cover a niche exhaustively rank better than generalist directories
- User engagement signals: editorial sites with genuine readers outperform thin listing aggregators

### Are they monetised
Urban List and Neat Places: advertising and sponsored placements. JWNZ: member subscription fees. Wedding directories: paid listings at $250-$400/year. None appear to be high-revenue businesses; most are brand-building plays or niche media operations.

---

## 2. Fast-Build Tools for Directory Sites in 2026

### Tool comparison

| Tool | MVP Time | Monthly Cost | SEO Rendering | Best For |
|---|---|---|---|---|
| Softr + Airtable | 1-2 weeks | $50-$100 | Server-rendered, Google-indexable | No-code, fast launch, basic directories |
| Webflow CMS + Airtable + Whalesync | 3-5 weeks | $100-$200 | Static/SSR, strong SEO | No-code, design-quality matters |
| Next.js + Airtable (custom) | 4-8 weeks | $20-$50 (infra only) | SSG/SSR, best-in-class SEO | Dev-available, large listing count, programmatic SEO |
| Dorik | 1-2 weeks | $20-$40 | Server-rendered, solid SEO basics | Simplest no-code option, less flexible |
| Typedream | 1 week | $15-$30 | Static | Landing pages, not suited to database-driven directories |

### Key SEO considerations

**Rendering matters.** Google's guidance as of 2025-2026 is clear: SSG (static site generation) and SSR (server-side rendering) are preferred. Client-side rendering (CSR) risks incomplete indexing. Dynamic rendering is deprecated. Softr renders server-side and is indexable. Next.js with SSG is the gold standard for programmatic SEO at scale.

**Programmatic SEO is the real play for directories.** The core value of a directory for SEO is not the homepage: it is hundreds of individual listing pages, each targeting a long-tail query. "Moissanite rings Auckland," "recycled gold jeweller Wellington," "ethical engagement rings NZ." Each page becomes a unique, indexed URL. This only works if each listing has genuine, differentiated content (not a copied-in blurb).

**Build recommendation for Miozuki:** If pursuing this, Next.js + Airtable is the natural choice. Miozuki's main site is already Next.js on Vercel. A directory site could be a separate subdomain (`directory.miozuki.co.nz` or a standalone domain) built with the same stack. Airtable handles the listing database; Next.js generates static pages at build time. Estimated build: 4-6 weeks part-time with developer involvement. No recurring SaaS cost beyond Airtable Team (~$24/month).

The Softr route launches faster (1-2 weeks) but sacrifices programmatic SEO granularity and long-term flexibility. Acceptable for validating concept; not ideal for serious SEO play.

---

## 3. Successful Niche Directory Examples

**Retro Dodo** (retro gaming): Launched June 2019, reached $55K monthly revenue by November 2022. Built topical authority through exhaustive niche coverage, topic clusters, YouTube, and newsletters. Relevant lesson: breadth of content within the niche mattered as much as the directory itself.

**Bike Lock Wiki**: Niche cycling content site (not a pure directory but highly relevant), earns ~$12K/month. Lesson: narrow topical focus with genuine expert content beats broad scope.

**AI Tools Directory by Whalesync**: Built a 1,000+ listing AI tools directory in one week using Airtable + Webflow + Whalesync. Relevant lesson on speed-to-launch: the tooling exists to move extremely fast. However, many AI tool directories launched in 2023-2024 have since faced Google devaluation due to thin, duplicated content.

**Hello May** (Australia/NZ wedding directory and magazine): The most relevant comparable. Established curated wedding vendor directory covering Australia and NZ. Ranks well for wedding vendor searches. Critically, its authority comes from the editorial magazine component, not just the directory. Vendors pay for featured listings; the magazine content drives organic search; the directory monetises the traffic. This is the model that works: content-first, directory-second.

**Mindfully Wed** (sustainable weddings, Australia/NZ focus): Smaller example of a niche-within-niche approach for ethical and sustainable wedding vendors across Australia and NZ. Sustainable Wedding Alliance takes a similar approach globally.

**Key pattern across all successful examples:**
- Launched with 50-200 curated listings, not empty or near-empty
- Supplemented listings with original editorial content (guides, comparisons, "how to choose X")
- Organic authority built in months 9-18, not months 1-6
- Monetisation followed traffic; not the reverse

---

## 4. Directory Concepts for Miozuki

### 4a. Ethical Jewellers NZ

A curated directory of NZ jewellers using recycled metals, lab-grown stones, and ethical sourcing.

**SEO upside:** The query gap is real. "Ethical jewellers NZ" returns retailer pages, not a curated directory. There is a clear search intent not currently served by a standalone directory. Topical authority here could drive relevant backlinks from wedding blogs, sustainability media, and consumer guides.

**Build effort:** Medium. Requires sourcing 30-80 NZ jewellers, verifying ethical credentials, and writing original per-listing content. Content quality per listing is critical. Lightweight Next.js build off existing stack.

**Conflict risk:** Low to moderate. Miozuki would be listing direct competitors. However, the framing is as a category resource, not a retailer. The "conflict" is actually a strength: it positions Miozuki as a category leader and trusted voice, not just a seller. The risk is that a competitor captures more referral traffic from the directory than Miozuki does. Mitigate by ensuring Miozuki's own listing is prominent and well-featured.

**Monetisation potential:** Low in NZ. The market is too small for paid listings to generate meaningful revenue. Monetisation is indirect: brand authority, backlinks to miozuki.co.nz, category leadership positioning. Do not expect direct directory revenue.

**Brand alignment:** Strong. Ethical sourcing, recycled metals, and lab-grown stones are directly on-brand for Miozuki's moissanite and pearl positioning.

---

### 4b. Moissanite Guide NZ

An educational and comparison site covering all NZ moissanite retailers, stone grades, brand comparisons, and buying guides.

**SEO upside:** Highest of the three concepts. "Moissanite NZ" is a transactional and research query with clear buyer intent. No standalone guide or comparison site currently occupies this space. Miozuki already ranks for "moissanite vs diamond NZ" (confirmed in search results). A dedicated guide site could capture the full top-of-funnel research journey: "what is moissanite," "moissanite vs lab diamond NZ," "best moissanite NZ," "Charles & Colvard vs NEO moissanite." Each page targets a distinct keyword cluster.

**Build effort:** Relatively low. Content is largely educational, can be built from Miozuki's existing knowledge base. The "directory" component (retailer listings) is small (10-15 NZ retailers). Most of the value is in the guide content, not listing volume.

**Conflict risk:** Moderate. Listing competitors is uncomfortable but creates credibility. A comparison page that honestly evaluates retailers, including Miozuki, is more trustworthy and more likely to rank than a page that only promotes one brand. The risk is manageable: Miozuki controls the framing, and a well-structured comparison that highlights Miozuki's differentiators (pearl combinations, NZD pricing, DTC) converts readers effectively.

**Monetisation potential:** Low direct revenue in NZ market. Indirect SEO and brand authority value is significant. Over 12-18 months, a guide site with strong rankings for "moissanite NZ" queries generates qualified referral traffic to miozuki.co.nz.

**Brand alignment:** Very strong. Miozuki is a moissanite retailer building category authority. Owning the NZ moissanite education space is a natural extension of what the brand should be doing on its main site anyway. This concept is less a separate site and more an expansion of Miozuki's blog/content strategy, potentially hosted at `moissanite.co.nz` (note: moissanite.co.nz is already registered, confirmed in search results as active) or a subdomain.

---

### 4c. Conscious Wedding Vendors NZ

A broader sustainable wedding directory covering venues, photographers, florists, caterers, jewellers, and celebrants with ethical or sustainable credentials.

**SEO upside:** Weaker than concepts A and B. The NZ wedding directory space is genuinely crowded. WeddingWise alone has 3,794 vendors and 6,593 reviews. Entering this space as a new domain requires differentiating on curation quality and niche (sustainable/ethical) rather than breadth. Mindfully Wed already occupies this space in the AU/NZ region. The keyword volume for sustainable wedding searches in NZ specifically is likely low (small population).

**Build effort:** High. A credible wedding vendor directory requires listings across many categories: venues, photographers, florists, caterers, stylists, celebrants, DJs, planners. Minimum credible launch probably requires 80-150 listings across 8-10 categories. That is a significant curation and outreach burden.

**Conflict risk:** Low. Jewellers are one category among many; no direct competitor dynamic.

**Monetisation potential:** Moderate if listings grow to 300+. Wedding vendor paid listings ($250-$400/year) are an established NZ market. Revenue potential exists but requires significant scale first.

**Brand alignment:** Weak. Miozuki is a jewellery brand, not a wedding planning brand. Owning a wedding directory dilutes rather than reinforces the Miozuki brand identity. The connection to Miozuki's core business is indirect.

---

## 5. Honest Risks

### What kills directory sites

**Thin content per listing.** The most common failure mode. A directory of 200 listings, each with a business name, address, and one copied sentence, provides no value and attracts Google's helpful content penalties. The 2024-2025 Google core updates specifically targeted thin, AI-generated, and low-value aggregated content. Each listing needs original, useful content to survive algorithmically.

**Chicken-and-egg on listings.** A directory with 10 listings is not useful to visitors. But convincing 80 businesses to participate requires demonstrating value. NZ's small market size exacerbates this: there are genuinely fewer ethical NZ jewellers or moissanite retailers to list than in the US or UK.

**New domain authority timeline.** A new domain starts with no trust. Google's sandbox effect for new domains can suppress rankings for 6-12 months regardless of content quality. Building from a subdomain of miozuki.co.nz (`guide.miozuki.co.nz`) partially mitigates this by inheriting some domain trust, but subdomain authority transfer is partial and contested among SEO practitioners.

**Content maintenance burden.** Directory listings go stale. Businesses close, change details, drop ethical practices. Outdated listings harm trust and SEO. Maintenance is ongoing and underestimated.

**Competitor backlash.** Listing competitors and then ranking above their own sites for queries like "moissanite NZ" will not go unnoticed. Unlikely to cause serious problems in a small NZ market, but worth acknowledging.

### Minimum viable listing count

No hard Google threshold exists, but practitioners consistently cite 50-100 well-described, unique listings as the minimum for a directory to be perceived as genuinely useful. Below that, the site reads as a placeholder and is unlikely to earn backlinks or social sharing. For the Moissanite Guide NZ concept, the listing count is secondary to educational content quality: 10-15 detailed retailer profiles with original assessments is sufficient because the guide content carries the SEO weight.

### Realistic time-to-authority for a new NZ niche directory

- Months 1-3: Technical setup, content creation, initial listings. Little organic traffic.
- Months 3-6: Indexing, early rankings for long-tail queries. Some traffic from branded searches and referrals.
- Months 6-12: Compounding organic traffic if content is strong and backlinks are being earned.
- Months 12-18: First meaningful organic authority. Rankings for mid-volume queries.
- Months 18-24: Sustained traffic if maintained. First signs of industry recognition and inbound link acquisition.

This assumes consistent content production and active outreach. A neglected directory sees no meaningful authority growth past month 6.

---

## Recommendation

Pursue the Moissanite Guide NZ concept. Do not build the Ethical Jewellers NZ or Conscious Wedding Vendors NZ directories.

The reasoning is direct:

1. The "Moissanite Guide NZ" concept is not primarily a directory: it is an educational content hub with a small, well-curated retailer comparison component. The SEO value comes from guide content, not listing volume. That changes the build economics entirely. Miozuki already has some of this content on its blog ("Moissanite vs Diamond NZ" is ranking). The guide site is an extension of what Miozuki should be doing regardless.

2. The search gap is real and unoccupied. No standalone moissanite guide or comparison site exists for the NZ market. The gap will close eventually: either a competitor builds it, or an affiliate marketer spots the opportunity. First-mover advantage in a small market is meaningful.

3. The conflict risk is overstated. Listing competitors in a comparison site, and then ranking above them for "moissanite NZ" queries, is brand-building, not brand-dilution. Miozuki controls the framing. A credible comparison that highlights Miozuki's differentiators is more persuasive than a page that only talks about Miozuki.

4. Build cost and time are low relative to concepts A and C. Most content can be derived from Miozuki's existing product knowledge. Hosting as `guide.miozuki.co.nz` or a thin standalone domain avoids building from zero authority.

**On timing:** The original 12-18 month deferral was reasonable in 2025 but should be revisited. The moissanite search opportunity is relatively niche, and the NZ market is small enough that building the content now, incrementally, carries low risk and low cost. AI content tooling in 2026 makes drafting guide pages faster, but thin AI content will not rank: human editorial oversight on each page is still required. The work is manageable at low velocity (2-3 guide pages per month) without a dedicated resource.

Start in months 4-6, not months 12-18. Build it as a content project on the existing stack, not a separate business. Keep the scope narrow: NZ moissanite, pearl alternatives, and lab-grown stones. Expand only if traffic data justifies it.

---

*First draft, April 2026. Requires Ryo's review before any action.*
