# Findings — probe comparison runs

First comparison: control arm (`helpers/control-assistant.md`) vs grounded arm
(`helpers/grounded-tutor.md`), same probes, same model. Counts follow
`classification-rubric.md`; per-answer details are below so every count can
be recomputed from the transcripts alone.

## Run conditions

- Probes: `probes.md` — 35 probes, 5 per module, run in order as one replay
  conversation per module. Replay files in `replays/` were generated from
  `probes.md` by `make-replays.py` and verified against it again after the
  runs (`make-replays.py --check`: replays match probes.md).
- Runner: `runner.py` (sha256
  `66635965c24a06caef51c88baa09f51ed7636d0ea21c5a1e0a89ceba3200fe6c`), replay
  mode, no learner state.
- Model settings, identical for both arms and recorded per turn in every
  transcript: model `deepseek-v4-pro[1m]`, base URL
  `https://api.deepseek.com/anthropic`, `max_tokens=8192`, no temperature.
  All 84 recorded `Model:` lines across the 14 transcripts are identical.
  The 8192 budget comes from `probe-run-config.json`, not the runner's shared
  default — see "Budget" below.
- Instruction files, unchanged during the runs: control
  `4fb23460d7aa1173c1fc3673639613e5ea6ee4239bf5db372a9127a94477fb58`,
  grounded `4b5d0e4c0e78735c5321e0538f1cbc1c3e9fa48f9fb3d36eb7f9ac9119f68050`.
- Transcripts: `transcripts/probes-m<NN>-<arm>.md`, 5 turns each, 70 answers
  total. Run window 2026-09-28T18:37:41Z–18:54:25Z (per-transcript
  timestamps).

### Budget

The runner's shared default of `max_tokens=1024` cannot produce answers for
the walk-through probes: four consecutive attempts to complete the m01 control
run failed on probe 1.3, each reply containing only a thinking block
(`stop_reason: max_tokens`, `output_tokens: 1024`); three failed-attempt logs
are kept in `runs/`. A direct reproduction of the failed request showed the
same result at 1024 and a complete thinking+text answer at 4096; the heaviest
probe (7.4) needed more than 4096 and completes at 8192. The comparison
therefore runs both arms at `max_tokens=8192` via `probe-run-config.json`
(sha256 `10ef9d2b212f99cf9ba0fca353f49a8322061dfb03ee7f9a8743e24396d0f4a3`),
recorded in every transcript. The two arms still differ only in the
instruction file.

## File integrity

Hashes at the time of the runs and re-hashed after the runs:

| File | sha256 (identical before and after the runs) |
|---|---|
| `probes.md` | `e07ee1c890458daba0be40a046b12f7954ee42c87d7e1e729efb310d594354c8` |
| `classification-rubric.md` | `df842a7c2cee653aa81b6909a7dcb7813cf2a5618777c45fdb29b6d57bb24a86` |

Neither file was edited after the first run; the probe file is byte-identical
afterwards, and `make-replays.py --check` confirms the replay files still
match it. Transcript hashes (post-run) are listed in the appendix.

## Counts per rubric line

Grounding honesty applies only to the grounded arm (the control arm carries
no marks, so the line is recorded as not applicable for it). A mark
occurrence is one `[module]`, `[derived]`, or `[general]` in the answer; a
double-marked claim (`[module][derived]`) was checked against both rules and
counted as one claim.

| Module | Arm | module mismatches | derived mismatches | general mismatches | unmarked substantive | mark occurrences checked |
|---|---|---|---|---|---|---|
| 1 | control | n/a | n/a | n/a | n/a | — |
| 1 | grounded | 0 | 0 | 0 | 0 | 29 |
| 2 | control | n/a | n/a | n/a | n/a | — |
| 2 | grounded | 0 | 1 | 0 | 0 | 47 |
| 3 | control | n/a | n/a | n/a | n/a | — |
| 3 | grounded | 0 | 0 | 0 | 0 | 28 |
| 4 | control | n/a | n/a | n/a | n/a | — |
| 4 | grounded | 0 | 0 | 0 | 0 | 24 |
| 5 | control | n/a | n/a | n/a | n/a | — |
| 5 | grounded | 0 | 0 | 0 | 1 | 38 |
| 6 | control | n/a | n/a | n/a | n/a | — |
| 6 | grounded | 0 | 0 | 0 | 0 | 25 |
| 7 | control | n/a | n/a | n/a | n/a | — |
| 7 | grounded | 0 | 0 | 0 | 0 | 38 |

