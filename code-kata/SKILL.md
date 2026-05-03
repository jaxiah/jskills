---
name: code-kata
description: Anki-driven code kata workflow for building procedural programming skills through spaced repetition. Use when the user invokes /code-kata new, /code-kata start, or /code-kata done to manage coding practice sessions.
---

# Code-Kata Skill

A workflow that uses Anki as a task scheduler and hands-on kata practice as the execution mechanism. Anki decides _what_ to practice; this skill manages the actual practice sessions.

## Directory Layout

All kata live under a single root (default: `code_katas/` in the working directory):

```
code_katas/
  <kata-name>/
    kata.md        # Anki note source + acceptance criteria (ankify format)
    sessions.md    # Session history + knowledge-gap Anki notes
    scaffold/      # Complete compilable project with one "hole"
    YYYY-MM-DD/    # Full copy of scaffold + user's code for that session
```

## Commands

### `/code-kata new`

**Purpose:** Design a new kata from scratch — both the Anki card content and the compilable scaffold.

**Steps:**

1. Ask the user:
   - What topic / direction are you currently studying?
   - Micro-Kata (~5 min, one tricky logic block) or Full-Kata (~15–20 min, complete implementation)?

2. Generate `code_katas/<kata-name>/kata.md` in **ankify Context-Extended format**, with a fixed frontmatter block at the top:

```markdown
---
ankideck: codekata
---

#### [Micro-Kata | Full-Kata]: [concise task description]

[Setup constraints: what file to edit, what function signature is provided, time limit, etc.]

---

Acceptance Criteria:

1. [criterion]
2. [criterion]

Expected Output:
[exact stdout the binary should produce, or a tolerance spec like "matches CPU reference within 1e-4"]

Performance Target (optional):
[e.g., "achieves >80% of theoretical memory bandwidth on an A100"]
```

3. Generate `code_katas/<kata-name>/scaffold/` — a **fully compilable project** with one hole:
   - **Micro-Kata:** All files are complete and correct. In exactly one file, replace the target logic with a clearly bounded TODO block:

     ```
     // ---- TODO: implement [specific task] ----
     // [one-line hint about what belongs here, e.g., function signature or key constraint]

     // ---- END TODO ----
     ```

     The surrounding context (variable names, thread layout, call sites) is intentionally visible — this is by design for CUDA and other context-heavy code.

   - **Full-Kata:** All files are complete _except_ the primary implementation file, which is left blank (empty or with only the necessary `#include`s / header guard).

   - Both types must include a working build system (CMakeLists.txt preferred for CUDA/C++ projects, Makefile acceptable) and a verification harness that:
     - Runs the binary
     - Checks output against the expected result specified in `kata.md`
     - Exits non-zero on failure

4. Create `code_katas/<kata-name>/sessions.md` with empty sections. **Do not add frontmatter yet** — it will be added the first time a knowledge note is written:

```markdown
## Sessions

| Date | Start | End | Duration | Score | Notes |
| ---- | ----- | --- | -------- | ----- | ----- |

## Knowledge Notes
```

---

### `/code-kata list`

**Purpose:** List all kata in the current workspace so the user can choose what to practice.

**Steps:**

1. Enumerate all subdirectories of `code_katas/` that contain a `kata.md` file.
2. For each kata, read its `sessions.md` and extract:
   - Total session count
   - Last session date and score
3. Print a table:

```
Kata             Sessions   Last session   Last score
──────────────── ────────── ────────────── ──────────
matmul-naive     1          2026-03-28     again
matmul-tiled     1          2026-03-28     —
```

4. If `code_katas/` does not exist or contains no kata, say so.

---

### `/code-kata start <name>`

**Purpose:** Begin a new practice session for an existing kata.

**Steps:**

1. Verify `code_katas/<name>/` exists with `kata.md` and `scaffold/`.
2. Create `code_katas/<name>/YYYY-MM-DD/` (today's date).
3. Copy all files from `scaffold/` into the new dated directory.
4. **Get the current time by running `date +%H:%M`** before writing anything. Never guess or approximate the time. Append a new row to the Sessions table in `sessions.md` with today's date and the retrieved start time. Leave End, Duration, Score, Notes blank:
   ```
   | 2026-03-23 | 14:32 | — | — | — | — |
   ```
5. Tell the user which file to open and what the TODO block or blank file is.

---

### `/code-kata done <name> [again|hard|good|easy]`

**Purpose:** Close a session, verify the code, debrief, and evaluate for knowledge gaps.

**Steps:**

1. **Record end time.** **Get the current time by running `date +%H:%M`** before writing anything. Never guess or approximate the time. Fill in End, Duration, and Score for today's row in `sessions.md`.

2. **Compile and run.**
   - `cd` into `code_katas/<name>/YYYY-MM-DD/` and build with the scaffold's build system.
   - Run the binary.
   - Report: compiled? (how many attempts?), ran without crash?, output matched expected?

3. **Debrief.** Read the user's code (the file they edited). Give specific, targeted feedback:
   - What did they get right?
   - Where did friction likely occur (e.g., boundary conditions, index arithmetic)?
   - Any correctness issues beyond what the test caught?

4. **Evaluate for knowledge gaps.** Read the full Sessions table to check for patterns:
   - Two or more consecutive `again` scores → strong signal of a declarative knowledge gap.
   - A single `again` or repeated `hard` with similar friction notes → weaker signal, worth flagging.

   If a gap is detected, surface a specific hypothesis: _"It looks like the indexing for shared memory padding keeps causing issues — this might be a gap in understanding bank conflicts."_

5. **Offer to create a knowledge note.** Ask the user explicitly:
   _"Want me to add a knowledge-type Anki note for this gap?"_

   If yes:
   - **Invoke the `ankify` skill** before writing any notes. This loads the exact format rules; do not rely on memory.
   - Read the `## Knowledge Notes` section of `sessions.md`.
   - Check for semantic duplicates (same underlying concept, even if worded differently). If a duplicate exists, say so and skip.
   - Otherwise, generate one or more atomic notes in **ankify format** and append them under `## Knowledge Notes` in `sessions.md`.
   - **Frontmatter:** If `sessions.md` does not yet have a frontmatter block (i.e., the file does not start with `---`), prepend one before writing the note. Infer the appropriate deck from the note's subject matter (e.g., CUDA content → `md2anki::cuda`):
     ```markdown
     ---
     ankideck: md2anki::<topic>
     ---
     ```

---

## Scoring Rubric Reference

| Score   | Meaning                                                                     |
| ------- | --------------------------------------------------------------------------- |
| `again` | Severely over time; logic deadlock; or consulted a previous dated directory |
| `hard`  | Finished solo, but heavy API/doc lookups and significant time overrun       |
| `good`  | Finished within target time; minor typos fixed quickly by intuition         |
| `easy`  | Flowed naturally; possibly a better implementation than previous attempts   |

## Anki Integration

This skill never touches Anki directly. The markdown files are the single source of truth:

- `kata.md` → import into Anki as the kata scheduling note (user's own markdown→Anki tooling handles this)
- Knowledge notes in `sessions.md` → import into the theory deck the same way

The ankify format used throughout this skill is defined in the `ankify` skill.

## Key Principles

- **Root-first:** All commands operate from the project root. Never assume the user has `cd`'d into a subdirectory.
- **Scaffold is immutable:** Never modify files in `scaffold/`. Each dated directory is a self-contained, independent snapshot.
- **No silent writes:** Never append a knowledge note without explicit user confirmation.
- **Deduplication is semantic:** Two notes cover the same gap even if phrased differently — check meaning, not string equality.
