# output-rendering.md - palamedes long-form PDF output mode

Load when the user asks for a palamedes **long-form report** rendered as PDF or HTML, or any phrasing that implies a comprehensive visual deliverable (not just markdown).

Triggers: "render as PDF", "output to PDF", "render to HTML", "make it a deliverable", "show me a PDF", "produce a printable", "as a PDF report", "render this", "I want a PDF", "full report PDF". Implicit trigger: any L3+ report with a non-technical audience or a recipient who will read it on a phone or print it.

**Related output mode:** for a high-level dense reference card variant (A4 landscape, claim + explainer + strength + citation-link tables, intended for at-a-glance reading and printing), see `references/landscape-summary-report.md`. The two modes are complementary; long-form `REPORT.md` is the authoritative artifact, landscape `ONEPAGER.md` is a derived skim layer.

## Reference implementation

The canonical implementation lives at `/Users/wjia/Projects/babytime/render/` and consists of three files:

- `render.py` - markdown → augmented HTML → Letter PDF via headless Chrome
- `style.css` - the design system (solarpunk editorial)
- `template.html` - the page shell with hero block

Invocation:

```
<venv-python> /Users/wjia/Projects/babytime/render/render.py <category-dir>
```

It reads `<category-dir>/REPORT.md` and writes `<category-dir>/REPORT.html` and `<category-dir>/REPORT.pdf`.

For any new palamedes report that wants this output mode, the simplest path is to copy `render/` into the project root and adjust the category-routing in `extract_meta()` if the title doesn't match the existing patterns.

## Design principles (load-bearing)

These were codified in babytime/monitors after multiple iterations of user feedback. Future palamedes PDF/HTML output should preserve them unless the user explicitly overrides.

### 1. Restraint over decoration

Typography hierarchy carries the design, not color blocks, icons, or chrome. No gradients, no rounded-corner badges with all-caps labels, no Material Design lifts, no shadowboxes.

### 2. Solarpunk editorial palette

Warm parchment paper (`#F0E8D7`), charcoal-brown ink (`#2B2622`), forest moss / sage / amber-honey / terracotta accents. No bright tech blue. No pure white. The default reading experience should feel like a printed magazine page, not a SaaS dashboard.

The full palette in `style.css`:

```
--paper:        #F0E8D7;    /* warm parchment background */
--paper-card:   #F7F0E0;    /* slightly lighter for sidebars */
--paper-deep:   #E6DCC4;    /* darker parchment for table headers */
--ink:          #2B2622;    /* charcoal-brown body text */
--ink-soft:     #5C544A;    /* muted bark */
--ink-faint:    #8A8074;    /* faded for metadata */
--moss:         #3D5238;    /* forest moss - primary accent */
--sage:         #8A9B7E;    /* sage green - secondary accent */
--amber:        #B68232;    /* amber honey - tertiary accent */
--terracotta:   #A85C3B;    /* terracotta - warm warning */
--rust:         #8B3A2E;    /* deep rust - alarm */
--ochre:        #8C6720;    /* earthy yellow ochre */
--indigo:       #3D4A5E;    /* muted indigo - cool counterpoint */
```

### 3. Letter page size, body fills the page

Page: Letter portrait, 1.8cm top, 1.0cm sides, 2.0cm bottom. **Body column has no max-width**: it fills the full page-usable space (~63em at 8.75pt serif) and wraps naturally around right-floated citation blocks.

Citations float right with `width: 24em` and `margin-left: 2em` (~2 character gap between body text and the citation block). Where a citation is present, body line length is constrained to ~37em next to it; where no citation, body extends the full ~63em.

This shape was iterated three times on 2026-05-18: first widening from 36em → 38em with a 25em gutter, then doubling the citation width (12.5em → 24em), then removing the body max-width entirely so the main text reaches the right edge wherever no citation is floating. The final shape is "Tufte gutter only when a citation needs it; full bleed everywhere else".

Tables use `width: 100%` of main and inherit the same full-page extent.

### 4. Smaller body type, generous line-height

9.5pt serif (Iowan Old Style → Palatino → Georgia → Cambria fallback chain). Line-height 1.6. Hyphens enabled. Old-style figures (`onum`) by default; tabular (`tnum`) in tables.

