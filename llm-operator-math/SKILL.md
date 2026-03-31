---
name: llm-operator-math
description: Decompose any LLM (or VLM) into fine-grained operators, write long-form math explainer READMEs, implement each operator in pure NumPy, and validate against PyTorch ground truth activations. Use when user wants to study, explain, or verify the mathematical internals of a neural network model operator-by-operator.
---

# LLM Operator Math Explainer & Verifier

Turn any HuggingFace model into an **operator-by-operator math study guide** with runnable NumPy verification.

This skill orchestrates the full workflow: operator enumeration → activation dumping → math README authoring → naive NumPy implementation → end-to-end validation.

## When to Use

- User wants to **understand the math** behind a model's inference pipeline
- User wants to **implement operators from scratch** (NumPy, no framework magic)
- User wants a **teaching-quality walkthrough** of how a specific model works internally
- User mentions: "operator math", "explain the math of", "implement in numpy", "verify against pytorch", "operator-by-operator", or similar

## Integration with Other Skills

This skill works best when preceded by:

1. **write-a-prd** — to define the target model, scope (which operators), audience level, and testing strategy
2. **prd-to-issues** — to break the PRD into one issue per operator (or operator group)

If the user already has a PRD and issues in `BACKLOG/`, skip straight to Phase 2 below. If not, suggest using those skills first or do a lightweight version inline.

---

## Phase 1: Project Scaffolding

### 1.1 Directory Structure Convention

```
project-root/
  BACKLOG/                     # PRD and ISSUE files (from write-a-prd / prd-to-issues)
  e2e/
    dump_activations.py        # PyTorch hook-based activation dumper
    validate.py                # Shared validation utilities
    run_numpy_e2e.py           # E2E runner that calls all operator validations
  operators/
    00_overview/
      README.md                # Complete operator list, execution order, architecture diagram
    NN_operator_name/
      README.md                # Long-form math explainer (the core deliverable)
      impl.py                  # Pure NumPy implementation + validation functions
  activations/                 # Dumped .npy files (gitignored, regenerable)
  pyproject.toml
  .gitignore
```

