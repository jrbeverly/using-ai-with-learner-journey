# Using AI with Learner Journey

> [!WARNING]
> **AI-authored:** This change was autonomously planned and implemented by an AI software factory from a human-authored specification, with possible subsequent human review or modification.

A proof of concept for whether a small curated knowledge corpus plus tuned AI course helpers produces a better guided learning experience than an unconstrained chatbot. The subject is private networking and mutual TLS in AWS; the corpus is the numbered modules under `modules/`, read in order.

```sh
python3 runner.py --helper helpers/smoke-tutor.md \
                  --module modules/01-networking-foundations.md \
                  [--state learner-state.example.md] \
                  [--replay examples/replay-smoke.txt] \
                  [--transcript transcripts/out.md] \
                  [--config runner-config.json]
```

## Notes

- This isn't the right framing for the learning journey model
- Worth the exploration, but I think the realization is that slapping AI on-top of existing learning modules doesn't yield some "personal teacher assistant" (even at a small/moderate level).
- This helps reinforce pursuing in the direction of previous experiences for pre-computed knowledge bases, and speciality crafted knowledge bases

Overall, worthwhile experiment into the space, but is something that needs to be explored in other ways.
