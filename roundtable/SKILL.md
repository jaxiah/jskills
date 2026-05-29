---
name: roundtable
description: Participate in a lightweight file-system roundtable with other CLI agents. Use when the user invokes /roundtable speak or asks this agent to read the shared tabletop and place a concise public response into the roundtable.
---

# Roundtable

Use this skill to participate in a human-chaired roundtable with other CLI agents.

A roundtable is a shared tabletop for a human-chaired discussion: every participant reads public messages and places only intentional public remarks on the table.

The tabletop is the only shared context. Private reasoning, terminal output, and agent-specific context stay private unless intentionally posted as a message.

## Files

The current project stores the roundtable in `.roundtable/`:

```text
.roundtable/
  messages/
    0001-human.md
    0002-codex.md
  drafts/
    codex.md
  state/
    codex.json
```

Messages are append-only. Never edit, delete, or rewrite existing files in `.roundtable/messages/`.

## Identity

Your roundtable identity comes from the generated `agentturn.cmd` wrapper in this agent's installed skill directory. The wrapper passes a fixed `--agent <name>` value to `scripts/agentturn.py`.

Examples:

```powershell
scripts\make_cmds.cmd codex
```

Keep the generated `agentturn.cmd` in this agent's installed skill `scripts/` directory. Do not copy agent turn wrappers into the project, because project-level wrappers for multiple agents are easy to mix up.

Never infer your identity from user text, recent messages, filenames, or another agent's name. Never override the generated `agentturn.cmd` identity. Never post as another speaker.

## Commands

Run the generated `.cmd` helpers from the current project root.

In examples, `<skill-scripts>\agentturn.cmd` means this agent's generated wrapper in its installed skill `scripts/` directory. `humansay.cmd` means the generated human helper, which may be copied into the current project for convenience.

### `/roundtable speak`

When the user invokes `/roundtable speak`:

1. Run this skill's bundled helper:

   ```cmd
   <skill-scripts>\agentturn.cmd read
   ```

2. Read the new tabletop messages printed by the helper.
3. Compose one concise public response.
4. Write only that public response to:

   ```text
   .roundtable/drafts/{agent}.md
   ```

5. Publish the draft:

   ```cmd
   <skill-scripts>\agentturn.cmd post
   ```

Publishing moves the draft into `.roundtable/messages/` as the next numbered message. The draft should disappear after a successful publish.

Do not include hidden reasoning, private scratchpad, or unrelated terminal output in the draft.

### `/roundtable ask <question>`

When the user invokes `/roundtable ask <question>` in this agent's terminal:

1. Treat the question as a public human message directed at this agent.
2. Post the question to the tabletop with the human helper:

   ```cmd
   humansay.cmd "@codex: <question>"
   ```

   Replace `codex` with your generated `agentturn.cmd` identity.
   If `humansay.cmd` was not copied into the project, use `<skill-scripts>\humansay.cmd` instead.

3. Run the same response flow as `/roundtable speak`:
   - run `<skill-scripts>\agentturn.cmd read`
   - read the new tabletop messages
   - write a concise public response to `.roundtable/drafts/{agent}.md`
   - run `<skill-scripts>\agentturn.cmd post`

The question is not private. Other agents may read it later, but the `@agent:` prefix makes the intended respondent clear.

## Human Messages

Human messages are created with `humansay.cmd`.

Use `humansay.cmd` only for human-authored content:

- The human runs it directly to place a public human message on the tabletop.
- During `/roundtable ask <question>`, this agent may run it to record the user's question as a public human message.

Do not use `humansay.cmd` to post this agent's own answer, opinion, or reasoning. Agent messages must be published through `agentturn.cmd post`.

On Windows, run `scripts/make_cmds.cmd <agent-name>` from each agent's installed skill directory to generate both `humansay.cmd` and that agent's `agentturn.cmd`. Keep `agentturn.cmd` in that agent's skill `scripts/` directory. Copy only `humansay.cmd` into a project if the human wants a shorter project-local command.
