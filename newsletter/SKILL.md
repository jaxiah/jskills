---
name: newsletter
description: Generate on-demand Chinese Markdown newsletters from configured research sources, clustering unread materials by topic before splitting into issues of at most 20 items. Each issue contains linked theme overviews and individual article summaries. Use when the user requests a research digest or newsletter.
---

# Research Newsletter

Generate a newsletter when requested, not a review paper. Scheduling, email delivery, and PDF/HTML rendering are outside this skill. Instructions and references are in English; newsletter overviews and individual summaries are simplified Chinese Markdown with English halfwidth punctuation for technically literate readers. Translate non-Chinese author abstracts into Chinese; keep the original-language materials in the archive, not as a second body in the newsletter.

## Execution Contract

- Follow the existing path: `archive.py sync` -> `pending` -> read cached originals -> understand and cluster the full set -> split and write Markdown -> `check` each issue -> `mark used` after content verification. Invoke `archive.py` as `python -X utf8 <skill-path>/scripts/archive.py <command>` through the actual installed skill path. Ordinary generation does not require new executable code.
- Reuse the skill's scripts for supported feed/API parsing, archiving, deduplication, and validation; use normal file-reading/editing tools for materials and newsletter prose. Do not create issue-specific or batch-specific generator scripts, or equivalent ad hoc inline programs. Changing URLs within supported source types, dates, article counts, or themes changes arguments and content, not the implementation. One-off ordinary-webpage discovery is a separate exception described below, not a newsletter-generation dependency.
- Missing reusable capabilities and new stable API adapters belong in the skill's scripts, with tests and documented invocation, when updating the skill. Site-specific webpage selectors and parsers do not: handle those flexibly for the current task without adding them to the skill. Normal tool calls and short shell commands for reading files or invoking existing helpers are appropriate.

## Data Directory

`D:/newsletters` is the data root. The skill directory contains only guidance and executable helpers. Running this skill's `scripts/archive.py init` creates:

- `feeds.txt`: user-maintained source URLs, one per line; lines beginning with `#` are comments. `sync` supports RSS/Atom and explicitly adapted APIs, currently Hugging Face Daily Papers (`https://huggingface.co/api/daily_papers`). Ordinary webpage URLs are not automated feeds; if present, handle them separately as described below.
- `state.sqlite`: deduplication, processing status, and the current source-selected scope. Use `archive.py processed` to inspect completed materials.
- `materials/<id>/`: original HTML or PDF, readable text where available, and metadata. This is a download cache, not a source-selection mechanism.
- `issues/`: generated newsletter Markdown.

On each invocation, retrieve the current items from `feeds.txt`. Process uncompleted materials originally published within the past year, using the original publication date rather than a feed update or feature date. Undated items are not automatically archived; use `add <URL>` when explicitly requested. Sources expose only their currently returned entries; the one-year rule does not require traversing website history or guarantee historical backfill.

Source entries determine the scope, SQLite determines completion, and the local cache determines whether downloading is necessary. After `state.sqlite` is deleted, register only cached materials matched by the current sources as pending. Do not import unrelated cached items or pretend to recover lost completion history. Reuse complete cached originals, download only missing files, and report invalid caches without overwriting existing files.

## Collection and Understanding

