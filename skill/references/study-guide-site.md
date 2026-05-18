# study-guide-site.md - palamedes multi-page study-guide template

Load when the user asks for a palamedes deliverable that is meant to be **studied over weeks**, **opened daily**, or used as a **reference corpus for exam prep / certification / cram program**. The output is a browseable HTML site with a router page, per-day study pages, full rendered corpus, and a pedagogy appendix built on memory-and-recall research.

**Triggers:** "build me a study guide", "exam prep program", "cram program", "certification site", "curriculum site", "weekday cadence", "study program for [N] days", "open in my browser each morning", "make me a daily study site", "ISC2 / CISSP / OSCP / bar / boards / clinical / CFA prep site", "study plan with mnemonics", "memory palace for [exam]", "pedagogy appendix", "spaced repetition program".

This template extends the screen-first multi-page variant from `references/output-rendering.md` with **pedagogy scaffolding**: a memory palace, mnemonic quick-reference, evidence-tagged techniques appendix, and a daily integration schedule that overlays the cadence-data.

## When this template is appropriate

| User goal | This template? |
|---|---|
| One-time PDF for a decision (e.g. babytime/monitors) | No - use `output-rendering.md` PDF mode |
| Landscape skim sheet (e.g. fridge magnet) | No - use `landscape-summary-report.md` |
| Browseable daily-cadence site for N days, no exam | Yes, partial - skip the pedagogy appendix |
| Browseable daily-cadence site for an exam / cert / board | **Yes, full template** |
| Reference encyclopedia, no time component | No - use the long-form PDF mode |

The pedagogy appendix is the load-bearing differentiator. Skip it for non-exam study sites (e.g. a 30-day fitness program); include it for any high-volume rote-plus-application content where the user will be tested.

## Reference implementations

Two worked examples, both at `/Users/wjia/Projects/`:

| Project | Subject | Days | Pages | Pedagogy appendix |
|---|---|---|---|---|
| `qa-prep/study_guide/daily/` | QA Engineering interview prep | 30 | 35 HTML | No (skill-acquisition, not exam) |
| `cc-prep/study_guide/daily/` | ISC2 CC certification cram | 10 weekdays | 16 HTML | **Yes, full Appendix D** |

The CC-prep build is the canonical worked example of this template, including the pedagogy appendix. The qa-prep build is the canonical worked example of the bare multi-page variant.

## Output structure (load-bearing)

A study-guide site has three or four layers of artifacts:

```
study_guide/
├── <Subject>_Study_Guide.md         # primary corpus, 5-10 Parts + Appendices A-D
├── PRACTICE_EXAMS.md                # mock 1-2 (always-include for exam sites)
├── PRACTICE_EXAMS_2.md              # mock 3-4 (weighted to weak domains)
├── glossary.md                      # every initialism defined
├── daily_notes.md                   # persistent user-notes store (delimiter blocks per anchor)
├── daily/                           # HTML site output
│   ├── index.html                   # router (today auto-detect) + server banner + notes tools
│   ├── day-NN.html                  # per-day pages (N = number of cadence days)
│   ├── guide.html                   # full Study_Guide.md rendered
│   ├── exams.html                   # mocks 1-2 rendered
│   ├── mocks2.html                  # mocks 3-4 rendered
│   ├── glossary.html
│   ├── style.css                    # solarpunk screen-first + notes UI + mode pill
│   └── notes.js                     # hybrid LS/BE notes client (vanilla JS, no framework)
├── anki/
│   └── <subject>_glossary.apkg      # spaced-repetition deck
├── scripts/
│   ├── render_html.py               # bakes notes into HTML at build time
│   ├── notes_server.py              # stdlib HTTP: static files + /api/note CRUD
│   ├── build_anki.py
│   └── em_dash_fix.py
└── index.html (at repo root)        # meta-refresh to daily/index.html for GH Pages
```

The Anki deck is mandatory for any exam-prep study site. Spaced repetition is the most evidence-backed technique in the pedagogy literature (Serra et al. 2025), and Anki implements it automatically. The deck-build script ingests `glossary.md` and filters out terms the user already knows from prior context.

## Pedagogy appendix template (Appendix D pattern)

Every exam-prep study site SHOULD include this appendix in the primary corpus. The structure is six subsections, modeled after `cc-prep/study_guide/CC_Study_Guide.md` Appendix D.