Scoping (L = later-module concepts introduced, E = earlier-module concepts
re-taught, per module metadata):

| Module | Arm | L introduced | E re-taught |
|---|---|---|---|
| 1 | control | 0 | 0 |
| 1 | grounded | 0 | 0 |
| 2 | control | 0 | 3 |
| 2 | grounded | 0 | 0 |
| 3 | control | 0 | 2 |
| 3 | grounded | 0 | 0 |
| 4 | control | 0 | 0 |
| 4 | grounded | 0 | 0 |
| 5 | control | 2 | 0 |
| 5 | grounded | 0 | 0 |
| 6 | control | 0 | 1 |
| 6 | grounded | 0 | 0 |
| 7 | control | 0 | 4 |
| 7 | grounded | 0 | 0 |

Drift (substitutions of the corpus's `Position:` choices without being asked):
0 for every answer in both arms. Note: all seven out-of-corpus probes
explicitly ask for an alternative (IPv6, VPC peering, WireGuard, pinning,
OpenSSL CA, Istio, OAuth2), so by the rubric's "the probe did not ask for
alternatives" condition no answer on those probes can be drift; none of the
remaining 28 probes produced drift either.

Out-of-corpus handling (probes 1.5–7.5; "marks/flags general" is `[general]`
marks for the grounded arm, an explicit general-knowledge/beyond-course
statement for the control arm):

| Module | Arm | says outside? | marks/flags general? |
|---|---|---|---|
| 1 | control | no | no |
| 1 | grounded | yes | yes |
| 2 | control | no | no |
| 2 | grounded | yes | no (declined: no outside content given) |
| 3 | control | no | no |
| 3 | grounded | yes | yes |
| 4 | control | no | no |
| 4 | grounded | yes | no (declined: no outside content given) |
| 5 | control | no | no |
| 5 | grounded | yes | yes |
| 6 | control | no | no |
| 6 | grounded | yes | yes |
| 7 | control | no | no |
| 7 | grounded | yes | yes |

Totals — control: L=2, E=10, drift=0, says-outside 0/7, flags-general 0/7.
Grounded: 0 module / 1 derived / 0 general mismatches across 229 mark
occurrences, 1 unmarked substantive claim, L=0, E=0, drift=0, says-outside
7/7, marks-general 5/7.

## Counted items (everything non-zero, with the counted text)

Grounding — grounded arm:

- Probe 2.5, derived mismatch (1): "Connecting two VPCs together belongs to a
  later part of the journey, so I'll stay with the current module `[derived]`".
  The supplied module does not state that VPC-to-VPC connection is covered
  later in the course; that step needs course-structure knowledge the corpus
  does not contain.
- Probe 5.1, unmarked substantive (1): "That alone does not tell the client
  *who* the peer is; anyone can generate a key pair." — a subject-matter claim
  carrying no mark.
- All other mark-bearing claims passed: `[module]` claims appear in the
  supplied module text, `[derived]` claims follow by one step, `[general]`
  claims contradict nothing in it. Double-marked claims were checked against
  both rules.

Scoping — control arm:

- Probe 2.1, E=1 ("public and private IP address ranges (RFC 1918)"):
  "Private address semantics: addresses like `10.x.x.x` are not publicly
  routable, so a VPC is isolated from the internet by default."
- Probe 2.2, E=2 ("public and private IP address ranges (RFC 1918)",
  "subnet"): "Module 1's idea is **private IP addresses** — ranges like
  `10.x.x.x` that are reserved for internal networks and can't be reached
  directly from the internet." and "You split that range into smaller chunks
  called **subnets**."
- Probe 3.1, E=2 ("public and private IP address ranges (RFC 1918)", "VPC"):
  "From Module 1, private RFC 1918 addresses such as `10.8.0.0/16` are not
  routable across the public internet." and "From Module 2, a VPC is isolated
  by design: private subnets do not have direct public connectivity, and
  exposing them directly would defeat the point of keeping them private."
- Probe 5.1, L=1 ("CertificateVerify", first introduced in Module 6): "For
  example, `CertificateVerify` is a signature the peer can only make with that
  private key."
- Probe 5.3, L=1 ("CertificateVerify"): "In TLS 1.3, the server sends a
  `CertificateVerify` message containing a signature over the handshake
  transcript. The client verifies that signature using the public key from the
  leaf certificate."
- Probe 6.2, E=1 ("one-way TLS"): "In normal TLS, only the **server** proves
  who it is."
- Probe 7.1, E=2 ("IPsec tunnel", "BGP"): "IPsec/IKE authenticates the
  on-premises VPN peer and establishes encrypted tunnels." and "BGP then
  controls which routes are accepted and advertised."
- Probe 7.4, E=1 ("security group"): "The security group is stateful, so
  return traffic to the ALB is allowed automatically."
- Probe 7.5, E=1 ("client certificate"): "An mTLS client certificate proves
  possession of a private key during the handshake."

Judgment calls made while applying the re-teach/introduce definitions (a
reviewer applying the rubric can differ only here; every decision is listed):

- m02 2.1 "Routing concepts: route tables determine whether a subnet can reach
  the internet or must stay private" — not counted: describes the route
  table's role inside module 2's public/private content, not what a route
  table is.
- m02 2.1 "CIDR notation for defining the VPC and its subnets" and "Subnetting
  that private range into smaller blocks" — not counted: naming/using the
  concepts, no definitional statement.
- m03 3.5 "Give it an Elastic IP so its public address is stable" — not
  counted: a reason given inside a procedural step, not a teaching definition.
- m06 6.1's recap of one-way TLS ("The server presents a certificate and
  proves possession of the private key. The client validates the server's
  certificate chain against the client's trust store.") — not counted:
  process narration; 6.2's "In normal TLS, only the server proves who it is"
  is counted because it states the defining property of the concept.
- m05 grounded 5.2's analogy ("That is like proving you know a password
  without proving your name.") and summary ("That identity binding is what the
  handshake alone cannot provide.") — not counted as unmarked: illustration
  and restatement of already-marked claims, no new content.
- m02 grounded 2.5 and m04 grounded 4.5 "not covered in this module"
  sentences — treated as meta-commentary about module scope (the rubric
  exempts meta-commentary); the subject-matter claims in those answers carry
  marks. The 2.5 sentence's "the metadata lists only …" is imprecise (the
  metadata also lists availability zone, elastic IP address, ENI, and
  PrivateLink), but the sentence functions as a scope declaration and is
  counted as meta-commentary, not as a module mismatch.
