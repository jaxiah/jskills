# Skill Selection

Keep or create a skill only when it captures knowledge or behavior that an agent cannot reliably infer on its own, such as:

- Exact personal conventions or output formats that must remain consistent.
- Specialized domain knowledge and validation procedures.
- Executable scripts, assets, or external protocols required to complete the task.
- A focused, repeatedly used workflow where omitted steps have caused concrete failures.

Do not create or retain a skill merely to restate general software-engineering knowledge. In particular, avoid:

- Long mandatory pipelines of planning, design, implementation, and status documents.
- Process artifacts that exist mainly to prove that a step was followed.
- Instructions already enforced more reliably by repository tests, linters, types, CI, or a short repository-level rule.
- Broad workflows that increase the user's coordination burden without producing measurably better results.
- Hidden dependencies on other skills or file conventions that are not intrinsic to the skill's purpose.

Prefer small, independent skills with explicit triggers and narrow responsibilities. Let the agent choose ordinary implementation steps. Constrain important outcomes with executable checks, keep durable project conventions in `AGENTS.md`, and use human or independent-agent review only where judgment is genuinely needed.

Evaluate a skill by whether it reduces repeated user effort and prevents observed failures, not by how comprehensive its procedure appears. If a skill no longer earns its maintenance and context cost, simplify or remove it.