### 5. Tier-tag chips are footnote-style, not badges

Inline tier-tag citations like `[T1, CPSC-26-307]` render as small monospace chips with subtle color hint by tier. T1 → moss outline, T2 → soft-ink outline, T3 → faint italic. They should look like footnote markers, not pills.

### 6. Margin notes for digressions

The `aside.margin-note` element floats into the right gutter (Tufte-style). Use for citations, asides, definitions, parenthetical explanations that interrupt the body flow. Width: 24em, font 7pt sans, sage left-border. The `aside.citation` (moss border, expanded source metadata) and `aside.marginalia` (amber border, italic serif) variants share the same 24em block.

Markdown invocation pattern:

```html
<aside class="margin-note">
  <strong>Why this matters:</strong> brief context that would have been
  a parenthetical in the body.
</aside>
```

### 7. Color used sparingly and with meaning

The recall warnings are the only place where strong color is allowed. STOP callouts in rust, CAVEAT callouts in ochre, OK callouts in moss. Tables auto-color rows based on keyword detection (recall, fire hazard, do not use → stop; caveat, downgrade, flagged → warn; none found, clean of recalls → ok).

### 8. h2 underline rule, not border-bottom

H2 sections get a thin moss line **above** the heading (1.8em wide, 1px), not a corporate border-bottom. The line orients the reader to the heading as a chapter mark, not as a horizontal divider.

### 9. SVG diagrams inline, copyright-clean

Original diagrams hand-written in SVG and embedded inline in the markdown. The renderer passes HTML through verbatim. No reliance on external images, no Google Charts, no Mermaid (which renders inconsistently in headless Chrome). The recall-timeline diagram in `babytime/monitors/REPORT.md` is the worked example.

### 10. Product links and prices as parentheticals where applicable

If the report recommends a purchaseable product:

- Link to the canonical retailer page (vendor direct, Best Buy, Target, Walmart, Lowes, or a specialty retailer for the category)
- Approximate price as a parenthetical with the retrieval date stamped in the report metadata or section header
- Avoid affiliate links unless explicitly requested
- Avoid Amazon-only links where a non-affiliated retailer exists for counterfeit-prone categories

## What the output mode does NOT do

- It does not auto-generate margin notes from the markdown. The author opts in by writing `<aside class="margin-note">` blocks.
- It does not auto-trim source citations. The full tier-tag chips remain in the body; they are visually de-emphasized to footnote weight.
- It does not paginate by content. Headless Chrome handles pagination via CSS `page-break-*` hints; the author can add `page-break-before: always` to specific elements when needed.
- It does not enforce a one-page summary. The author should explicitly write a "Decision card" section at the top if a one-page-readable summary is the goal.

## Failure modes to avoid

These were caught and corrected in babytime/monitors iterations.

- **Gradient hero with bright-color badges:** failed v1 of the design as "vibecoded." Replace with a calm editorial hero (paper background, dark heading, sage divider).
- **Versioned narrative in the report body:** the report should describe the **current** correct claims, not the history of how the report got there. Adversarial-review history lives in companion `ADVERSARIAL_REVIEW*.md` files, not in the main report.
- **EMF or unscientific claims as evaluation criteria:** every criterion in the report should have a regulatory or peer-reviewed grounding. Personal-comfort criteria belong in user-stated criteria but should not appear as criteria-with-citations.
- **Dense markdown body without a decision card up front:** parents and other cognitively-overloaded readers will not read a 6000-word report end-to-end. A "Decision card" or "Recommendations at a glance" section at the top is mandatory for any L3+ buyer-facing report.
- **Tables that exceed the body column width:** if a table has too many columns, drop columns rather than spilling. Use a separate full-width figure if needed.
- **Em-dashes (` - `):** banned per Wei voice rules. Use ` - ` (hyphen-space) or `,` instead. Scrub before render.

## Quick-start: applying this to a new palamedes report

