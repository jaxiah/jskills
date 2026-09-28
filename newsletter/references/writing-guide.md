# Research Newsletter Writing Guide

Goal: help a technically literate reader understand **what changed, why it matters, how it works, and what the evidence warrants**, with as little unnecessary effort as possible. This is a reporting guide, not a required set of visible headings or intermediate documents.

Read [Michael Black's scientific writing method](michael-black-writing-methodology.md) for the reasoning and examples behind the insight, argument, and evidence distinctions. Black's account is practitioner guidance; the research below qualifies specific communication choices rather than certifying his entire method. Conference submission, LaTeX, and video advice do not become newsletter requirements.

These references are in English. The deliverable remains simplified Chinese Markdown with English halfwidth punctuation, original source links, and usable local archive links.

## Coverage and Source Fidelity

- Cover every eligible, source-selected pending item. Reader interest is the reader's decision. Popularity, institutional prestige, and an attractive abstract establish neither importance nor a reason to omit an item.
- Give each item substantive treatment. Identify its problem, actual contribution, strongest available evidence, and limits. Different items may need different lengths; a bare title and link is not coverage. Explicitly identify inaccessible originals and the resulting gaps rather than claiming they were verified.
- Recover the source's account before improving its presentation. Distinguish research evidence, implementation releases, company announcements, practitioner experience, and predictions. Do not invent a hypothesis, insight, experiment, or novelty claim to make a source fit the guide.

## Explanation and Insight

- Establish relevance through a concrete problem or use, not adjectives. Connect **Why / What / Evidence / So what**: why the problem matters, what changed, what supports it, and what a reader can reasonably conclude. Include negative or mixed findings when they change that conclusion.
- Separate the obstacle, the nugget, and the technical contribution. A new module is not itself an explanation. Where the source supports one, explain how a changed assumption or formulation motivates the design and how the design relates to the result.
- Use **Goal -> Problem -> Solution** to make the need for a solution apparent. A small revealing example can establish the difficulty. Introduce technical details when readers have the prerequisites to understand their purpose; do not follow the researchers' chronology or invent obstacles for narrative effect.
- Attribute the authors' insight to them. Identify cross-source synthesis and conditional implications as the newsletter's analysis. If no conceptual insight is established, describe the actual contribution without manufacturing a breakthrough.

## Organization and Reader Effort

- State the sources, temporal scope, and completed coverage near the beginning; identify incomplete coverage clearly. Organize by domain or research problem. Keep unrelated materials separate instead of forcing a single trend or using one-main-story advice to discard items.
- Explain whether related works compete, complement one another, share an assumption, or address different bottlenecks. Compare numerical results directly only when tasks, data, metrics, baselines, and relevant operating conditions justify it. Non-comparable numbers can still support a carefully bounded conceptual discussion.
- Use familiar information to link backward and establish the next sentence's topic. Put the new information that deserves emphasis at a natural point of closure. **Given -> New** is a reader-expectation principle, not a rule that all old information must precede all new information. Repair unexplained topic shifts rather than sprinkling in transition words.
- Keep necessary terms and explain unfamiliar ones on first use. Avoid stacks of jargon and unnecessary syntactic interruptions. Naming a concept and supplying a definition does not necessarily explain its role; show the relationship the reader needs. Do not replace precise differences with "faster" or "better."
- Prefer concrete subjects, actions, and mechanisms to unspecified capability claims such as "enables" or promotional accounts of results. Cut filler without cutting conditions or reasoning. Use text, figures, or equations according to explanatory need, not as a required trio for every item. Do not mechanically reproduce an abstract or a fixed four-sentence pattern.

## Evidence and Claim Strength

- Put the metric, direction, comparator, relevant setting, and boundary next to an important result. Distinguish observed outcomes from proposed explanations, author-reported results from independent verification, and promised availability from an actual release.
- Ask what a comparison tests, not just which score wins. Check simple alternatives, fairness, and confounded changes. Single-factor ablations do not rule out interactions or establish every mechanism. Without inspecting the implementation, do not claim that code and equations were independently checked.
- Link the original near the supported statement. Preserve uncertainty and specify its cause. Do not generalize a single benchmark into overall superiority, latency into monetary savings, or a plausible mechanism into a measured benefit. State genuine achievements directly without inflating them.

## Comprehension and Verification

- Reconcile the draft with the pending list: every item needs substantive discussion or an explicit access gap. No silent omissions or interest-based completion decisions.
- On a separate pass, use only the draft to answer: what is the problem, contribution, and underlying insight if one exists? How does the method relate to the result? Which evidence supports which claim? What is author assertion, what is newsletter interpretation, and what remains unresolved? Missing answers require better explanation, not cosmetic polish.
- Return to the originals to check those answers, including dates, methods, numbers, baselines, and scope. Reader comprehension and source fidelity are different checks. Fluency scores cannot substitute for either. One agent can perform both passes; no extra agent, scored rubric, or saved process artifact is required.

## Research Basis and Limits

The reporting constraints above combine project requirements, practitioner guidance, and research-informed choices. They are not an experimentally validated package or a universal optimum.

- **Synthesis and comparability:** [Cochrane Handbook, Chapter 12](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-12) discusses presenting and synthesizing findings when meta-analysis is unsuitable. Borrow explicit grouping and attention to incompatible evidence; do not label this source-bounded newsletter a comprehensive systematic review.
- **Reader expectations:** [Gopen and Swan, The Science of Scientific Writing](https://www.cs.tufts.edu/comp/150FP/archive/george-gopen/sci.html) connects topic positions, emphasis at closure, and proximity of subjects to verbs with readers' interpretation. It explicitly presents principles rather than absolute rules; passive voice can be appropriate when it preserves the topic. This is explanatory writing guidance, not a controlled trial of Given -> New.
- **Background knowledge and coherence:** [McNamara et al., Are Good Texts Always Better?](https://www.tandfonline.com/doi/abs/10.1207/s1532690xci1401_1) reports interactions among coherence, prior knowledge, and the level of understanding measured in science-text experiments. Readers with little domain knowledge benefited from coherence; knowledgeable readers sometimes benefited from inference-demanding text. Use this to calibrate explanation, not to deliberately obscure the newsletter or claim that maximal explicitness is always optimal.
- **Jargon and engagement:** [Shulman et al., The Effects of Jargon on Processing Fluency, Self-Perceptions, and Scientific Engagement](https://journals.sagepub.com/doi/full/10.1177/0261927X20902177) found effects on processing fluency and self-reported scientific engagement, even with definitions available. This supports avoiding unnecessary terminology; it does not establish that removing all technical vocabulary maximizes actual comprehension.
- **Limits of plain-language prescriptions:** [Stoll et al., Plain language summaries: A systematic review of theory, guidelines and empirical research](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0268789) finds that empirical evaluation covers only part of the many guideline criteria, with heterogeneous studies and outcomes. Treat concise style rules as useful, qualified tools rather than guarantees of understanding.
- **Uncertainty communication:** [van der Bles et al., The effects of communicating uncertainty on public trust in facts and numbers](https://pmc.ncbi.nlm.nih.gov/articles/PMC7149229/) found that numerical ranges around estimates did not substantially reduce trust in the studied settings, while verbal uncertainty had different effects. The study concerns particular facts, formats, and audiences; it does not prove that every caveat improves trust. Do not conceal real uncertainty to sound decisive or invent intervals absent from the evidence.
- **Perceived clarity versus comprehension:** [Guo et al., Are LLM-generated plain language summaries truly understandable?](https://www.sciencedirect.com/science/article/pii/S1532046426000626) reports that similar perceived clarity of LLM and human health summaries coexisted with better comprehension-question performance for human summaries. The accessible publisher abstract supports this distinction; it is not a universal finding about all models or technical newsletters.
- **Source-grounded questions:** [QAFactEval](https://aclanthology.org/2022.naacl-main.187/) studies question-answering-based factual-consistency evaluation and emphasizes component choices such as question generation and answerability. Borrow the idea of checking whether claims yield source-supported answers. A manual comprehension pass is not the QAFactEval metric and does not inherit its benchmark performance.