### D.1 Evidence summary (load-bearing claims tagged)

Open with the four headline techniques and the three compounders. Each gets:

- One paragraph definition
- A tier-tagged citation
- One bolded "practical for [SUBJECT]" application sentence

The four headlines:
1. **Retrieval practice / testing effect** `[T1-verified, read:body]` (Serra et al. 2025; modern resurgence Roediger and Karpicke 2006)
2. **Transfer-appropriate processing** `[T1-verified, read:body]` (Morris et al. 1977, cited in Serra et al. 2025) - practice form must match test form
3. **Spaced repetition** `[T2-verified]` (Ebbinghaus 1885 + modern meta-analyses)
4. **Method of loci (memory palace)** `[T1-verified, read:body]` (Ondrej et al. 2025 systematic review and meta-analysis, British Journal of Psychology; effect sizes d=0.42-0.88 for immediate serial recall; GRADE rating very low to low)

The three compounders:
5. **Dual coding** `[T2-verified]` (Paivio 1971; mechanism confirmed in Ondrej et al. 2025)
6. **Interleaving** `[T2-cited]` (Rohrer and Taylor 2007; Bjork 1994)
7. **Generation effect** `[T2-cited]` (Slamecka and Graf 1978)
Plus sleep consolidation, elaborative interrogation, chunking as supporting techniques.

Always include the transfer-appropriate-processing caveat: **practice questions transfer better than flashcard recall when the test is MCQ application.** This anchors the recommendation that mocks beat the palace if the user has to pick one.

### D.2 The memory palace (build-your-own framework, with fallback)

**D.2 ships as a build-your-own elicitation framework.** Pre-built palaces are demoted to a fallback block at the end of D.2, framed as "if you have less than 90 seconds." The default path teaches the learner to pick their own space, loci, and images. This is the same self-reference-effect mechanism (Ondrej et al. 2025) that the inline blockquotes lean on; D.2 is its full walkthrough.

The framework has four parts:

**1. Pick your space.** A space the learner can walk through in their head without thinking about it: current home, childhood home, an old apartment, a workplace, a school route. Familiarity is load-bearing; novelty kills the technique. If the learner has no single highly-familiar space, propose two candidates and have them pick one before building.

**2. Map domains to rooms.** N domains in the curriculum → N rooms in the chosen space. The mapping should respect natural traffic patterns (start at the entrance, end at the bedroom) so the walk has narrative direction.

**3. Pick 5-7 loci per room.** Each locus is a piece of furniture, fixture, or named zone. Capacity ceiling: **~2 items per locus** before interference (Ondrej et al. 2025). If a domain has 15 concepts to anchor, the room needs 7-8 loci, not 5.

**4. Build the image at each locus.** For each concept-on-locus pair, the learner writes:
- The spatial reference (which fixture, where in the room)
- A vivid mental image (engages dual coding, per Paivio 1971; mechanism confirmed in Ondrej et al. 2025)
- Optionally a bizarre or emotionally-charged twist (Ondrej et al. 2025: "users to create their own bizarre associations, which are often emotionally charged")

The locus-pattern table below is for the learner to draw on when stuck. It teaches the SHAPE of a useful locus, not the specific image. Image specifics must come from the learner.

**Cadence:** walk the palace before sleep for the first 3 days, then 2x/week. Final walkthrough on exam-eve takes 3-5 minutes total.

**Fallback pre-built palace (demoted, for time-pressured learners only):** include at the end of D.2 in a clearly-marked "Fallback" subsection. Surface the same locus-pattern table the learner would have used. Frame the pre-built palace as a starting kit that the learner is encouraged to overwrite with their own images as they walk it.

**Concrete loci patterns that work across domains:**

| Locus type | Best for | Why |
|---|---|---|
| Multi-shelf pantry/bookshelf | Ordered hierarchies (OSI layers, drug schedules, criminal-statute tiers) | Spatial ordering top-to-bottom maps to list order |
| Four-cushion couch / four-poster bed | 4-item lists where ORDER matters | Each cushion/post is a distinct locus |
| Faucets/burners on stove | Ascending intensity scales (firewall types, surgical urgency, severity codes) | Front-to-back or left-to-right maps to weak-to-strong |
| Spice rack / medicine cabinet bottles | Equivalent-tier alternatives | Each bottle is a distinct option |
| Picture-in-picture TV / mirror reflection | Relationship diagrams (PKI flow, IPsec topology, contract-formation flow) | Multiple elements visible at once |
| Toothbrushes / sponges in a row | 3-state classifications (data states, sleep stages, perfusion states) | Visual scale of intensity or progression |

