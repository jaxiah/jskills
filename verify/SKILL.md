---
name: verify
description: Execute and close an ISSUE whose acceptance criteria are quantitative — performance targets, accuracy thresholds, memory limits, or other measurable outcomes. Use when ISSUE criteria are benchmarks or measurements rather than behavioral pass/fail tests. Counterpart to tdd for quantitative ISSUEs.
---

# Verify

Execute an ISSUE whose acceptance criteria are quantitative. Establishes baselines, implements, measures, and closes the ISSUE.

## Workflow

### 1. Planning

- [ ] Ask the user for the ISSUE filename (e.g. `INVEST-001-ISSUE-001-fix-bandwidth.md`)
- [ ] Check `BACKLOG/` for any `<ISSUE-prefix>-AMENDMENT-*.md` marked BLOCKED — if one exists, resolve it first via `resolve-amendment`
- [ ] Look for `<ISSUE-prefix>-DESIGN-*.md` — if it exists, read it for interface constraints
- [ ] Read each acceptance criterion and classify:
  - `[benchmark]` — run a benchmark, compare against target
  - `[measure]` — measure a scalar (accuracy, delta, memory usage), compare against threshold
  - `[manual]` — requires direct human observation
- [ ] **Establish baselines** for every `[benchmark]` and `[measure]` criterion before touching any code
- [ ] Get user approval on the plan

### 2. Implement

Make the changes required by the ISSUE. Keep changes scoped — do not fix things outside the ISSUE.

### 3. Measure

For each criterion, re-run the same benchmark or measurement used for the baseline. Record: baseline value, target, achieved value. Use identical conditions (hardware, config, input size) for baseline and final runs.

### 4. Iterate if needed

If a criterion is not met, investigate and adjust. If a criterion appears unreachable, create an amendment — same format as tdd interrupts (see tdd skill) — and stop.

### 5. Close the ISSUE

After all criteria are met:

- [ ] Check off `- [x]` each criterion in the ISSUE file
- [ ] Append a completion record:

```markdown
## Completed

YYYY-MM-DD — all acceptance criteria met. Verified via measurement.
```

## Checklist

```
[ ] Baseline established before any code changes
[ ] Same measurement method and conditions for baseline and final
[ ] Each criterion explicitly pass or fail — no "roughly OK"
[ ] Changes scoped to the ISSUE
```