- **First-class support: RSS/Atom.** Use the common parser across sites; adding or replacing a feed URL does not require site-specific code.
- **Second-level support: explicitly adapted APIs.** Hugging Face Daily Papers is currently supported. Add other APIs as reusable adapters when needed; arbitrary JSON is not a common source schema. Do not implement ordinary list-page parsers or HTML fallback inside the skill.
- Invoke `python -X utf8 <skill-path>/scripts/archive.py sync`, then `pending`, through the actual skill path; no global command is needed. `pending` is the current coverage list, not every file in the cache. Inspect sync errors and skipped-date counts; unsupported sources, API failures, and changed schemas must be reported, not silently treated as empty feeds or replaced with webpage scraping.
- **Ordinary webpages are agent-led, per-task work.** When requested or listed in `feeds.txt`, use browsing tools or one-off extraction outside the skill to discover article URLs. Prefer an available feed or supported API; do not rewrite the user's list or silently claim equivalent coverage. Apply the same one-year publication window and report uncertain dates or access gaps. After `sync`, register verified, eligible article URLs with `archive.py add <URL>` before reading `pending`, so the existing cache, deduplication, and completion tracking still apply. An unresolved page is a coverage gap, not an empty feed. This exception permits task-local extraction code, not a custom newsletter generator or a permanent website parser.
- A Daily Papers API URL with `limit` can return multiple editions; do not call it a single latest edition. Use `sync --date YYYY-MM-DD` for an explicitly selected edition. Report what the API returned, including an empty list, without a webpage fallback. Do not rewrite `feeds.txt` to accommodate a one-off request.
- Understand every selected article before clustering. An author-written abstract, introduction, or early overall description is often sufficient; full-paper reading is not mandatory. Read further when needed to resolve a mechanism, comparison, number, or ambiguity. For blogs, read their opening argument and relevant supporting passages. Do not cluster from titles alone or treat platform-generated summaries as primary evidence.
- Recover the problem, actual contribution or argument, how it works, and the available evidence and limits. If only the abstract was read, do not invent implementation details, ablations, or limitations, or imply that the full paper was checked. Distinguish an author's abstract from an agent-written summary. In agent-written prose, preserve necessary technical terms and explain unfamiliar ones briefly.
- Originals remain archived under `materials/` even when only selected passages are read. Use `readable.txt`, HTML, or the archived PDF as appropriate. Unread, inaccessible, or incompletely archived materials remain pending; identify the gap rather than claiming completion.

## Cluster Before Splitting

- Cluster the entire eligible pending set by actual content first, then partition it into newsletters. Do not take the first 20 records and cluster that slice. Group by shared research question, obstacle, approach, or application within a domain, not merely a broad keyword such as "AI" or "agents."
- Each newsletter contains **at most 20 distinct articles**, with no limit on the number of newsletters. Cover all eligible materials across the batch; interest, popularity, and narrative convenience are not selection criteria. Each article has one primary cluster and appears in exactly one issue, even if it relates to multiple themes.
- Keep a coherent cluster together when it fits. Split clusters larger than 20 along meaningful subtopics where possible; otherwise use coherent continuation parts. Combine small clusters only when genuinely related. Do not fill an issue to 20 by mixing unrelated subjects, manufacture relationships, or drop small clusters or singletons. Rebalance small remainders when that improves coherence without breaking the cap.
- Finish the global grouping before writing issue-local overviews. This is reasoning, not a required saved planning artifact. If work remains unfinished, report the remaining scope and preserve pending status.

## Two-Part Newsletter

Start with a title and a short source/date/coverage note, including the part number for a batch. Then use exactly two H2 sections, titled in Chinese: "Theme Overview" and "Individual Summaries."

### Theme Overview

- Write **one natural paragraph per theme**, optionally beginning with a bold theme label. Each paragraph has an intelligible progression, like a focused introduction: establish a shared problem, show how the included works approach it, and explain supported differences, connections, or unresolved questions.
- **Do not stitch unrelated sentences or abstracts into a paragraph.** Actually understand each article and its role in the theme. "A does X; B does Y; C does Z" is not a coherent overview just because the sentences share a label. Transition words cannot manufacture a logical connection. If the relationship cannot be explained, revise the cluster rather than force the prose.
- Every sentence making an article-specific claim links to the corresponding H3 heading below, using a normal Markdown heading link, such as `[1](#1-budgetkv)` for `### 1. BudgetKV`, or a descriptive label. Comparisons or syntheses involving several articles cite all relevant entries. The overview's citations are internal links, not just original web URLs; every included article is naturally represented and cited in its own issue's overview.
- Explain whether works compete, complement one another, address different bottlenecks, or challenge an assumption only when supported. Keep author claims distinct from the newsletter's interpretation. Do not invent consensus, causality, historical progression, novelty, or directly compare incompatible benchmark scores. A singleton theme can explain its own question without a fabricated cross-paper connection.