### D.3 Domain-by-domain mnemonic quick reference

For each domain, list the highest-leverage acronyms and chunks. Optimize for order-sensitive lists. Avoid mnemonics for unordered conceptual material - they waste effort.

Mnemonic typology to consider:

- **Acronyms** (PASA, ATMA, PDCP) for short ordered lists where first letters spell something
- **Acrostics** ("All People Seem To Need Data Processing" for OSI) for medium ordered lists
- **Chunking** (port numbers grouped by function) for high-volume rote of numerical content
- **Number-shape or major system** for arbitrary digit sequences (rarely needed for cert exams)
- **Story method** when items have a natural narrative sequence (e.g. attack-chain phases)

Always state the mnemonic in BOTH expanded form AND its compressed form. The compressed form is the retrieval cue; the expanded form is the verification target.

### D.4 Daily integration schedule

Overlay the pedagogy on the cadence-data. One row per day. Three columns:

| Day | Memory work (15-30 min, evening) | New techniques to apply |
|---|---|---|

The schedule should:
- Build palace rooms incrementally (Day 1 = one room, by mid-program all rooms anchored)
- Introduce one new technique each day or every-other-day
- Schedule post-mock palace-re-anchoring sessions ("After Mock 2: anchor 5 missed concepts at vacant loci")
- End with a no-new-material day before the exam and an explicit sleep target

### D.5 Honest caveats

Always include these five caveats, customized to subject:

1. **The mocks beat the palace.** Retrieval practice has decades of replication; MoL has effect sizes but GRADE very low-to-low. Anchor time accordingly.
2. **Mnemonics encode pointers, not understanding.** Use them as access paths, not substitutes.
3. **Transfer-appropriate processing applies to the learner too.** Practice form should match exam form.
4. **Memory palaces have a known capacity ceiling.** ~2 items per locus.
5. **Sleep matters more than one more re-read.** Slow-wave + REM consolidation. If choosing between cram and bed, go to bed.

### D.6 Sources

The minimum citation list for the pedagogy appendix:

- `[T1-verified, read:body]` Ondrej J. et al. (2025). "The method of loci in the context of psychological research: A systematic review and meta-analysis." British Journal of Psychology. PMC12514325. https://pmc.ncbi.nlm.nih.gov/articles/PMC12514325/
- `[T1-verified, read:body]` Serra M.J., Kaminske A.N., Nebel C., Coppola K.M. (2025). "The Use of Retrieval Practice in the Health Professions: A State-of-the-Art Review." PMC12292765. https://pmc.ncbi.nlm.nih.gov/articles/PMC12292765/
- `[T2-cited]` Roediger H.L., Karpicke J.D. (2006). "Test-enhanced learning."
- `[T2-cited]` Morris C.D., Bransford J.D., Franks J.J. (1977). "Levels of processing versus transfer appropriate processing."
- `[T2-cited]` Paivio A. (1971). Imagery and Verbal Processes.
- `[T2-cited]` Miller G.A. (1956) / Cowan N. (2001). Working memory capacity.
- `[T2-cited]` Bjork R.A. (1994). Desirable difficulties.
- `[T2-cited]` Rohrer D., Taylor K. (2007). Interleaving.
- `[T2-cited]` Slamecka N.J., Graf P. (1978). Generation effect.
- `[T2-cited]` Walker M. (2017). Why We Sleep.
- `[priors-only]` Ebbinghaus H. (1885). Über das Gedächtnis.

Both T1-verified sources should be body-read before shipping the appendix. The retrieval-practice review (Serra et al. 2025) is the load-bearing source for technique-1 and technique-2; the MoL meta-analysis (Ondrej et al. 2025) is the load-bearing source for technique-4 and for the capacity-ceiling caveat.

## Inline memory-anchor blockquotes (elicitation-first)

