# My Agent Skills

Copy `install-targets.local.example.txt` to `install-targets.local.txt`, then edit it with one agent skills directory per line:

```text
%USERPROFILE%\.claude\skills
%USERPROFILE%\.gemini\skills
%USERPROFILE%\.codex\skills
```

Then run `install.cmd` to copy every skill directory in this repo into those targets.

Existing skill directories in the target locations are updated in place with `Copy-Item -Force`; matching files are overwritten, and extra local files are left untouched.

`install-targets.local.txt` is intentionally ignored so each machine can maintain its own agent install paths.
