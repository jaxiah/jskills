---
name: md-code-tour
description: Explore a codebase and produce TWO complementary artifacts — a navigable Markdown document (note-centric reading) and a `.tour` file (code-centric navigation in Neovim via codetour.lua). Always output both files for the same conceptual tour.
---

# md-code-tour

Generate two files that support two reading modes for the same codebase tour:

- **Note-centric** (`<name>.md`): prose-first document with `file:line` references, jumpable via `gF` in Neovim.
- **Code-centric** (`<name>.tour`): JSON content, `.tour` extension. Loaded into Neovim's quickfix + description panel via `:TourLoad`; also natively supported by VS Code codetour extension.

The two files **must share the exact same basename** — `:TourLoad` auto-detects `<stem>.tour` from the open `<stem>.md` buffer.

### Naming rule

Tour filename = MD filename with `.md` replaced by `.tour`. Example: `llm-walkthrough.md` → `llm-walkthrough.tour`.

---

## Output 1 — Markdown document (`<name>.md`)

### File references

Always use paths **relative to the repo root**:

```
`optimum/exporters/openvino/model_configs.py:1738`
```

Jumpable with Neovim `gF` (cursor on path, press `gF`) or `gf` with vim-gf-file-line.

### Document structure

````markdown
# <Title>

Brief one-paragraph overview of what this document covers and why it matters.

> **Navigation tip**: place cursor on any `file:line` reference and press `gF` to jump.
> For step-by-step code navigation: `:TourLoad` then `]q` / `[q`.

---

## Overview table (optional)

| File              | What changes / why it matters |
| ----------------- | ----------------------------- |
| `path/to/file.py` | ...                           |

---

## Step N: <Name>

**File**: `path/to/file.py:LINE`

Prose explanation of _why_ this step exists and what problem it solves.

```python
# Inline snippet: only the key lines, not the whole function
def key_function(...):
    return something_interesting
```

Optional: comparison table, edge-case note, "why not X?" callout.
````

---

## Output 2 — Tour JSON (`<name>.tour.json`)

### Format

```json
{
  "title": "Feature X: implementation walkthrough",
  "description": "How Feature X is implemented across the codebase, in the order a reader would trace the data flow.",
  "steps": [
    {
      "file": "src/core/processor.py",
      "line": 42,
      "description": "**[1/3] Entry point — where the request arrives**\n\n`process()` is the top-level function. It validates the input, delegates to the subsystem, and returns the result. This is the right place to start reading."
    },
    {
      "file": "src/subsystem/handler.py",
      "line": 10,
      "description": "**[2/3] Core logic — the main transformation**\n\n`handle()` does the heavy lifting. It takes the validated input from step 1, applies the transformation, and produces an intermediate result that step 3 will consume."
    },
    {
      "file": "src/output/formatter.py",
      "line": 88,
      "description": "**[3/3] Output — format and return**\n\n`format_result()` converts the intermediate result into the final output shape. Note the special handling for edge cases on line 95 — this is where most bugs have historically appeared."
    }
  ]
}
```

### Field rules

| Field                 | Required    | Notes                                                                                                              |
| --------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------ |
| `title`               | yes         | Short name shown in quickfix title bar                                                                             |
| `description`         | recommended | Top-level tour summary (shown in quickfix title, can be multiline)                                                 |
| `steps[].file`        | yes         | Path **relative to repo root** (Neovim always launched from root)                                                  |
| `steps[].line`        | yes         | 1-based line number; verify accuracy before writing                                                                |
| `steps[].description` | yes         | Full description; supports markdown (`**bold**`, `\n\n` paragraphs); displayed in the persistent description panel |

### Step description style

- Start with `**[N/Total] Short title**` so the one-line preview in the quickfix window is useful.
- Add a blank line (`\n\n`) before the detailed explanation.
- Use `\n\n` for paragraph breaks, `\n` for line breaks within a paragraph.
- Inline code: backticks (`` `symbol` ``).
- No need to repeat the file/line — the panel header shows it.
- **Never use bare ASCII double quotes `"` inside description strings.** They break JSON parsing. Use curly quotes `"..."` (U+201C/U+201D), corner brackets `「...」`, or escape as `\"`. Backticks are preferred for quoting terms inline anyway.

---

## Workflow

1. **Understand the scope**: ask what logic to document (feature, data flow, refactor, etc.)
2. **Explore the codebase**: read relevant files, find exact line numbers
3. **Identify the narrative**: structure around _questions the reader has_, not file names
4. **Draft the steps**: decide the ordered list of (file, line) waypoints
5. **Write both files simultaneously**: prose for `.md`, description strings for `.json`
6. **Verify all line numbers**: grep or read each file to confirm accuracy before writing
7. **Output**: place both files next to each other — `<name>.md` and `<name>.json`, same basename, no suffix variation

---

## Neovim integration (codetour.lua)

Bundled at `codetour.lua` in this skill's directory. Copy it into your Neovim config (e.g. `~/.config/nvim/lua/codetour.lua`) and `require` it from your init.

```
:TourLoad                   — auto-detect <stem>.tour from current .md buffer
:TourLoad path/to/t.json    — explicit load
]q / [q                     — next / prev step (existing quickfix keymaps)
Enter on qf line            — jump to any step directly
:cc N                       — jump to step N by number
```

Layout when a tour is active:

```
┌──────────────────────────┐
│    code window (main)    │
├──────────────────────────┤
│    description (B)       │  ← full step description, always visible
├──────────────────────────┤
│    quickfix (A)          │  ← all steps overview; Enter to jump to any step
└──────────────────────────┘
```

Navigation is driven by the standard quickfix machinery. `]q`/`[q` move through the list; codetour hooks `QuickFixCmdPost` to auto-update the description panel. No separate tour-specific keymaps needed.

---

## Quality rules

- Every `file:line` (in both `.md` and `.json`) must be **accurate** — verify by reading the file before writing, never estimate.
- Step descriptions must explain **why**, not just restate what the code does.
- Keep inline snippets in `.md` **minimal** — only lines needed to understand the point.
- Sections / steps should answer **questions the reader has**, not mirror file structure.
- Explanation prose in `.md` goes **before** the code fence, never as comments inside it.
- Snippets must be **verbatim** excerpts — do not paraphrase or simplify the source.
