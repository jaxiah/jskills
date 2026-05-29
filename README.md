# My Agent Skills

Copy `install-targets.local.example.txt` to `install-targets.local.txt`, then edit it with one agent skills directory per line:

```text
%USERPROFILE%\.claude\skills
%USERPROFILE%\.gemini\skills
%USERPROFILE%\.codex\skills
```

Then run `install.cmd` to copy every skill directory in this repo into those targets.

Existing directories are skipped so each agent install can keep local customizations. Delete old junctions or symlinks manually before running `install.cmd` if you want them replaced with real copies.

`install-targets.local.txt` is intentionally ignored so each machine can maintain its own agent install paths.
