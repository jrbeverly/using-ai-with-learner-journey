# Learner Journey

## Vision

Explore whether a small, curated body of technical knowledge can be combined with targeted AI instructions to create a useful guided learning experience.

The idea is to treat AI as an interactive learning companion around intentionally prepared material rather than as the sole source of instruction.

A learner should be able to move through a subject using a mixture of:

- written material;
- diagrams;
- videos;
- recordings;
- audio;
- examples;
- and AI interaction.

The AI should help explain, connect, reinforce, and explore the material as the learner progresses.

The purpose of this work is not to build a complete learning-management platform or a production educational product.

It is a paper prototype intended to test whether relatively simple combinations of knowledge corpora and agent instructions can create meaningfully better technical learning experiences.

## Initial Subject

Use a bounded technical topic as the first experiment.

One suitable example is private networking and mutual TLS in AWS, potentially including related concepts such as:

- private network connectivity;
- VPC networking;
- routing;
- VPNs;
- certificates;
- TLS;
- mutual TLS;
- trust relationships;
- private service communication;
- and the interactions between these concepts.

The exact subject matter is not particularly important to the architecture.

The subject simply needs to be complex enough that a learner benefits from explanations, questions, examples, and relationships between concepts.

## Knowledge Corpus

Create a small corpus containing the technical information the learner should work from.

The corpus does not need to follow one rigid format.

It may contain:

- Markdown documents;
- technical notes;
- reference material;
- diagrams;
- architecture examples;
- transcripts;
- links;
- recordings;
- videos;
- or other useful learning material.

The initial goal is not to create a polished textbook.

The goal is to establish a bounded body of knowledge against which the AI can operate.

That distinction is important.

Instead of giving an agent a broad instruction such as:

> teach me AWS networking

the experiment should allow the agent to operate against something closer to:

> here is the material for this learning journey; help the learner understand it.

## Learning Structure

Organize the corpus into a simple sequence of learning areas or modules.

The structure should reflect conceptual dependencies.

For example, a learner may need to understand basic private networking before discussing VPN connectivity, and may need to understand ordinary TLS before mutual TLS becomes useful.

A possible structure might resemble:

> networking foundations
> → private connectivity
> → VPNs and routing
> → TLS foundations
> → certificates and trust
> → mutual TLS
> → combined architecture

This is only an example.

The learning structure should emerge from the chosen subject.

The important property is that the learner has a reasonable progression rather than being presented with an unordered collection of documents.

## AI as a Learning Companion

The AI should operate as an interactive layer around the learning material.

Its purpose is not merely to summarize documents.

It should be capable of helping a learner with tasks such as:

- explaining a concept in another way;
- answering questions;
- connecting one concept to an earlier concept;
- walking through an example;
- explaining why an architecture behaves the way it does;
- identifying missing prerequisite knowledge;
- comparing related concepts;
- helping reason through a hypothetical scenario;
- checking understanding;
- and clarifying terminology.

The learner should be able to move between static material and conversation naturally.

Conceptually:

> consume material → ask questions → explore concept → continue material

The AI fills the gap between authored content and the learner's individual areas of confusion or curiosity.

## Agent Instructions

Create a series of prompts or agent instruction files that tune AI behaviour for different parts of the learner journey.

The goal is to explore how much useful educational behaviour can be produced through relatively small instructions.

For example, different agents or instruction sets might focus on:

- foundational explanation;
- architecture walkthroughs;
- questioning and knowledge checks;
- troubleshooting examples;
- conceptual comparison;
- or a particular learning module.

There is no requirement that each module have a completely separate agent.

The implementation should experiment with whatever arrangement makes the learning behaviours easy to test.

The interesting question is:

> how much does deliberate agent instruction improve the learning experience compared with using a general-purpose assistant?

## Course Helper Modules

Treat the agent instructions as something similar to course helper modules.

Each helper can understand:

- the relevant corpus;
- where the learner is in the journey;
- what concepts have already been introduced;
- what assumptions it may safely make;
- and what kind of assistance it is expected to provide.

For example, an mTLS helper should not necessarily begin every explanation from the basics of IP networking if those concepts belong to earlier modules.

Similarly, an introductory networking helper should avoid unnecessarily introducing advanced concepts that belong later in the learning path.

The project should explore whether this contextual specialization creates a more coherent educational experience.

## Grounding

Where practical, keep the agents grounded in the supplied corpus.

The learner should be able to distinguish between:

- information explicitly represented in the learning material;
- explanations or deductions based on that material;
- and broader information supplied from the model's general knowledge.

This is particularly useful when the corpus describes an opinionated architecture or intentionally simplified model.

The AI should not casually replace the intended course material with a different architecture simply because another approach also exists.

At the same time, grounding should not make the agent incapable of explaining concepts naturally.

The project should explore that balance.

## Adaptive Explanation