1. Write the report markdown with the standard palamedes sections: TL;DR → findings → limits → what-would-change → open-questions → references.
2. Add a "Decision card" section as the first body section if the report is buyer-facing or decision-driving.
3. Use tier-tag chips inline: `[T1, FCC-2AOKB-T8352]`, `[T2, CR-WIFI-MONITORS]`.
4. Embed any SVG diagrams inline. Hand-write them rather than pulling external images.
5. Copy `/Users/wjia/Projects/babytime/render/` into the project directory or a sibling. Update `extract_meta()` category routing if needed.
6. Run `render.py <project-dir>`. Output: `REPORT.html` and `REPORT.pdf` next to the source markdown.

## Optional invocation pattern

When the user asks for PDF/HTML output, the canonical Cascade flow is:

1. Run the palamedes loop (P1 → P2 → P3 → P4) to produce the markdown report.
2. Apply the design principles above when shaping the markdown (decision card at top, tier-tag chips, recommend-against section, SVG figures inline).
3. Invoke the render pipeline at the end: `render.py <dir>` → PDF.
4. Surface the PDF path and page count to the user.

The output mode is **opt-in**. Plain markdown output remains the default for L0-L2 sessions and any session where the user does not explicitly request a visual deliverable.

## Worked example

`/Users/wjia/Projects/babytime/monitors/REPORT.pdf` (Letter, ~20 pages, ~440 KB) is the canonical worked example. The source markdown is `REPORT.md` in the same directory.

Cross-references inside babytime that use the same render pipeline:

- `car-seats/`, `strollers/`, `sleep/`, `feeding/`, `travel/`, `bathing/` are pre-registered with P1 docs and queued for full P2+ retrieval. When rendered, they will use the same `render/` system and inherit the design system documented here.

---

## Screen-first multi-page variant (daily-cadence sites)

The long-form PDF mode above is the default. The same design system can be applied to a **multi-page browseable HTML site** when the deliverable is meant to be opened daily, navigated week-by-week, or used as a reference corpus rather than read end-to-end as a printed artifact.

**For exam-prep / certification / cram-program sites,** there is a richer template that extends this variant with a pedagogy appendix (memory palace, mnemonic quick-reference, evidence-tagged techniques, daily integration schedule). See `references/study-guide-site.md`. The remainder of this section documents the bare multi-page mechanics that both variants share.

**Triggers for this bare variant:** "render all pages in HTML", "daily site", "browseable", "weekday cadence", "curriculum site", "open in my browser each morning", "with citations on the right" (Tufte margin notes are the screen-first answer to the PDF tier-tag chips). For exam-prep sites specifically, prefer the `study-guide-site.md` triggers.

### Reference implementation

`/Users/wjia/Projects/qa-prep/scripts/render_html.py` is the canonical worked example. It produces:

- `index.html` - router page with JS that auto-detects today's weekday index and either redirects to the right daily page or shows a rest/not-started/complete message. The router uses a `DEFAULT_START` constant and `localStorage`-free date math.
- `day-NN.html` for N in 01..30 - one page per study day, each with a hero block (week / day / overall index), a "today's focus" callout, Tufte-style margin notes with citations, an external-links list, and prev/next daynav.
- `<corpus>.html` for each markdown source - full markdown rendered to solarpunk HTML, with a breadcrumb back to index.
- `style.css` - adapted from `babytime/render/style.css`; same palette, same hierarchy, but with screen-first rules in the cascade and `@media print` rules at the bottom for printability.

The 30-day metadata is a Python `DAYS` list inside the generator. Each entry has `w, d, title, focus, citations, links`. Citations render as `<aside class="margin-note">` blocks that float into the right gutter on viewports ≥1050px and inline as bordered blockquotes on narrower viewports.

### Design adaptations from the PDF variant

The screen-first variant keeps the solarpunk palette, serif type, narrow column, and Tufte margins. It changes:

| Element | PDF variant | Screen-first variant |
|---|---|---|
| Page size | Letter portrait, `@page` rules | Browser viewport, `max-width: 36em` |
| Body type | 9.5pt serif | 16px (1rem) serif |
| Margin column | Always present, `float: right` | `float: right` on ≥1050px viewports, inline bordered blockquote on narrower |
| Tier-tag chips | Inline `[T1, ID]` footnote chips | Replaced by margin-note `<aside>` for screen browsing |
| Pagination | `page-break-*` CSS | Per-page navigation (prev/next/index) |
| Hero block | Letter-page title block | Compact `.hero` with day-of-N metadata |
| Print | Default | `@media print` block preserves PDF behavior; pages print cleanly without site nav |

