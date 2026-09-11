# Module 1: Foundations

## Network Devices

**What it is:**
- A computer network is a digital telecommunications network that allows nodes (devices) to share resources with each other.
- Even the simplest possible network — two PCs connected with a single cable — counts as a network, because through that cable the two devices can share resources with one another.
- Two core roles exist in any network interaction:
  - **Client** — a device that accesses a service made available by a server.
  - **Server** — a device that provides a service or function for clients (e.g. serving a file, hosting an application).
- A single device isn't permanently "a client" or "a server" — the same PC can act as a client in one interaction and a server in another, depending on the situation.

**Why it matters:**
- We don't connect end devices (PCs, servers) directly to each other in real networks — that doesn't scale. Instead, connections are aggregated through a dedicated device: the **switch**.
- **Switch:** has many interfaces (ports) for end hosts to connect to, and is responsible for forwarding traffic *within* a single LAN.
- Switches, on their own, cannot connect a LAN to the internet or pass traffic between two separate LANs — this is where the **router** comes in: a router provides connectivity *between* networks (e.g. connecting LAN1 to LAN2, or a LAN to a WAN/the internet).
- **Firewall:** a specialty network device placed strategically (centrally, or at the edge of a network) to monitor and control traffic entering or exiting a network, based on configured rules.
  - **Network firewalls** — dedicated hardware devices that filter traffic passing between a WAN and a LAN.
  - **Host-based firewalls** — software applications running on an individual machine that filter traffic entering/exiting that specific device.

**Common confusion / gotcha:**
- It's easy to think a switch alone can "run a network," but a switch only handles Layer 2 forwarding *inside* one LAN. Without a router, that LAN is isolated from every other network, including the internet.
- A firewall isn't necessarily one single box — the same protective function can exist as a hardware device (network firewall) or as software running on an endpoint (host-based firewall), and both are commonly used together for layered security.

**What breaks if this goes wrong:**
- If devices are connected without a switch aggregating them (e.g. daisy-chained directly), the network becomes fragile and doesn't scale — this isn't how real networks are built.
- If a LAN has no router, hosts inside it can talk to each other but have no way to reach any other network or the internet.

**Note to self:**
- The client/server distinction is about the *role in a given exchange*, not a fixed identity of the device — this took a moment to click, but it makes sense once you think of a laptop that both requests a webpage (client) and shares a printer (server) at the same time.

---

## Interfaces & Cables

**What it is:**
- Before devices can exchange data meaningfully, they need to agree on **protocols and standards** — a set of rules defining how data should be communicated between devices over a network. If two devices "speak" different protocols, they can't exchange data at all.
- **Ethernet** is a collection of network protocols and standards that define how wired LAN communication works. These standards were formalized by the **IEEE** (Institute of Electrical and Electronics Engineers) starting with IEEE 802.3 in 1983.

**Key specs / reference tables:**

*Bit/byte conversions used when reading data rates:*
- 1 kilobit (kb) = 1,000 bits
- 1 megabit (Mb) = 1,000,000 bits
- 1 gigabit (Gb) = 1,000,000,000 bits
- Data on a wire is measured in **bits**, not bytes.

*Common Ethernet speed standards:*

| Speed | Common Name | IEEE Standard | Informal Name | Max Length (copper) |
|---|---|---|---|---|
| 10 Mbps | Ethernet | 802.3i | 10Base-T | 100 m |
| 100 Mbps | Fast Ethernet | 802.3u | 100Base-T | 100 m |
| 1 Gbps | Gigabit Ethernet | 802.3ab | 1000Base-T | 100 m |
| 10 Gbps | 10 Gig Ethernet | 802.3an | 10GBase-T | 100 m |

*Fiber-based standards (for longer distances):*

| Informal Name | IEEE Standard | Speed | Cable Type | Max Length |
|---|---|---|---|---|
| 1000Base-LX | 802.3z | 1 Gbps | Multimode or Single-mode | 550 m / 5 km |
| 10GBase-SR | 802.3ae | 10 Gbps | Multimode | 400 m |
| 10GBase-LR | 802.3ae | 10 Gbps | Single-mode | 10 km |
| 10GBase-ER | 802.3ae | 10 Gbps | Single-mode | 30 km |

*(Note: "Base" refers to baseband signaling; "T" indicates twisted-pair cabling.)*