### Individual Summaries

- Give each article exactly one H3 heading with its display number and recognizable title. Use plain-text, unique headings in the same thematic order as the overview and restart display numbering in each issue. No HTML anchors or material IDs in headings are needed. Use GitHub-style heading fragments: lowercase letters, replace spaces with hyphens, remove other whitespace and punctuation except existing hyphens/underscores, and retain Chinese characters. Update citations whenever a heading changes. Do not use H3 headings for themes or add lower-level headings inside entries.
- **If the article has an author-written abstract, translate the complete abstract faithfully into Chinese.** Use that translation as the individual summary, without condensing, adding claims, or appending a second agent-generated summary. Preserve numbers, comparisons, conditions, qualifications, and uncertainty; retain useful technical terms in English when translating them would obscure their meaning. If an improvement's unit is ambiguous, preserve the source's wording rather than silently deciding between a relative percentage and percentage points. An already-Chinese abstract can be reused. Feed excerpts, truncated descriptions, and platform-generated AI summaries do not count as author abstracts; retrieve the actual abstract from the source when needed.
- **Only when there is no author-written abstract, write a self-contained Chinese summary.** Explain the problem, specific contribution or argument, the mechanism when understood, the strongest available evidence, and meaningful limits. Use connected prose of whatever length the material needs, not a rigid sentence count or a visible checklist. A title-and-link list is not coverage.
- Put the translation or summary directly below its H3 as ordinary paragraphs, not a blockquote or code block. No repeated "author abstract" heading or English duplicate is needed. Explain abstract translation versus agent summarization in the issue's short reading-scope note; for a mixed issue, identify exceptions in a brief source note beside their links.
- In generated summaries and overviews, give numerical claims their metric, comparison, relevant conditions, and boundary. Treat a blog's examples or experience as such, not as an experiment. State missing evidence honestly rather than inventing numbers, criticism, or insights to fill a template. Avoid promotional language and paper boilerplate in agent-written prose; do not use these editing rules to omit or embellish claims in an abstract translation.
- Include the original URL and an openable local archive link, such as `[Local PDF](../materials/<material-id>/paper.pdf)` or the saved HTML, in either case. The local link identifies the archived material independently of the heading. Reusing an abstract does not imply independent reproduction or full-paper verification.

## Saving and Completion

Save Markdown only under `D:/newsletters/issues/`. Use `newsletter-YYYYMMDD-HHMM.md` for one issue or `newsletter-YYYYMMDD-HHMM-part-01.md`, `-part-02.md`, etc. for a batch. Add a suffix on collision instead of overwriting. Do not create an empty newsletter when there are no new materials.

- Reread the overview for logical continuity, then verify important claims against the passages actually consulted. Check that every article has a complete Chinese abstract translation or, only when no abstract exists, a substantive Chinese summary. Check translations against the originals for omissions, altered numbers, and stronger claims. Check ordinary-paragraph formatting, overview citations and links, and ensure the batch has no omissions or duplicated articles. A structural validator cannot establish understanding or source fidelity.
- Run `archive.py check <issue-path>` for each saved issue. Only after the content and sources are checked, run `archive.py mark used <id>... --issue <issue-path>` separately for each issue and its own article IDs. `mark` also checks the structure and the 20-item cap; it does not verify scientific claims. Unfinished items stay pending. Report all issue paths, total completed and unfinished counts, and source gaps.

## Optional Paper-Writing Reference

[Michael Black's scientific writing methodology](references/michael-black-writing-methodology.md) is for a later, explicitly requested paper or substantial literature review. It is not a mandatory newsletter reference or a reason to force incoming materials into one paper-like argument. The newsletter's writing rules are entirely above.
