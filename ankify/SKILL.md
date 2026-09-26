---
name: ankify
description: Transform knowledge into atomic, unambiguous Anki notes following Michael Nielsen and Piotr Wozniak's principles. Use when creating high-quality learning material for SRS.
---

# Ankify

Generate high-quality Anki cards (notes) optimized for long-term retention.

## Core Rules

Default to Wozniak's [20 Rules of Knowledge Formulation](references/20-rules.md), especially the minimum information principle. Most cards should be quick to answer, not mini-explanations. Keep the recall target small without imposing a fixed front/back length ratio.

1. **One recall target per card.** Before drafting, identify the single fact, distinction, or missing link the card tests. If the target cannot be stated in one sentence, narrow the prompt or split the card. For source lists, reduce each point to its smallest useful recall target.

2. **Unambiguous prompt.** The front must stand on its own during review and specify what is being asked clearly enough to have exactly one intended answer. Do not make the learner guess the scope or level of detail.

3. **Shortest sufficient answer.** The back should fully satisfy the prompt, preferably in 1-2 sentences. Do not add recaps, tradeoffs, adjacent background, or "why this matters" unless the prompt asks for them. Use mnemonics when they directly support recall, not as unrelated answer padding.

4. **Balanced context.** Put enough context on the front to make the recall target clear and situate it within a coherent idea. A diagram, table, or setup may be worth revisiting even when every detail is not needed to produce the answer. Keep that context relevant and proportionate to the learning objective: avoid both a bare prompt with a long explanatory back and a large reference page testing a trivial detail. If the back grows long, move necessary context to the front, narrow the target, or split the card. Judge balance by relevance and cognitive load, not by matching front and back lengths.

## Formatting Constraints & Pitfalls

- **No Note Separators**: NEVER use `---` to separate multiple notes. Use it only within a single note, between a Basic prompt and answer or a Cloze prompt and its answer-side supplement.
- **No Trailing Separators**: Never end a note or a file with `---`.
- **No Empty Backs**: If you use `---`, there MUST be content after it.
- **One H4 per Note**: Do not bundle multiple questions under one header.
- **Long Back Warning**: If the back feels long, move necessary context to the front, narrow the prompt, or split the note.

## Format Guidelines (STRICT)

Each note MUST follow one of these exact markdown structures. Never mix them.

### 1. Standard Format (Simple Q&A)

Use this for most Basic Q&A notes. If the question is self-sufficient, use this. NO horizontal separator (`---`) allowed anywhere.

```markdown
#### <specific front prompt / main question>

<back answer>
```

### 2. Context-Extended Format (Complex Prompts)

Use **ONLY** when the prompt needs a code snippet, diagram, situational constraint, or intentional knowledge scaffold that supports recall of a complex mechanism without cluttering the H4 title.
Exactly ONE `---` to separate front from back. _(Leave exactly one blank line before and after the `---` separator to prevent markdown rendering errors)._ NEVER put a `---` at the very end of the note.
Everything before `---` is the front-side context/setup, and everything after `---` is the back answer. Do not add extra metadata fields or labels to restate this structure.

```markdown
#### <specific front prompt / main question>

<optional context, code snippet, or setup clarifying the prompt>

---

<back answer>
```

### 3. Cloze Format

Use one `####` heading per note. Put at least one deletion in the heading or in the text before any separator, using `{{c1::hidden text}}` or `{{c1::hidden text::hint}}`. Use different numbers (`c1`, `c2`, ...) for separate cards; repeat a number when multiple deletions should be hidden on the same card.

Without `---`, the heading and entire body are shown while recalling. If supplementary content is needed after revealing the answer, put exactly one `---` after the cloze text, with exactly one blank line on each side. Everything after `---` is shown after revealing the answer on every card generated from the note. That content must be nonempty. Do not put the only cloze deletion below `---`.

**One deletion, no supplement:** One cloze number creates one card; no `---` is needed.

```markdown
#### Queue removal order

A queue removes the {{c1::oldest}} item first.
```

**Independent deletions:** `c1` and `c2` create two cards, each hiding one part of the relationship.

```markdown
#### Queue insertion and removal ends

A queue inserts at the {{c1::tail}} and removes from the {{c2::head}}.
```

**Grouped deletions:** Repeating `c1` creates one card that hides both parts together.

```markdown
#### Queue insertion and removal as one pair

A queue {{c1::inserts at the tail}} and {{c1::removes from the head}}.
```

**Hint and answer-side supplement:** The hint appears while recalling; the text after `---` appears only after revealing the answer.

```markdown
#### LRU cache eviction

An LRU cache evicts the {{c1::least recently used::recency criterion}} entry.

---

Recency refers to accesses, not insertion order.
```

**Invalid placement:** This is not a Cloze-format note because its only deletion is below `---`.

```markdown
#### LRU cache eviction

Which entry does the cache evict?

---

The {{c1::least recently used}} entry.
```

## Examples of Rule Application

### Example 1: Minimum Fact & Open-Ended Prompts (Knowledge Rule)

**Bad Example** (Violates: specific prompts, minimum information, generic H4 title)

```markdown
#### CUDA Shared Memory

What is it, where does it live, and how do you sync it?

---

It is an on-chip memory space that is much faster than global memory. It is shared among all threads in a thread block. You must use `__syncthreads()` to prevent race conditions.
```

**Good Example** (Split into atomic, testable facts with unique H4s)

```markdown
#### Where does CUDA shared memory reside physically compared to global memory?

On-chip.

#### What is the maximum visibility scope of a dynamically allocated shared memory array?

`extern __shared__ float shared_array[];`

---

All threads within the same **thread block**.
```

### Example 2: Avoiding Enumerations & Structural Preference (Knowledge Rule)

**Bad Example** (Violates: avoid large sets, minimum information)

```markdown
#### How do you optimize VLM inference?

1. Use INT8/INT4 Quantization.
2. Implement FlashAttention.
3. Use speculative decoding.
4. Optimize the visual encoder.
```

**Good Example** (Targets specific mechanisms with unique prompts and context)

```markdown
#### Which attention algorithm avoids materializing the large attention matrix during attention?

Autoregressive inference is memory-bandwidth sensitive, and materializing the full attention matrix would add large memory traffic.

---

**FlashAttention**.
```

### Example 3: Multiple Notes Formatting (Formatting Rule)

**Bad Example** (Violates: using `---` as a note separator. It is completely forbidden to put `---` between notes or at the end.)

```markdown
#### What is the time complexity of binary search?

O(log n).

---

#### What is the space complexity of iterative binary search?

O(1).

---
```

**Good Example** (Standard format, consecutive notes separated simply by spacing, NO `---` between notes)

```markdown
#### What is the time complexity of binary search?

O(log n).

#### What is the space complexity of iterative binary search?

O(1).
```

## Workflow

1.  **Analyze**: Breakdown the source material into the smallest possible concepts.
2.  **Identify recall target**: State the one target each card tests before drafting. In Cloze notes, each distinct `cN` generates a card, so evaluate each target separately; split cards that bundle unrelated facts.
3.  **Formulate**: Draft questions that are short, clear, and unambiguous, with enough front-side context for recall.
4.  **Format**: Apply the Standard, Context-Extended, or Cloze format according to the intended recall.
5.  **Validate**: Ensure the answer is concise and directly addresses the question. Delete any back sentence that answers something the front did not ask.
