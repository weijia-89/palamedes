# landscape-summary-report.md - palamedes optional output mode

Load when the user asks for a **high-level summary one-pager** rendered for at-a-glance reading rather than the full long-form report. This is the dense-reference variant; the full-report variant is in `output-rendering.md`.

## Invocation triggers

Direct phrasings:

- "landscape summary report"
- "landscape summary"
- "landscape report"
- "one-pager"
- "one-page summary"
- "high-level summary"
- "executive summary" (when the user means a printable, not a chat reply)
- "decision card" / "decision card PDF" (distinct from the in-report Decision-card *section* documented in `output-rendering.md`)
- "skim sheet"
- "at-a-glance reference"
- "evidence summary card"
- "quick reference card"
- "cheat sheet" (informal but common)
- "TL;DR PDF" / "TLDR report"
- "fridge magnet" (colloquial — a real user phrasing for "something I can print and pin up")

Implicit triggers:

- User has already received a full palamedes report and asks for a condensed version
- User asks for a deliverable scoped to a person who will not read 10+ pages (partner, parent, executive)
- Stakes L2 or L3 + audience is non-technical or time-constrained
- User mentions printing, sharing, or pinning up

## When this mode is the right answer

Use the landscape summary when **all** of the following hold:

- The full palamedes loop (P1 → P4) has already been run, or is being run in the same session
- The report has a small, tightly-bounded set of claims (typically 10-30 rows total across all tiers)
- The reader will scan the document, not read it end-to-end
- Hyperlinks to primary citations are the artifact's main job, beyond the claim summary itself
- A single A4 or A3 landscape page (or 2-3 pages at most) is the size target

Use the full long-form report (`output-rendering.md`) instead when:

- The report needs section-level prose (methods, limitations, dose-response, adversarial review)
- The audience is a domain expert who will read end-to-end
- Read-depth audit, references section, and what-would-change-my-mind section are themselves load-bearing
- The report is the authoritative output and a one-pager would be a derivative

The two modes are complementary, not alternatives. The expected pattern is **long-form `REPORT.md` first, then `ONEPAGER.md` as a derived skim layer that links to the long form for depth.**

## Reference implementation

Canonical implementation: `/Users/wjia/Projects/babytime/render/render_onepager.py`.

It imports helpers from `render.py` (the full-report renderer) and overrides the layout for landscape one-pager use. Three files involved:

- `render.py` - full-report renderer (parent)
- `render_onepager.py` - one-pager renderer (overrides)
- `style.css` - shared design system; `render_onepager.py` appends CSS overrides on top

Invocation:

```
<venv-python> /Users/wjia/Projects/babytime/render/render_onepager.py <category-dir>
```

Reads `<category-dir>/ONEPAGER.md` and writes `<category-dir>/ONEPAGER.html` and `<category-dir>/ONEPAGER.pdf`.

Worked example: `/Users/wjia/Projects/babytime/prenatal-late/ONEPAGER.pdf` is a personalized prenatal one-pager rendered for a specific user at 25 weeks gestation. Source: `/Users/wjia/Projects/babytime/prenatal-late/ONEPAGER.md`.

## Design overrides relative to the full report

| Attribute | Full report | Landscape one-pager |
|---|---|---|
| Page size | Letter portrait | A4 landscape |
| Page margins | 1.8 / 1.6 / 2.0 cm | 1.2 / 1.4 / 1.3 cm |
| Body type size | 9.5pt serif | 8.5pt serif |
| Body column max-width | 44em (book column) | 100% (full landscape width) |
| Table cell font | inherits body | 7.8pt with `tnum` enabled |
| Hero block | full editorial hero with subtitle paragraph | compressed hero, single-line subtitle |
| Footer | category - version | category - version - landscape summary |
| Tier-tag chips | small monospace, footnote weight | small sans, slightly bolder for glance reading |
| Page-break-inside on tables | avoid per row | auto, break-inside allowed |
| Margin notes (asides) | supported (right gutter, Tufte-style) | not used — landscape leaves no gutter |

The palette, fonts, and tier-tag color hint are inherited unchanged from `style.css`. The one-pager should look like the full report's denser cousin, not a different document.

## Content structure (load-bearing)

The one-pager has a fixed structure. Deviating from it is allowed but should be a deliberate authorial choice, not a slip.

### 1. Hero block
- H1: `<topic> v<n> one-pager - <one-line audience/scope>`
- Metadata line: `palamedes v3 · stakes=L<0-4> · date=<YYYY-MM-DD>`
- One-paragraph subtitle that states what the document is and what it is NOT
- (Optional) Tier-reading callout: small box that translates the SOLID/PROMISING/AVOID color coding to the reader.

### 2. SOLID table (or "Do this")
- Heading: `## Do this (solid evidence)`
- Columns: Claim · What and when · Strength · Primary citation
- Each row is one claim. The "What and when" cell can be 2-3 lines but no more.
- "Strength" column holds the bare word SOLID (the renderer auto-colors the row).
- "Primary citation" is a single markdown hyperlink to the authoritative source.

### 3. PROMISING table (or "Worth trying")
- Heading: `## Worth trying (promising evidence; modest effects)`
- Same column structure as SOLID.
- Each row should declare the **effect size** in the "What and when" cell. Honesty about modest effect size is part of the tier's value.

### 4. AVOID table
- Heading: `## Avoid`
- Columns: Avoid · Why (with citation) · Use instead
- **Every row must have at least one inline hyperlink in the "Why" cell.** The strength of this table is that each avoid-claim is one click from its evidence.
- The "Use instead" column is the actionable substitute; do not leave it blank.

