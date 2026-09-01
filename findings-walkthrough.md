# Findings — end-to-end walkthrough and success review

One learner, the whole journey: all seven modules in order, the material
(documents and the diagrams), every helper, and a learner-state file that
evolves across the journey, recorded in one transcript
(`transcripts/walkthrough.md`). This note applies the pre-committed success
criteria to all recorded evidence — the round-1 and round-2 transcripts plus
the walkthrough — and answers the question list in `VISION.md`.

## Walkthrough run conditions

Fifteen runs appended to one transcript, in journey order. Each run is one
replay conversation (helper + module), so a turn's helper, module, learner
state, model settings, and timestamp are recorded per turn by the runner:

| Segment | Helper | Module | Turns | Config |
|---|---|---|---|---|
| 00-control | control-assistant | 01 | 2 | 1024, no state |
| 01-smoke | smoke-tutor | 01 | 4 | 8192, state |
| 01-check | knowledge-check | 01 | 5 | 1024, state |
| 02-tutor | grounded-tutor | 02 | 4 | 8192, state |
| 02-check | knowledge-check | 02 | 6 | 1024, state |
| 03-tutor | grounded-tutor | 03 | 4 | 8192, state |
| 03-check | knowledge-check | 03 | 6 | 1024, state |
| 04-tutor | grounded-tutor | 04 | 4 | 8192, state |
| 04-check | knowledge-check | 04 | 7 | 1024, state |
| 05-tutor | grounded-tutor | 05 | 4 | 8192, state |
| 05-check | knowledge-check | 05 | 7 | 1024, state |
| 06-tutor | mtls-tutor | 06 | 4 | 8192, state |
| 06-check | knowledge-check | 06 | 7 | 1024, state |
| 07-tutor | architecture-tutor | 07 | 4 | 8192, state |
| 07-check | knowledge-check | 07 | 5 | 1024, state |

