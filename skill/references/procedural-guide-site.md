# procedural-guide-site.md — palamedes fix / how-to / setup guide (single-file HTML)

Load when the user asks for a **step-by-step guide to fix, build, install, or configure something** and wants an **offline, phone-friendly HTML walkthrough** — not a markdown memo, not a multi-day study site, not a PDF report.

**Triggers:** "fix guide", "how to fix", "walkthrough", "step by step", "setup guide", "install guide", "repair guide", "make me a guide like the forester", "procedural guide", "put it back together", "reassembly steps", "tool organization", "shopping list by workflow", "rag pc setup guide", "signal setup guide", "palamedes guide", "HTML guide I can open in the browser".

**Not this template:** exam cram / daily cadence → `study-guide-site.md`. Decision PDF for a buyer → `output-rendering.md`. One-page skim → `landscape-summary-report.md`.

## When this template is appropriate

| User goal | Template |
|---|---|
| Fix a car part / appliance / hardware with remove + reinstall | **Yes** |
| Software install (RAG PC, Signal, self-hosted stack) | **Yes** (adapt `#restore-bay` → `#restore-system` or `#restore-desktop`) |
| Research report / product comparison | No — markdown + optional PDF |
| 30-day study program | No — study-guide site |
| Quick chat answer, no artifact | No — plain palamedes chat output |

## Reference implementations

| Guide | Path | Domain |
|---|---|---|
| **Canonical worked example** | `~/Downloads/2015-forester-ac-clutch-fix-guide.html` (+ `2015-forester-ac-clutch-fix-guide-images/`) | Physical repair — shim-first A/C clutch |
| **Template skeleton** | `~/Projects/palamedes/templates/procedural-guide/template.html` | Copy → fill placeholders |

Run palamedes P1→P4 **before** authoring: tier-tag load-bearing specs (torque, gap, version pins, security settings). The HTML is the **product**; `localonly/<slug>-research.md` holds citations and adversarial notes at L2+.

## Output contract (load-bearing)

### Deliverable layout

```
<output-dir>/
├── <slug>-guide.html          # self-contained HTML (CSS inline) OR html + css/ + images/
├── <slug>-guide-images/       # optional; relative paths from HTML
│   ├── ATTRIBUTIONS.md        # required if third-party photos
│   └── forum/ …               # optional subfolders
└── localonly/                 # optional at L2+
    ├── <slug>-REFERENCES.md
    └── <slug>-research.md
```

**Default:** one `.html` file with inline `<style>` so it opens from `file://` in a garage or on a phone with no server.

### Mandatory section IDs

Every guide MUST implement these anchors (empty sections OK only if truly N/A — disclose in `#overview`):

| ID | Purpose |
|---|---|
| `#start-here` | Go/no-go test before disassembly or install (symptom → confirm → next) |
| `#shopping` | Parts/tools split by **workflow**, not one merged junk drawer |
| `#wf-primary` | Minimum path (start here) — first workflow table |
| `#wf-*` | Optional fallbacks only if symptom needs them (relay, relay test, tier-2 fix…) |
| `#bench-setup` | Tray zones, zip bags, photo-before-remove, phase discipline |
| `#walkthrough` | Lettered parts A…K (expand/shrink as needed; see below) |
| `#restore-*` | **Put it back** — domain-specific (`#restore-bay`, `#restore-desktop`, `#restore-vm`) |
| `#verify` | Success criteria + rollback if verify fails |
| `#safety` | Hazards, PPE, irreversible steps |
| `#prevent` | Recurrence / maintenance / when to escalate |

Sticky nav MUST link at minimum: Start here · Walkthrough · Bench layout · Put it back · Parts & buy · Safety.

### Walkthrough part lettering (symmetric remove / reinstall)

Palamedes guides treat **reassembly as first-class**, not an afterthought.

| Phase | Typical parts | Content |
|---|---|---|
| Diagnose / gate | `#start-here` | Tap test, version check, backup confirm |
| Open access | **A** | Remove covers; **photo + bag bolts** |
| Preconditions | **B** | Lube, anti-seize, config export — what touches what |
| Primary disassembly | **C–E** | Remove, adjust, one critical change only |
| Reinstall transition | **F** | Switch trays; verify preserved parts |
| Reassembly | **G–I** | Seat component, draw-in tool, final fastener |
| Restore environment | **J** (`#restore-*`) | Overflow tank, cable routing, service restart |
| Verify | **K** (`#verify`) | Measurements, smoke test, 30-min soak |