In addition to Appendix D, insert a one-paragraph blockquote at the top of each major Part of the corpus. **The blockquote is an elicitation prompt, not a dictation.** The learner picks the room, the loci, and the images. The blockquote scaffolds the choice; it does not pre-populate it.

This is a load-bearing decision derived from Ondrej et al. 2025 § "autobiographical memory, self-reference effect, and emotional context enhancement". User-generated bizarre associations encode stronger than experimenter-supplied ones. A blockquote that hands the learner a fixed palace bypasses the self-reference mechanism and reduces the technique to rote re-reading. **The dictation regression has been observed in earlier study-site builds; ship elicitation by default.**

Pattern (elicitation):

```markdown
## Part N - [Domain Name]

> **Memory anchors for Part N - [Domain Name].** Pick one room of a familiar
> space (your home, an old apartment, a workplace). For each of the 4-6
> highest-leverage chunks below, choose a locus inside that room and a
> vivid image that fixes the chunk in place. Spend two minutes building it
> now; walk it again tonight before sleep.
>
> - **[Chunk 1 label]**: [one-line referent describing the thing to anchor, not how to anchor it]
> - **[Chunk 2 label]**: [...]
> - **[Chunk 3 label]**: [...]
> - **[Chunk 4 label]**: [...]
>
> See Appendix D.2 for the build-your-own framework, the locus-pattern
> table, and a pre-built fallback palace if you have less than 90 seconds.

[Part body continues...]
```

Markdown blockquotes render as styled callouts in both the long-form PDF mode and the screen-first variant. The blockquote should be the FIRST element under the Part heading, before the introductory paragraph.

The fallback pre-built palace from Appendix D.2 is still shipped in the corpus for time-pressured learners. It is **demoted to "fallback" in framing**, not removed. The default path is the elicitation framework.

## Per-section elicitation at miss-pattern sub-sections

In addition to the Part-level blockquotes, insert a short elicitation prompt at every sub-section under Appendix B (the high-frequency miss patterns). Pattern from `cc-prep/study_guide/CC_Study_Guide.md` Appendix B:

```markdown
### Miss pattern N: [Confusion or trap]

> **Anchor this trap.** Pick a single image you will never forget that
> separates [correct concept] from [wrong concept]. Write the image in one
> sentence below; commit it to a locus in your palace tonight.

[Body explaining the miss pattern, the correct answer, and why the trap is common.]
```

This pattern works because miss patterns are exactly the points where the learner has already failed once. The mechanism is the testing effect (Serra et al. 2025) compounded with self-generated imagery (Ondrej et al. 2025). The prompt forces a fresh encoding at the failure surface.

Target one elicitation prompt per miss pattern. For the cc-prep build that produced 14 prompts across 15 miss patterns (one pattern had no useful image-separability and was left as plain prose).

### Appendix-level blockquote at the top of the miss-pattern section

In addition to the per-pattern prompts, place ONE blockquote at the top of the miss-pattern appendix (Appendix B in cc-prep) that asks the learner to bind each pattern to a locus that ALREADY exists in their D.2 palace, rather than creating new loci. The mechanism: a miss pattern is almost always a disambiguation trap on content the learner already encoded once. The fresh encoding should sit at the existing locus as a secondary detail (a small sign on the post, a sticker on the jar), not at a new locus that competes for capacity.

```markdown
## Appendix B - High-frequency miss patterns

> **Memory anchors for Appendix B miss patterns.** Each of the patterns
> below corresponds to content you already anchored in your palace
> (D.2). Walk the relevant room, find the existing locus for the
> concept, and add ONE secondary detail at that locus that captures the
> miss-pattern trap (the disambiguation, the rule, the off-by-one).
> Two minutes per pattern; about 30 minutes total across the week.
>
> See Appendix D.2 for the palace map and D.2.1 for the pre-built fallback.
```

This blockquote is the load-bearing connector between Appendix B and Appendix D.2; without it, learners encode miss patterns as a flat list and lose the palace structure. With it, the miss patterns become disambiguators on existing anchors, which is the actual pedagogical job.

## Persistent user-notes feature (hybrid localStorage + backend)

