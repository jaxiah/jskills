---
name: resolve-amendment
description: Review and resolve a BLOCKED AMENDMENT file created during design, TDD, or verify. Use when the user wants to unblock a stalled session, review a proposed change to an ISSUE or DESIGN file, or approve/reject an amendment.
---

# Resolve Amendment

An AMENDMENT file is created when the `design`, `tdd`, or `verify` skill hits a problem it cannot resolve without human input. This skill guides the human through reviewing the amendment and updating the affected files so work can continue.

## Process

### 1. Locate the AMENDMENT file

Ask the user for the AMENDMENT filename (e.g. `PRD-002-ISSUE-004-AMENDMENT-matmul-tiling.md` or `INVEST-001-ISSUE-002-AMENDMENT-bandwidth-target.md`).
Read it from `BACKLOG/`.

### 2. Read the affected files

Read the parent ISSUE file. If the amendment is a DESIGN-ERROR, also read the DESIGN file.

### 3. Present a clear summary

Show the user:

- Which criterion or design decision is blocked
- The amendment type (IMPOSSIBLE / AMBIGUOUS / DESIGN-ERROR)
- The evidence provided
- The proposed change

### 4. Facilitate the decision

Ask the user to choose one of:

- **Approve** — the proposed change is correct; proceed with updating the files
- **Reject** — the proposed change is wrong; the original spec stands; explain why the problem is not actually a blocker
- **Modify** — the proposed change needs adjustment; work with the user to agree on the right fix

### 5. Apply the resolution

**If approved or modified:**

- Update the ISSUE or DESIGN file as agreed. For ISSUE changes: modify acceptance criteria. For DESIGN changes: update the affected interface or module boundary.
- Do NOT delete the AMENDMENT file — append a resolution record at the bottom:

```markdown
## Resolution

YYYY-MM-DD — [Approved | Modified]: <one-sentence description of what changed and why>
```

**If rejected:**

- Append a resolution record explaining why the spec stands:

```markdown
## Resolution

YYYY-MM-DD — Rejected: <one-sentence explanation of why this is not a blocker>
```

- The blocked session may need guidance on how to proceed given the original spec.

### 6. Signal the unblock

Tell the user which skill to re-invoke to continue: `design`, `tdd`, or `verify`.