**Rules:**
- Every **remove** step that frees a fastener or hose gets a matching **restore** substep in Part J (or inline if trivial).
- Use `ol.substeps` for ≥3 micro-steps inside one numbered step.
- Use `ul.checklist` for tool sweeps and “nothing left in bay” audits.

### Bench setup card (required inside `#walkthrough` or `#bench-setup`)

Include a `table.kit-table` with columns: **Zone · What lives here · When you need it**.

Minimum zones:
1. **At-work-site kit** — tools in hand the whole job
2. **Remove pile** — disassembly-only consumables
3. **Install pile** — do not open until transition part
4. **Labeled bags** — name each (`REMOVED SHIM`, `OVERFLOW 10 MM`, …)
5. **Rest surface** — where removed assemblies sit

### Shopping / workflows (required in `#shopping`)

- Split tables by **workflow** with `#wf-<slug>` anchors.
- Tag line: `$ range · when to use` (e.g. "Shim only · start here").
- State primary retailer preference once (domain default or user standing rules — e.g. local hardware vs vendor docs).
- **Reject paths** in prose: what NOT to buy (wrong head, wrong length, wrong tier).
- Link-check note with date optional for URLs.

### Evidence in the HTML

- Load-bearing numbers (gap, torque, version, port): tag in `research-note` or footnote with `[verified]` / `[inferred]` / `[unknown]`.
- Forum or third-party photos: `ATTRIBUTIONS.md` + link in `fig-cap`.
- Do not fabricate ASINs or part numbers — `[unknown]` + spec string is better than a guessed SKU.

## Visual system

Copy CSS from `templates/procedural-guide/template.html` (dark garage-friendly palette). Do not fork a third theme per guide.

| Class | Use |
|---|---|
| `ol.steps` | Numbered walkthrough |
| `ol.substeps` | a/b/c under a step |
| `ul.checklist` | Audits, cleanup |
| `.card` | Checklists, bench setup, after-job |
| `.alert-danger` / `.alert-warn` / `.alert-info` | Irreversible / caution / info |
| `.retailer-table` | Shopping workflows |
| `.kit-table` | Bench zones |
| `.forum-photo` | Full-width community photos |
| `details.defer` | Optional paths (relay swap, advanced debug) |

## Domain adaptation cheatsheet

| Domain | `#start-here` | `#restore-*` | `#bench-setup` twist |
|---|---|---|---|
| Auto repair | Tap test + feeler gauge | `#restore-bay` | Fender tray, zip bags for bolts |
| RAG / local LLM PC | GPU/driver/version gate | `#restore-desktop` | USB stick with configs; separate install vs debug piles |
| Signal / privacy app | Backup + key export | `#restore-phone` | Old phone stays on tray until verify |
| Home appliance | Unplug + water shutoff | `#restore-kitchen` | Towels, drip pan |

## Authoring workflow (palamedes session)

1. **P1 Frame** — stakes (L2 typical for DIY fix), pre-register success criterion.
2. **P2 Retrieve** — service manual, forum thread, vendor docs, version pins.
3. **P3 Adversarial** — what breaks if user skips reinstall step? Wrong bolt? Wrong config flag?
4. **P4 Synthesize** — fill template; **write restore parts before shipping**.
5. **Verify artifact** — open HTML locally; click every nav anchor; confirm `#restore-*` exists.

Optional at L3: companion `ADVERSARIAL_REVIEW.md` per `SKILL.md` §5a.

## Failure modes to avoid

- **Remove-only guide** — user reaches dead end at "install reverse of removal." Forbidden.
- **One shopping table** — mixes primary fix with fallbacks; user over-buys.
- **No labeled bags** — lost center bolt, wrong shim stack.
- **External CSS/CDN** — breaks offline in garage.
- **Magic Patterns for this template** — use inline CSS skeleton; MP is for app UI (`html-design-workflow.md`), not procedural guides.

## Quick-start

```bash
cp ~/Projects/palamedes/templates/procedural-guide/template.html ~/Downloads/my-project-guide.html
# Edit placeholders; add images/ sibling folder; open in browser
```

Tell the user the output path when done.