One useful property of AI-based learning is that explanations do not need to be identical for every learner.

The system should explore interactions such as:

- "explain that more simply";
- "give me a concrete example";
- "show me how these two concepts relate";
- "why wouldn't we use the other approach?";
- "walk through the request flow";
- "what would fail if this certificate expired?";
- or "I understand VPNs but not where mTLS fits."

The agent should be able to adapt the explanation while remaining anchored to the intended learning objectives.

This adaptive layer is one of the primary capabilities being tested.

## Knowledge Checks

Experiment with using AI to help the learner determine whether they actually understand a concept.

This might include:

- short questions;
- scenario-based questions;
- asking the learner to explain something back;
- architecture reasoning;
- identifying incorrect assumptions;
- or working through a failure scenario.

Avoid turning this immediately into a formal grading system.

The first question is whether conversational checks improve understanding and expose gaps that passive reading would not.

## Multiple Media

The learner journey does not need to be text-only.

A module might contain:

- a concise written explanation;
- an architecture diagram;
- a short recording;
- a video walkthrough;
- or another medium that suits the subject.

The AI should then provide the interactive layer around those materials.

For example:

> watch architecture walkthrough
> → ask AI about one connection
> → inspect diagram
> → ask AI to trace a request through it
> → continue to next module

The project should not require every medium to be used.

The point is to avoid treating chatbot conversation as the only possible learning interface.

## Learner State

Some awareness of the learner's current position may be useful.

This could be very simple.

For example, the agent might know:

- which module is currently being studied;
- which concepts have already been introduced;
- what the learner has recently asked about;
- and which concepts appear to remain unclear.

Do not build a sophisticated learner-profile system before proving that this information materially improves the experience.

A lightweight representation is enough for the initial experiment.

## Prompt Tuning

The prompts themselves are a central artefact of this project.

Experiment with instructions affecting behaviours such as:

- how concise explanations should be;
- how much prerequisite knowledge to assume;
- when to provide examples;
- when to ask the learner a question;
- whether to introduce terminology before or after an intuitive explanation;
- how strongly to stay within the corpus;
- how to handle incorrect learner assumptions;
- and how to respond when the learner wants greater depth.

The goal is to identify patterns that produce a useful educational interaction without requiring a highly complex orchestration system.

## Questions

The project should help answer questions such as:

- Does a curated corpus improve AI teaching compared with an unconstrained general-purpose model?
- How much material is required before grounding becomes useful?
- Does dividing a subject into modules improve explanation quality?
- Are specialized course-helper instructions materially better than one general instruction set?
- How much learner state needs to be retained?
- Can AI reliably distinguish between concepts that have already been introduced and concepts that belong later?
- Which prompt patterns produce useful explanations without excessive verbosity?
- Can the AI expose misunderstandings effectively?
- Are AI-generated knowledge checks useful?
- How well does the experience work when documents, diagrams, video, and audio are mixed?
- Does the learner still benefit from a deliberate course sequence when they can ask arbitrary questions?
- How strongly should the AI remain constrained to the corpus?
- What happens when the learner asks questions outside the prepared material?
- Which parts of the experience need intentionally authored content, and which can reasonably be delegated to AI?

These questions should guide experimentation rather than define a fixed product design.

## Boundaries

Do not build a complete learning platform.

The initial project does not need:

- user accounts;
- formal grading;
- certificates;
- sophisticated progress tracking;
- course marketplaces;
- large-scale content management;
- analytics;
- extensive personalization;
- or production-grade educational infrastructure.

Likewise, do not attempt to create a massive knowledge corpus.

A small, carefully bounded subject is preferable because it makes the effects of the agent instructions easier to observe.

The purpose is to test the learning model:

> curated knowledge + learning sequence + AI interaction

Everything else is secondary.

## Expected Output

The repository should contain enough material to demonstrate an end-to-end learner journey.

Useful outputs may include:

- a small technical knowledge corpus;
- a sequence of learning modules;
- supporting diagrams or other media;
- several agent instruction files;
- example learner interactions;
- knowledge-check experiments;
- and notes comparing different prompt or agent behaviours.

The repository should make it possible to run through the journey as a learner and evaluate whether the AI layer meaningfully improves the experience.

## Success

The project is successful if a learner can use a relatively small set of curated material and AI helpers to develop a coherent understanding of a technical subject.

The strongest result would demonstrate that:

- the authored material provides direction and authoritative context;
- the AI provides useful adaptive explanation;
- learners can explore questions without losing the intended learning structure;
- different agent instructions materially influence educational quality;
- and the combination is more useful than either static documentation or an unconstrained chatbot by itself.

The central question is:

> Can a small corpus of intentionally structured knowledge, combined with tuned AI course helpers, create a practical and reusable technical learner journey?

The paper prototype should explore that question far enough to determine which parts of the approach are worth developing further.
