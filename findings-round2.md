# Findings — specialization, learner state, and knowledge checks

Round 2 of the learner-journey experiments. Three questions, one experiment
each:

1. Are specialized course helpers materially better than the single grounded
   tutor?
2. How much learner state is needed for it to matter?
3. Do conversational knowledge checks expose misunderstandings that passive
   reading would not?

Counts follow `classification-rubric.md` (round 1's Lines 1-4 plus the round-2
Lines 2b, 5, and 6); per-answer detail is below so every count can be
recomputed from the transcripts alone.

## Run conditions

- Probes: `probes.md`, extended for this round with six scoping probes
  (6.6-6.8, 7.6-7.8); 41 probes total. The scoping probes ask about an
  earlier module's concept by name while the helper serves a later module.
- Specialization scope: modules 6 and 7 — the two modules that have a
  specialized helper (`helpers/mtls-tutor.md` for Module 6,
  `helpers/architecture-tutor.md` for Module 7, both from the specialized-
  helpers issue). Every probe in those two sections (the original five plus
  the additions) was answered by both arms — the general grounded tutor and
  the matching specialized helper — in one replay conversation per module.
  Modules 1-5 have no specialized helper, so no specialization arm exists
  for their probes; their grounded answers from round 1 (identical model
  settings) stand. The scoping additions were asked of both arms, matching
  the issue's examples (the mTLS helper gets a networking-foundations
  question and a certificate question).
- Learner-state runs: module 1 probes through the grounded tutor twice, arm
  S0 without a state file and arm S1 with `learner-state.example.md`
  (current module, one concept marked unclear, two recent questions).
  Nothing else differs; both transcripts record the state presence per turn.
- Knowledge-check sessions: three scripted sessions against
  `helpers/knowledge-check.md` — `examples/replay-check-m06-planted.txt`
  (Module 6, planted server/client certificate swap),
  `examples/replay-check-m05-explain.txt` (Module 5, incorrect explain-back
  of chain validation), `examples/replay-check-m06-correct.txt` (Module 6,
  correct answers throughout).
- Runner: `runner.py`, replay mode. Scripts: `run-experiments.sh` drives all
  nine runs with the same retry policy as round 1.
- Model settings, identical for both arms of the specialization runs and
  recorded per turn in every transcript: model `deepseek-v4-pro[1m]`, base
  URL `https://api.deepseek.com/anthropic`, `max_tokens=8192`, no
  temperature (from `probe-run-config.json`). All 36 recorded `Model:` lines
  across the four specialization transcripts are identical; the state-run
  pair also ran at 8192. The check sessions ran at the runner's shared
  default `max_tokens=1024` like the smoke session.
- Run window: 2026-09-28T19:13:34Z-19:23:17Z (per-transcript timestamps).
  Transcripts: `transcripts/spec-m06-<arm>.md`,
  `transcripts/spec-m07-<arm>.md`, `transcripts/state-m01-<arm>.md`,
  `transcripts/check-*.md`; 8, 8, 5, and 6/5/6 turns respectively.

### Budget

The check sessions ran at 1024. Two sessions' first attempts died on the
closing turn with a thinking-only reply (`runner: error: model reply has no
text blocks` — the same failure mode round 1 recorded at 1024) and were
retried from clean transcripts; the failed-attempt logs are kept in `runs/`
(`check-m06-planted.attempt-1-failed.log`,
`check-m05-explain.attempt-1-failed.log`). One retried reply in the
explain-back session is still truncated mid-correction by the 1024 budget
(see the session detail); the counts record the truncation.

## File integrity

Hashes taken immediately before the first run and re-taken after the last
run; the two sets are identical.

| File | sha256 (identical before and after the runs) |
|---|---|
| `probes.md` | `ebae0e66f3f117f6927872b3e3737d78e8b0ce703643e3463b67398114bbc6a7` |
| `classification-rubric.md` | `8110d09277b6efe485bfc96f34486466b326d65760c72a1c25a9aa388af4e582` |
| `helpers/grounded-tutor.md` | `4b5d0e4c0e78735c5321e0538f1cbc1c3e9fa48f9fb3d36eb7f9ac9119f68050` |
| `helpers/mtls-tutor.md` | `173a3dc30da08e96da558d5ce7fc18dd295cb4b26369fb6e0d088af7eb7e8bc1` |
| `helpers/architecture-tutor.md` | `e33eab6d0fbc2aabb8bb8963bf35dbb68dd17d20c1d74c49efec15b2cfc04469` |
| `helpers/knowledge-check.md` | `2d004cdef8c95568e1c9056f455724418773f192c7a84242e633dc463d484d97` |
| `learner-state.example.md` | `0edc55f1d83f9544adb2779a4a659eb956b398fc99500985dd42d9a5e8bf5c40` |
| `examples/replay-check-m06-planted.txt` | `83cba7916b90ae4a03a3ee2eea798925a0aca94dd141c6f335531e3e80b4dbf9` |
| `examples/replay-check-m05-explain.txt` | `6c656c16ef3e91300458cc0fbcb3c0d1a306baddeab9dd5e3a66db26ba1c2d21` |
| `examples/replay-check-m06-correct.txt` | `31ba6cd2548748b5e95bce140d3cbf14c8345d7ac41fcda317cbc00aeaacb2a3` |

