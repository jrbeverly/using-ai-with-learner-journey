# Learner conversation transcript
## Run — 2026-09-28T17:35:01Z (replay)
- Helper: smoke-tutor (helpers/smoke-tutor.md)
- Module: modules/01-networking-foundations.md
- Learner state: present (learner-state.example.md)
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Base URL: https://api.deepseek.com/anthropic

### Turn 1
- Helper: smoke-tutor
- Module: modules/01-networking-foundations.md
- Learner state: present (learner-state.example.md)
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Time: 2026-09-28T17:35:04Z

Learner:

What does a route table do when a packet arrives?

Helper reply (verbatim):

When a router receives a packet, it looks up the packet’s destination address in its route table. The route table contains entries mapping address prefixes to a next hop — either another router or “local” for directly attached networks. The router uses the most specific matching prefix to decide where to forward the packet next. [module]

If no more specific entry matches, the router uses the default route, `0.0.0.0/0`, which matches every destination and sends traffic to the configured next hop. [module] A host applies the same logic in miniature: traffic for its own subnet goes directly to the destination, while everything else goes to its default gateway. [module]

### Turn 2
- Helper: smoke-tutor
- Module: modules/01-networking-foundations.md
- Learner state: present (learner-state.example.md)
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Time: 2026-09-28T17:35:07Z

Learner:

Why does the most specific matching prefix win?

Helper reply (verbatim):

The module states that “the most specific matching prefix wins” but does not explain why. [module]

[general] In networking, this is usually called “longest prefix match.” A more specific prefix describes a smaller, more precise set of destinations, so it is treated as a better match than a broad prefix like `0.0.0.0/0`. This lets routers have a general default route while still overriding it for particular networks, which keeps routing tables smaller and more manageable.
