---
name: roundtable
description: Participate in a lightweight file-system roundtable with other CLI agents. Use when the user asks for a roundtable speak turn, invokes /roundtable speak, invokes $roundtable speak, or asks this agent to read the shared tabletop and place a concise public response into the roundtable.
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

In examples, `<skill-scripts>\agentturn.cmd` means this agent's generated wrapper in its installed skill `scripts/` directory.

## Starting a Roundtable

A roundtable starts when the human places the first message on the tabletop from the project root.

This creates `.roundtable/messages/0001-human.md` if the roundtable does not already exist.

After the opening human message, the human can ask agents to participate from their own terminals with the roundtable `speak` operation.

Common invocations:

- Claude Code / Gemini CLI: `/roundtable speak`
- Codex: `$roundtable speak`
- Natural language: "use roundtable to speak"

### `speak`

When the user asks this agent to perform a roundtable `speak` turn:

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

## Human Messages

Human messages are created with `humansay.py`.

Use `humansay.py` only for human-authored content:

- The human runs it directly to place a public human message on the tabletop. They can use `--at <agent-name>` to indicate who the message is for.

Do not use `humansay.py` yourself. Agent messages must be published through `agentturn.cmd post`.

On Windows, run `scripts/make_cmds.cmd <agent-name>` from each agent's installed skill directory. This generates `agentturn.cmd` in the skill's `scripts/` directory, and places a `roundtable.cmd` TUI launcher in your current project root for human use.
