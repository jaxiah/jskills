---
name: newsletter
description: Generate an on-demand Chinese Markdown research newsletter covering all unprocessed materials returned by configured sources. Use when the user requests a research digest or newsletter, with source verification and organization by domain or research problem.
---

# Research Newsletter

Generate a Chinese Markdown review when requested. Do not impose a weekly schedule or a fixed reporting window. Scheduling, email delivery, and final rendering formats are outside this skill.

## Data Directory

`D:/newsletters` is the data root. The skill directory contains only guidance and executable helpers. Running this skill's `scripts/archive.py init` creates:

- `feeds.txt`: user-maintained RSS/Atom URLs or the official Hugging Face Daily Papers API URL, one per line; lines beginning with `#` are comments.
- `state.sqlite`: deduplication, processing status, and the current source-selected scope. Use `archive.py processed` to inspect completed materials.
- `materials/<id>/`: original HTML or PDF, readable text where available, and metadata. This is a download cache, not a source-selection mechanism.
- `issues/`: generated newsletter Markdown.

On each invocation, retrieve the current items from the URLs in `feeds.txt`. Process uncompleted materials whose original publication date falls within the past three years. Items without a parseable date are not automatically archived; use `add <URL>` when explicitly requested. RSS exposes only its currently retained entries. Infrequent manual runs can miss updates outside a source's retention window; this skill does not promise to backfill a website's history.

Source entries determine the scope, SQLite determines completion, and the local cache determines whether downloading is necessary. After `state.sqlite` is deleted, register only cached materials matched by the current sources as pending. Do not import unrelated cached items or pretend to recover lost completion history. Reuse complete cached originals, download only missing files, and report invalid caches without overwriting existing files.

## Output Preferences

- Language: simplified Chinese.
- Punctuation: English halfwidth punctuation throughout, including Chinese prose.
- Audience: technically literate readers who may not know every subfield.

## Coverage

- Cover every uncompleted item returned by the current sources and eligible under the date rule, including previously unfinished items that remain in the current results. Do not filter by interest, popularity, domain, or narrative convenience, and do not set an item-count limit. The reader decides what interests them.
- Give each material substantive treatment: its problem, contribution, evidence, and limits. Length may vary, but a title-and-link list is not coverage. Do not revert to stitched abstracts to accommodate more items.
- Identify inaccessible originals and evidence gaps explicitly; do not invent conclusions. If work remains unfinished, report that scope and preserve pending status rather than claiming full completion.

## Collection and Writing

- Run this skill's `scripts/archive.py sync`, then `pending`. `sync` retrieves the source lists, checks matching caches, and downloads only as needed; it reports `downloaded` and `reused` counts separately. It does not traverse website history. `pending` lists only uncompleted items selected by the most recent synchronization, not everything in the cache. For a particular Hugging Face Daily Papers edition, use `sync --date YYYY-MM-DD`. For a user-supplied article or paper URL, use `add <URL>` to archive or reuse it and add it to the current scope. Invoke the helper through its actual installed skill path; no global command is needed. Use `python -X utf8 <skill-path>/scripts/archive.py <command>` for UTF-8 output on Windows.
- Use `pending` as the coverage list. For web pages, read `readable.txt` and check `source.html` as needed. For papers, read the archived `paper.pdf` or `source.pdf`. Necessary historical originals may be consulted as background, but they are not new materials and do not change source-selected coverage. An incomplete snapshot or failed download is not a verified original and must not be marked complete.
- Read the [writing guide](references/writing-guide.md) and [full methodology](references/michael-black-writing-methodology.md). Review all pending materials and write a coherent synthesis organized by domain or problem, keeping unrelated work separate. Explain the relationships among obstacles, insights, technical choices, and evidence. Do not invent insights or turn submission and typesetting advice into required steps. Do not reprocess completed items. After drafting, perform a separate comprehension and source-verification pass, and reconcile coverage with the pending list.

## Saving and Completion

Save Markdown only to `D:/newsletters/issues/`, named `newsletter-YYYYMMDD-HHMM.md`. Add a suffix on collision instead of overwriting. For each material, include the original web link and an openable local archive link from `issues/` to the HTML or PDF under `../materials/<id>/`.

Only after verifying the original and substantively covering it in the saved issue, run `archive.py mark used <id>... --issue <issue-path>`. Unread or inaccessible originals remain pending; lack of interest is never a reason to mark an item complete. Report the issue path, completed and unfinished counts, and source gaps. Do not generate PDF or HTML at this stage.
