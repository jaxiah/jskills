# Investigation & Fix Workflow

**INVEST → ISSUE → DESIGN → VERIFY / TDD**

This is the workflow for diagnosing and fixing existing problems — bugs, crashes, hangs, performance regressions, numerical inconsistencies, behavioral instability. Use it when something is wrong and you need to understand why before you can fix it.

---

## Pipeline

```
write-an-invest
    └─> (invest-to-issues, same process as prd-to-issues)
            └─> design  (optional)
                    └─> verify   (quantitative criteria: benchmarks, measurements)
                    └─> tdd      (behavioral criteria: pass/fail tests)
                            └─> resolve-amendment  (if blocked)
```

---

## Steps

### 1. `write-an-invest` — Investigate the problem

**Input**: a problem phenomenon (bug report, perf number, crash log, etc.)
**Output**: `BACKLOG/INVEST-NNN-slug.md` (living document — append as investigation progresses)

Captures: phenomenon, expected vs actual, reproduction steps, baseline measurements, hypotheses, checks performed, current conclusion, status.

The INVEST file stays `OPEN` until the conclusion is clear enough to generate ISSUEs. Update it with a `## Update YYYY-MM-DD` section each time new findings are added.

---

### 2. Generate ISSUEs — Converge to executable work

**Input**: a converged INVEST file (status `CONVERGED`).
**Output**: `BACKLOG/INVEST-NNN-ISSUE-MMM-slug.md` (one per slice)

Use the same vertical-slice process as `prd-to-issues`. Each ISSUE is one concrete action: a fix, a diagnostic step, a benchmark run, a validation. Acceptance criteria trace back to the investigation's conclusion.

---

### 3. `design` — Design interfaces _(optional)_

**Input**: an ISSUE file.
**Output**: `BACKLOG/INVEST-NNN-ISSUE-MMM-DESIGN-slug.md`

Same as the PRD track. Most relevant for ISSUEs that involve interface changes. For pure measurement or diagnostic ISSUEs, skip this step.

---

### 4a. `verify` — Quantitative acceptance

**Input**: an ISSUE file with `[benchmark]` or `[measure]` criteria.
**Output**: closed ISSUE with measurements recorded.

Establish baseline → implement → measure → compare against target. Use identical conditions for baseline and final runs. If a target is unreachable, create an AMENDMENT.

### 4b. `tdd` — Behavioral acceptance

**Input**: an ISSUE file with behavioral pass/fail criteria.
**Output**: working code + closed ISSUE.

Use when the fix has testable behavioral correctness (e.g. "output matches reference within 1e-4", "no crash on input X"). Red → Green → Refactor.

---

### Amendment handling

If `design`, `verify`, or `tdd` creates a `BACKLOG/INVEST-NNN-ISSUE-MMM-AMENDMENT-slug.md`, use `resolve-amendment` to review and unblock.

---

## File naming

| Artifact  | Convention                               |
| --------- | ---------------------------------------- |
| INVEST    | `INVEST-NNN-slug.md`                     |
| ISSUE     | `INVEST-NNN-ISSUE-MMM-slug.md`           |
| DESIGN    | `INVEST-NNN-ISSUE-MMM-DESIGN-slug.md`    |
| AMENDMENT | `INVEST-NNN-ISSUE-MMM-AMENDMENT-slug.md` |

NNN = INVEST sequence (glob `BACKLOG/INVEST-*.md`), separate from PRD counter.
MMM = ISSUE sequence scoped to this INVEST (glob `BACKLOG/INVEST-NNN-ISSUE-*.md`), starting from 001.