**UTP (Unshielded Twisted Pair) cables:**
- No metallic shielding — which could make them vulnerable to electrical interference (EMI) — but the wires within each pair are twisted together specifically to help cancel out that interference.
- Contains 4 twisted pairs (8 wires total).
- **10Base-T / 100Base-T** connections only use 2 of the 4 pairs — one pair to Transmit (Tx), one to Receive (Rx):
  - Pins 1, 2 → Transmit
  - Pins 3, 6 → Receive
- **Full duplex transmission** means both connected devices can send data at the same time with no risk of collisions, because separate wire pairs are used for transmitting and receiving.
- **1000Base-T / 10GBase-T** (Gigabit and above) use *all 4 pairs*, with each pair operating bidirectionally — this is part of why these standards can reach much higher speeds.

**Straight-through vs. crossover cables:**
- A **straight-through cable** connects the same pin number on one end to the same pin number on the other end (pin 1 → pin 1, pin 2 → pin 2, etc.). This is used when connecting *dissimilar* device types, e.g. PC–switch, switch–router.
- A **crossover cable** reverses the transmit/receive pairs on each end (e.g. pins 1,2,3,6 on one end map to pins 3,6,1,2 on the other). This is used when connecting *similar* device types directly, e.g. router–router, switch–switch, PC–router.
- Every copper Ethernet cable has an RJ-45 connector on each end.

**Transmit/Receive pin reference by device type:**

| Device Type | Transmit Pins | Receive Pins |
|---|---|---|
| Router | 1, 2 | 3, 6 |
| PC | 1, 2 | 3, 6 |
| Switch | 3, 6 | 1, 2 |

**Auto MDI-X:**
- Most modern networking devices have moved past needing the "correct" straight-through or crossover cable at all — they include a feature called **Auto MDI-X**, which automatically detects the connection type and adjusts accordingly.

**Fiber optic cable:**
- Instead of sending an electrical signal over copper wiring, fiber cables send **light** over glass fibers. There are two connectors on each end — one for transmitting, one for receiving.
- **Cable structure (cross-section):**
  1. The fiber glass core itself
  2. Cladding that reflects light back into the core
  3. A protective buffer
  4. The outer jacket of the cable
- **Multimode fiber:**
  - Has a wider glass core than single-mode fiber.
  - The wider core allows light to enter at multiple angles/modes simultaneously.
  - Supports longer cable runs than UTP, but shorter than single-mode fiber.
  - Cheaper than single-mode fiber, due to cheaper LED-based SFP transmitters.
- **Single-mode fiber:**
  - Has a narrower glass core than multimode fiber.
  - Light enters at a single angle (mode) from a laser-based transmitter.
  - Supports the longest cable runs of any of these options — longer than both UTP and multimode fiber.
  - More expensive than multimode fiber, due to more expensive laser-based SFP transmitters.
- **SFP transceiver:** SFP = Small Form-Factor Pluggable — a modular port used in networking equipment (switches, routers, firewalls) to connect fiber (or sometimes copper) cabling.

**UTP vs. Fiber-Optic — comparison:**

| | UTP | Fiber-Optic |
|---|---|---|
| Cost | Lower | Higher |
| Max distance | Shorter | Longer |
| Vulnerability to EMI | Can be vulnerable | Not vulnerable |
| Port cost | RJ-45 ports are cheaper | SFP ports are more expensive (single-mode pricier than multimode) |
| Signal leakage / security | Emits a faint signal outside the cable, which could potentially be intercepted (a security consideration) | Emits no signal outside the cable (no equivalent security risk) |

**Common confusion / gotcha:**
- It's tempting to think crossover cables are "the special case" and straight-through is "the normal case" — but the actual rule is about whether the two connected devices are the *same type* (crossover) or *different types* (straight-through). With Auto MDI-X on modern hardware, this distinction barely matters in practice anymore, but it's still core exam/interview knowledge.
- Data rates are measured in **bits**, not bytes — mixing these up leads to a 8x miscalculation (1 byte = 8 bits), which is an easy mistake when eyeballing bandwidth numbers.

**What breaks if this goes wrong:**
- Using the wrong cable type (straight-through vs. crossover) on hardware *without* Auto MDI-X will prevent the link from coming up at all — no connectivity, no link light.
- Running UTP cable beyond its ~100 m limit causes signal degradation and unreliable or failed connectivity — this is exactly why fiber exists for longer runs.
- Choosing multimode fiber for a long-haul link that actually needs single-mode range will result in the link not reaching the required distance.

**Note to self:**
- The straight-through/crossover logic finally clicked by thinking of it as "if the devices are already speaking on matching pins, you need to cross them; if they're mismatched roles, straight-through already lines them up correctly."