Study-guide sites have a load-bearing pedagogical use for user-annotation: as the learner takes mocks and re-reads the corpus, they generate per-section observations ("this is where I keep tripping up", "my image for the OSI palace shelf is X"). These observations belong with the section that generated them, and they belong somewhere durable. Without a notes feature, learners reach for a separate notebook or text file, lose the spatial co-location with the section, and lose the durability across rebuilds when the site re-renders.

The cc-prep build is the canonical implementation. It ships three modes, ranked from most-capable to least:

| Mode | Trigger | Add / edit / delete | Storage |
|---|---|---|---|
| **BE** | localhost + backend running | Yes | Writes through to markdown source files |
| **LS** | localhost or `file://`, BE not running | Yes (new notes only) | `localStorage` only |
| **Pages** | non-localhost deployment (e.g. GitHub Pages) | Yes (new notes only) | `localStorage` only, banner explains read-only |

Baked-in notes from the markdown source render correctly in all three modes. Only the write path varies.

### Architecture

```
study_guide/
├── daily_notes.md          # persistent store: <!-- user-notes:ANCHOR --> blocks
├── CC_Study_Guide.md       # corpus; user-notes blocks for non-day anchors
└── daily/
    ├── notes.js            # client: BE probe, LS, CRUD, import/export
    ├── style.css           # +note button, edit form, banner, mode pill
    └── *.html              # baked-in <aside class="user-note"> at build time
scripts/
└── notes_server.py         # stdlib HTTP: static files + /api/note CRUD
index.html                  # root-level redirect to daily/index.html (GH Pages entry)
```

The backend is a single Python file using `http.server.ThreadingHTTPServer` with no third-party dependencies. The client is one vanilla-JS file with no framework. Both can be lifted into a new study-guide build with minimal modification.

### Anchor scheme

Every notable section in the corpus exposes an anchor that notes can attach to. The conventions cc-prep uses:

- Day pages: three anchors per day (`day-N-focus`, `day-N-citations`, `day-N-links`).
- Corpus pages: every `h2` heading carries `data-notable-anchor="corpus-{basename}-{slug}"`, where `basename` is the corpus-page filename without extension (e.g. `guide`, `exams`, `mocks2`, `glossary`) and `slug` is the heading's auto-generated id. The per-page basename namespace is load-bearing: it prevents anchor collisions between two corpus pages that happen to share a slug (e.g. both `glossary.html` and `guide.html` could have an `h2 id="a"`).
- The BE accepts any `^[a-z0-9-]+$` anchor. The renderer's `target_file_for_anchor` function routes `day-N-*` anchors to `daily_notes.md` and everything else to the primary corpus markdown.

In the rendered HTML, notable sections carry `data-notable-anchor="ANCHOR"`. The client finds these on page load and wires a `+ note` affordance to each.

Implementation note: `render_corpus_page` accepts a `basename` argument and a shared `notes_by_anchor` dict. For every `h2` in the rendered markdown the renderer injects the `data-notable-anchor` attribute AND appends any baked-in user notes for that anchor inline. The same `parse_daily_notes` + `render_user_notes_html` helpers used for day pages are reused unchanged.

### Backend API contract

```
POST   /api/note            body: {anchor, text}    → {ok, note_id}
PUT    /api/note/<note_id>  body: {text}            → {ok, note_id}
DELETE /api/note/<note_id>                          → {ok, note_id}
```

Note IDs auto-assign as `note-<anchor>-<N>` in source order. Notes are stored as markdown lines inside delimiter blocks:

```markdown
<!-- user-notes:day-1-focus -->
*the OSI shelf I built has Application on top: toaster, kettle, salt cellar...*{.user-note #note-day-1-focus-1}
<!-- /user-notes:day-1-focus -->
```

