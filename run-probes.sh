#!/bin/sh
# Runs every probe against both arms, replay mode, one shared config.
# probe-run-config.json raises the output budget beyond the runner default:
# at max_tokens=1024 the model spends the whole budget on reasoning and the
# walk-through probes get no text answer (see findings.md). A run whose model
# replies have no text blocks is retried from a clean transcript;
# failed-attempt logs are kept for the record.
set -eu
cd "$(dirname "$0")"

python3 make-replays.py

mkdir -p runs
attempts=3
while IFS="$(printf '\t')" read -r tag module; do
  for arm in control-assistant grounded-tutor; do
    attempt=1
    while :; do
      if python3 runner.py \
          --helper "helpers/$arm.md" \
          --module "$module" \
          --replay "replays/probes-$tag.txt" \
          --transcript "transcripts/probes-$tag-$arm.md" \
          --config probe-run-config.json \
          > "runs/probes-$tag-$arm.log"; then
        break
      fi
      mv "runs/probes-$tag-$arm.log" "runs/probes-$tag-$arm.attempt-$attempt-failed.log"
      rm -f "transcripts/probes-$tag-$arm.md"
      attempt=$((attempt + 1))
      if [ "$attempt" -gt "$attempts" ]; then
        echo "run-probes: probes-$tag-$arm failed $attempts attempts" >&2
        exit 1
      fi
    done
  done
done < replays/manifest.txt

echo "run-probes: all runs complete"
