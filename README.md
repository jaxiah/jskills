# My Agent Skills

Copy `link-targets.local.example.txt` to `link-targets.local.txt`, then edit it with one agent skills directory per line:

```text
%USERPROFILE%\.claude\skills
%USERPROFILE%\.gemini\skills
%USERPROFILE%\.codex\skills
```

Then run `link.cmd` to link every skill directory in this repo into those targets.

`link-targets.local.txt` is intentionally ignored so each machine can maintain its own agent install paths.