The `*text*{.user-note #id}` syntax uses `markdown-it-attrs` to render as `<aside class="user-note" id="note-day-1-focus-1">`. Special characters in user text (`\`, `*`, `{`, `}`) are escaped with backslash on write and decoded on read.

### Client probe

On page load, `notes.js` POSTs `{}` to `/api/note`. A 400 response (BE's "anchor and text required") signals BE is reachable. Network error signals BE is offline. The probe runs only on `localhost`/`127.0.0.1` hostnames; non-localhost hosts skip the probe and use LS mode directly. Probe timeout is 800ms via AbortController.

### Server-start banner and mode pill

The index page renders a callout near the top with the exact backend-start command and a click-to-copy button. The banner is hidden by default and revealed by JS based on mode:

- BE mode: "Backend running. Notes save to markdown." (green callout, copy-block hidden)
- LS mode: "Backend not running. Notes save to your browser only." (info callout, copy-block visible)
- Pages mode: "Read-only deployment. Notes save to your browser only." (info callout, copy-block visible, explains how to clone and run locally)

Non-index pages get a small bottom-left mode pill instead of the full banner. Bottom-left is thumb-zone friendly per the Buds garden-home UX defaults (right-thumb users; top-right is the worst zone for frequently-used affordances).

### Import / export for sync

LS mode and Pages mode have an export button on the index that downloads all browser-stored notes as `daily_notes_export_YYYY-MM-DD.md`. The export uses the same delimiter-block format `daily_notes.md` uses, so import via the file picker either POSTs each note to BE (when running) or merges into LS (when not).

Typical sync workflow for a learner who takes notes on their phone:

1. Phone on Pages: jot notes throughout study. Notes accumulate in browser storage.
2. Laptop on Pages: open index, click Export, get the markdown file.
3. Laptop with backend running: open `http://localhost:8765/`, click Import, select the file. Notes land in `daily_notes.md`. Commit.
4. Next render rebakes the notes into HTML so they display everywhere.

### Optimistic DOM insert

Add and edit operations update the DOM immediately, then send the BE / LS write asynchronously. On BE failure, the operation surfaces an alert and rolls back. The pedagogical reason for optimistic insert: at study velocity, even 200ms of latency between "I typed a thought" and "the thought appears beside the section that prompted it" breaks the encoding loop. Optimistic insert keeps the loop tight.

### Why this is hybrid and not "just localStorage" or "just BE"

`localStorage`-only loses the durability across rebuilds: when the renderer regenerates HTML, baked-in notes survive but LS notes only exist in the one browser that wrote them. Backend-only loses the offline path: learners on a phone or on a different machine can't add notes. The hybrid model preserves both: BE is the canonical store for durable, sharable notes; LS is the offline fallback that round-trips through export/import.

### Failure modes specific to the notes feature

- **CORS or mixed-content blocking the probe on non-localhost hostnames.** The probe runs only on `localhost`/`127.0.0.1` by design. Never call `http://localhost:...` from an `https://...example.github.io/...` page; the request will be blocked. The mode-detection function short-circuits to `pages` mode for non-localhost hosts before the probe runs.
- **Baked-in notes opened for edit while BE is offline.** Without a guard, the edit form opens, the user types, Save fails with an error. cc-prep gates the click handler: baked notes (`data-source="baked"`) only open an edit form when BE is reachable. Offline learners get a single clear alert instead.
- **Note ID collisions on import-then-add.** Imports preserve note IDs in the export. If a learner imports a file from a separate device after adding new notes locally, IDs can collide. The import path mints new IDs (`note-ls-<anchor>-<ts>-<seq>`) rather than reusing the imported ones for this reason.
- **Print rules.** The notes feature elements (banner, pill, +note button, edit form) must be `display: none` in print rules. The persistent `<aside class="user-note">` notes themselves SHOULD print, in the gutter.

## Generator and Anki integration

The render pipeline is the same as `references/output-rendering.md` screen-first variant. Add a small generator for the Anki deck:

```python
# scripts/build_anki.py
import genanki
# Parse glossary.md
# Filter out user's known-terms exclusion list
# Emit .apkg with domain tags
```

The exclusion list lives in `scripts/build_anki.py` as a top-of-file constant. Update it before each rebuild based on user's stated prior knowledge ("I already know HTTP/HTTPS, TLS, AES, OAuth..."). The principled defaults to exclude:

- Web fundamentals the user works with daily (HTTP/HTTPS, TLS, REST, OAuth, SAML, OIDC, JWT)
- Crypto primitives the user has shipped (AES, RSA, SHA-256, hashing)
- Compliance frameworks the user has audited (GDPR, HIPAA, SOX, PCI DSS)
- Attack types covered in OWASP Top 10 the user has worked on (SQLi, XSS, CSRF)

Card count target: 60-150 per domain-set. Tags should match domains and cross-cutting categories (e.g. for ISC2 CC: `D1 D2 D3 D4 D5` plus `acl bc crypto ethics ir net nist phys pki risk`).

## Workflow: applying the template to a new subject

1. **Pre-flight (palamedes loop on the curriculum):**
   - Pull the official exam outline / curriculum / syllabus. Read body.
   - Identify N domains and their weightings.
   - Ask the user for prior knowledge scores per domain (this drives content weighting and Anki exclusion list).
   - Confirm the learner has a highly-familiar space available for the memory palace; if not, agree on a candidate before D.2 is written.

2. **Build the corpus:**
   - Write `<Subject>_Study_Guide.md` with N Parts (one per domain), weighted to user's weak spots
   - Write `PRACTICE_EXAMS.md` with mocks 1-2 (exam-weight matched)
   - Optional `PRACTICE_EXAMS_2.md` with mocks weighted to weak domains
   - Write `glossary.md`

3. **Build the pedagogy appendix (elicitation-first):**
   - Run the palamedes loop on the memory-and-recall literature (or cite this reference and the two T1 sources already retrieved)
   - Write D.2 as a build-your-own framework with locus-pattern table; demote any pre-built palace to a Fallback subsection at the end of D.2
   - Write the mnemonic quick-reference per Part
   - Write the daily integration schedule
   - Include all 5 honest caveats

4. **Insert inline memory-anchor blockquotes (elicitation):**
   - One elicitation blockquote at the top of each Part (pattern above)
   - One short elicitation prompt at every miss-pattern sub-section under Appendix B
   - Cross-reference Appendix D.2 from each Part blockquote
   - Verify no blockquote dictates a specific image to the learner

5. **Build the daily site:**
   - Copy `cc-prep/scripts/render_html.py` and `cc-prep/study_guide/daily/style.css`
   - Edit the `DAYS` data structure
   - Generate

6. **Build the persistent notes feature:**
   - Copy `cc-prep/scripts/notes_server.py` (stdlib HTTP, no deps to install)
   - Copy `cc-prep/study_guide/daily/notes.js` (vanilla JS client)
   - Scaffold `study_guide/daily_notes.md` with three delimiter blocks per day (`day-N-focus`, `day-N-citations`, `day-N-links`)
   - In the renderer, add `parse_daily_notes` + `render_user_notes_html` helpers and wrap notable sections with `data-notable-anchor` markers
   - For corpus pages (guide, exams, mocks2, glossary, or whatever the build calls them), extend `render_corpus_page` to accept a `basename` argument and inject `data-notable-anchor="corpus-{basename}-{slug}"` on every `h2`, with baked-in user notes appended inline. Wire each corpus-page call site to pass its own basename and the shared `notes_by_anchor` dict.
   - Add the server-start banner to the index render and the `<script src="notes.js" defer>` include to `PAGE_TMPL`
   - Add the notes-tools section (Export / Import / Clear) to the index
   - Add a root-level `index.html` meta-refresh redirect to `study_guide/daily/index.html` for GH Pages compatibility

7. **Build the Anki deck:**
   - Copy `cc-prep/scripts/build_anki.py`
   - Edit the exclusion list per user's prior knowledge
   - Generate the .apkg

8. **Verify:**
   - All HTML files render without em-dashes (scrub before render)
   - Router auto-routes to today's page
   - All Part blockquotes render as styled callouts AND read as elicitation, not dictation
   - Appendix D.4 schedule lines up with the cadence dates
   - Anki deck imports cleanly
   - Notes feature smoke test: start `notes_server.py`, POST a note, verify it lands in `daily_notes.md`, PUT to update, DELETE to remove, confirm the markdown is restored. Static-file serving returns 200 for `index.html` and `notes.js`.
   - GH Pages dry-run: open `study_guide/daily/index.html` directly via `file://` (no backend, no localhost); confirm baked-in notes display, mode pill says "view-only", server banner shows the start command, and Export downloads a clean markdown file.

## Failure modes specific to study-guide sites

- **Pedagogy appendix without T1-verified sources.** The memory-palace and retrieval-practice claims are load-bearing for the entire pedagogy section. Body-read Ondrej 2025 and Serra 2025 before shipping. Citation laundering ("studies show spaced repetition works") is an iron-law violation per palamedes Anti-Pattern #5.
- **Dictation regression in inline blockquotes.** Cascade default is often to hand the learner a fixed palace with named loci and images. This bypasses the self-reference mechanism (Ondrej et al. 2025) and degrades the technique. The blockquote must scaffold the learner's choice, not pre-populate it. Pre-built fallback exists in D.2; do not let it migrate up into the Part-level blockquotes.
- **Memory palace built on an unfamiliar space.** The palace works because the route is HIGHLY familiar (Ondrej et al. 2025: "autobiographical memory, self-reference effect, and emotional context enhancement"). If the user does not have a single familiar space they could walk through in their head, propose a workplace or childhood home instead of inventing one.
- **>2 concepts per locus.** Violates the capacity ceiling and produces interference. If a Part has 15 concepts, the room needs 7-8 loci, not 5.
- **Mnemonics for unordered material.** The acronyms work because they encode SEQUENCE. For unordered conceptual material (e.g. "what is the CIA triad"), the user needs comprehension, not a mnemonic.
- **Daily schedule that introduces too much per day.** Cram fatigue is real. Cap each day at: one Domain section read + one Anki block (15-25 min) + one palace-walk (5 min) + on Mock days the mock itself (2 hours). Anything more produces diminishing returns.
- **Em-dashes in HTML output.** Banned per Wei voice rules. The render pipeline includes `scripts/em_dash_fix.py` that should run BEFORE the HTML generator. Verify zero em-dashes in generated HTML before declaring done.
- **Skipping the "mocks beat the palace" caveat.** Without this caveat, learners over-invest in mnemonics. The caveat must appear in D.5 AND in any user-facing recommendation about how to spend study time.
- **Notes feature shipped without GH Pages compatibility.** If the renderer assumes BE is always reachable, the deployed site silently breaks the write path on Pages. Always implement the three-mode probe (BE / LS / Pages) and the read-only banner from day one, not as a follow-up. See the dedicated notes-feature failure-mode list in the Persistent user-notes feature section above for CORS, baked-edit-while-offline, and ID-collision pitfalls.

## Cross-references

- Screen-first multi-page mechanics (router, daily pages, margin notes): `references/output-rendering.md`
- Long-form PDF design system (solarpunk palette, Letter portrait): `references/output-rendering.md`
- Landscape one-pager skim sheet for the exam-prep dashboard: `references/landscape-summary-report.md`
- Source grading for the pedagogy citations: `references/source-grading.md`
- LLM-as-instrument check for the appendix sources: `references/llm-failure-modes.md`
- Thumb-zone defaults for mobile affordances (mode pill placement): MEMORY[414a438e] (Buds garden-home UX defaults, 2026-05-17)

## Version history

- **v3 (2026-05-18, same day as v2):** Added the Appendix-level miss-pattern blockquote pattern that binds miss patterns to existing D.2 loci as secondary details (rather than creating new loci that compete for palace capacity). Added the per-corpus-page anchor namespace (`corpus-{basename}-{slug}`) to the Anchor scheme section, including the implementation note that `render_corpus_page` accepts a `basename` argument and threads `notes_by_anchor` through. Extended Workflow step 6 with the corpus-page extension bullet so the notes feature works on guide / exams / mocks2 / glossary pages, not just day pages. Source: cc-prep commit `dfe1ca4` (corpus-page notes anchors + mnemonic sweep).
- **v2 (2026-05-18, same day as v1):** Reframed inline memory-anchor blockquotes as elicitation prompts (D1A), demoted pre-built palaces to a fallback in D.2, added the per-section elicitation pattern at miss-pattern sub-sections, added the entire persistent user-notes feature section (hybrid LS/BE/Pages with optimistic DOM insert, server-start banner, mode pill, import/export markdown), updated Output structure to include `daily_notes.md`, `notes_server.py`, `notes.js`, and the root-level GH Pages redirect, expanded Workflow with step 6 (notes feature) and a notes/GH-Pages smoke-test verify, added the dictation-regression and notes-feature failure modes. Source: cc-prep build through 2026-05-18, commits `3f0e0d8` (D1A) and `5f403c4` (Chunk 3).
- v1 (2026-05-18): Extracted from `output-rendering.md` screen-first multi-page variant. Added pedagogy appendix template, memory palace pattern, inline memory-anchor blockquote pattern, daily integration schedule pattern. CC-prep is canonical worked example.
