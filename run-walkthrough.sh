#!/bin/sh
# End-to-end walkthrough: one learner completes all seven modules in
# order, using the material (documents and the diagrams), every helper,
# and the learner-state file (walkthrough-state.md), recorded in one
# transcript (transcripts/walkthrough.md).
#
# Segments, in journey order (helper / module / replay):
#   00-control  control-assistant  module 1  pre-course big-picture question, no state
#   01-smoke    smoke-tutor         module 1  tutor questions (the helper the README
#                                            usage example pairs with module 1)
#   01-check .. 07-check   knowledge-check   one check session per module
#   02-tutor .. 05-tutor   grounded-tutor    modules 2-5
#   06-tutor    mtls-tutor          module 6  the module's specialized helper
#   07-tutor    architecture-tutor  module 7  the module's specialized helper
#
# Tutor segments run at max_tokens=8192 (probe-run-config.json), the
# budget round 1 found walk-through questions need: at the shared
# default of 1024 the model spends the whole output budget on reasoning
# and the diagram-trace turns get no text answer (see findings.md
# "Budget"). The first Module 1 tutor attempt at 1024 failed all three
# attempts that way; the logs are kept in runs/. The check segments and
# the pre-course control segment run at the shared default
# (runner-config.json, max_tokens=1024), like round 2's check sessions.
# Every tutor and check segment passes the learner state file; the
# script rewrites it at each module boundary to reflect what the
# recorded check sessions left clear or unclear, so the file evolves as
# the journey progresses.
#
# A run whose model replies have no text blocks is retried from a clean
# part transcript (3 attempts); failed-attempt logs are kept in runs/.
# Each completed segment is appended to transcripts/walkthrough.md.
#
# Usage:
#   sh run-walkthrough.sh reset        start a fresh transcripts/walkthrough.md
#   sh run-walkthrough.sh [segment]    run one named segment
#   sh run-walkthrough.sh finalize     write the learner's end-of-journey state (state_s8)
#   sh run-walkthrough.sh              run the whole journey in order, then finalize
set -eu
cd "$(dirname "$0")"

mkdir -p runs

state_s1() {
cat > walkthrough-state.md <<'EOF'
# Learner state

- Current module: modules/01-networking-foundations.md

## Concepts that remain unclear

- How NAT translates reply packets back to the private host

## Recent questions

- Why can't a private host talk to the internet without NAT?
- What does 0.0.0.0/0 actually match?
EOF
}

state_s2() {
cat > walkthrough-state.md <<'EOF'
# Learner state

- Current module: modules/02-private-connectivity-vpc.md

## Concepts that remain unclear

- (none — the Module 1 check resolved the NAT reply-translation question)

## Recent questions

- Why does the most specific matching prefix win?
- What must the NAT device remember to translate replies back?
EOF
}

state_s3() {
cat > walkthrough-state.md <<'EOF'
# Learner state

- Current module: modules/03-vpns-and-routing.md

## Concepts that remain unclear

- (none — the Module 2 check left nothing open)

## Recent questions

- Why is a NAT gateway outbound-only?
- What does stateful mean for a security group?
EOF
}

state_s4() {
cat > walkthrough-state.md <<'EOF'
# Learner state

- Current module: modules/04-tls-foundations.md

## Concepts that remain unclear

- (none — the Module 3 check left nothing open)

## Recent questions

- Why do VPN connections carry two equivalent tunnels?
- What does BGP do that static routes cannot?
EOF
}

state_s5() {
cat > walkthrough-state.md <<'EOF'
# Learner state

- Current module: modules/05-certificates-and-trust.md

## Concepts that remain unclear

- Why the stream is encrypted with the session key rather than the server's public key (I answered this wrong in the Module 4 check before correcting it)

## Recent questions

- What makes confidentiality and integrity automatic?
- Why does the handshake use asymmetric cryptography at all?
EOF
}

state_s6() {
cat > walkthrough-state.md <<'EOF'
# Learner state

- Current module: modules/06-mutual-tls.md

## Concepts that remain unclear

- What revocation covers that the validity period does not (in the Module 5 check I described CRLs as checking whether a CA is still trusted)

## Recent questions

- Why does the root CA's self-signature end the chain of worth?
- What does the Private CA cost shape in Module 7?
EOF
}

state_s7() {
cat > walkthrough-state.md <<'EOF'
# Learner state

- Current module: modules/07-combined-architecture.md

## Concepts that remain unclear

- Which ALB mode validates at the edge (I had verify and passthrough swapped in the Module 6 check)

## Recent questions

- What exactly is reversed in mTLS?
- Why verify mode rather than passthrough?
EOF
}

state_s8() {
cat > walkthrough-state.md <<'EOF'
# Learner state

- Current module: modules/07-combined-architecture.md

## Concepts that remain unclear

- Where TLS ends between ALB and instance (the Module 7 check: the path and trust boundaries were right, but the ALB-to-instance hop being plain HTTP was not stated)

## Recent questions

- In the diagram, trace a request from the engineer's laptop to a service instance and back
- Why not rely on ACM auto-renewal for client certificates?
EOF
}

