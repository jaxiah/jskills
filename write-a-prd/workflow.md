# Feature Development Workflow

**PRD → ISSUE → DESIGN → TDD**

This is the workflow for building new capabilities. Use it when you know what you want to build and need to go from requirements to working code.

---

## Pipeline

```
write-a-prd
    └─> prd-to-issues
            └─> design  (optional but strongly recommended)
                    └─> tdd
                            └─> resolve-amendment  (if blocked)
```

---

## Steps

### 1. `write-a-prd` — Define the capability

**Input**: a problem to solve or a capability to build.
**Output**: `BACKLOG/PRD-NNN-slug.md`

Captures: problem statement, solution, user stories, module-level implementation decisions, testing decisions (module level only), out of scope.

Do NOT put function signatures or type definitions in the PRD — those belong in DESIGN.

---

### 2. `prd-to-issues` — Break into vertical slices

**Input**: a PRD file.
**Output**: `BACKLOG/PRD-NNN-ISSUE-MMM-slug.md` (one per slice)

Each ISSUE is a thin vertical slice through all layers — schema, logic, API, tests. A completed ISSUE is independently demoable. Each acceptance criterion traces back to a numbered user story in the PRD.

---

### 3. `design` — Design public interfaces _(optional)_

**Input**: an ISSUE file.
**Output**: `BACKLOG/PRD-NNN-ISSUE-MMM-DESIGN-slug.md`

Defines function signatures, type definitions, module boundaries, and testing priorities. TDD treats these interfaces as fixed. If design reveals a criterion is impossible or ambiguous, create an AMENDMENT and stop.

Skip this step only for trivial ISSUEs with no interface changes.

---

### 4. `tdd` — Implement and close

**Input**: an ISSUE file (and its DESIGN file if present).
**Output**: working code + closed ISSUE (checkboxes ticked, `## Completed` appended)

Red → Green → Refactor, one behavior at a time. If implementation reveals a problem with the spec, create an AMENDMENT and stop — do not silently lower the bar.

---

### Amendment handling

If `design` or `tdd` creates a `BACKLOG/PRD-NNN-ISSUE-MMM-AMENDMENT-slug.md`, use `resolve-amendment` to review and unblock before continuing.

---

## File naming

| Artifact  | Convention                            |
| --------- | ------------------------------------- |
| PRD       | `PRD-NNN-slug.md`                     |
| ISSUE     | `PRD-NNN-ISSUE-MMM-slug.md`           |
| DESIGN    | `PRD-NNN-ISSUE-MMM-DESIGN-slug.md`    |
| AMENDMENT | `PRD-NNN-ISSUE-MMM-AMENDMENT-slug.md` |

NNN = PRD sequence (glob `BACKLOG/PRD-*.md`).
MMM = ISSUE sequence scoped to this PRD (glob `BACKLOG/PRD-NNN-ISSUE-*.md`), starting from 001.
