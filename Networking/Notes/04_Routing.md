## Dynamic Routing

**What it is:**
- Dynamic routing is when routers automatically learn about networks and build their routing tables by exchanging information with neighboring routers — instead of an administrator manually configuring every route (static routing).
- Once configured, routers running a dynamic routing protocol continuously share reachability information with each other, so each router ends up with a routing table describing how to reach networks it isn't even directly connected to.

**Why it matters:**
- The biggest advantage over static routing is **automatic adaptation**. If a link or router in the network fails, routers running a dynamic protocol will detect that the route is gone and automatically recalculate an alternate path (if one exists) — without any manual reconfiguration.
- With static routing, if the configured path fails, traffic keeps getting sent toward a dead end until someone manually fixes it. Dynamic routing removes that single point of manual dependency, which matters a lot at real-world scale where networks change constantly (links flap, new subnets get added, hardware fails).

**Types of dynamic routing protocols (by scope):**

- **IGP (Interior Gateway Protocol)** — used *within* a single Autonomous System (AS) — i.e. within one organization's network (e.g. one company).
- **EGP (Exterior Gateway Protocol)** — used *between* different Autonomous Systems — i.e. between separate organizations/ISPs. In practice, **BGP (Border Gateway Protocol)** is the only EGP actually used in the real world (it's what runs the internet's backbone routing between ISPs and large networks).
- Example: ISP A and ISP B are each their own AS; Company A and Company B are also their own ASes. Routes get exchanged *within* each AS using an IGP, and *between* ASes using BGP.

**Types of dynamic routing protocols (by algorithm):**

| Type | How it works | Example protocols |
|---|---|---|
| **Distance Vector** | Each router shares its entire routing table (or relevant parts of it) with directly connected neighbors. Routers don't have a full picture of the network topology — they just trust what neighbors tell them ("routing by rumor"). | RIP |
| **Link State** | Each router builds a complete map (topology database) of the entire network by flooding link-state information to all routers, then independently runs a shortest-path algorithm (like Dijkstra/SPF) to calculate the best route to every destination. | OSPF, IS-IS |
| **Path Vector** | Similar to distance vector, but also carries the AS path information along with each route, which is used to detect and prevent loops between autonomous systems. | BGP |

**Key commands / steps:**
- No single universal command set here since this covers the concept of dynamic routing broadly — the actual configuration commands are protocol-specific (e.g. `router ospf`, `router eigrp`, `router bgp`), which are covered separately.

**How routers choose between multiple routes — Administrative Distance (AD):**
- If a router learns about the **same destination network** from two *different* routing sources (e.g. a static route and an OSPF route, or OSPF and EIGRP), it needs a way to decide which one to trust and install in the routing table.
- **Administrative Distance (AD)** is a trustworthiness rating assigned to each route source. **Lower AD = more trusted = preferred.**

| Route Source | Default AD |
|---|---|
| Directly connected | 0 |
| Static route | 1 |
| eBGP (external BGP) | 20 |
| EIGRP | 90 |
| OSPF | 110 |
| IS-IS | 115 |
| RIP | 120 |
| iBGP (internal BGP) | 200 |
| Unknown / unreachable | 255 |

- Whichever route source has the lowest AD for a given destination wins and gets installed in the routing table — the others are kept as backups but not used unless the preferred one becomes unavailable.

**How routers choose between multiple routes from the *same* protocol — Metric:**
- If two routes to the same destination come from the **same** routing protocol (so they have identical AD), the router compares their **metric** instead — a protocol-specific value used to judge which path is "best" according to that protocol's own logic.
- Different protocols calculate metric completely differently, so metrics **cannot be meaningfully compared across different protocols**. For example, an OSPF route to 192.168.4.0/24 might have a metric of 20, while an EIGRP route to the same network might have a metric of 3328 — these numbers aren't on the same scale and can't be used to judge which protocol's route is objectively "better." That comparison is exactly what Administrative Distance exists to resolve instead.

**Common confusion / gotcha:**
- It's easy to assume a "lower metric number from any protocol" always wins overall — but metric only matters for breaking ties *within* the same protocol. Between different protocols, **AD decides first**, and metric is irrelevant at that stage.
- Static routes having an AD of 1 (very trusted, second only to directly connected routes) is why a manually configured static route will always override a dynamically learned route to the same destination, unless the static route is deliberately configured with a higher AD (a "floating static route") specifically to act as a backup.

**What breaks if this goes wrong:**
- If AD is misunderstood, someone might assume a dynamic protocol's route will automatically take priority over a static route — leading to confusion when traffic keeps following the static route even after the dynamic protocol has learned a "better" path.
- If a network relies purely on static routing and a link goes down, traffic keeps getting forwarded toward that dead link until manually fixed — this is the core weakness dynamic routing is designed to solve.

**Note to self:**
- The two-step decision process finally made sense as: **first AD decides *which protocol's* route to trust, then metric decides *which specific path* within that same protocol is best.** Keeping those two steps mentally separate stopped the confusion between "which is better, AD or metric."
