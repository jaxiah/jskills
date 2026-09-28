# Michael Black's Scientific Writing Method: Insight, Argument, and Evidence

## Source and Scope

This reference reconstructs the method behind Michael Black's *Writing a good scientific paper. The secrets I share with my students.* from the original English article in the user-provided HTML and the primary materials discussed below. It is not a translation of the earlier Chinese reference, a reproduction of the article, or a claim that Black published this exact framework. The organization and explanatory connections are a synthesis; newsletter applications are identified separately.

The article is available on [Medium](https://medium.com/@black_51980/writing-a-good-scientific-paper-c0f8af480c91) and through [Black's research institute](https://is.mpg.de/news/writing-a-good-scientific-paper). The saved HTML records a Medium publication date of 2024-11-09. The 2026-09-28 date in the local filename is a capture date, not the article's publication date.

Black writes from his experience in computer vision, machine learning, and computer graphics, especially conference communities such as CVPR, ICCV, ECCV, NeurIPS, and SIGGRAPH. His ambition is not simply acceptance: a paper should teach an idea that remains useful to the field. Three kinds of guidance must stay distinct:

- **Research and communication practice:** identifying an insight, constructing an argument, explaining mechanisms, and helping readers evaluate evidence.
- **Personal experience and preferences:** judgments about first impressions, reviewer psychology, tense, naming, visual style, and length. These are not automatically experimentally established laws of writing.
- **Publication-specific requirements:** page limits, citation conventions, and rules for supplementary material. Check the actual venue rather than universalizing a historical example.

Use this as a substantive reference, not a mandatory production pipeline. Its questions can guide thinking without creating extra plans, evidence forms, notation tables, or review reports for every newsletter.

## Reading Map

- [1. Writing Is Part of Doing the Research](#1-writing-is-part-of-doing-the-research)
- [2. Establish the Research Before Polishing the Prose](#2-establish-the-research-before-polishing-the-prose)
- [3. The Nugget Is Not the Technical Contribution](#3-the-nugget-is-not-the-technical-contribution)
- [4. Teach Through Goal, Problem, and Solution](#4-teach-through-goal-problem-and-solution)
- [5. Design the Different Entrances to the Paper](#5-design-the-different-entrances-to-the-paper)
- [6. Related Work Should Teach a Way of Thinking](#6-related-work-should-teach-a-way-of-thinking)
- [7. Experiments Should Explain What Matters](#7-experiments-should-explain-what-matters)
- [8. Coordinate Text, Equations, Figures, and Code](#8-coordinate-text-equations-figures-and-code)
- [9. Make the Prose Say Exactly What Happened](#9-make-the-prose-say-exactly-what-happened)
- [10. Revise the Argument and Use Collaborators Well](#10-revise-the-argument-and-use-collaborators-well)
- [11. Finish the Whole Communication Artifact](#11-finish-the-whole-communication-artifact)
- [12. Apply the Method to This Newsletter](#12-apply-the-method-to-this-newsletter)
- [13. Source Coverage and Verification Boundaries](#13-source-coverage-and-verification-boundaries)

## 1. Writing Is Part of Doing the Research

Original sections: *Introduction*, *The biggest mistake in paper writing*, *Conferences do not accept results. They accept papers.*, *Basics of writing*, *Equations*, *Figures*.

Black's most forceful warning is about not writing. Students can spend their entire effort on code and results, postponing the paper until they are exhausted and the deadline is imminent. A successful experiment does not itself constitute a submission. The work still has to become a clear, coherent, supported account that somebody outside the project can understand.

Reading a finished paper creates a misleading intuition about this effort. The reader encounters a compact argument after its difficulties have been removed; the writer must discover the argument, resolve inconsistencies, choose explanations, and coordinate every representation of the work. The speed of reading is therefore a poor estimate of the time needed to write.

Writing early is useful for more than scheduling:

- An early introduction exposes whether the goal and obstacle are actually understood.
- Equations written alongside code expose discrepancies while there is still time to fix the implementation and rerun experiments.
- Preliminary figures expose which comparisons the argument needs, before the researcher commits to the wrong experiments.
- Explaining the work exposes assumptions that were invisible while the team was immersed in implementation.

**Synthesis:** writing, implementation, and evaluation are mutually correcting activities. Treating prose as the final packaging removes one of the mechanisms by which the research becomes intelligible and checkable.

Black also argues that polish affects confidence. Poor figures, confused notation, sloppy references, and difficult prose make it easier for a reviewer to distrust the work. His account of first impressions is especially strong: a weak introduction may leave a reviewer unreceptive to what follows. This is an experienced researcher's warning about communication, not proof that reviewers always behave this way or that polished presentation establishes scientific validity. The appropriate response is to remove avoidable misunderstanding, not to substitute presentation for evidence.

## 2. Establish the Research Before Polishing the Prose

Original sections: *Questions to ask before you start*, *Introduction*, *Strategy*, *Experiments*.

Black's preparatory questions are connected. They ask whether there is a worthwhile, testable idea that can be explained, evaluated, and completed. They are not an administrative checklist to attach to every draft.

### Goal, Audience, and Need

Identify a goal outside the authors' preferences. The reader needs to understand why the problem matters, who would use the result, and who could build on it. Saying that the authors are interested in a topic does not establish its relevance.

A concrete need of the research team can be a good starting point: wanting the method to solve an actual problem is more informative than wanting another contribution. But explain the need in terms the audience can evaluate. Personal motivation must become a recognizable problem in the world.

Audience identification also determines the explanation. What does this reader already know? What must be introduced? Which distinction would change their understanding or decisions? The eventual paper should answer these questions rather than presume the reader has lived through the project.

### Hypothesis and Impediment

Black wants researchers to be able to state their hypothesis even if that sentence never appears in the paper. Ask what would establish it, what would contradict it, and how the experiments distinguish those possibilities.

This guards against incremental engineering without explanation. Changing modules, data, and parameters until a score improves may produce a useful system, but it does not automatically explain what has been learned. A hypothesis gives the changes a reason and gives the results an interpretive purpose.

Then identify the impediment: why has the goal not already been achieved? It might involve assumptions, data, mathematics, computation, or implementation. The obstacle must be real and specific enough that the proposed solution addresses it. A vague assertion that existing work is inadequate is not a substitute.

### Insight, Evaluation, and Feasibility

Keep the remaining questions together:

- What insight makes progress possible? This is the nugget, not just the name of a technique.
- Which previous works are central, and what do their limitations reveal? Understand their achievements as well as their omissions.
- How will the method be evaluated quantitatively? The measurements must bear on the claim being made.
- What demonstration makes the idea's operation visible? A demo and quantitative evaluation serve different purposes.
- What are the important risks, and is the necessary data available?
- Can the work be explained to a senior scientist in at most three sentences?
- What would a teaser image show to communicate the core idea?

The pitch and imagined teaser are diagnostic tools. If neither is possible, the problem may be an unresolved idea rather than inadequate wording. Conversely, a compelling pitch does not demonstrate that the hypothesis is true.

**Newsletter application:** recover these relationships from the source. Do not invent a hypothesis the authors never state, retrofit a clean research history, or reject a blog, dataset release, or tool announcement for not having the structure of a research experiment.

## 3. The Nugget Is Not the Technical Contribution

Original sections: *The Nugget*, *Questions to ask before you start*.

The nugget is the pivotal insight that changes how the problem can be approached. Black credits the term to his postdoctoral adviser, Allan Jepson. He frames it as a new way of seeing the world that makes a previously unsolved problem solvable. His essential distinction is between that insight and the technical contribution that follows from it.

A new architecture, optimization procedure, representation, or dataset can be a contribution. Naming it does not yet communicate the insight. The reader needs to understand why this choice makes sense: what was previously misunderstood, separated, assumed, or overlooked, and how a different view changes the available solution.

For explanation, distinguish five layers:

1. The existing way of understanding the problem.
2. The limitation or missed connection in that understanding.
3. The new observation or reformulation.
4. The technical construction that follows from it.
5. The evidence for the construction and, where available, for the underlying explanation.

These are analytical distinctions, not five required paragraphs. A benchmark improvement may support a particular implementation without isolating why it works. The prose should not quietly treat those two claims as equivalent.

### Optical Flow: A Reformulation Opens a Second Opportunity

Black's example concerns violations of two assumptions used in optical flow: spatial smoothness and brightness constancy. Motion boundaries make the first assumption fail. Changes in image brightness can make the second fail. As he describes the prior emphasis, the field concentrated on spatial discontinuities while overlooking violations of brightness constancy.

The important move is not merely to add another correction term. Recasting the problem in robust statistical terms makes violations of both assumptions instances of a common phenomenon. An approach developed to handle one source of failure now provides a way to handle the other within the same framework.

Compare these descriptions:

- **Contribution only:** a robust optical-flow algorithm improves the estimates.
- **Insight and consequence:** spatial discontinuities and brightness-constancy violations need not be handled as unrelated exceptions; treating them as assumption violations within robust estimation creates a unified route to handling both.

The second description explains why the technical framework is consequential before introducing its mathematical details. That is the function of the nugget: it connects to something the reader knows and then changes the reader's view of it.

The blog calls this a 1992 paper, but its linked [Black and Anandan conference version](https://files.is.tue.mpg.de/black/papers/iccv93.pdf) is from ICCV 1993. A [Brown-hosted scan](https://cs.brown.edu/research/pubs/pdfs/1993/Black-1993-FRE.pdf) was used in the earlier source check. Keep the blog's recollection separate from the publication metadata of the linked version.

### Two Difficult Problems Can Sometimes Become Easier Together

Black describes another recurring form of insight: the field struggles separately with X and Y, but solving them jointly exposes a useful connection. The surprising part is not the act of combining components. It is the reason the combination makes the problem easier.

To communicate such a nugget, explain what the two parts supply to one another: information, constraints, a shared representation, or a different formulation. Combining two difficult tasks is not inherently a simplification. The claim still needs an explanation and evidence.

**Newsletter application:** do not manufacture a nugget for every source. Some contributions are useful engineering, new measurements, infrastructure, or negative results without a stated conceptual reversal. Explain their actual value. A synthesis across papers belongs to the newsletter writer and must not be attributed to an individual paper's authors.

## 4. Teach Through Goal, Problem, and Solution

Original sections: *How to tell a story: Goal, Problem, Solution*, *Introduction*, *Abstract*.

### Make the Reader Understand Why the Solution Is Needed

Black connects scientific explanation to familiar story structures. A desired outcome becomes meaningful through an obstacle and a way of overcoming it. In a paper, the desired outcome is a research goal; the obstacles are substantive difficulties, not fictional antagonists.

The sequence has a specific explanatory role:

- **Goal:** establish something worth achieving.
- **Problem:** show why it is not currently available.
- **Solution:** introduce the insight that changes that situation.

Starting with the solution reverses this dependency. The reader receives a technique before understanding why it is needed and cannot yet judge which details matter.

Black's sequence is recursive. A reformulation can remove one difficulty while exposing another; a technical development addresses that difficulty; implementation may then require a further idea. The reader encounters each piece when its purpose becomes apparent. This is different from describing every obstacle at the beginning and then listing all components without explaining their relationships.

**Synthesis:** narrative here organizes dependencies in understanding. The structure should make the method intelligible, not stage a victory over straw-man prior work. Words such as "however" and "therefore" are useful only when they express genuine limitations and consequences.

### Discover the Teaching Order Before the Paper Order

Black recommends preparing a talk first. A talk makes the teaching goal explicit and leaves less room to bury the idea in text. It forces decisions about what the audience must understand first, which example establishes the problem, and when technical detail becomes useful.

Without a talk, explain the work to a friend. Observe the explanation's natural order, the missing prerequisites, and the questions the listener asks. Use this to shape the introduction. The order in which the researchers discovered the method need not be the order in which readers can best understand it.

He also recommends studying good papers as explanations. Ask not merely what their results are, but how their arguments work: why the opening is effective, how an example changes understanding, and where the author introduces each concept. Award-winning papers are one suggested source of examples, not evidence that every claim in them is correct.

### Freeman's Example Creates a Need for the Principle

Black highlights [William Freeman's generic-viewpoint report](https://merl.com/publications/docs/TR93-11a.pdf). Its shading example admits multiple combinations of shape and illumination that fit one image. Some explanations depend on a special alignment: small changes in lighting alter their appearance markedly. Other explanations remain compatible over a broader range. The example motivates a probabilistic treatment of this difference rather than an arbitrary choice of preferred shape.

The report's example and Figure 3 caption were checked; its mathematical derivations were not independently revalidated.

**Synthesis:** a revealing example does more than decorate a theory. It lets the reader encounter a difficulty that the theory will resolve. The mathematical machinery then answers a question the reader already understands. The transferable principle is this explanatory progression, not a requirement to begin every article with a visual ambiguity.

### One Main Story Can Have Necessary Subparts

Black advises one main story per paper. Two independent major ideas can compete for attention, leaving readers remembering only one. Subparts are appropriate when they contribute to a coherent central explanation.

**Newsletter application:** apply this at the level of a source or a genuinely related group. An issue covering several fields does not need one unifying story. Do not discard unrelated sources to make the narrative tidier.

## 5. Design the Different Entrances to the Paper

Original sections: *The title*, *The Acronym*, *Teaser*, *Abstract*, *Introduction*.

Readers may encounter the title alone, the abstract and teaser, or the introduction before deciding to continue. Each entrance needs to communicate a meaningful account without making promises that the full work cannot support.

### Title: A Compact Concept, Not Just a Name

Black treats the title as a further compression of the abstract. It should be short, suggestive, and capable of bringing the core concept to mind. Cleverness becomes a problem when it displaces accuracy or makes the work sound like a marketing exercise.

He gives "Towards" as an option for work that begins a direction without claiming to complete it, and "On" for work that establishes a foundation or insight. These are choices for calibrating what the title promises, not an exhaustive classification of papers.

A useful acronym may help readers associate the paper with code or a model. Its expanded words should not be forced into a title that no longer explains the work.

### Abstract: Establish the Need and Make the Reasoning Visible

The [Nature summary-paragraph guide](https://www.nature.com/documents/nature-summary-paragraph.pdf) moves from a broad introduction, through more specific background and the problem, to the main result, its relation to previous knowledge, and a wider context. Its layers acknowledge readers entering from different disciplines. It is a publisher's style guide, not experimental proof of an optimal sentence count.

Black's own fill-in abstract repeatedly connects obstacles and responses. Reconstructed by function rather than copied as a template, it does the following:

1. Establish an important task and the existing approach.
2. Identify a limitation of that approach.
3. Introduce the nugget as a different way to address the limitation.
4. Explain what this resolves and what remains unresolved.
5. Introduce the technical development needed for the remaining problem.
6. Explain any further difficulty and the response to it.
7. Describe qualitative and quantitative evaluation, the comparison, and the observed result.
8. State the availability of code and data.

Black's signposts include "Unfortunately," "In contrast," "Consequently," "While promising," and "Therefore." They matter because they expose whether the account advances logically. A succession of impressive nouns does not. Nevertheless, inserting transition words cannot create a missing relationship, and the example's superior performance must not become an assumption imposed on every paper. Report the actual result, including mixed or negative evidence. Code that is promised, released, or checked by the writer represents three different states.

### Introduction: Explain the Problem in the World

The introduction develops the same explanation at greater depth. Replace a declaration of the authors' interests with an account of why the goal matters and why it remains difficult. The contribution becomes relevant through that account, not through the authors' enthusiasm.

The central ideas, contribution, and significance should be recoverable without making readers assemble them from scattered sections. This is not a reason to replace the argument with a contribution list; the list is useful when it gives readers a clear reference point for the argument.

### Teaser: An Independent Visual Digest

Black distinguishes three useful possibilities: informative results, a problem-and-solution comparison, or a simple system overview. A detailed architecture diagram often presupposes the knowledge the first page is supposed to teach. Use it as an entrance only when it really functions as an easily understood overview.

The abstract and teaser should agree about the core idea. A reader who sees only those two should receive an accurate digest, not a spectacular example detached from the method's actual scope.

### Naming: Meaning, Memory, and Retrieval

Black values short, pronounceable, distinctive acronyms. He calls a good acronym "invertible": it should help the reader infer or remember the words behind it, not merely sound catchy. His examples reveal several separate concerns:

- SMPL expands to Skinned Multi-Person Linear model and reinforces the intended simplicity. Its earlier name, SIMPLE, was hard to retrieve in email because it was a common word.
- MANO draws on the Spanish word for hand. Its expansion is less straightforward, but it is distinctive. The earlier HAND name tried to occupy a generic category that belongs to many models.
- For clothing work, he collects descriptive nouns and verbs, searches combinations of their initials for clothing-related words, and works back toward meaningful expansions. CAPE, WRAP, and ClothE illustrate this exploration.

The underlying method balances semantic association, pronounceability, recoverability, and searchability. A [Scrabble word finder](https://word.tips/scrabble-word-finder/) can assist with combinations; it cannot judge whether a name represents the science. These are naming experiences, not controlled experiments on citation or communication effects.

**Newsletter application:** preserve established names and explain them where helpful. Do not create an acronym, teaser, or publication-style abstract for every report.

## 6. Related Work Should Teach a Way of Thinking

Original sections: *Previous work*, *Bibliography*.

Black considers related work part of a paper's lasting intellectual value. A reader should leave with a way to understand the field, not merely a list of predecessors or a sequence of claims that every predecessor was deficient.

Organize by topics, common assumptions, or related approaches. Each paragraph should explain what earlier work gets right and what it misses. This requires analysis: which problem the methods address, which assumptions they share, and where their differences become consequential. The new work then occupies a precise position in that map.

This is not courtesy added after establishing novelty. Understanding earlier achievements is part of establishing what the new contribution actually is. A distorted account of prior work creates a distorted account of progress.

Black also recommends historical investigation. Follow the chain of reasoning backward rather than relying entirely on recent papers. A claim to be first is poorly supported if the apparent novelty comes from a short reading horizon or a renamed older idea. The phrase "to the best of our knowledge" does not repair inadequate knowledge.

His preference for present tense in this section reflects the view that earlier methods remain available intellectual objects. It is an English style preference, not a rule that historical events must be represented as current events.

**Newsletter application:** grouping should explain relationships. Papers may offer competing solutions, complementary components, alternative assumptions, or answers at different levels of a problem. Numerical comparability is not required for a conceptual comparison, but be explicit about what is being compared.

The skill's three-year limit governs incoming materials, not the age of knowledge needed to explain them. Historical sources can be checked as background. They do not become new items, restore a deleted processing history, or change the source-selected coverage of the current issue.

## 7. Experiments Should Explain What Matters

Original sections: *Experiments*, *Questions to ask before you start*, *Strategy*, *Basics of writing*.

### Test the Simple Alternative Early

Before celebrating a complicated new method, ask whether a simpler method solves the problem. Implementing the baseline early can reveal that the supposed obstacle is not what the researcher thought, or that additional complexity brings little benefit.

A weak comparator makes victory easy but reduces what the experiment teaches. The scientific question is not whether the new system can beat something, but whether the evidence establishes why the proposed advance is needed and what it accomplishes.

### Separate Changes So the Result Is Interpretable

Black strongly advocates changing one thing at a time. Changing both method and data obscures attribution: the score changes, but the reader cannot tell which change mattered. Ablation is useful when it makes the important factors identifiable, rather than simply supplying another table.

**Qualification from experimental-design guidance:** one-factor-at-a-time experiments do not identify interactions between factors. The [NIST discussion](https://www.itl.nist.gov/div898/handbook/pri/section2/pri212.htm) makes this limitation explicit. Preserve Black's demand for interpretable comparisons without adopting his strongest wording as a claim that single-factor changes are the only scientific way forward. An interacting system may require joint or factorial comparisons. An ablation table is not automatic proof of a complete mechanism.

### Compare to Learn, Not to Humiliate

Black's aim for comparison is learning and teaching. Explain what different methods reveal, not just which one wins. His rejection of promotional language about results follows from this: experiments test a hypothesis rather than sell a product.

**Newsletter application:** ask whether comparisons share relevant data, training or tuning budgets, inputs, tasks, metrics, and runtime conditions. Identify what is controlled, what is confounded, and which conclusions the differences permit. These checks apply Black's fairness principle to reporting; they are not a list of measurements he requires every paper to include.

A demonstration can make an idea intuitive. A benchmark can measure performance under a particular protocol. An ablation can isolate a factor under its tested conditions. None should silently substitute for the others.

### Explain the Meaning of the Numbers

Connect results to claims. Which hypothesis does a comparison test? What interpretation does it support? Where does it stop being informative? A table does not relieve the writer of explaining the relationship between evidence and conclusion.

Avoid both overclaiming and underclaiming. State a genuine contribution clearly and at its actual scope. Do not generalize a narrow result into universal superiority, and do not weaken a demonstrated result into an unspecified possibility.

Discuss limitations even when doing so may expose the work to criticism. A practical future direction can explain how a limitation might be addressed, but it does not erase the current limitation. The resulting account should leave the reader knowing both what has become possible and what remains unresolved.

## 8. Coordinate Text, Equations, Figures, and Code

Original sections: *Basics of writing*, *Equations*, *Figures*, *Teaser*.

### Different Representations Do Different Work

Black recommends explaining an important concept through text, an equation, and a figure:

- Text communicates the idea in less technical terms.
- An equation makes the relationship precise.
- A figure supplies intuition.

This is not the same as duplicating paragraphs or repeating a derivation. Different representations offer different routes into a concept. Alternation also gives the paper rhythm and relief from uninterrupted abstraction.

The consistency requirement remains: each route should explain the same method and assumptions. A helpful picture cannot quietly describe a simplified process that contradicts the equation or the implementation.

### Equations Must Describe the Code That Produced the Results

This is one of Black's strongest technical warnings. If the final implementation contains a workaround or an inelegant choice, the paper cannot replace it with a cleaner mathematical story that did not produce the reported results.

Writing equations early gives the team a chance to detect the discrepancy and change the code while new experiments are still possible. Once the experiments are complete, faithfully describing the actual implementation is essential. Improving the stated algorithm without obtaining evidence for that algorithm breaks the connection between method and results.

**Newsletter application:** distinguish a method described by authors from a code-to-equation comparison performed by the writer. Reading the paper alone does not establish that the implementation was independently verified.

### Notation Should Reduce Work for the Reader

Choose distinguishable representations for scalars, vectors, matrices, indices, constants, functions, sets, and parameters. Do not reuse a symbol for unrelated meanings. Otherwise the reader must repeatedly infer which object a statement refers to before they can understand it.

Black suggests maintaining a notation table from the beginning and adding each symbol as it appears. The table exposes inconsistencies before they spread. His bold, italic, and Greek-letter examples are possible conventions, not a universal notation standard; the article's illustrative `\Alpha` should not be copied as though it were a predefined LaTeX command.

For a newsletter, consistent terms and an explanation on first use may be sufficient. There is no requirement to publish a notation appendix for every item.

### Figures Form a Paper Within the Paper

Some readers look mainly at figures and captions. Black asks the writer to make that route genuinely informative: the figures should communicate the key idea and results, not just look impressive.

Create them early. He sketches prospective figures on a whiteboard, photographs them, and inserts placeholders in the draft. Imagining a comparison helps determine which experiments are necessary. Replace the sketches as results become available.

For each figure, check what the reader should look at, what they should learn, what the colors mean, and whether an important detail needs an arrow or circle. Label plot axes and units. Make text readable without zooming. Refer to the figure in the prose and explain its role. Use color to encode information rather than as decoration.

Black attributes some of Sintel's popularity to its attractive imagery. That is his interpretation of a case, not verified evidence that visual beauty caused the dataset's adoption.

**Newsletter application:** use a figure or equation when it materially aids understanding. Do not turn the three-representation recommendation into a requirement to attach both to every short item. Equally, do not remove an essential relationship merely to shorten the prose.

## 9. Make the Prose Say Exactly What Happened

Original sections: *Basics of writing*, *Introduction*, *Strategy*.

### Cut Filler, Not the Explanation

Black's first writing tip is to use fewer words. Tightening an argument often improves it because unnecessary setup and repetition obscure its central relationships. This is a revision method, not an instruction to remove conditions, causal links, or evidence.

Avoid announcing what a section will do when simply doing it is clearer. A short paper rarely needs a paragraph describing its entire section sequence. Black allows an overview when a complicated method genuinely needs one, preferably with a helpful figure. The question is whether the signpost solves a reader's problem.

When text or equations recur because the argument keeps restarting, repair the organization. Do not confuse this with the complementary representations discussed above.

### Identify the Agent of an Action

An automatic procedure should be described as an action of the method, not as though the authors manually perform every step. Distinguish what the researchers did from what the algorithm does. The reader needs to know which operations are implemented, which are human choices, and which are only proposed.

This is a question of semantic accuracy, not a blanket ban on "we" or passive grammatical constructions. A sentence can be active and still hide its mechanism; another can be passive yet clearly identify what happens.

### Replace Vague Capability with Mechanism

Words such as "provides," "enables," and "allows" can leave the explanation unfinished. Ask how the method produces the claimed capability. Black's correction of "allows to" is partly grammatical, but the deeper question is who does what and through which process.

An illustrative example, not a reported research result:

- Vague: "The new module enables efficient inference."
- Mechanistic: "The module caches representations of unchanged regions, so later steps recompute only the regions that changed."

The second sentence explains a computational change. It still does not establish end-to-end speed, which requires an appropriate measurement. Mechanistic precision must not itself become a shortcut to an unsupported outcome claim.

### Be Direct About Completed Work and Specific About Uncertainty

Black objects to describing an accomplished operation as merely something the authors can do or aim to do. If it was done, state it. If it was not done, do not imply otherwise.

This is different from removing genuine uncertainty. An observation, an explanation proposed for it, and a prediction are different claims. Direct prose should make their status clearer, not collapse them into a single confident assertion.

Comparatives need reference points. More accurate than what? More robust under which perturbations? Better on which metric? Terms such as "unique" or "paramount" make exceptionally strong claims; enthusiasm does not supply the needed support. A phrase such as "to that end" also needs a clear antecedent, not just an academic tone.

### Keep Small Conventions Consistent

Black's English-paper preferences include avoiding contractions and exclamation marks, expanding abbreviations on first use, hyphenating compound adjectives appropriately, keeping heading capitalization consistent, and not italicizing `et al.` or `e.g.`. Citation spacing should be deliberate rather than omitted or doubled.

He prefers present tense for methods and continuing knowledge, including related work, while acknowledging that data collection and human participation often require past tense. Preserve the distinction between ongoing descriptions and events that happened. These English preferences do not imply that the Chinese newsletter needs an artificial tense scheme.

### Do Not Confuse Fluent Model Output with Understanding

Black permits model assistance with grammar but warns against handing over the writing. His concern is that fluent sentences can be verbose, imprecise, and empty of the insight the researcher actually has. His objections to terms such as "showcase" also reflect a substantive stance: results evaluate a hypothesis; they are not product advertising.

This newsletter deliberately uses agents, so it cannot honestly claim to follow a prohibition on model-authored prose. The applicable constraint is that the agent must reconstruct the source's reasoning and preserve its evidential limits. Human judgment remains final. Fluency, vocabulary policing, or a high style score cannot replace that work.

## 10. Revise the Argument and Use Collaborators Well

Original sections: *Co-Authors*, *Basics of writing*, *Strategy*, *The final push*, *Conclusions*, *Final thought*.

### Draft Early, Then Improve the Logic

An early draft can be rough. Black explicitly permits writing the introduction before results exist so that the logic becomes visible. Get the argument into a form that can be criticized before spending effort on grammar.

This does not license predetermining the findings. If results contradict the proposed story, revise the story. An early explanation is a tool for research, not a commitment that justifies excluding inconvenient evidence.

Revision should make the paper shorter where that sharpens the reasoning, more explicit where a connection is missing, and more consistent across its parts. Good prose emerges through rewriting rather than through a single polished-sounding generation.

### Use Senior Attention for Senior Judgment

The first author carries the main writing responsibility. Waiting long enough does not make a busy senior coauthor responsible for rescuing the manuscript.

Give collaborators a draft sufficiently developed that they can work on the important issues: the argument, the insight, the position relative to prior work, and whether the evidence is adequate. Making them repair basic copyediting wastes the attention that could improve the substance. This is not a demand to hide uncertainty; bring unresolved substantive questions into view.

### Make Evaluation Easier Without Gaming It

Black recommends understanding the reviewer's job. Reviewers must summarize ideas and experiments, identify significance and strengths, and judge weaknesses in originality, evidence, and presentation.

The paper should make those judgments possible. A three-to-five-sentence summary should be recoverable. Contributions should be clearly located. Explain the meaning of experimental validation rather than expecting the reader to infer it from a table. Establish the actual advance over previous work and be honest about limitations.

Black suggests explicit signposting, including a contributions paragraph and language identifying key ideas and experimental significance. The function is to help a time-constrained reader find the argument; such labels cannot substitute for that argument or make an unsupported claim acceptable.

### At the Deadline, Tell the Story the Evidence Supports

When the ideal paper no longer matches the available results, Black advises accepting what is actually in hand. A smaller, genuine insight may produce a better paper than a grand claim sustained by hope.

Reduce the claim to the supported achievement, not the standard of truthfulness. Do not describe missing results as completed, invent a nugget, or omit contrary evidence to preserve an award-winning story.

### Let the Conclusion Use What the Reader Has Learned

The conclusion revisits the main insight and results, but it can offer more analysis than the abstract because the reader has now seen the evidence. It should not merely repeat an opening promise.

Future work should emerge from specific limitations and plausible ways forward. A long inventory of ambitions can look like an attempt to claim the whole field. A proposed path remains a proposal; it does not resolve the limitation today.

Black's final encouragement to enjoy writing belongs to this method too. Creativity and collaboration are compatible with rigor. The purpose of structure is to communicate an idea, not to turn the work into a ritual.

## 11. Finish the Whole Communication Artifact

Original sections: *The End Game*, *Bibliography*, *Latex things*, *Equations*, *Figures*, *Supplemental material and video*.

### Proofread as a First-Time Reader

Black insists on repeated proofreading by multiple people, including every word of the title, captions, and equations. This requires a sufficiently complete draft before the deadline.

Read as though the acronyms, mathematics, and literature were unfamiliar. The writer's knowledge otherwise fills gaps that remain real gaps for everyone else. Ask what the document itself makes understandable, not what the author can explain after being challenged.

For the newsletter, a focused comprehension pass and a separate return to the sources preserve this distinction without requiring a formal scorecard or an additional agent.

### References Are Part of the Reader's Ability to Check

Check for missing central work, incomplete entries, mistaken metadata, and inappropriate versions. Black prefers the definitive published version when one exists. Complete information, including pages where available, makes the source easier to locate.

Sort numerical citations; `\usepackage[numbers,sort,compress]{natbib}` is his automation example. Protect capitalization in BibTeX with braces such as `{SMPL}` and `{3D}`. Inspect unresolved-reference markers in the compiled PDF rather than assuming the bibliography is correct because the prose is polished.

Do not make a bare citation number the subject of a sentence. Explain which work or idea the citation supports. Black also notes that references may influence reviewer matching. Retain the substantive point, appropriate treatment of prior work, without turning that observation into advice to manipulate assignment.

**Newsletter application:** link both the definitive version and an accessible author version where useful. Do not remove an arXiv or local archive link merely because a formally published version exists. A source must remain usable by the reader.

### Layout Should Serve Readability

Black's LaTeX advice addresses a constrained, often two-column publication format:

- Top or bottom figure placement can avoid the extra whitespace of an in-column float. His examples favor `[t]` or `[tbh]`.
- `\centering` avoids the additional vertical space associated with a `center` environment.
- Excessive negative `\vspace` can make the paper cramped and harder to read.
- Rewriting a paragraph with one or two words stranded on its final line can save space while improving the wording.
- Small edits can move a section heading back to the previous page and remove substantial whitespace; layout changes are not proportional to the number of words cut.
- Treat an equation as part of the sentence, including appropriate commas or periods. Comment-only lines can separate LaTeX source visually without introducing a new paragraph.
- Place a hat over the intended symbol: `\hat{c}_i`, rather than `\hat{c_i}`.
- Keep long equations out of gutters and margins. Move a definition into adjoining prose or use a suitable multiline form. The article's `eqnarray` and `\lefteqn` examples are historical implementations, not a prescribed default for new documents.
- Use proper TeX quotation syntax rather than assuming a straight opening double quote produces the intended typeset quotation mark.

These are tools for making a complete argument fit legibly. They are not a reason to remove essential evidence or evade a venue's formatting rules.

Black also recommends filling the available eight pages, based on his reading of reviewer impressions. Treat this as conference-specific experience, not a general minimum length, a reason to add filler, or a requirement for newsletter output. No PDF or LaTeX publishing stage is introduced by this reference.

### Supplementary Material Must Keep Its Promises

Deliver what the main text promises. Maintain the same professional standard, include failure cases and examples beyond the chosen success, keep the material clear, and tell readers where and why to consult it. Material that is never signposted cannot reliably help the reader.

The blog's warning against new experiments needs a policy-specific reading. The linked [CVPR 2024 reviewer guidelines](https://cvpr.thecvf.com/Conferences/2024/ReviewerGuidelines) allow details and results that do not fit the paper, but prohibit results from an improved method after additional tuning or training, and an updated or corrected submission PDF. That is not a universal prohibition on every additional result. These are historical rules; do not present them as all venues' current policy.

### Use Video as a Different Explanatory Medium

A video is not a paper read aloud or a sequence of paper screenshots. Time can make an idea visible: overlay successive results so differences become perceptible, animate a conceptual change, or introduce comparisons progressively rather than displaying everything at once.

Black recommends planning early, writing a narration script, recording sentences separately for easier editing, and checking playback on different machines. He favors narration over forcing viewers to read extensive on-screen text and suggests a short target, under four minutes, while recognizing exceptions.

He praises the [mip-NeRF video](https://jonbarron.info/mipnerf/) for teaching the idea through motion rather than reproducing the paper's structure, particularly around 5:42 and 6:11. Those timestamp judgments come from Black; the project page and its dynamic explanation were checked, but the video segments were not independently reviewed. His praised example also exceeds his proposed length, showing that the intended purpose matters more than literal obedience to the heuristic.

**Newsletter application:** preserve the explanatory benefit of a demonstration when relevant, but do not require a video, teaser, supplement, or typeset layout for each source.

## 12. Apply the Method to This Newsletter

This section is a project-specific application, not an additional section of Black's article.

### Recover an Explanation, Not a Better-Sounding Abstract

For a research source, the writer should be able to explain the connected relationships:

- What outcome matters, and what actually obstructs it?
- What changes in the authors' understanding or formulation?
- How does that change lead to the technical design?
- Which evidence supports the result, and which evidence supports the proposed explanation?
- What should a reader now believe, consider, or investigate, and what remains unestablished?

The final prose need not expose these questions as headings. A fixed four-sentence template can hide a missing mechanism just as easily as an abstract can. Write enough to make the important relationships understandable.

For a blog or announcement, examine the stated reasons, examples, observations, and argument. Do not fabricate experimental evidence or turn a practitioner's experience into a universal finding.

### Full Coverage and Coherent Organization Are Compatible

The configured sources determine the incoming materials. The processing state determines which have already been completed. The local material archive is a download cache, not an alternative source-selection policy.

Every eligible, source-selected pending item must receive substantive treatment, or a clearly identified access gap if its original cannot be verified. Interest, popularity, institutional prestige, and narrative convenience are not grounds for exclusion. Different length is acceptable; silently dropping an item or reducing it to a bare title and link is not.

Organize by domain and then by an actual problem where useful. Show relationships among papers only when supported. An unrelated item can have its own section. Black's one-main-story advice applies within a source or a coherent group, not as a demand to force the entire issue into one theme.

Necessary historical context can clarify the current materials without changing this coverage. Mark it as background and do not treat it as a new feed item.

### Keep Three Kinds of Insight Distinct

- **The authors' insight:** supported by and attributed to the original source.
- **The newsletter's synthesis:** a relationship inferred across sources, with its basis made clear.
- **The newsletter's interpretation of implications:** an explicitly conditional analysis, not a demonstrated result.

An insightful article does not acquire depth by adding a final sentence saying the work is important. Depth comes from explaining a consequential relationship: why an assumption limits a method, why a representation changes the problem, why a comparison supports only a local conclusion, or why two approaches complement one another.

Such explanation remains accountable to the sources. When the relationship is absent or uncertain, say so rather than manufacturing a conceptual breakthrough.

### Improve Understanding Without Losing Faithfulness

Use [writing-guide.md](writing-guide.md) for the concise reporting constraints and empirical qualifications. Its principles operate at different levels:

- Goal, Problem, and Solution explain why a response is needed.
- The nugget distinguishes the underlying insight from the implemented contribution.
- Given-to-new organization helps readers track a sentence or paragraph.
- Evidence checking constrains what the resulting explanation can claim.

Do not collapse these into a universal template. Remove jargon density, filler, and unnecessary syntactic burden, not the logic the reader needs. A text that feels clear can still be misleading or poorly understood.

The reference documents are in English; the newsletter remains in simplified Chinese with English halfwidth punctuation. Continue to produce Markdown with original web links and usable local archive links. This method does not add scheduling, email delivery, a rendering stage, or mandatory intermediate artifacts.

## 13. Source Coverage and Verification Boundaries

### Coverage of the Original Article

| Original sections | Treatment in this reference |
| --- | --- |
| Preface; Introduction | Community and experience, lasting usefulness, reading good papers, talks, examples, first impressions |
| The biggest mistake in paper writing; Conferences do not accept results. They accept papers. | Writing effort and its feedback into research |
| Questions to ask before you start | Goal, audience, hypothesis, impediment, nugget, pitch, teaser, previous work, evaluation, demo, risks, data |
| How to tell a story: Goal, Problem, Solution; The Nugget | Recursive teaching structure, insight versus contribution, optical flow, jointly solving difficulties |
| The title; The Acronym; Teaser; Abstract; Introduction | Conceptual entrances, naming and retrieval, visual digest, obstacle-response reasoning, reader-centered motivation |
| Previous work; Experiments | Thematic and historical explanation, simple baselines, attribution, fair comparison |
| Equations; Figures | Code consistency, notation, punctuation, early visual planning, a standalone visual argument |
| Co-Authors; Basics of writing; Strategy | Author responsibility, early drafts, precise prose, reviewer tasks, calibrated claims, limitations |
| The final push; Conclusions | Supported scope, insight and analysis after evidence, bounded future work |
| The End Game; Bibliography; Latex things | Fresh-reader proofreading, reference completeness, typesetting and space constraints |
| Supplemental material and video; Final thought | Promises, policies, failures, medium-specific explanation, creativity and collaboration |

### References and What Was Actually Checked

| Source | Verification scope and purpose |
| --- | --- |
| [Black's Medium article](https://medium.com/@black_51980/writing-a-good-scientific-paper-c0f8af480c91) | Main article read from the supplied complete local HTML, excluding Medium recommendations and subscription inserts; embedded equation examples were inspected in the earlier pass |
| [Freeman, The Generic Viewpoint Assumption in a Bayesian Framework](https://merl.com/publications/docs/TR93-11a.pdf) | Example, Figure 3 caption, and associated explanation checked; not an independent validation of the derivations. The PDF contains several printing and version dates, so the report identifier is not treated as a unique publication date |
| [Black and Anandan, ICCV 1993](https://files.is.tue.mpg.de/black/papers/iccv93.pdf), with [Brown scan](https://cs.brown.edu/research/pubs/pdfs/1993/Black-1993-FRE.pdf) | Earlier check of title, year, abstract, and introduction using the scan because extraction from the original was garbled; mirror unavailable on this rewrite's retry; no experiment reproduced |
| [Black and Rangarajan, IJCV 1996](https://is.mpg.de/publications/black-ijcv-1996) | Earlier check of the institute's publication metadata and abstract for the title example; not a full-paper reading. The former domain in the blog and a direct retry of the current page were inaccessible |
| [Nature summary-paragraph guide](https://www.nature.com/documents/nature-summary-paragraph.pdf) | Full one-page publisher guide checked for background layers, main result, previous knowledge, and wider context |
| [CVPR 2024 reviewer guidelines](https://cvpr.thecvf.com/Conferences/2024/ReviewerGuidelines) | Historical evaluation guidance and supplementary-material distinction checked; not a statement of current rules at every conference |
| [mip-NeRF project](https://jonbarron.info/mipnerf/) | Project page and dynamic conceptual explanation checked; timestamp-specific video assessments remain Black's |
| [NIST, One variable at a time](https://www.itl.nist.gov/div898/handbook/pri/section2/pri212.htm) | Additional source, not a link in Black's article; used only to qualify claims about single-factor experiments and interactions |

Author and adviser homepages, the Scrabble helper, and Sintel serve biographical, naming, or illustrative roles in the article. They were not treated as independent evidence that a writing intervention improves comprehension. The broader science-communication studies and their limits are documented in [writing-guide.md](writing-guide.md).
