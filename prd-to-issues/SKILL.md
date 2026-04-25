---
name: prd-to-issues
description: Break a PRD into independently-grabbable local ISSUE files using tracer-bullet vertical slices. Use when user wants to convert a PRD to issues, create implementation tickets, or break down a PRD into work items.
---

# PRD to Issues

Break a PRD into independently-grabbable ISSUE files using vertical slices (tracer bullets).
All files live in the project's `BACKLOG/` directory.

## Process

### 1. Locate the PRD

Ask the user for the PRD filename (e.g. `PRD-003-my-feature.md`).

Read it from `BACKLOG/` using the Read tool. If the PRD is already in context, skip the read.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code.

### 3. Draft vertical slices

Break the PRD into **tracer bullet** issues. Each issue is a thin vertical slice that cuts through ALL integration layers end-to-end, NOT a horizontal slice of one layer.

Slices may be 'HITL' or 'AFK'. HITL slices require human interaction, such as an architectural decision or a design review. AFK slices can be implemented and merged without human interaction. Prefer AFK over HITL where possible.

<vertical-slice-rules>
- Each slice delivers a narrow but COMPLETE path through every layer (schema, API, UI, tests)
- A completed slice is demoable or verifiable on its own
- Prefer many thin slices over few thick ones
</vertical-slice-rules>

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each slice, show:

- **Title**: short descriptive name
- **Type**: HITL / AFK
- **Blocked by**: which other slices (if any) must complete first
- **User stories covered**: which user stories from the PRD this addresses

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the dependency relationships correct?
- Should any slices be merged or split further?
- Are the correct slices marked as HITL and AFK?

Iterate until the user approves the breakdown.

### 5. Create the ISSUE files

**Determine next sequence number**: glob `BACKLOG/*.md`, extract the highest 3-digit prefix across ALL files (PRD-NNN, ISSUE-NNN, RFC-NNN share the same global sequence), increment by 1.

For each approved slice, write a local file to `BACKLOG/` using the filename convention:
`ISSUE-NNN-short-slug.md`

Create files in dependency order (blockers first) so you can reference real filenames in the "Blocked by" field.

Do NOT modify the parent PRD file.

<issue-template>
## Parent PRD

[PRD-NNN-slug.md](PRD-NNN-slug.md)

## What to build

A concise description of this vertical slice. Describe the end-to-end behavior, not layer-by-layer implementation. Reference specific sections of the parent PRD rather than duplicating content.

## Acceptance criteria

Each criterion must trace back to at least one numbered user story from the parent PRD. Write criteria as observable, verifiable outcomes — not implementation steps.

- [ ] Criterion 1 _(covers user story N)_
- [ ] Criterion 2 _(covers user story N)_
- [ ] Criterion 3 _(covers user story N)_

## Blocked by

- Blocked by [ISSUE-NNN-slug.md](ISSUE-NNN-slug.md) (if any)

Or "None - can start immediately" if no blockers.

## User stories addressed

Reference by number from the parent PRD:

- User story 3
- User story 7

</issue-template>
