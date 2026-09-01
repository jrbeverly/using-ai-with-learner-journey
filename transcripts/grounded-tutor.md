# Learner conversation transcript
## Run — 2026-09-28T17:40:53Z (replay)
- Helper: grounded-tutor (helpers/grounded-tutor.md)
- Module: modules/01-networking-foundations.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Base URL: https://api.deepseek.com/anthropic

### Turn 1
- Helper: grounded-tutor
- Module: modules/01-networking-foundations.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Time: 2026-09-28T17:40:59Z

Learner:

What does a route table do when a packet arrives?

Helper reply (verbatim):

When a packet arrives, the router looks up the packet’s destination address in its route table [module]. The route table maps prefixes to next hops — either another router or “local” for a directly attached network [module]. The router does not just use the first row that matches; it chooses the most specific matching prefix [module][derived]. For example, in the module’s diagram, a packet for `10.0.2.9` matches `10.0.2.0/24`, so router A forwards it to next hop `10.0.9.2` rather than sending it out the default route [module]. If no more specific prefix matches, the `0.0.0.0/0` default route catches the traffic [module].

### Turn 2
- Helper: grounded-tutor
- Module: modules/01-networking-foundations.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Time: 2026-09-28T17:41:07Z

Learner:

Why does the most specific matching prefix win?

Helper reply (verbatim):

The module doesn’t spell out the reason directly, but it follows from how the route table is described. The entry `0.0.0.0/0` matches every possible destination [module]. If the most specific match didn’t win, that catch-all would always be chosen and no other route could ever be used [derived]. A prefix like `10.0.2.0/24` fixes more bits, so it matches a smaller, more precise set of addresses than a broad prefix does [derived]. That lets the router make a more specific next-hop decision, which is why the default route is only used “when nothing more specific matches” [module].