### Router pattern (auto-detect today)

```javascript
const START = "2026-05-18"; // a Monday
function todayIdx() {
  const start = new Date(...START.split("-").map(Number)); start.setHours(0,0,0,0);
  const today = new Date(); today.setHours(0,0,0,0);
  if (today < start) return -1;            // not started
  const dow = today.getDay();
  if (dow === 0 || dow === 6) return -2;   // rest day (Sat/Sun)
  // Count weekdays from start (exclusive) to today (exclusive)
  let n = 0; const cur = new Date(start);
  while (cur < today) {
    cur.setDate(cur.getDate() + 1);
    const d = cur.getDay();
    if (d !== 0 && d !== 6) n++;
  }
  return n; // 0-indexed
}
```

The router redirects after a 3-second delay (`setTimeout`) so the user can stop the redirect by clicking the "Stay on index" link.

### Citation pattern (Tufte margins)

Citations are written as a Python tuple list per day: `(label, gloss)`. They render as:

```html
<aside class="margin-note">
  <strong>Roediger & Karpicke 2006</strong>: students who study + test outperform
  study-only on a 1-week delayed recall test
</aside>
```

On wide viewports the aside floats into the right gutter alongside the focus block. On narrow viewports it becomes a sage-bordered inline block immediately following the focus paragraph. This gives the screen-first version the same scholarly weight that the PDF gets from inline tier-tag chips.

### Failure modes specific to the multi-page variant

- **Linking to raw markdown files.** Defeats the whole point of HTML rendering. Every link should target a rendered `.html` file in the same output directory. The generator should render the corpus alongside the daily pages so there are no `.md` link targets.
- **JS-heavy router without a fallback.** The TOC grid below the router status must remain functional even if JS fails or the user opens the site in a privacy-strict context. Test with JS disabled before declaring done.
- **Floats appearing before the content they cite.** Margin-note asides should be placed in the HTML *after* the paragraph they annotate, not before. Floats inherit their starting Y from source order.
- **Print rules colliding with screen rules.** Keep `@media print` strictly at the end of the CSS and wrap all print-specific layout there. The screen-first defaults (`max-width: 36em`, `margin-left: 18em` on wide viewports) would break Letter-portrait pagination if applied in print.

### Quick-start: applying the multi-page variant to a new domain

1. Source markdown: write your corpus as a small number of well-structured `.md` files.
2. Copy `qa-prep/scripts/render_html.py` and `qa-prep/study_guide/daily/style.css` into the new project.
3. Edit the `DAYS` list (or replace with whatever cadence-data shape applies, e.g. weeks for a longer program, modules for a course).
4. Edit the corpus-page rendering at the bottom of `main()` to point at your `.md` files.
5. Run the generator (uses `/Users/wjia/Projects/.venv-pdf/bin/python` for the markdown-it + jinja2 deps).
6. Open `<outdir>/sindex.html` in a browser. The router will route to today's page.

| Project | Subject | Days | Pages | Pedagogy appendix |
|---|---|---|---|---|
| ### Worked example| QA Engineering interview prep | 0 | 3| No |
| `/Users/wjia/Projecs/cc-prep/sudy_guide/diy/` | ISC2CCcerifiti rm | 10eedays | 16 HTML | **Yes (Appnix D)**|

Th q-rpbd() is thecncal xampleof baremlti-ae vaintc-prpbuild(2026-05-17, pegogyappdx add2026-05-18)  th caonical xape offll exam-pptemeocmne nreferences/--t

`/Users/wjia/Projects/qa-prep/study_guide/daily/` (35 HTML files, ~280KB total) is the canonical worked example. Built 2026-05-17 alongside the QA study program. The source `DAYS` data lives inside `scripts/render_html.py`; the source corpus lives at `study_guide/QA_Study_Guide.md`, `study_guide/PRACTICE_EXAMS.md`, `gap_analysis.md`, `resource_index.md`.
