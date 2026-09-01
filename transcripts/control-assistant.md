# Learner conversation transcript
## Run — 2026-09-28T17:40:39Z (replay)
- Helper: control-assistant (helpers/control-assistant.md)
- Module: modules/01-networking-foundations.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Base URL: https://api.deepseek.com/anthropic

### Turn 1
- Helper: control-assistant
- Module: modules/01-networking-foundations.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Time: 2026-09-28T17:40:41Z

Learner:

What does a route table do when a packet arrives?

Helper reply (verbatim):

When a packet arrives, a router looks at the packet's **destination IP address** and checks its **route table** to decide where to forward it.

The route table contains entries that map a destination prefix to a next hop. For example:

- `10.0.1.0/24` → local (directly attached network)
- `10.0.2.0/24` → `10.0.9.2` (another router)
- `0.0.0.0/0` → `10.0.9.1` (default route)

The router picks the **most specific matching prefix**. If no more specific route matches, it uses the default route `0.0.0.0/0`, when one exists. The packet is then sent to the chosen next hop, or delivered directly if the destination is on a local network.

### Turn 2
- Helper: control-assistant
- Module: modules/01-networking-foundations.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Time: 2026-09-28T17:40:50Z

Learner:

Why does the most specific matching prefix win?

Helper reply (verbatim):

The most specific matching prefix wins because it represents the most precise routing information for that destination.

Routing uses **longest prefix match**: the entry that matches the largest number of leading bits in the destination address is the one chosen.

For example, a packet to `10.0.2.9` may match all of these:

- `0.0.0.0/0` — matches everything
- `10.0.0.0/8` — matches any `10.x.x.x`
- `10.0.2.0/24` — matches only `10.0.2.x`

The router uses `10.0.2.0/24` because it is the most specific. That route was explicitly defined for that smaller address range, so it is likely to be the correct or more direct path. The broader routes act as fallbacks, not as equally specific choices.

This design allows hierarchical routing: a few broad routes plus narrower exceptions.