`make-replays.py --check` confirms the replay files still match `probes.md`
after the runs. The grounded-tutor hash is unchanged from round 1's recorded
`4b5d0e4c...`; `probe-run-config.json` is unchanged from round 1's recorded
`10ef9d2b...`. The round-1 `probes.md` hash (`e07ee1c8...`) corresponds to
the file before this round's scoping additions, verifiable against the
round-1 commit. Transcript hashes (post-run) are listed in the appendix.

## Experiment 1 — Specialization (modules 6 and 7, both arms)

Question: are specialized course helpers materially better than the single
grounded tutor?

### Line 1 — Grounding honesty (both arms mark)

| Module | Arm | module mismatches | derived mismatches | general mismatches | unmarked substantive | mark occurrences checked |
|---|---|---|---|---|---|---|
| 6 | grounded | 0 | 0 | 0 | 0 | 32 |
| 6 | mtls | 0 | 0 | 0 | 0 | 25 |
| 7 | grounded | 0 | 0 | 0 | 0 | 44 |
| 7 | mtls-architecture | 0 | 0 | 0 | 0 | 48 |

### Line 2 — Scoping (L = later concepts introduced, E = earlier re-taught)

| Module | Arm | L introduced | E re-taught |
|---|---|---|---|
| 6 | grounded | 0 | 0 |
| 6 | mtls | 0 | 0 |
| 7 | grounded | 0 | 0 |
| 7 | architecture | 0 | 0 |

Neither arm re-taught an earlier concept on any original probe; both hold
scope exactly as round 1's grounded arm did.

### Line 2b — Scoping probes

| Probe | Arm | re-teaches-asked | re-teaches-extra (names) | honesty | returns |
|---|---|---|---|---|---|
| 6.6 (NAT) | grounded | yes | 1 (private IP address ranges, RFC 1918) | ok | no |
| 6.6 (NAT) | mtls | yes | 1 (private IP address ranges, RFC 1918) | ok | no |
| 6.7 (certificate + chain) | grounded | yes | 0 | ok | yes |
| 6.7 (certificate + chain) | mtls | yes | 0 | ok | yes |
| 6.8 (one-way TLS validation) | grounded | yes | 0 | ok | yes |
| 6.8 (one-way TLS validation) | mtls | yes | 0 | ok | yes |
| 7.6 (route table + default route) | grounded | yes | 0 | ok | yes |
| 7.6 (route table + default route) | architecture | yes | 0 | ok | yes |
| 7.7 (chain + validation checks) | grounded | yes | 0 | ok | yes |
| 7.7 (chain + validation checks) | architecture | yes | 0 | ok | yes |
| 7.8 (verify vs passthrough) | grounded | yes | 0 | ok | yes |
| 7.8 (verify vs passthrough) | architecture | yes | 0 | ok | yes |

Every scoping-probe answer defines the asked concept (both arms are
instructed to answer when asked). Both arms re-teach exactly one concept
beyond the asked one — the RFC 1918 private ranges inside the 6.6 NAT
answers, both arms — and nothing extra elsewhere. Honesty is clean in all
twelve: earlier-module claims carry `[general]` or `[derived]`; no
`[module]`-marked earlier-module claim appears. Both arms return to the
module's framing on 5 of 6 scoping probes (only 6.6 closes without it).

Says-outside on the scoping probes (recorded, not a rubric line): both arms
declare the question outside the module when the concept is far from it
(6.6 NAT, 7.6 route tables, 7.8 passthrough) and answer without the
declaration when it is adjacent (6.8, 7.7, grounded's 6.7; mtls's 6.7 gives
only a boundary note, "This is Module 5 material, not Module 6"). The arms
agree probe for probe.

