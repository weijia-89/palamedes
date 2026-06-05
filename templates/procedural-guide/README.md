# Procedural guide template (palamedes)

Single-file offline HTML for **fix / install / setup** walkthroughs.

| File | Role |
|------|------|
| `template.html` | Copy → fill `{{placeholders}}` → save as `<slug>-guide.html` |
| `../../skill/references/procedural-guide-site.md` | Full output contract, section IDs, part lettering |

**Worked example:** `~/Downloads/2015-forester-ac-clutch-fix-guide.html`

**Quick start:**

```bash
cp template.html ~/Downloads/my-rag-pc-guide.html
# open in editor; replace placeholders; add sibling *-guide-images/ if needed
open ~/Downloads/my-rag-pc-guide.html
```

Trigger in Cursor: ask palamedes for a **fix guide**, **setup guide**, or **walkthrough** with HTML output.