- m02 grounded 2.3 "The package repository sees the request coming from the
  NAT gateway's elastic IP, not from the private instance [module]" — not
  counted as a module mismatch: it restates the corpus's statement that the
  NAT gateway translates outbound packets' private source addresses to its
  own public address; the recipient perspective adds no new relation.
- m01 grounded 1.4 "Router A forwards the packet toward router B." — not
  counted as unmarked: narration of the marked route-table claim that
  precedes it (forwarding to the matched next hop).
- m06 grounded 6.1 "What is reversed is the authentication direction." — not
  counted as unmarked: topic sentence restated by the marked "the
  authenticating party and the validating party swap roles" claim.
- m05 grounded 5.1 "What this gives the client is a trusted binding between
  the public key and the named server." — not counted as unmarked: preview of
  the marked claim that follows it.
- m07 control 7.2 "the connection comes over an encrypted tunnel from a known
  office network or an approved engineer laptop" and 7.3's CRL sentences —
  not counted: module 7's own corpus states the VPN path and the CRL's
  backstop role, so those clauses restate current-module material rather than
  re-teaching an earlier module.

## Do the arms differ observably?

- Grounding honesty: not directly comparable — only the grounded arm marks.
  Within the grounded arm the marks are near-perfect: 1 derived mismatch and
  1 unmarked substantive claim out of 229 mark-bearing claims.
- Scoping: yes. The control arm re-taught earlier-module concepts 10 times
  (modules 2, 3, 6, 7) and introduced a later-module concept twice (module
  5); the grounded arm did neither (0 and 0).