### Line 3 — Drift

0 for every answer in all four arms (module 6's verify-mode position and
module 7's three positions are never contradicted or silently substituted).

### Line 4 — Out-of-corpus handling (probes 6.5, 7.5)

| Probe | Arm | says outside? | marks general? |
|---|---|---|---|
| 6.5 | grounded | yes | yes |
| 6.5 | mtls | yes | yes |
| 7.5 | grounded | yes | yes |
| 7.5 | architecture | yes | yes |

### Judgment calls

- mtls 6.4 "In the diagram, `ClientHello` and the server's `ServerHello`,
  `Certificate`, and `Finished` are the normal one-way TLS messages.
  `[module]`" — not counted as a module mismatch: restates the module's
  "mirrors Module 4 in reverse" applied to the diagram's message list.
- grounded 6.1/6.2 opening sentences describing one-way TLS roles ("In the
  ordinary TLS setup from Module 4, the server proves its identity...") —
  not counted as unmarked substantive or as E re-teach: narration of the
  Module-4 baseline in answers to probes that explicitly ask for the
  Module-4 connection, the same treatment round 1 gave the grounded arm's
  6.1 recap.
- grounded 6.3 "If the chain is valid, the ALB accepts the connection"
  `[module]` — not counted: complement of the corpus's "Invalid certificates
  are rejected at the edge".
- grounded 7.8's closing contrast ("at the ALB in verify mode, or at the
  backend in passthrough mode") — counted as a return to module framing,
  one side of the contrast being the module's own mode.

### Answer to question 1

No material specialization effect is observable on this probe set. The
specialized helpers and the general grounded tutor produce equivalent
scoping behaviour: both re-teach nothing on the original probes (E=0, L=0),
both define exactly the asked concept on the scoping probes and one extra
concept once (the same one, on the same probe), both mark earlier-module
content honestly, and both return to the module's framing at the same rate
(5 of 6). The only observable differences are stylistic: the architecture
tutor anchors every flow trace to diagram elements and repeats the
diagram's labels ("the `:443` TLS + mTLS verify box"), the grounded tutor
prefers bullet lists. The grounded tutor already carries the
do-not-re-teach rule, so specializing it per module adds nothing measurable
here — one well-tuned general instruction covers what the two specialized
helpers were built to do.

## Experiment 2 — Learner state (module 1, grounded tutor)

Question: how much learner state is needed for it to matter?

### Line 5 — State effect

| Probe | S1 state-referencing | Observable difference |
|---|---|---|
| 1.1 | yes — explains the reply-translation mechanism (the state's unclear concept) in a `[general]` translation-table paragraph S0 does not have | differs: reply-path elaboration (state-derived) |
| 1.2 | no (reply emphasis inherited from the turn-1 answer it simplifies) | identical beyond that inherited emphasis |
| 1.3 | yes — closes by walking replies back to the matching source ports, which the probe does not ask for | differs: reply-path closure (state-derived) plus per-clause marks and example values |
| 1.4 | no | differs: S1 elaborates router B's local-route handling and adds a closing decision summary; not attributable to specific state content |
| 1.5 | no | identical substance; S1 uses inline mark justifications |

S1 state-referencing turns: 2 of 5. Both land on the state's unclear concept
(NAT reply translation), in the two probes that touch NAT.

Judgment call: the S1 replies address the state's unclear concept without
quoting the state file; counted as state-referencing because the
module-plus-probe alone does not prompt that content (S0's paired turns
prove the baseline).

### Answer to question 2

A single populated state file — current module, one unclear concept, two
recent questions — already matters, even in a helper whose instruction never
mentions state. The grounded tutor's with-state arm added the reply-
translation mechanism (exactly the unclear concept) to both NAT probes and
nowhere else, and the arms' other answers differ only cosmetically. The
state file's effect is the unclear-concept field; the recent-questions and
current-module fields produced no observable difference here (the module is
supplied anyway, and the recent questions are answered by the probes
themselves). For a helper that consumes state by instruction, the
knowledge-check helper, the same file steers the first question to the
unclear concept (the `transcripts/knowledge-check.md` smoke session opens
with it). So: one file is enough for the state to matter; the single field
that does the work is the unclear-concepts list.

## Experiment 3 — Knowledge-check sessions

Question: do conversational checks expose misunderstandings that passive
reading would not?

### Line 6 — Surfacing

| Session | Planted gap | Surfaced | Suggested record | False alarms |
|---|---|---|---|---|
| `check-m06-planted` | server/client certificate roles swapped (turns 2-3); trust store said to hold the server's own certificates (turn 4) | yes — turn 2 names the swap and corrects it, then re-asks in smaller form; turn 3: "Still swapped" with side-by-side correction; turn 4: "Partly right... the server-side trust store is not for that" | yes — turn 3 ("I'd record this one as unclear" in learner-state form); turn 6 closing note lists both gaps | 0 |
| `check-m05-explain` | chain-signature direction reversed ("the leaf certificate signs the intermediate") | yes — turn 2: "One piece is reversed, though: the leaf does not sign the intermediate, and the intermediate does not sign the root" (the correction sentence is then cut off by the 1024 budget) | yes — turn 5 closing note (the un-answered trust-anchor follow-up) | 0 |
| `check-m06-correct` | none | n/a | yes — turn 6 closing note ("Why ALB mTLS recommends verify mode — you described verify and passthrough but didn't give the recommendation or reason") | 0 |

Notes:

- The planted session never announces the confusion and never asks whether
  it is right; the helper names it on the learner's first statement (turn 2)
  and keeps correcting on repetition. Its turn-3 record suggestion uses the
  learner-state form exactly as the helper instruction specifies.
- In the planted session the helper also did not false-alarm on the
  correct verify/passthrough answer (turn 5: "Your description of the two
  modes is right"), and when the learner skipped its re-check question it
  said so plainly ("you didn't answer the re-check") without inventing a
  gap.
- The explain-back session's turn-3 learner restatement ("The signatures go
  up the chain... the client starts at the leaf and verifies each signature
  as it walks up") was ambiguous enough that the helper read it as
  corrected — the planted error was already named in turn 2, so surfacing
  holds; the script's persistence wording did not.
- The correct session's one suggested record is accurate, not a false
  alarm: the scripted answer described the two modes but did omit the
  recommendation half of the question.

### Answer to question 3

Yes. Both planted gaps — a role swap stated as fact and a wrong
explain-back — were named and corrected without the learner announcing
anything, and the correct learner passed with zero false alarms. The checks
stay conversational (no scores anywhere) and the helper converts a
persisting gap into a concrete learner-state record suggestion, which is
exactly the bridge the state experiment shows matters.

## Observations

- The scoping probes show both arms decide "outside the module" by
  distance, not by rule: NAT and route tables get the outside declaration;
  certificates and TLS validation (adjacent to mTLS) do not, in both arms.
- The check sessions' 1024 budget is tight for Module 5-6 content: two
  first attempts died on the closing turn with thinking-only replies, and
  one retried correction is truncated mid-sentence. The probe runs at 8192
  show no such truncation. A check helper likely needs the higher budget or
  shorter replies for later modules.
- The with-state grounded tutor marks more finely than the no-state arm
  ("`[module]` for ports, `[general]` for the port number"). Whether this
  is state-driven or model variation is not separable in this design; it is
  recorded as an observable difference.

## Appendix — transcript hashes (post-run)

- `transcripts/spec-m06-grounded.md`
  `c39cdaa0d7c2780b1f6c73a73405525e753cab34bbcd3d6d5d74acca62cc6fa8`
- `transcripts/spec-m06-mtls.md`
  `42ddc3e7f82d39fb43ef91cd9f5cd0a7a5e1243d8394f5269282546f7746db42`
- `transcripts/spec-m07-grounded.md`
  `6bf9296d6240fe0b16c19e8a7a9f1f7461da8c7e054caa732df80d31469e4892`
- `transcripts/spec-m07-architecture.md`
  `33e77ce51d5f199c04951861667ba294134089b2ad4b8afb5d4c79e13cafb7fe`
- `transcripts/state-m01-none.md`
  `cda9c98f2b70a0479ef2c79a17a603ddb792af406e9bd3b3390f769b6fc3c965`
- `transcripts/state-m01-state.md`
  `379be38387f885f68861028a360fa9c4131c67f8bc4f94d32f482f515c0d8f33`
- `transcripts/check-m06-planted.md`
  `0d974016715e52b863878590a315c3d825e0031ac75174c951f562e0a22a73ae`
- `transcripts/check-m05-explain.md`
  `405dda04c1d6bd39336901871c862c4b8fa36b8d5aeffa42d83175ba6ab73e02`
- `transcripts/check-m06-correct.md`
  `65a185671f1ee31c08ec30b6fdcd2183528db287d6122ab87548c3f682d1267c`
