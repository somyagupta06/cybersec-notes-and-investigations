# Module 1: Foundations

## EtherChannel

**What it is:**
- EtherChannel bundles multiple physical links between two switches (e.g. ASW1 and DSW1) into a single logical link.
- The rest of the network — including Spanning Tree — sees this bundle as *one* interface, not several separate ones, even though there are multiple physical cables underneath.

**Why it matters:**
- Without EtherChannel, if you run multiple redundant physical links between two switches, STP will block all but one of them to prevent a Layer 2 loop — wasting the extra bandwidth those links could offer.
- With EtherChannel, since STP sees only one logical link, *all* the bundled physical links stay active and forward traffic. This gives you both redundancy (if one physical link fails, traffic just uses the others) and aggregated bandwidth, without STP shutting anything down.
- This connects to bandwidth oversubscription: the total bandwidth demanded by all end hosts on a network is often greater than the bandwidth of the uplink connecting distribution/core switches. Some oversubscription is normal and acceptable — but if it's too high, users start noticing congestion. Adding more capacity via EtherChannel (rather than one single high-capacity link) is a practical way to relieve that congestion.

**How traffic is distributed across the bundle:**
- EtherChannel doesn't split a single flow's traffic across multiple links — that would risk frames arriving out of order.
- Instead, it load-balances *per flow*. A hash algorithm looks at fields such as source/destination MAC, source/destination IP, or source/destination port (depending on configuration) to decide which physical link a given flow will consistently use.
- Example: if PC1 talks to SRV1, that whole conversation goes over one physical link in the bundle. If PC1 also talks to SRV2, that separate flow might get hashed to a different physical link. This is how EtherChannel is also a basic form of load balancing.

**Ways to form an EtherChannel (negotiation protocols):**
| Protocol | Standard | Modes |
|---|---|---|
| PAgP (Port Aggregation Protocol) | Cisco proprietary | `desirable` (active), `auto` (passive) |
| LACP (Link Aggregation Control Protocol) | IEEE 802.3ad (industry standard) | `active`, `passive` |
| Static / ON | No protocol, manual | `on` only |

**Mode compatibility rules:**
- active + active → EtherChannel forms
- active + passive → EtherChannel forms
- passive + passive → does **not** form (both sides waiting for the other to initiate)
- on + on → forms (static, no negotiation)
- on + anything else (active/passive/auto/desirable) → does **not** form

**Key requirements before interfaces can bundle:**
- Member interfaces must have **matching configuration**:
  - Same duplex (full/half)
  - Same speed
  - Same switchport mode (access or trunk)
  - Same allowed VLANs / native VLAN (for trunk interfaces)
- The channel-group number must match **between interfaces on the same switch**, but it does *not* need to match the channel-group number used on the other switch (e.g. channel-group 1 on ASW1 can still form an EtherChannel with channel-group 2 on DSW1).

**Key commands:**
```
SW(config-if-range)# channel-protocol {pagp | lacp}
   → manually specifies which negotiation protocol the member interfaces should use

SW(config-if-range)# channel-group <number> mode <mode>
   → configures the interfaces to form the EtherChannel

SW# show etherchannel summary
   → verifies the status of an EtherChannel
```

**Layer 3 EtherChannel:**
- Modern network design increasingly favors Layer 3 connections between switches instead of Layer 2, because Layer 3 links don't need Spanning Tree at all — routed ports don't forward Layer 2 broadcasts, so a Layer 2 loop simply can't form over them.
- Example config (turning member interfaces into routed ports and bundling them into a Layer 3 EtherChannel):
```
ASW1(config)# int range g0/0-3
ASW1(config-if-range)# no switchport
ASW1(config-if-range)# channel-group 1 mode active
ASW1(config-if-range)# int po1
ASW1(config-if)# ip address 10.0.0.1 255.255.255.252
ASW1(config)# do show etherchannel summary
```
- Important nuance: even with EtherChannel in use, a Layer 2 loop can *still* occur if multiple switches are interconnected in a mesh and none of the connections between them are bundled as port-channels. If all inter-switch links are plain access/trunk ports (not part of an EtherChannel), Spanning Tree is still needed to block redundant paths and prevent broadcast storms.
- If, instead, all those inter-switch connections are made using **routed ports** (Layer 3), no Layer 2 broadcast can loop through them — so Spanning Tree becomes unnecessary for that part of the topology.

**Common confusion / gotcha:**
- It's easy to assume EtherChannel automatically prevents *all* loops in a network — it doesn't. It only prevents STP from blocking the *bundled* links. If switches are meshed together with separate, non-bundled links, a Layer 2 loop is still very much possible and STP is still needed there.
- The channel-group number is a local identifier per switch, not something that has to match end-to-end — this trips people up initially.

**What breaks if this goes wrong:**
- Mismatched member interface settings (different speed, duplex, VLANs, or switchport mode) will prevent the EtherChannel from forming correctly, or cause it to behave inconsistently.
- Wrong mode combination (e.g. passive + passive) means no EtherChannel forms at all — the links stay as separate interfaces, and STP will go back to blocking the redundant ones.
- Forgetting to secure non-bundled redundant links between meshed switches with STP (when not using Layer 3 connections) can lead to broadcast storms.

**Note to self:**
- The biggest realization here: EtherChannel's value isn't just "more bandwidth" — it's that it changes how STP *perceives* the topology, turning multiple physical links into one logical one so STP never needs to block any of them.
