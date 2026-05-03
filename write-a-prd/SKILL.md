---
name: write-a-prd
description: Create a PRD through user interview, codebase exploration, and module design, then submit as a GitHub issue. Use when user wants to write a PRD, create a product requirements document, or plan a new feature.
---

This skill is the entry point of the feature development workflow. See [workflow.md](workflow.md) for the full pipeline: PRD → ISSUE → DESIGN → TDD.

This skill will be invoked when the user wants to create a PRD. You may skip steps if you don't consider them necessary.

1. Ask the user for a long, detailed description of the problem they want to solve and any potential ideas for solutions.

2. Explore the repo to verify their assertions and understand the current state of the codebase.

3. Interview the user relentlessly about every aspect of this plan until you reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one.

4. Sketch out the major modules you will need to build or modify to complete the implementation. Actively look for opportunities to extract deep modules that can be tested in isolation.

A deep module (as opposed to a shallow module) is one which encapsulates a lot of functionality in a simple, testable interface which rarely changes.

Check with the user that these modules match their expectations. Check with the user which modules they want tests written for.

5. Once you have a complete understanding of the problem and solution, use the template below to write the PRD. Save it as a local file in the project's `BACKLOG/` directory.

**Filename convention**: `PRD-NNN-short-slug.md` where NNN is the next PRD-specific sequence number.
To find NNN: glob `BACKLOG/PRD-*.md`, extract the highest 3-digit prefix among PRD files only, increment by 1. PRD and ISSUE use separate counters.

<prd-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A LONG, numbered list of user stories. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

This list of user stories should be extremely extensive and cover all aspects of the feature.

## Implementation Decisions

A list of implementation decisions that were made. Stay at the module level — interface-level detail (function signatures, type definitions) belongs in the DESIGN file, not here.

This can include:

- Which modules will be built or modified, and what each one is responsible for
- How modules interact with each other (data flow, call direction)
- Architectural decisions
- Schema changes (entity level, not field-by-field)
- External API endpoints introduced (e.g. new REST routes — not their request/response schemas)
- Technical clarifications from the developer

Do NOT include: function signatures, type definitions, internal API contracts, or specific file paths. They are volatile and will be outdated quickly. That detail belongs in the DESIGN file.

## Testing Decisions

High-level testing decisions only — specific interface-level testing priorities are deferred to the Design stage. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested (module names, not function signatures)
- Prior art for the tests (i.e. similar types of tests in the codebase)

Do NOT specify which functions or behaviors to test, or in what order. That belongs in the DESIGN file.

## Out of Scope

A description of the things that are out of scope for this PRD.

## Further Notes

Any further notes about the feature.

</prd-template>
