---
name: write-an-invest
description: Open or update an investigation document for a bug, performance issue, crash, hang, numerical inconsistency, or any "existing thing has a problem" scenario. Use when user wants to investigate a problem or document findings. Produces a living INVEST file that can generate ISSUEs when the conclusion is clear.
---

# Write an Investigation

This skill is the entry point of the investigation & fix workflow. See [workflow.md](workflow.md) for the full pipeline: INVEST → ISSUE → DESIGN → VERIFY / TDD.

An INVEST file is a **living document** — append findings as the investigation progresses. When the conclusion is clear, generate ISSUEs to execute the fix.

## Process

### 1. New or existing?

- **New**: ask for a short description of the problem. Create `INVEST-NNN-short-slug.md`.
- **Existing**: ask for the filename, read it, then append a new `## Update YYYY-MM-DD` section.

**Filename convention**: `INVEST-NNN-short-slug.md`. To find NNN: glob `BACKLOG/INVEST-*.md`, extract the highest 3-digit prefix, increment by 1. INVEST uses its own counter, separate from PRD.

### 2. Interview the user

Ask relentlessly until you have a complete picture. Walk down each branch of the problem tree, resolving ambiguities one by one. For each question, if you can answer it by exploring the codebase, do that instead of asking.

Cover at minimum:

- What exactly was observed? (error message, metric value, behavior — be specific)
- What was expected instead?
- Is it deterministic or intermittent? Under what conditions does it appear?
- When did it first appear? Has it ever worked correctly?
- What changed recently (code, config, hardware, data, environment)?
- How to reproduce it minimally?
- What is the baseline measurement, if quantitative (throughput, latency, accuracy)?
- What has already been tried or ruled out?
- What is the hardware/software environment (GPU model, driver, framework version, etc.)?
- Are there related issues, similar past problems, or known constraints?

After the interview, explore the relevant codebase areas to verify the user's description and surface context they may have missed.

### 3. Write or update

New investigation → create the file using the template.
Existing investigation → append findings under a new `## Update YYYY-MM-DD` section.

### 4. Decide: generate ISSUEs?

If the conclusion is clear enough to act on, ask the user. If yes, draft vertical slices and create `INVEST-MMM-ISSUE-NNN-short-slug.md` files — same process as `prd-to-issues`.

If not, save the current state and stop. The investigation stays `OPEN`.

<invest-template>

## Phenomenon

What was observed. Be specific: error message, metric value, behavior, hardware/config context.

## Expected

What should have happened instead.

## Reproduction

Minimal steps to reproduce.

## Baseline

Quantitative measurements at investigation start (throughput, latency, accuracy, etc.). Leave blank if not applicable.

## Hypotheses

- [ ] Hypothesis 1

## Checks performed

| Date | Check | Result |
| ---- | ----- | ------ |

## Conclusion

Current best explanation. Update as investigation progresses.

## Status

`OPEN` / `CONVERGED` / `CLOSED`

## Issues generated

<!-- filled in when ISSUEs are created -->

</invest-template>
