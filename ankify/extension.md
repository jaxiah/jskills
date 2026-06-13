# Ankify Extension: Visual Process Notes

Use this extension when source material includes screenshots, diagrams, GIFs, slide animations, videos, or extracted key frames, and the goal is to turn a visual mechanism into high-quality Anki notes.

This extension does not replace the core Ankify rules. Minimum facts, unambiguous prompts, one H4 per note, and the standard or context-extended formats still apply.

## Goal

Do not summarize the whole visual. Preserve the smallest mechanism, state transition, or causal step that is worth reviewing later.

Good targets:

- A pipeline state transition.
- A register file, RAT, RS, ROB, or cache state change.
- A diagram edge that explains causality.
- A before and after comparison.
- A short algorithm or hardware mechanism shown across frames.

Bad targets:

- A full slide summary.
- A long animation transcript.
- A general caption for a picture.
- A screenshot kept only as a reminder to reread the source.

## Workflow

1. Identify the learning target first.
   Ask what the learner should reconstruct from memory. Prefer one mechanism or transition, not every visual detail.

2. Read the visual state explicitly.
   Extract the concrete before and after state. For tables and simulations, name the relevant rows, columns, tags, values, stages, arrows, or highlighted cells.

3. Separate visual facts from mechanism.
   State what the visual shows, then infer the rule. Example: "RF shows `R5` changes from tag `a` to tag `d`" supports "destination rename updates the latest mapping."

4. Use context-extended notes when the image is needed.
   Put the image, key frame, or minimal setup on the front. Put the reconstruction on the back. Use exactly one `---` only for the front/back boundary.

5. Keep process-trace backs to 3-5 steps.
   Use steps only when the visual target is a genuine process or state transition. Otherwise keep the back short, usually 1-2 sentences. If a process needs more than 5 steps, split it into anchor cards or a smaller process card.

6. Correct misleading explanations.
   Replace visual-proximity explanations with mechanism explanations. For example, replace "because the instructions are adjacent" with "because the rename table current mapping points to that producer."

7. Preserve useful media links.
   Keep the user's existing Obsidian wiki links, widths, and asset names unless the user asks to move or rename files.

## Source-Specific Guidance

### Screenshots and Diagrams

- Identify the one region that carries the learning signal.
- Ignore decorative labels and unrelated surrounding state.
- If the note needs the whole image for context, still describe only the relevant transition on the back.

### GIFs and Slide Animations

- Inspect key frames instead of treating the animation as one opaque image.
- Choose the frame where the meaningful state change becomes visible.
- If needed, mention the before state and after state in the front context.
- Do not turn a long animation into one giant card. Extract one process per card.

### Videos

- Sample or extract key frames around the explanation point.
- Prefer stable frames that show a completed state transition over blurry motion frames.
- Use a video-derived card only when the visual state adds information that text alone would lose.
- If the video contains many mechanisms, create a short set of notes around the most reusable mechanisms, not a chronological transcript.

## Preferred Note Shape

Use a context-extended note when the visual is required:

```markdown
#### <specific mechanism question>

![[image-or-frame.png|900]]

<minimal setup needed to interpret the visual>.

---

<short answer, or a 3-5 step reconstruction for a true process trace.>
```

Use a standard note when the visual is only supporting evidence and the prompt is already self-contained.

## Mutlu/DDCA Pipeline Simulation Pattern

For Mutlu or DDCA pipeline simulation notes, focus on changes in these structures:

- RF or RAT mappings.
- Reservation station source fields, especially valid, tag, and value.
- ROB order, completion, and commit state.
- Functional unit occupancy and latency.
- CDB or broadcast events.
- Timeline columns that show fetch, decode, execute, writeback, or commit.

Common useful targets:

- Allocate a tag for a destination.
- Look up a source operand and bind it to a value or producer tag.
- Wake up an RS entry after a matching tag broadcast.
- Dispatch a ready instruction to a functional unit.
- Write a result back to waiting consumers.
- Commit results in program order.

## Quality Checklist

- The front includes enough context to make the image interpretable in a large mixed deck.
- The back explains one mechanism, not the whole slide.
- The back answers the mechanism named in the front, not every visible detail in the image.
- The answer distinguishes observed state from inferred rule.
- The note avoids vague phrases like "this is important" or "as shown above."
- The note avoids relying on visual proximity when the real cause is a table mapping, tag match, dependency, or program order rule.
- The note is short enough to review without replaying the whole source material.
