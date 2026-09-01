# Classification rubric — learner journey comparison

Frozen before any run. Every line below is a mechanical rule; each count cites
the answer and the claim, concept, or position it counted. Lines 1-4 date from
round 1 (first comparison). Round 2 (specialization, learner-state, and
knowledge-check experiments) adds Line 2b (scoping probes), Line 5 (state
effect), and Line 6 (knowledge-check surfacing), frozen before the round-2
runs. The probe file is `probes.md`; transcripts live under `transcripts/`.

## Units and inputs

- A **probe** is one message from `probes.md`, identified by its id (for
  example 3.4). A **turn** is one probe asked in a run; an **answer** is the
  helper reply recorded for that turn.
- The **corpus for an answer** is the module the answer was given for: the
  metadata block plus the content sections of `modules/NN-*.md`, exactly as
  supplied to both arms by the runner. It does not include other modules.
- The **grounded arm** marks claims with `[module]`, `[derived]`, and
  `[general]`. The issue's `corpus`-marked class maps to `[module]`; the
  other two classes map by name. The **control arm** carries no marks, so
  Line 1 is recorded for it as not applicable.

## Line 1 — Grounding honesty (grounded arm only)

A **claim** is a sentence or clause ending in one of the three marks. For each
claim in an answer:

- `[module]`-marked: the claim's content must appear in the corpus for that
  answer (verbatim, or a restatement that keeps the same subject, predicate,
  and quantity; pronoun resolution and cosmetic rewording allowed). A claim
  that asserts something the corpus does not state is a **module mismatch**.
- `[derived]`-marked: the claim must follow from the corpus by one obvious
  step — unpacking a defined term, arithmetic on numbers the corpus gives, or
  applying a stated rule to a stated case. A claim that needs knowledge the
  corpus does not contain, or that asserts a step the corpus does not support,
  is a **derived mismatch**.
- `[general]`-marked: the claim is a **general mismatch** only if it
  contradicts the corpus. Contradiction means the corpus states X and the
  claim states not-X on the same point.
- Additionally, count **unmarked substantive claims**: claims about the
  subject matter that carry no mark (framing, restating the question, and
  meta-commentary about the module do not count).

Count per answer: module mismatches, derived mismatches, general mismatches,
unmarked substantive claims.

## Line 2 — Scoping

Each module's metadata block lists the concepts that module introduces. For an
answer given with module N:

- **L** = concepts introduced by modules N+1..7, taken from those modules'
  metadata blocks:
  - Module 2: VPC, availability zone, AWS subnet, public subnet, private
    subnet, internet gateway, NAT gateway, elastic IP address, elastic network
    interface (ENI), security group, VPC interface endpoint, AWS PrivateLink.
  - Module 3: IPsec tunnel, AWS Site-to-Site VPN, virtual private gateway,
    customer gateway, transit gateway, AWS Client VPN, BGP, route propagation.
  - Module 4: TLS, HTTPS, handshake, symmetric encryption, asymmetric
    encryption, session key, cipher suite, Server Name Indication (SNI),
    server certificate, one-way TLS.
  - Module 5: X.509 certificate, public key, private key, certificate
    authority (CA), root CA, intermediate CA, certificate chain, trust anchor,
    trust store, subject alternative name (SAN), validity period, revocation
    (CRL, OCSP), AWS Certificate Manager (ACM), AWS Private CA.
  - Module 6: mutual TLS (mTLS), client certificate, CertificateRequest,
    CertificateVerify, Application Load Balancer (ALB), ALB listener, ALB
    trust store, verify mode, passthrough mode, X-Amzn-Mtls headers.
  - Module 7: target group, certificate renewal and rotation.
- **E** = the union of the concept lists of modules 1..N-1, each module's
  list taken from its metadata block and given above: Module 1's list in
  full here — IP address, CIDR, subnet, packet, routing, route table, default
  route, default gateway, TCP, port, DNS, public and private IP address
  ranges (RFC 1918), network address translation (NAT) — and Modules 2-7's
  lists as stated in the L section above. (So E for module 2 is Module 1's
  list; E for module 6 is Modules 1-5's lists; and so on.)

**Introduce** (count against L): the answer states what a later concept is —
a definitional statement about it or an explanation of how it works — not
merely naming it, saying it comes later, or using its name in passing.

**Re-teach** (count against E): the answer states what an earlier concept is —
a definitional statement about it — not merely using the concept inside an
explanation of current-module material, and not a bare cross-reference.

Count per answer: distinct L concepts introduced, distinct E concepts
re-taught, each with the concept names recorded.

## Line 3 — Drift

The corpus states its positions in `Position:` sentences. For an answer given
with module N, the applicable positions are:

- Module 2: (a) "a NAT gateway is for outbound-only traffic — a service that
  must be reachable from outside belongs behind an ingress point in a public
  subnet instead"; (b) "private subnets should reach AWS services through
  endpoints rather than a NAT gateway wherever an endpoint exists".
- Module 3: (a) "prefer BGP wherever the device supports it, because it
  survives prefix changes without manual edits"; (b) "once more than one VPC
  or one VPN is involved, terminate VPNs on a transit gateway rather than
  per-VPC gateways".
- Module 6: "use verify mode" — chain validation at the edge, not pushed into
  each application.
- Module 7: (a) "Certificates are the only credentials"; (b) "Client
  authentication happens at the edge" (the ALB terminates mTLS, instances get
  plain HTTP plus identity headers); (c) "Network privacy is layered, not
  single".
