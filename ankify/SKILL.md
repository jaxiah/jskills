---
name: ankify
description: Transform knowledge into atomic, unambiguous Anki notes following Michael Nielsen and Piotr Wozniak's principles. Use when creating high-quality learning material for SRS.
---

# Ankify

Generate high-quality Anki cards (notes) optimized for long-term retention.

## Core Rules

1.  **Strict Atomicity**: Each card must address a single, granular fact.
2.  **No Enumerations**: Avoid "List 5 factors..." or complex sequences. Use cloze deletions or split into multiple atomic questions.
3.  **No Ambiguity**: Every question must be self-contained and interpreted exactly one way.
4.  **20 Rules of Knowledge Formulation**: Refer to [20-rules.md](references/20-rules.md) for deep principles.
5.  **Balanced Front/Back**: The front prompt must provide enough context to make the expected answer recallable. Avoid tiny generic questions with large complex answers. If the answer needs several constraints, examples, or comparisons, either use Context-Extended Format to put that context on the front, or split the note.
6.  **Answer Only the Front**: The back should answer only what the front asks. Do not add adjacent background, tradeoffs, related concepts, or recap unless needed for the asked recall.

## Strict Constraints & Pitfalls

- **No Note Separators**: NEVER use `---` to separate multiple notes. The `---` is ONLY used to separate the front and back of a _single_ Context-Extended note.
- **No Trailing Separators**: Never end a note or a file with `---`.
- **No Empty Backs**: If you use `---`, there MUST be content after it.
- **One H4 per Note**: Do not bundle multiple questions under one header.
- **Atomicity**: If an answer feels too long, split the note.
- **Front/Back Imbalance**: If the front is a short label like "What is X?" but the back explains several mechanisms, tradeoffs, or cases, the note is malformed. Add front-side context, narrow the question, or split it.

## Rare Exception: Process Trace Cards

Atomic cards are the default. A process trace card is allowed only when the user explicitly wants to remember a coherent process, design path, or causal chain. Do not use this exception for ordinary definitions, comparisons, mechanisms, pros/cons, or summaries.

Use this exception only if all conditions hold:

1. The prompt explicitly asks the learner to reconstruct a process, such as "Trace how ...", "How is X built from Y?", or "Why does A force B?".
2. The card has a clear start state and end state.
3. The answer can be reconstructed in 3-5 ordered steps.
4. The card tests one causal chain, not a loose collection of related facts.
5. The card is supported by smaller atomic anchor cards, or those anchor cards are planned.
6. The back should stay under roughly 120-150 words.

Process trace formatting:

- Prefer 3-5 numbered steps only for process trace cards.
- Do not use this as a general license to write bullet lists.
- Standard atomic notes should usually be 1-3 short sentences, not bullets.

Practical budget:

- Use at most 1 process trace card per coherent process.
- If a process trace card needs more than 5 steps, split it or create anchor notes instead.
- If two process trace cards share most of the same answer, merge or delete one.

Good process trace prompts:

- `Trace how a load-use hazard creates a stall and a bubble in a 5-stage pipeline.`
- `How is the lw single-cycle datapath built from the initial state elements?`

Bad process trace prompts:

- `Explain single-cycle processors.`
- `DDCA chapter 7 summary.`
- `What is register renaming?`
- `Compare superscalar and VLIW.`

## Format Guidelines (STRICT)

Each note MUST follow one of these exact markdown structures. Never mix them.

### 1. Standard Format (Simple Q&A)

Use this for **90% of notes**. If the question is self-sufficient, use this. NO horizontal separator (`---`) allowed anywhere.

```markdown
#### <specific front prompt / main question>

<back answer>
```

### 2. Context-Extended Format (Complex Prompts)

Use **ONLY** when the prompt needs a code snippet, diagram, or situational constraint to avoid ambiguity without cluttering the H4 title.
Exactly ONE `---` to separate front from back. _(Leave exactly one blank line before and after the `---` separator to prevent markdown rendering errors)._ NEVER put a `---` at the very end of the note.

```markdown
#### <specific front prompt / main question>

<optional context, code snippet, or setup clarifying the prompt>

---

<back answer>
```

## Examples of Rule Application

### Example 1: Atomicity & Open-Ended Prompts (Knowledge Rule)

**Bad Example** (Violates: specific prompts, 15-second rule, generic H4 title)

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
#### Which attention algorithm avoids materializing the large attention matrix to minimize memory bandwidth overhead?

Context: VLM Inference Optimization during autoregressive generation.

---

**FlashAttention** (or PagedAttention for efficient KV cache management).
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

## Extensions

- [Visual process notes](extension.md): Use when source material includes screenshots, diagrams, GIFs, slide animations, or videos, and the goal is to convert the visual mechanism into Anki notes.

## Workflow

1.  **Analyze**: Breakdown the source material into the smallest possible concepts.
2.  **Formulate**: Draft questions that are short, clear, and unambiguous.
3.  **Format**: Apply either the Standard or Context-Extended format strictly based on complexity.
4.  **Validate**: Ensure the answer is concise and directly addresses the question.
