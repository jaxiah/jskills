---
name: tdd
description: Test-driven development with red-green-refactor loop. Use when user wants to build features or fix bugs using TDD, mentions "red-green-refactor", wants integration tests, or asks for test-first development.
---

# Test-Driven Development

## Philosophy

**Core principle**: Tests should verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't.

**Good tests** are integration-style: they exercise real code paths through public APIs. They describe _what_ the system does, not _how_ it does it. A good test reads like a specification - "user can checkout with valid cart" tells you exactly what capability exists. These tests survive refactors because they don't care about internal structure.

**Bad tests** are coupled to implementation. They mock internal collaborators, test private methods, or verify through external means (like querying a database directly instead of using the interface). The warning sign: your test breaks when you refactor, but behavior hasn't changed. If you rename an internal function and tests fail, those tests were testing implementation, not behavior.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Anti-Pattern: Horizontal Slices

**DO NOT write all tests first, then all implementation.** This is "horizontal slicing" - treating RED as "write all tests" and GREEN as "write all code."

This produces **crap tests**:

- Tests written in bulk test _imagined_ behavior, not _actual_ behavior
- You end up testing the _shape_ of things (data structures, function signatures) rather than user-facing behavior
- Tests become insensitive to real changes - they pass when behavior breaks, fail when behavior is fine
- You outrun your headlights, committing to test structure before understanding the implementation

**Correct approach**: Vertical slices via tracer bullets. One test → one implementation → repeat. Each test responds to what you learned from the previous cycle. Because you just wrote the code, you know exactly what behavior matters and how to verify it.

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
  ...
```

## Workflow

### 1. Planning

Before writing any code:

- [ ] Ask the user for the ISSUE filename if not already known (e.g. `PRD-002-ISSUE-004-my-slice.md`)
- [ ] Check `BACKLOG/` for any existing `<ISSUE-prefix>-AMENDMENT-*.md` for this issue marked BLOCKED. If one exists, do not proceed — resolve the amendment with the user first.
- [ ] Look for `<ISSUE-prefix>-DESIGN-*.md` in `BACKLOG/`. If it does **not** exist, stop and run the `design` skill first — TDD requires confirmed interfaces before proceeding.
- [ ] Read the DESIGN file for confirmed interfaces and testing priorities.
- [ ] Treat the interfaces in the DESIGN file as fixed. Do not redesign them here. If implementation will require interface changes, that is an Amendment candidate — flag it, do not silently change.
- [ ] **Map every acceptance criterion to a test.** Read each criterion in the ISSUE and write down which test will verify it. If a criterion cannot be covered by an automated test, mark it explicitly as `[manual]` — it will require direct execution before the issue can be closed.
- [ ] List the behaviors to test (not implementation steps), derived from the criteria mapping above
- [ ] Get user approval on the plan

**You can't test everything** — this applies to edge cases and implementation details, not to acceptance criteria. Every acceptance criterion must be covered by either an automated test or a `[manual]` marker. No criterion may be silently skipped.

**A placeholder test that doesn't verify any acceptance criterion is not a test — it is a liability.** It passes when things are broken and gives false confidence. Every test must trace back to at least one acceptance criterion.

### 2. Tracer Bullet

Write ONE test that confirms ONE thing about the system:

```
RED:   Write test for first behavior → test fails
GREEN: Write minimal code to pass → test passes
```

This is your tracer bullet - proves the path works end-to-end.

### 3. Incremental Loop

For each remaining behavior:

```
RED:   Write next test → fails
GREEN: Minimal code to pass → passes
```

Rules:

- One test at a time
- Only enough code to pass current test
- Don't anticipate future tests
- Keep tests focused on observable behavior

### 4. Refactor

After all tests pass, look for [refactor candidates](refactoring.md):

- [ ] Extract duplication
- [ ] Deepen modules (move complexity behind simple interfaces)
- [ ] Apply SOLID principles where natural
- [ ] Consider what new code reveals about existing code
- [ ] Run tests after each refactor step

**Never refactor while RED.** Get to GREEN first.

### 5. Close the ISSUE

After all tests pass and refactor is complete:

- [ ] Read the parent ISSUE file from `BACKLOG/`
- [ ] Go through each acceptance criterion — check off `- [x]` any that are now satisfied by the implementation
- [ ] For `[manual]` criteria, execute them directly now. Do not infer pass/fail.
- [ ] Append a completion record at the bottom of the ISSUE file:

```markdown
## Completed

YYYY-MM-DD — all acceptance criteria met. Implemented via TDD.
```

If some criteria are intentionally deferred (out of scope for this session), note them explicitly rather than leaving them unchecked without explanation.

### Interrupt: When implementation reveals a problem

This can fire at any point during steps 2, 3, or 4 — not only at the end.

During TDD you may discover that an acceptance criterion is impossible, ambiguous, or that the DESIGN file has an error. This is normal — implementation surfaces information that design cannot anticipate.

**Do not modify the ISSUE or DESIGN file directly.** Instead:

1. Create `BACKLOG/<ISSUE-prefix>-AMENDMENT-short-slug.md` with the following structure:

```markdown
## Parent Issue

[<ISSUE-filename>](ISSUE-filename)

## Problem discovered

Which acceptance criterion or design decision is blocked, and at what point in implementation it was found.

## Type

- [ ] IMPOSSIBLE — cannot be done given current constraints (explain the constraint)
- [ ] AMBIGUOUS — criterion has multiple valid interpretations (show the ambiguity)
- [ ] DESIGN-ERROR — the interface specified in the DESIGN file does not work in practice (show the failed attempt)

## Evidence

For DESIGN-ERROR: include the implementation path that was tried and why it failed.
For IMPOSSIBLE: state the constraint explicitly (e.g. depends on ISSUE-NNN not yet done).
For AMBIGUOUS: show both interpretations and why neither is clearly correct.

## Proposed change

What specifically should be updated in the ISSUE or DESIGN file.

## TDD status

BLOCKED — awaiting human review.
```

2. Stop the TDD session. Do not work around the problem or silently lower the bar.
3. Wait for the human to review, approve, reject, or modify the amendment before continuing.

**The amendment requirement exists to prevent gaming.** Modifying acceptance criteria to match what was implemented — rather than implementing what was specified — produces software that satisfies paperwork, not users. The amendment process makes every backward change visible and human-approved.

## Checklist Per Cycle

```
[ ] Test describes behavior, not implementation
[ ] Test uses public interface only
[ ] Test would survive internal refactor
[ ] Code is minimal for this test
[ ] No speculative features added
```
