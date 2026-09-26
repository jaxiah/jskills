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

## Note Format

Each `####` heading begins one note. Use one of the Basic or Cloze structures below for that note; the next `####` begins a new note.

### Shared Rules

- Never use `---` to separate notes. Separate consecutive notes with blank lines.
- Use at most one `---` within a note. When present, leave exactly one blank line before and after it, and put nonempty content after it. Never end a note or file with `---`.
- Do not add labels or metadata fields merely to restate which content is the front or back.

### Basic

**Simple Q&A:** When the H4 is the complete prompt, put the answer directly below it. Do not use `---`.

```markdown
#### <specific prompt>

<answer>
```

**Front-side context:** When the prompt needs a code snippet, diagram, situational constraint, or knowledge scaffold, put that context after the H4. Use `---` to separate the full front from the answer.

```markdown
#### <specific prompt>

<context needed to interpret the prompt>

---

<answer>
```

### Cloze

Put at least one deletion in the H4 or in the text before any `---`. Use `{{c1::hidden text}}` or `{{c1::hidden text::hint}}`. Different numbers (`c1`, `c2`, ...) generate separate cards; repeating a number hides those deletions together on one card. Check each distinct `cN` against the one-recall-target rule.

Without `---`, the H4 and entire body appear on the recall side. When an answer-side supplement is needed, put it after `---`; it appears after revealing the answer on every card generated from the note. The supplement must be nonempty. A deletion that appears only below `---` does not make a Cloze note.

**One deletion, no supplement:**

```markdown
#### Queue removal order

A queue removes the {{c1::oldest}} item first.
```

**Independent deletions:** `c1` and `c2` generate two cards.

```markdown
#### Queue insertion and removal ends

A queue inserts at the {{c1::tail}} and removes from the {{c2::head}}.
```

**Grouped deletions:** Repeating `c1` generates one card hiding both parts.

```markdown
#### Queue insertion and removal as one pair

A queue {{c1::inserts at the tail}} and {{c1::removes from the head}}.
```

**Hint and answer-side supplement:**

```markdown
#### LRU cache eviction

An LRU cache evicts the {{c1::least recently used::recency criterion}} entry.

---

Recency refers to accesses, not insertion order.
```

**Invalid placement:** The only deletion is below `---`, so this is not a Cloze note.

```markdown
#### LRU cache eviction

Which entry does the cache evict?

---

The {{c1::least recently used}} entry.
```

### Example: Note Boundaries

**Bad:** `---` is used between notes and left at the end.

```markdown
#### What is the time complexity of binary search?

O(log n).

---

#### What is the space complexity of iterative binary search?

O(1).

---
```

**Good:** Each new H4 starts the next note; no separator is needed.

```markdown
#### What is the time complexity of binary search?

O(log n).

#### What is the space complexity of iterative binary search?

O(1).
```
