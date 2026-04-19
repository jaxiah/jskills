---
name: design
description: Translate an ISSUE into concrete public interfaces and module boundaries, ready for TDD. Use when user wants to design the implementation of an issue, plan interfaces, or prepare for test-driven development.
---

# Design

Translate an ISSUE into a concrete interface and module design that TDD can consume directly.

## Process

### 1. Read the ISSUE

Ask the user for the ISSUE filename (e.g. `ISSUE-004-my-slice.md`).
Read it from `BACKLOG/` using the Read tool. If the ISSUE is already in context, skip the read.

### 2. Explore the codebase

Explore the relevant parts of the codebase to understand:

- Existing module boundaries and naming conventions
- How similar features are structured
- Potential integration points and constraints

### 3. Design public interfaces

For each module the ISSUE touches, design:

- Public function/method signatures (names, parameters, return types)
- Type definitions or data structures introduced or modified
- Module boundaries — what is exposed vs. hidden
- Error handling contracts

Actively look for **deep module** opportunities: a small, stable public interface that hides significant implementation complexity behind it.

### 4. Confirm with the user

Present the proposed interfaces and ask:

- Do the interfaces match expectations?
- Are the module boundaries correct?
- Any naming or contract concerns?
- Which behaviors are highest priority to test first?

Iterate until the user approves.

### 5. Save the design

**Filename convention**: `DESIGN-of-<ISSUE-filename>` — derive directly from the parent ISSUE's filename.
Example: `ISSUE-004-matmul-tiling.md` → `DESIGN-of-ISSUE-004-matmul-tiling.md`. No global counter needed.

<design-template>

## Parent Issue

[ISSUE-NNN-slug.md](ISSUE-NNN-slug.md)

## Interfaces

For each module or component, document the public interface:

```
function_name(param: Type, param2: Type) -> ReturnType
```

Include a one-line description of what each entry does and any invariants it maintains.

## Module Boundaries

Which modules will be created or modified, and what each one encapsulates.

## Deep Module Opportunities

Places where complexity can be hidden behind a simple interface.

## Testing Priorities

Ordered list of behaviors to test, from most to least critical. Feeds directly into TDD planning.

## Open Questions

Any unresolved design questions that surfaced during this step.

</design-template>
