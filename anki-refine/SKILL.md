---
name: anki-refine
description: Refine Obsidian Markdown h4 blocks that represent Anki notes, located by ^anki-... anchor or h4 heading. Use when the user asks to refine, shorten, rewrite, split, review, or apply changes to an Anki note block identified by an anchor or h4 heading.
---

# Anki Refine

Refine Obsidian Markdown h4 blocks that represent Anki notes.

## Core Workflow

1. Treat the Obsidian h4 block as the source of truth for the Anki note.
2. Locate the Anki note block by either the supplied `^anki-...` anchor or the supplied h4 heading text.
3. By default, do not write files. First provide the refined note in the chat for review.
4. Iterate in chat until the user approves the exact wording.
5. Only write back when the user explicitly gives a clear apply instruction, such as `apply` or `write back`.
6. When applying, replace only the matched h4 block. Do not modify unrelated notes.

When rewriting Anki note content, also follow the `ankify` skill. `anki-refine` controls locating, review, and write-back workflow. `ankify` controls note quality.

## Locating the Note

Preferred locators:

- `^anki-...` anchor: globally unique and most reliable.
- `#### ...` h4 heading text: acceptable when the user provides the exact heading and it is unique in the vault.

Use literal search for an anchor:

```powershell
rg -n "\^anki-123" .
```

Use literal search for a h4 heading:

```powershell
rg -n -F "#### exact heading text" .
```

After finding the target, read the full h4 block: from the matched `#### ` heading through the line before the next `#### ` heading, or EOF. If locating by h4 heading, confirm the full heading line is an exact match before applying. If locating by anchor, first find the preceding `#### ` heading. Preserve the anchor line unless the user explicitly asks to remove it.

If multiple matches exist, show the candidate file paths/headings and ask the user which one to use. Do not write back unless the source h4 block is uniquely identified.

## Refinement Rules

- Keep the back tightly aligned with the front. Do not add background, tradeoffs, or related concepts unless the front asks for them.
- Prefer short, atomic notes. If a note is long because it covers multiple ideas, suggest splitting it.
- Do not add repeated "one-line summary" sentences after the idea is already stated.
- Prefer 1-3 short sentences for ordinary notes.
- Use bullets only when they make the answer materially easier to scan, not by default.
- Use the local term abbreviations if available at `D:\JNote\anki-term-abbreviations.md`.
- Keep Obsidian wiki image links intact.
- Follow the user's punctuation rule: use English half-width punctuation in all Chinese text.

## Applying Back

Before editing, restate which file and h4 heading will be replaced. Use a scoped edit that only replaces the selected h4 block. Clear Chinese instructions meaning write back, replace, or apply are also valid apply instructions.

After editing:

- If the original block had an anchor, check that it still exists.
- Check that no Chinese full-width punctuation was introduced.
- Briefly report the changed file and heading.
