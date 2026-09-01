#!/bin/sh
# Round-2 experiment runs.
#
# Specialization: modules 6 and 7 (the modules with a specialized helper),
# every probe in those sections — original plus scoping additions — through
# both arms, the general grounded tutor and the specialized helper, at
# identical model settings (probe-run-config.json, max_tokens=8192).
# Learner state: module 1 probes through the grounded tutor twice, once
# without a state file and once with learner-state.example.md; nothing else
# differs. Knowledge checks: the three scripted sessions against the
# knowledge-check helper at the runner's shared default (max_tokens=1024),
# like the smoke run.
#
# A run whose model replies have no text blocks is retried from a clean
# transcript; failed-attempt logs are kept for the record.
set -eu
cd "$(dirname "$0")"

python3 make-replays.py

attempts=3
run_one() {
  name=$1; helper=$2; module=$3; replay=$4; transcript=$5; config=$6; shift 6
  attempt=1
  while :; do
    if python3 runner.py \
        --helper "helpers/$helper.md" \
        --module "$module" \
        --replay "$replay" \
        --transcript "$transcript" \
        --config "$config" \
        "$@" \
        > "runs/$name.log"; then
      break
    fi
    mv "runs/$name.log" "runs/$name.attempt-$attempt-failed.log"
    rm -f "$transcript"
    attempt=$((attempt + 1))
    if [ "$attempt" -gt "$attempts" ]; then
      echo "run-experiments: $name failed $attempts attempts" >&2
      exit 1
    fi
  done
}

mkdir -p runs

# Specialization runs.
run_one spec-m06-grounded grounded-tutor modules/06-mutual-tls.md replays/probes-m06.txt transcripts/spec-m06-grounded.md probe-run-config.json
run_one spec-m06-mtls mtls-tutor modules/06-mutual-tls.md replays/probes-m06.txt transcripts/spec-m06-mtls.md probe-run-config.json
run_one spec-m07-grounded grounded-tutor modules/07-combined-architecture.md replays/probes-m07.txt transcripts/spec-m07-grounded.md probe-run-config.json
run_one spec-m07-architecture architecture-tutor modules/07-combined-architecture.md replays/probes-m07.txt transcripts/spec-m07-architecture.md probe-run-config.json

# Learner-state runs: same helper, same probes, with and without the state file.
run_one state-m01-none grounded-tutor modules/01-networking-foundations.md replays/probes-m01.txt transcripts/state-m01-none.md probe-run-config.json
run_one state-m01-state grounded-tutor modules/01-networking-foundations.md replays/probes-m01.txt transcripts/state-m01-state.md probe-run-config.json --state learner-state.example.md

# Knowledge-check sessions.
run_one check-m06-planted knowledge-check modules/06-mutual-tls.md examples/replay-check-m06-planted.txt transcripts/check-m06-planted.md runner-config.json
run_one check-m05-explain knowledge-check modules/05-certificates-and-trust.md examples/replay-check-m05-explain.txt transcripts/check-m05-explain.md runner-config.json
run_one check-m06-correct knowledge-check modules/06-mutual-tls.md examples/replay-check-m06-correct.txt transcripts/check-m06-correct.md runner-config.json

echo "run-experiments: all runs complete"