73 turns total, run window 2026-09-28T19:38:15Z–19:47:48Z (per-turn
timestamps). Model `deepseek-v4-pro[1m]` at
`https://api.deepseek.com/anthropic`, no temperature — the same settings as
every prior run; the two configs (`runner-config.json`, 1024, and
`probe-run-config.json`, 8192) are byte-identical to round 1's recorded
hashes, and `runner.py` is unchanged (sha256
`66635965c24a06caef51c88baa09f51ed7636d0ea21c5a1e0a89ceba3200fe6c`, matching
round 1's record). Every helper file in `helpers/` appears; the learner turns
reference specific module sections and diagram elements, so material
consumption is visible in the transcript, not just asserted.

Learner state: `walkthrough-state.md`, rewritten at each module boundary by
`run-walkthrough.sh` (stages S1–S8 are the script's `state_s*` functions; the
file on disk holds the final stage). Every tutor and check run records
"Learner state: present (walkthrough-state.md)".

Replays: `examples/replay-walkthrough-*.txt` (15 files, hashes in the
appendix). The learner is a scripted replay of a realistic journey, as the
issue allows.

### Fixes made while running the walkthrough, and their effect on recorded evidence

- Budget: the first attempt of the 01-smoke segment ran at the runner's
  shared default (`max_tokens=1024`) and failed all three attempts on the
  diagram-trace turn — each reply a thinking block only, no text (the failure
  mode round 1 recorded for walk-through probes). Failed logs are kept:
  `runs/walkthrough-01-smoke.attempt-1-failed.log` through
  `attempt-3-failed.log`. Following round 1's own resolution, the seven tutor
  segments run at 8192 via `probe-run-config.json`; the check segments and the
  control segment stay at the shared default, like round 2's check sessions.
  The choice is recorded in every run header of the transcript. Effect on
  already-recorded evidence: none — no comparison or experiment transcript
  was re-run or modified; the walkthrough is new evidence and each of its
  sections records its own settings.
- Scripting: while wiring the final learner-state write into the script, the
  07-check segment was re-run once; all three attempts of that re-run failed
  with the same thinking-only replies (the 1024 budget wall on the Module 7
  closing turn — the behaviour round 2 recorded on Modules 5 and 6). The
  recorded session in `transcripts/walkthrough.md` is the original run (header
  2026-09-28T19:47:16Z, before the re-run); the failed logs are kept
  (`runs/walkthrough-07-check.attempt-1-failed.log` through
  `attempt-3-failed.log`). The final state write is now the script's
  `finalize` step, which makes no model call.
- Also recorded, not fixed: the control segment's first reply ends mid-list
  ("…S3 or Dynam"), truncated by the 1024 budget — the control arm's
  essay-length answer does not fit the default budget, while every grounded
  answer in the same transcript fits.

## Success criteria (pre-committed, unchanged by this review)

### 1. Completion — pass

The walkthrough reaches the end of the sequence: the transcript's last
section is the Module 7 knowledge check, which closes with the suggested
final learner-state record ("Record in your learner state: - Where TLS ends
between ALB and instance — the path and trust boundaries were right, but the
ALB-to-instance hop being plain HTTP was not stated."). Per module, each
check either passes or correctly identifies the gap:

- M1 check: closing note "Solid: NAT reply translation, route tables and the
  default route, and the purpose of private address ranges. Nothing to record
  as unclear." — and it resolved the state file's unclear NAT concept
  ("NAT reply translation no longer looked unclear").
- M2 check: "Nothing from this check needs to go in your learner state as
  unclear".
- M3 check: "Everything you explained matched the module, so I have nothing
  new to suggest recording as unclear."
- M4 check: the planted slip (stream encrypted with the server's public key)
  is named in turn 3 ("There's a gap here. The server's public key is not
  what encrypts the stream.") and the correction is accepted in turn 4
  ("Yes, that's correct").
- M5 check: the planted slip (CRLs check CA trust) is named in turn 4 ("One
  correction: revocation is not about whether the CA is still trusted") and
  accepted in turn 5; the closing note: "The only wobble was revocation — you
  corrected it cleanly."
- M6 check: the planted verify/passthrough swap is named in turn 5 ("You've
  swapped the two names.") and the correction accepted in turn 6.
- M7 check: the check itself identifies the gap the learner's trace missed
  (the ALB-to-instance hop is plain HTTP, not TLS) and suggests recording it.

### 2. Anchoring — fail (strict reading of the criterion)

The criterion demands zero mismatches between marks and corpus text across
all comparison and experiment transcripts. Round 1 recorded one derived
mismatch, verified here directly in the transcript, not only in the findings
note: `transcripts/probes-m02-grounded-tutor.md` line 113, probe 2.5 —
"Connecting two VPCs together belongs to a later part of the journey, so
I'll stay with the current module `[derived]`." The supplied Module 2 corpus
does not state that VPC-to-VPC connection is covered later in the course
(and no later module covers it), so the claim needs course-structure
knowledge the corpus does not contain — a derived mismatch under the rubric.
One of 229 mark-bearing claims in round 1 fails; everything else is clean:
0 module mismatches and 0 general mismatches in round 1, and round 2's
specialization transcripts (149 mark occurrences) add none. The round-1
unmarked substantive claim (`transcripts/probes-m05-grounded-tutor.md` line
24, "That alone does not tell the client *who* the peer is; anyone can
generate a key pair.") is a missing mark, not a mismatched mark, so it does
not decide this criterion. The walkthrough adds one further mark anomaly,
recorded below. Verdict: fail — zero was required, one was found; the
failure is a single derived mismatch, and everything else the criterion
describes holds.

### 3. Differentiation — pass

The scoping line shows an observable count difference between the arms:
control L=2, E=10 versus grounded L=0, E=0 across round 1's 35 probes
(`findings.md`, recomputable from the per-item lists there). Spot-verified
here in the transcripts: `probes-m02-control-assistant.md` line 46
("Module 1's idea is **private IP addresses** — ranges like `10.x.x.x`…"),
`probes-m03-control-assistant.md` line 22 (RFC 1918 and VPC re-taught),
`probes-m05-control-assistant.md` line 37 ("`CertificateVerify` is a
signature the peer can only make with that private key" — a Module 6 concept
introduced in Module 5), `probes-m07-control-assistant.md` line 176 ("The
security group is stateful…" — a Module 2 concept). The grounded arm's 0/0
on the same probes is visible in the paired transcripts.

### 4. Misunderstanding exposure — pass

`transcripts/check-m06-planted.md` turn 2: the learner states the
certificate roles swapped as fact, never announcing the confusion; the
helper names the mix-up ("the certificate is named for who *holds* it, not
who receives it") and re-asks in smaller form; turn 3 corrects side by side
("Still swapped, so let's put the two sides side by side"). The correct-
answers session recorded zero false alarms (`transcripts/check-m06-correct.md`).
The walkthrough adds three more surfacing events in one journey: the M4
session-key slip, the M5 CRL slip, and the M6 verify/passthrough swap, each
named and re-asked, with no false alarm on the clean answers in the same
sessions.

### 5. Boundedness — pass

Corpus within budget: `modules/` totals 3,884 words (`wc -w`), under the
4,000-word budget the README records. No production infrastructure: the five
experiment commits (`f7dff43..HEAD`) touch nothing outside
`ai-driven-learning/using-ai-with-learner-journey/` — no `.gitea`, `docs`,
or shared code — and this review's working tree is confined to the same
directory. Every walkthrough artifact (replays, `run-walkthrough.sh`,
`walkthrough-state.md`, `transcripts/walkthrough.md`, `runs/walkthrough-*.log`)
lives inside that directory.

## Walkthrough mark check (new evidence, counted separately)

The walkthrough's grounded answers carry 134 `[module]`, 43 `[derived]`, and
4 `[general]` canonical marks. The helpers also invented annotation variants
the rubric does not define: `[derived from diagram]` (4, architecture tutor),
`[module, inferred from the diagram]` (1, smoke tutor), and inline
justification forms `[derived: …]` / `[derived — …]` (2). The annotated forms
remain judgeable under the rubric's rules, but they complicate mechanical
counting. One candidate module mismatch: the 01-smoke turn-3 claim that
router B treats `10.0.2.0/24` as local is marked
"[module, inferred from the diagram]" while the corpus gives only router A's
table — an inference, so `[derived]` under the rubric. The annotation flags
the inference, but the mark is the wrong one. All other marked claims in the
15 sections check out under the same one-step rule rounds 1-2 used.

## VISION question list

Answers as far as the recorded evidence supports; unanswered questions are
named explicitly.

1. *Does a curated corpus improve AI teaching compared with an unconstrained
   general-purpose model?* — Yes, on the dimensions measured: the grounded
   arm never re-taught earlier concepts (E=0) or introduced later ones (L=0)
   across 41 probes while the control arm did both (E=10, L=2), and on all 7
   out-of-corpus probes the grounded arm declared the question outside the
   module while the control arm never did (0/7). The walkthrough adds the
   budget contrast: the control arm's big-picture answer truncates at the
   1024 default while grounded answers fit.
2. *How much material is required before grounding becomes useful?* —
   Partially answered. Grounding held up on a corpus of ~550 words per module
   (3,884 total). The single anchoring failure (probe 2.5) came not from too
   little material but from material the corpus lacked — course structure —
   which the tutor then invented. The minimum size is not tested (no smaller
   corpus variant exists).
3. *Does dividing a subject into modules improve explanation quality?* —
   Not directly answered; no unmodular control exists. What is shown: the
   module metadata's concept lists are what the scoping rubric and the
   helpers run on, and the sequence worked end to end in the walkthrough.
4. *Are specialized course-helper instructions materially better than one
   general instruction set?* — No, on this probe set: on modules 6 and 7 the
   specialized helpers and the grounded tutor behave identically probe for
   probe (round 2), and the walkthrough's specialized segments are
   indistinguishable in quality from the general ones.
5. *How much learner state needs to be retained?* — One file, and one field
   of it: the unclear-concepts list. Round 2's state experiment shows the
   with-state arm adding exactly the unclear concept to the two NAT probes,
   and nothing else changes; the current-module and recent-questions fields
   produced no observable difference. The walkthrough's M1 check opened with
   the state's unclear NAT concept and resolved it.
6. *Can AI reliably distinguish between concepts already introduced and
   concepts that belong later?* — Mostly yes: the grounded arm scores 0
   introduces and 0 re-teaches across all 41 probes, and the walkthrough's
   Module 5 tutor defers the Module 7 question ("covered later in the
   journey, so I won't introduce those Module 7 concepts here"). The
   counterexample is the same probe 2.5 claim: the tutor asserted course
   structure the corpus does not contain.
7. *Which prompt patterns produce useful explanations without excessive
   verbosity?* — Partially answered. The one-to-two-paragraph rule plus
   mandatory marks produces compact answers (grounded answers are one to two
   paragraphs; control answers are essays with invented example values, and
   one truncates at the default budget in the walkthrough). No finer-grained
   pattern-level comparison was run.
8. *Can the AI expose misunderstandings effectively?* — Yes: both round-2
   planted gaps were named without being announced and corrected with zero
   false alarms, and the walkthrough's three planted slips (M4, M5, M6) were
   each named, re-asked in smaller form, and corrected.
9. *Are AI-generated knowledge checks useful?* — Yes: they stay
   conversational (no scores anywhere), a persisting gap becomes a concrete
   learner-state record suggestion in the file's own form, and the M7
   walkthrough check surfaced a gap the scripted learner had not planted
   (the plain-HTTP hop).
10. *How well does the experience work when documents, diagrams, video, and
    audio are mixed?* — Unanswered: the corpus contains documents and ASCII
    diagrams only; no video or audio material was produced or tested.
11. *Does the learner still benefit from a deliberate course sequence when
    they can ask arbitrary questions?* — Unanswered as stated (no free-roam
    comparison run). Partial evidence: helpers hold scope even when asked
    off-sequence questions (the scoping probes; the walkthrough's M5 turn 4),
    so sequence integrity survives arbitrary questions; whether the learner
    benefits from the sequence itself was not measured.
12. *How strongly should the AI remain constrained to the corpus?* —
    Partially answered. Strong grounding works: marks stay honest at
    228/229 (round 1) and 149/149 (round 2), scope holds, and out-of-corpus
    handling is explicit. The two failure modes are over-constraining beyond
    what the corpus contains (the 2.5 course-structure claim) and, with
    weaker instructions, ambiguous marks (the smoke tutor's
    "[module, inferred from the diagram]"). The working balance: constrain
    claims to the corpus, allow the `[general]` escape with an explicit
    declaration.
13. *What happens when the learner asks questions outside the prepared
    material?* — Answered: the grounded arm says the question is outside the
    module (7/7), then either answers with `[general]` marks (5/7) or
    declines (2/7); the control arm never says so and answers unmarked. The
    walkthrough's M5 turn 4 shows the deferral for later-module material.
14. *Which parts of the experience need intentionally authored content, and
    which can reasonably be delegated to AI?* — Partially answered. What the
    authoring had to provide: the module texts, the metadata block (concept
    lists power the scoping rules; the Summary field is the only source the
    check helper draws questions from), the diagrams (the architecture tutor
    anchors every trace to them), and the `Position:` sentences (the drift
    rule defends them). What the AI handled without authoring: rephrasing,
    examples, diagram traces, check flow and record suggestions. Round 2
    shows one thing that does *not* need authoring: per-module specialized
    helper instructions.

## The central question

Can a small corpus of intentionally structured knowledge, combined with
tuned AI course helpers, create a practical and reusable technical learner
journey? — **Yes, with two practical caveats.** A learner completes the whole
journey on the corpus and helpers alone: scope holds, marks stay honest at
the rates above, checks catch both planted and unplanted gaps and feed the
state file, and the state file steers the next check. The caveats: (a) the
out-of-box output budget does not serve the journey — walk-through questions
produce thinking-only replies at 1024, so tutor sessions needed the 8192
config, and check closing turns are budget-tight at 1024 (two of round 2's
sessions and all three attempts of the walkthrough's M7 re-run died there);
(b) the tutor over-reaches where the corpus is silent about its own
structure (the 2.5 claim), so a "later in the journey" claim needs the
course structure supplied, not inferred.

## Worth developing further

- The knowledge-check helper paired with the learner-state file — the
  highest observed value: it surfaced every planted gap and one unplanted
  one, never false-alarmed, and its output is already in the state file's
  format (round-2 sessions; walkthrough M4/M5/M6/M7 checks).
- The grounded tutor's mark discipline and scoping rules — the one
  measurable differentiation (control E=10/L=2 versus grounded 0/0, and
  out-of-corpus 0/7 versus 7/7), and 228/229 marked claims honest.
- The metadata block as the authoring lever — concept lists drive scoping,
  the Summary drives the check helper, `Position:` sentences drive drift;
  everything that worked in the reviews runs off it.
- Fix before developing further: the output-budget policy (tutor content
  needs the larger budget; checks need either it or shorter closing notes)
  and supplying course structure to the tutor so "later in the journey"
  claims are grounded.
- Not worth developing further on this evidence: per-module specialized
  helpers (round 2 answer: no observable difference) and learner-state
  fields beyond the unclear-concepts list (round 2 answer).

## Observations (walkthrough)

- A realistic journey hits the round-1 budget wall immediately: the first
  tutor session's diagram-trace turn failed three times at 1024 with
  thinking-only replies before the session was moved to 8192, the budget
  round 1 had already fixed for probes.
- The control arm truncates at the default budget even for a big-picture
  question (the walkthrough's pre-course turn ends mid-list); grounded
  answers in the same transcript fit the budget.
- The check helper's closing turn remains budget-fragile at 1024: the M7
  re-run died on all three attempts; the M7 check is the heaviest module.
- Planted slips and a real gap were all surfaced without the learner
  announcing anything, and the helper's suggested record for the real gap
  matches the learner-state file's form exactly.
- The helper said the M6 swap "looks clear" after correction while the
  learner kept a note in the state file; both are visible in the evidence —
  the state file is the learner's own bookkeeping.
- Helper marks drift toward annotations the rubric does not define
  (`[derived from diagram]`, `[module, inferred from the diagram]`,
  `[derived: …]`); judgeable, but a mechanical counter needs the variants.

## Appendix — hashes (post-run)

- `transcripts/walkthrough.md`
  `9a86c09608f3e6b255ab2f369fd87a2c52789191bdaf5f4b89f9df3c42b386d8`
- `walkthrough-state.md` (final stage S8)
  `e5f9b7eb640aaf9daa121f62f53e6f7bd64de1be370cb76cc32a4a5322bafb30`
- `run-walkthrough.sh`
  `4be79fe54a211869a475b25a7fab5b069e0de1276c600fe4d668bf8adc7e5556`
- Replays (15), `examples/replay-walkthrough-*.txt`:
  `f0ff6baa…` (00-control), `8c737623…` (01-smoke), `45dda298…` (01-check),
  `a8d74c6e…` (02-tutor), `e975bda0…` (02-check), `97e1058f…` (03-tutor),
  `11e58594…` (03-check), `5d358045…` (04-tutor), `2ab09dea…` (04-check),
  `d79c8f19…` (05-tutor), `e0d1e29d…` (05-check), `7ab74aea…` (06-tutor),
  `06d8af58…` (06-check), `48be4853…` (07-tutor), `97cfad8d…` (07-check).
- `runner.py` `66635965…`, `probe-run-config.json` `10ef9d2b…` — unchanged
  from round 1's recorded hashes. `test-runner.py`: all checks passed.
  `make-replays.py --check`: replays match `probes.md`.