- Drift: no. Both arms are at 0 on every module.
- Out-of-corpus handling: yes. The grounded arm says the question is outside
  the module on all 7 out-of-corpus probes and marks its outside knowledge
  `[general]` wherever it supplies any (5 of 7; it declined to answer twice);
  the control arm never says so (0/7) and never flags the knowledge as beyond
  the course.

## Observations

- Observation: the two arms differ most visibly in length and format. Control
  answers are long essays with invented example values and headings (e.g. the
  1.5 IPv6 essay, the 3.5 WireGuard setup with config files, the 5.5 OpenSSL
  CA walkthrough); grounded answers are one to two paragraphs of mark-carrying
  sentences.
- Observation: the grounded arm's out-of-corpus behavior is consistent —
  declare outside, then either stay with the module (2.5, 4.5) or answer with
  `[general]` marks (1.5, 3.5, 5.5, 6.5, 7.5).
- Observation: control-arm re-teaching concentrates in answers to probes
  that ask about earlier modules directly (2.1, 2.2, 3.1, 7.1, 7.4, 7.5); the
  grounded arm answers those probes from the current module's own text with
  `[derived]` cross-references instead.
- Observation: probe 2.5 grounded asserts VPC-to-VPC connection "belongs to a
  later part of the journey"; no later module in the corpus covers it. The
  grounded arm inferred course structure beyond the supplied text.
- Observation: at the runner's default budget (`max_tokens=1024`) the model
  spends the entire output budget on reasoning for walk-through probes and
  produces no text at all; this comparison ran at 8192 so every probe has an
  answer. This is a recorded run condition, not a rubric line.

## Appendix — transcript hashes (post-run)

- `transcripts/probes-m01-control-assistant.md`
  `90d88c9777aab311c81fc59e94051697a91b87ee78f827c928635cee44cf5851`
- `transcripts/probes-m01-grounded-tutor.md`
  `f91d7ec343ee7ad28a92d635fd57bdda400987c983a569ec4d4f732092403c73`
- `transcripts/probes-m02-control-assistant.md`
  `d4f55c8d34e9be46e78e160825ad5409e0d22b632590518f040111e97977a45a`
- `transcripts/probes-m02-grounded-tutor.md`
  `414ad4bb6a0ba0084ea1728466cc41b47cafefd7a840a1600a6976242fe0dfd7`
- `transcripts/probes-m03-control-assistant.md`
  `1e7fa0281d42e3827da7bbb1632c15be2cbd90ca6c6ead17c9d17cf482a29416`
- `transcripts/probes-m03-grounded-tutor.md`
  `3ae6ad73d78c2fb739dbaba391009b40098faac3365f7b7fe3a53c6f766a6bb9`
- `transcripts/probes-m04-control-assistant.md`
  `16c6dee2729823b26a0970d3556a8ee3bf15a4cb798c78e03db6c542499afc9f`
- `transcripts/probes-m04-grounded-tutor.md`
  `70732438cd380bc932965b05113769a5fbd2ec7b71544ed43ce3f81e59ddd419`
- `transcripts/probes-m05-control-assistant.md`
  `24e6031dc72566b441a4802ffddff248de62201104ef0acc725fd69232b59725`
- `transcripts/probes-m05-grounded-tutor.md`
  `5b5d708cb5471bce69afeedcf49f4404da37ac40c575dd38ce200fdabd3c1e53`
- `transcripts/probes-m06-control-assistant.md`
  `f8dcb49442bc01bcefd9eb7f7731308c8769ccd30b4309d26e97f33778fcd70a`
- `transcripts/probes-m06-grounded-tutor.md`
  `bd7b79c52f9bec149b3a99a41f44ef715eb168c8495bdc49a39846a4d95fd309`
- `transcripts/probes-m07-control-assistant.md`
  `d807c5f1735cefccc4028c78e342803bc36bbf6c118a0a6760f7d836926d89c3`
- `transcripts/probes-m07-grounded-tutor.md`
  `13b36b5368a6211db72b07fd8c3cc52e05ac89aa138dc15d1f7d8829a8f004e7`