attempts=3
run_one() {
  name=$1; helper=$2; module=$3; replay=$4; with_state=$5; config=$6
  part="runs/$name.part.md"
  attempt=1
  while :; do
    rm -f "$part"
    state_arg=
    if [ "$with_state" = state ]; then
      state_arg="--state walkthrough-state.md"
    fi
    if python3 runner.py \
        --helper "helpers/$helper.md" \
        --module "$module" \
        --replay "$replay" \
        --transcript "$part" \
        --config "$config" \
        $state_arg \
        > "runs/$name.log"; then
      break
    fi
    mv "runs/$name.log" "runs/$name.attempt-$attempt-failed.log"
    rm -f "$part"
    attempt=$((attempt + 1))
    if [ "$attempt" -gt "$attempts" ]; then
      echo "run-walkthrough: $name failed $attempts attempts" >&2
      exit 1
    fi
  done
  tail -n +2 "$part" >> transcripts/walkthrough.md
  rm -f "$part"
}

run_segment() {
  case "$1" in
    walkthrough-00-control)
      run_one walkthrough-00-control control-assistant \
        modules/01-networking-foundations.md \
        examples/replay-walkthrough-00-control.txt nostate runner-config.json ;;
    walkthrough-01-smoke)
      state_s1
      run_one walkthrough-01-smoke smoke-tutor \
        modules/01-networking-foundations.md \
        examples/replay-walkthrough-01-smoke.txt state probe-run-config.json ;;
    walkthrough-01-check)
      run_one walkthrough-01-check knowledge-check \
        modules/01-networking-foundations.md \
        examples/replay-walkthrough-01-check.txt state runner-config.json ;;
    walkthrough-02-tutor)
      state_s2
      run_one walkthrough-02-tutor grounded-tutor \
        modules/02-private-connectivity-vpc.md \
        examples/replay-walkthrough-02-tutor.txt state probe-run-config.json ;;
    walkthrough-02-check)
      run_one walkthrough-02-check knowledge-check \
        modules/02-private-connectivity-vpc.md \
        examples/replay-walkthrough-02-check.txt state runner-config.json ;;
    walkthrough-03-tutor)
      state_s3
      run_one walkthrough-03-tutor grounded-tutor \
        modules/03-vpns-and-routing.md \
        examples/replay-walkthrough-03-tutor.txt state probe-run-config.json ;;
    walkthrough-03-check)
      run_one walkthrough-03-check knowledge-check \
        modules/03-vpns-and-routing.md \
        examples/replay-walkthrough-03-check.txt state runner-config.json ;;
    walkthrough-04-tutor)
      state_s4
      run_one walkthrough-04-tutor grounded-tutor \
        modules/04-tls-foundations.md \
        examples/replay-walkthrough-04-tutor.txt state probe-run-config.json ;;
    walkthrough-04-check)
      run_one walkthrough-04-check knowledge-check \
        modules/04-tls-foundations.md \
        examples/replay-walkthrough-04-check.txt state runner-config.json ;;
    walkthrough-05-tutor)
      state_s5
      run_one walkthrough-05-tutor grounded-tutor \
        modules/05-certificates-and-trust.md \
        examples/replay-walkthrough-05-tutor.txt state probe-run-config.json ;;
    walkthrough-05-check)
      run_one walkthrough-05-check knowledge-check \
        modules/05-certificates-and-trust.md \
        examples/replay-walkthrough-05-check.txt state runner-config.json ;;
    walkthrough-06-tutor)
      state_s6
      run_one walkthrough-06-tutor mtls-tutor \
        modules/06-mutual-tls.md \
        examples/replay-walkthrough-06-tutor.txt state probe-run-config.json ;;
    walkthrough-06-check)
      run_one walkthrough-06-check knowledge-check \
        modules/06-mutual-tls.md \
        examples/replay-walkthrough-06-check.txt state runner-config.json ;;
    walkthrough-07-tutor)
      state_s7
      run_one walkthrough-07-tutor architecture-tutor \
        modules/07-combined-architecture.md \
        examples/replay-walkthrough-07-tutor.txt state probe-run-config.json ;;
    walkthrough-07-check)
      run_one walkthrough-07-check knowledge-check \
        modules/07-combined-architecture.md \
        examples/replay-walkthrough-07-check.txt state runner-config.json ;;
    *)
      echo "run-walkthrough: unknown segment '$1'" >&2
      exit 1 ;;
  esac
}

all_segments="walkthrough-00-control walkthrough-01-smoke walkthrough-01-check walkthrough-02-tutor walkthrough-02-check walkthrough-03-tutor walkthrough-03-check walkthrough-04-tutor walkthrough-04-check walkthrough-05-tutor walkthrough-05-check walkthrough-06-tutor walkthrough-06-check walkthrough-07-tutor walkthrough-07-check"

if [ $# -eq 0 ]; then
  rm -f transcripts/walkthrough.md
  echo "# Learner conversation transcript" > transcripts/walkthrough.md
  for segment in $all_segments; do
    run_segment "$segment"
  done
  state_s8
  echo "run-walkthrough: all segments complete"
  exit 0
fi

if [ "$1" = reset ]; then
  rm -f transcripts/walkthrough.md
  echo "# Learner conversation transcript" > transcripts/walkthrough.md
  echo "run-walkthrough: transcript reset"
  exit 0
fi

if [ "$1" = finalize ]; then
  state_s8
  echo "run-walkthrough: learner state finalized"
  exit 0
fi

run_segment "$1"
echo "run-walkthrough: $1 complete"