- Modules 1, 4, 5: no `Position:` sentences; drift is not counted there.

An answer **drifts** once per position it contradicts: it presents the
opposite approach as its recommendation, or as acceptable default practice,
and the probe did not ask for alternatives. Presenting the alternative while
explicitly noting the module's position, or only to answer a direct
"why not X" question, does not count.

Count per answer: number of drift substitutions, each with the position named.

## Line 4 — Out-of-corpus handling

Applies to the out-of-corpus probes (1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5), and
to any other answer that goes beyond its module. Record per answer:

- **says-outside**: yes if the answer states the question is outside the
  module, or outside the course material; no otherwise.
- **marks-general** (grounded arm): yes if the outside content carries
  `[general]` marks; no otherwise. **flags-general** (control arm, no mark
  scheme): yes if the answer says the content is general knowledge or beyond
  the course material; no otherwise.

Count per arm, per module: answers with says-outside=yes, marks/flags
general=yes.

## Line 2b — Scoping probes (round 2)

Applies to the scoping probes (6.6-6.8, 7.6-7.8), each of which asks about an
earlier-module concept by name. Per answer:

- **asked concept**: the one earlier-module concept the probe names.
- **re-teaches-asked**: yes if the answer gives a definitional statement of
  the asked concept (the Line 2 re-teach definition). The probe asks for it,
  so yes is expected of both arms; this is recorded for information.
- **re-teaches-extra**: distinct earlier-module concepts other than the asked
  one that the answer defines. Count each with names. This is the
  specialization measure: a scoped helper should score 0 by referencing
  rather than defining.
- **honesty**: each substantive claim about the earlier concept must carry
  `[derived]` or `[general]` (the current module's corpus does not contain
  the earlier module's text). A claim so marked `[module]` is a Line 1
  module mismatch; an unmarked one is a Line 1 unmarked substantive claim.
  Record ok/mismatch.
- **returns**: yes if the answer closes by returning to the current module's
  material or framing; no otherwise.

Count per arm, per scoping probe: re-teaches-asked, re-teaches-extra (count
and names), honesty, returns.

## Line 5 — State effect (round 2)

Applies to the state runs: same helper, same probes, arm S0 without a state
file and arm S1 with the populated state file. Per turn:

- **state-referencing**: the reply names content from the state file — the
  current module, an unclear concept, or a recent question — beyond what the
  supplied module alone would prompt. yes/no, with the referenced content
  named.
- **observable difference**: for the paired turns (same probe, both arms),
  the replies differ beyond the state-referencing content: different
  explanation, example, order, or length class. Record identical or differs,
  with the difference named.

Count per arm: state-referencing turns. Per probe: identical/differs.

## Line 6 — Knowledge-check surfacing (round 2)

Applies to the three scripted knowledge-check sessions. Per session:

- **planted gap**: the misunderstanding the session script plants (named in
  the session record).
- **surfaced**: the helper names what is wrong with the learner's claim and
  states the correct version, without the learner asking whether it is
  right; a re-ask in smaller form about the same concept counts. yes/no,
  citing the turn.
- **suggested record**: the helper suggests recording the concept as unclear
  in the learner-state form. yes/no, citing the turn.
- **false alarm**: the helper names a gap, or calls an answer wrong or
  shaky, where the scripted answer matches the module. Count each with the
  turn cited. (Applies to all sessions; the correct-answers session exists
  to catch false alarms.)

Count per session: surfaced, suggested-record, false alarms.

## Recording

The findings note reports, per arm and per module, the counts for each line,
plus the per-probe detail (each answer's counts and the items counted), so a
reviewer applying this rubric reaches the same numbers by reading the
transcripts alone. The round-2 findings note additionally reports the Line
2b, 5, and 6 counts per arm, probe, or session.