### 5. Glossary / clarifications (optional)
- Brief explanations for jargon flagged in the main tables.
- Triggered when the audience-scoping line in the hero indicates non-specialist readers.

### 6. Time-anchored checklist
- Heading: `## <activity> milestones (timed from <starting point>)`
- Subheadings as time slices (weeks, days, sprint numbers, etc.).
- Each subheading is followed by a bullet list, not a run-on paragraph. Every item should be doable in one session.
- A "catch-up check" sub-section at the user's current time anchor is mandatory if the user gave one.

### 7. Emergency / escalation strip
- Heading: `## Call <X> immediately for` or `## Escalate immediately if`
- Single paragraph or condensed list of red-flag triggers.
- No citations needed — these are domain conventions, not load-bearing claims.

### 8. Footer
- Single italic line: `Single-analyst synthesis, not <domain> advice. Cross-check with <expert>. Full report in this directory's REPORT.md.`

## What this mode does NOT do

- It does not auto-trim the content from a full report. The author makes a deliberate scope-cut for the one-pager (typically by user instruction or audience-fit).
- It does not bypass the palamedes loop. The one-pager is the **output mode**, not a substitute for P1-P4. Citations in the one-pager must already be verified in the parent report's `REFERENCES.md`.
- It does not enforce single-page output. A landscape one-pager that spills to 2 or 3 pages is acceptable. Forcing single-page often requires cuts that lose load-bearing content. Make the cuts deliberately or accept 2-3 pages.
- It does not skip the AVOID citations. Every AVOID row needs a hyperlink. This is the rule that distinguishes a defensible AVOID table from an opinion list.
- It does not strip the read-depth audit. The audit lives in the parent `REPORT.md`; the one-pager references it.

## Failure modes to avoid

These were caught in babytime/prenatal-late iterations.

- **EMERGING tier on the one-pager.** If you find yourself listing a fourth tier ("mechanism plus 1 small study"), the bar is too low. Drop it. The one-pager is for claims that already cleared the SOLID or PROMISING bar.

- **AVOID rows without citations.** A row that says "avoid X because handwave" with no link is opinion, not evidence. Either find the citation or drop the row.

- **Soft-cheese style category errors.** When a folk recommendation has been refined ("avoid all soft cheese" → "avoid unpasteurized soft cheese"), the one-pager should carry the refined version, not the outdated one. The user trying to remember the rule will look at the one-pager, not the long form.

- **Auto-row-coloring red-dot false positives.** The renderer's `ROW_STOP_RE` flags words like `death`, `fire hazard`, `recall`. If a SOLID row contains "neonatal death" as a positive outcome metric, the row gets a red dot. Rephrase to `neonatal mortality` or `infant mortality` to clear the regex. The author should review the rendered PDF and rephrase any false-positive red dots before delivery.

- **Hero subtitle says what is INCLUDED but not what is EXCLUDED.** If the one-pager has been personalized (cut to a specific user's situation), the subtitle must state what was scoped out, so the reader does not assume an omission is an oversight. Worked example: `Personalized reference, scoped to what is NOT already on the plan. Standard vaccines (Tdap, RSV, flu, COVID), low-dose aspirin... are assumed handled and not listed.`

- **Run-on paragraphs in the checklist.** Convert run-on prose checklists to subheadings with bullet lists. A reader scanning a one-pager will glance, not parse comma-separated lists.

- **Hardcoded footer strings.** If the renderer hardcodes a topic-specific string in the page footer, future reports using the same renderer will inherit the wrong footer. The footer should pull from the H1 via CSS `string-set` (current `render_onepager.py` does this correctly after 2026-05-17 fix).

## Quick-start: applying this mode to a new palamedes report

1. Verify the parent `REPORT.md` exists in the project directory, with full palamedes loop already run.
2. Create `ONEPAGER.md` in the same directory.
3. Write the hero block: H1 with topic + version, metadata line, one-paragraph audience-scoping subtitle.
4. Write the SOLID, PROMISING, AVOID tables, one row per claim. Lift effect sizes and primary citations from `REFERENCES.md`.
5. Add a glossary section if any jargon is flagged.
6. Add the time-anchored checklist if the report is action-driving.
7. Add the emergency / escalation strip.
8. Run `render_onepager.py <project-dir>`.
9. Open the resulting PDF. Inspect every AVOID row for a citation. Inspect for false-positive red dots on SOLID rows. Inspect the hero subtitle for clarity on scope.
10. Surface the PDF path and page count to the user.

## Relationship to other palamedes deliverables

| Deliverable | Length | Audience | Render path | Best for |
|---|---|---|---|---|
| Chat reply | 100-800 words | Anyone | inline | L0-L2 questions; no PDF needed |
| `REPORT.md` long-form | 2000-8000 words | Domain expert / careful reader | `render.py` → Letter PDF | L3+ comprehensive reference |
| `ONEPAGER.md` landscape summary | 500-1500 words | Decision-maker / time-constrained / non-specialist | `render_onepager.py` → A4 landscape PDF | L2-L3 at-a-glance reference card |
| `REFERENCES.md` | as needed | Cite-trail follower | not rendered | provenance audit |

The one-pager is the artifact most likely to be printed, shared in chat, or pinned to a fridge or board. Its design should reflect that use case: high information density, glanceable structure, citation-linked, page-print-clean.