- **Numbering**: Operators are numbered in inference execution order (`01_`, `02_`, ...).
- **Naming**: Use lowercase_snake_case for directory names. The name should describe the mathematical operation, not the PyTorch module name.
- **activations/**: Always gitignore this directory — it's large and fully regenerable.

### 1.2 Activation Dumping Strategy

The cornerstone of this workflow is **hook-based activation dumping**:

1. Run the target model once through PyTorch (with a representative input)
2. Register `forward_hook` on every module of interest
3. Save each module's input and output tensors as `.npy` files (always `float32`)
4. For repeated layers (e.g., 28 decoder layers), only dump layer 0 to save space
5. Naming convention: `module__path__with__double_underscores_{input|output}.npy`

```python
# Core pattern for the hook:
def make_hook(name, output_dir):
    def hook_fn(module, input, output):
        # Save input (handle tuple inputs)
        inp = input[0] if isinstance(input, tuple) else input
        np.save(f"{output_dir}/{name}_input.npy", inp.detach().float().cpu().numpy())
        # Save output (handle tuple outputs)
        out = output[0] if isinstance(output, tuple) else output
        np.save(f"{output_dir}/{name}_output.npy", out.detach().float().cpu().numpy())
    return hook_fn
```

### 1.3 Validation Utilities (`e2e/validate.py`)

Provide a shared `validate()` function that:

- Compares shapes first (immediate fail on mismatch)
- Uses `np.allclose(actual, expected, atol=atol, rtol=rtol)`
- Prints: status, shape, dtype, max/mean absolute error, tolerance used
- On failure: shows worst-case index and values
- Returns `bool` for programmatic aggregation

Tolerance guidelines:

| Operation type                             | Recommended atol | Notes                            |
| ------------------------------------------ | ---------------- | -------------------------------- |
| Element-wise (activation functions, norms) | `1e-5`           | High precision expected          |
| Matrix multiplications (linear, attention) | `1e-4`           | Float32 accumulation differences |
| Multi-step compositions (full blocks)      | `1e-3` to `0.01` | Error compounds across steps     |

### 1.4 Weight Loading Pattern

```python
from safetensors import safe_open
from huggingface_hub import hf_hub_download, HfApi

def load_safetensors_weights(model_id: str, keys: list[str]) -> dict[str, np.ndarray]:
    """Load specific weight tensors from HuggingFace safetensors files.

    Always convert to float32 (models often store bf16/fp16).
    """
    api = HfApi()
    siblings = api.model_info(model_id).siblings
    safetensor_files = [s.rfilename for s in siblings if s.rfilename.endswith(".safetensors")]

    result = {}
    remaining = set(keys)
    for filename in safetensor_files:
        if not remaining:
            break
        path = hf_hub_download(repo_id=model_id, filename=filename)
        with safe_open(path, framework="pt", device="cpu") as f:
            for key in list(remaining):
                if key in f.keys():
                    result[key] = f.get_tensor(key).float().numpy()
                    remaining.discard(key)
    if remaining:
        raise KeyError(f"Weights not found: {remaining}")
    return result
```

---

## Phase 2: Operator Implementation (`impl.py`)

Each operator's `impl.py` follows a strict structure:

```python
"""NN — 算子名称 (English Name): 核心公式

用纯 NumPy 实现 <算子名称>，并用 <模型名> 的真实权重和激活值验证。
"""

import numpy as np
from e2e.validate import validate, load_activation

DUMP_DIR = "activations"
MODEL_ID = "<huggingface-model-id>"


# ---------------------------------------------------------------------------
# 核心算子 (Core Operator)
# ---------------------------------------------------------------------------
def operator_name(x: np.ndarray, ...) -> np.ndarray:
    """One-line description of what this does mathematically."""
    # Implementation: pure numpy, no torch, no scipy
    # Each line should map clearly to a step in the README's math derivation
    ...


# ---------------------------------------------------------------------------
# 权重加载工具 (Weight Loading — if this operator has learnable parameters)
# ---------------------------------------------------------------------------
def load_weights(...):
    ...


# ---------------------------------------------------------------------------
# 验证 (Validation)
# ---------------------------------------------------------------------------
def validate_case_1() -> bool:
    """Validate against a specific layer/module in the model."""
    print("\n=== Descriptive Title (input_shape) -> (output_shape) ===")
    x = load_activation(DUMP_DIR, "<input_activation_name>")
    expected = load_activation(DUMP_DIR, "<output_activation_name>")
    # Load weights if needed
    actual = operator_name(x, ...)
    return validate("<test_name>", actual, expected, atol=..., rtol=...)


def validate_case_2() -> bool:
    """Validate a second case (e.g., vision path vs text path)."""
    ...


if __name__ == "__main__":
    results = [validate_case_1(), validate_case_2()]
    print(f"\n{'='*60}")
    print(f"<算子名称>验证: {sum(results)}/{len(results)} 通过")
    if not all(results):
        raise SystemExit(1)
```

### Implementation Rules

1. **Pure NumPy only** in the core operator function — no PyTorch, no scipy, no sklearn
2. **No broadcasting tricks** that obscure the math — prefer explicit reshape/transpose so the reader can trace dimensions
3. **Variable names should match the README's notation** — if the README calls it $W_Q$, the code uses `W_Q`
4. **Two validation cases minimum** when the operator appears in both vision and text paths
5. **Weight tying awareness** — some models share weights (e.g., `lm_head.weight == embed_tokens.weight`); document this in a comment

---

## Phase 3: Math README Authoring (THE CORE DELIVERABLE)

The README is the **primary artifact** — it should be a standalone, publishable blog post that fully explains the operator's mathematics to someone with basic linear algebra knowledge.

### Target Audience

An **engineering graduate** who:

- Knows linear algebra fundamentals (matrix multiplication, eigenvalues, vector spaces)
- Knows basic calculus (derivatives, chain rule)
- Knows basic probability (mean, variance, distributions)
- Does NOT know deep learning, attention mechanisms, or neural network training
- Reads Chinese (Simplified) as the primary language

### Language Rules

- **Primary language**: Chinese (Simplified)
- **Keep English for**: technical terms, variable names, function names, paper titles, proper nouns
- **MathJax**: Use `$...$` for inline math, `$$...$$` for display math (GitHub/Markdown compatible)
- **Code blocks**: Python/NumPy snippets to bridge math → implementation

### Required Structure (10 Sections)

Every operator README MUST include all of the following sections. Sections may be reordered or merged slightly if it improves narrative flow, but no section may be omitted.

#### Section 1: Opening Hook & Motivation (为什么要关心这个算子?)

- Start with a **real-world analogy** that makes the abstract concept tangible
- Explain **why this operator exists** — what problem does it solve in the model?
- Give the reader a reason to care before any math appears
- Connect to the bigger picture: where does this operator sit in the inference pipeline?

#### Section 2: Prerequisites (前置知识)

- List and briefly review the math concepts needed
- Don't assume the reader remembers everything — provide quick refreshers
- Link forward: "we'll use this in Section 4 when we..."

#### Section 3: Core Mathematical Definition (核心数学定义)

- Present the **formal definition** with full notation
- Every symbol must be defined explicitly the first time it appears
- Use display math (`$$...$$`) for the main equations

#### Section 4: Step-by-Step Derivation (逐步推导)

- Walk through the math **one operation at a time**
- Show intermediate results — never skip steps
- Explain **why** each step is taken, not just what
- Use phrases like "注意这里..." and "之所以要这样做, 是因为..."

#### Section 5: Numerical Example (数值算例)

- Work through a **complete small example** with concrete numbers
- Choose dimensions small enough to trace by hand (e.g., 2×3 matrices)
- Show every intermediate computation result
- Optionally include a second example with a twist (edge case, different shape)

#### Section 6: Geometric / Visual Intuition (几何直觉)

- Explain what the operation **does geometrically** to the data
- Use analogies: rotations, projections, scaling, gating, filtering
- For operations in high-dimensional space, project down to 2D/3D for intuition

#### Section 7: Why This Design? (设计动机与历史)

- Brief history: who invented it, what paper introduced it, what it replaced
- Why this variant over alternatives (e.g., why RMSNorm over LayerNorm?)
- Tradeoffs: what does this design gain/lose?

#### Section 8: Model-Specific Details (在本模型中的具体应用)

- Exact dimensions, parameter counts, specific configuration values
- Which layers/modules use this operator
- Any model-specific quirks or non-standard usage
- Example: "Qwen2-VL 的 Vision Encoder 使用 embed_dim=1280, 16 heads, head_dim=80"

#### Section 9: NumPy Implementation Walkthrough (NumPy 实现详解)

- Present the **complete core function** from `impl.py`
- Annotate each line: which math equation does it implement?
- Explain shape transformations explicitly: "输入 shape 为 (B, T, D), 经过 reshape 变为..."
- Show how to load weights and run validation

#### Section 10: Common Pitfalls & Summary (常见陷阱与小结)

- List 3-5 common mistakes (numerical stability, shape errors, broadcasting traps)
- Provide a concise summary table or bullet list of key takeaways
- Optionally: further reading links (papers, blog posts)

### Writing Style Guide

1. **娓娓道来 (Flowing, methodical narrative)**: Write as if explaining to a curious colleague over coffee, not writing a textbook. Use conversational transitions.

2. **Progressive complexity**: Start with the simplest possible framing, then add complexity layer by layer. Never front-load all the complexity.

3. **Bridge every abstraction**: When introducing an abstract concept, immediately follow with a concrete example or analogy.

4. **Explicit dimension tracking**: Every time a tensor changes shape, state the before/after shapes. Use comments like `# (B, T, D) -> (B, T, H, d_k)`.

5. **No "obviously" or "trivially"**: If it were obvious, the reader wouldn't need the document.

6. **Section length targets**:
   - Total README: 400–1000+ lines of Markdown
   - Core operators (attention, RoPE, conv3d): 800–1200 lines
   - Simple operators (activation functions, norms): 400–700 lines
   - Composite operators (full blocks, MLP): 600–900 lines

7. **Use horizontal rules (`---`)** between major sections for visual breathing room.

8. **Subsections with numbered headings** (`## 1. ...`, `### 1.1 ...`) for easy navigation.

---

## Phase 4: E2E Validation Runner

Create `e2e/run_numpy_e2e.py` that:

1. Imports each operator's validation functions
2. Runs them in inference execution order
3. Collects pass/fail results
4. Prints a summary table at the end

```
============================================================
E2E Validation Summary: 20/20 PASS
============================================================
[PASS] 01_linear: vision_fc1_linear
[PASS] 01_linear: text_gate_proj_linear
...
```

The E2E runner is the final deliverable that proves all implementations are correct.

---

## Workflow Summary

```
[write-a-prd]  →  PRD in BACKLOG/
       ↓
[prd-to-issues]  →  One ISSUE per operator (or operator group)
       ↓
[This skill - Phase 1]  →  Scaffold: e2e/, operators/00_overview/, dump script
       ↓
Run dump_activations.py  →  activations/*.npy ground truth
       ↓
[This skill - Phase 2]  →  For each operator: impl.py with validation
       ↓
[This skill - Phase 3]  →  For each operator: README.md math explainer
       ↓
[This skill - Phase 4]  →  E2E runner: all operators pass
       ↓
Git commit with all artifacts
```

### Parallelization Strategy

- Phase 2 operators can be implemented in **dependency order** (some operators depend on others, e.g., attention depends on linear, softmax, RoPE)
- Phase 3 READMEs can be written in **parallel batches** using background agents — group by complexity:
  - Batch 1: Simple element-wise ops (activation functions, norms)
  - Batch 2: Medium complexity (linear, embedding, residual)
  - Batch 3: Complex (attention, RoPE, conv3d, patch merger)
  - Batch 4: Composite (full blocks, decoder layers, lm_head)

### Quality Checklist

Before committing, verify:

- [ ] All `impl.py` files run individually (`python -m operators.NN_name.impl`)
- [ ] E2E runner passes all validations
- [ ] Every README has all 10 required sections
- [ ] MathJax renders correctly (no broken `$...$` pairs)
- [ ] Dimension annotations are consistent across README and impl.py
- [ ] Model-specific numbers (hidden_size, num_heads, etc.) are accurate
- [ ] Variable names in code match notation in README
