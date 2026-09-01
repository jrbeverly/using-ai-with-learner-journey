# Learner conversation transcript
## Run — 2026-09-28T18:42:17Z (replay)
- Helper: control-assistant (helpers/control-assistant.md)
- Module: modules/03-vpns-and-routing.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=8192)
- Base URL: https://api.deepseek.com/anthropic

### Turn 1
- Helper: control-assistant
- Module: modules/03-vpns-and-routing.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=8192)
- Time: 2026-09-28T18:42:31Z

Learner:

The module says a Site-to-Site VPN makes two private networks behave as if directly connected. Connect this to Modules 1 and 2: why is a path across the public internet needed at all, and what does the tunnel hide?

Helper reply (verbatim):

The path across the public internet is needed because the VPC and the office/data center are in different physical locations and are not connected by a private cable. From Module 1, private RFC 1918 addresses such as `10.8.0.0/16` are not routable across the public internet. From Module 2, a VPC is isolated by design: private subnets do not have direct public connectivity, and exposing them directly would defeat the point of keeping them private.

So if the two private networks need to talk, there are two choices:

- a dedicated private physical connection, such as AWS Direct Connect, or
- a path over the public internet — which is where the VPN comes in.

The tunnel hides the private nature of the traffic from the public internet. A packet from `10.8.0.0/16` to a VPC subnet is wrapped inside an IPsec packet whose outer source and destination are the public VPN endpoints — for example, the customer gateway device and the AWS virtual private gateway or transit gateway. The inner private IP addresses, topology, and payload are encrypted.

To the internet, it looks like only opaque, encrypted traffic flowing between the two VPN endpoints. To the two private networks, it looks like they are directly connected, because their private routes and addressing work across the tunnel without being exposed.

### Turn 2
- Helper: control-assistant
- Module: modules/03-vpns-and-routing.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=8192)
- Time: 2026-09-28T18:42:36Z

Learner:

Explain that more simply.

Helper reply (verbatim):

Think of two private networks as two locked buildings that are far apart. To connect them, they use the public internet — a public road — because they don’t have their own private road between them.

But private network traffic normally can’t travel safely over that public road: it uses private addresses and should not be exposed.

A VPN fixes this by putting the private traffic inside an encrypted “armored truck.” The truck travels over the public internet between the two VPN devices. Outsiders can see the truck moving, but they can’t see what is inside it — not the private addresses, not the data.

So to the two private networks, it feels like they are directly connected. The tunnel hides their private traffic from the public internet.

### Turn 3
- Helper: control-assistant
- Module: modules/03-vpns-and-routing.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=8192)
- Time: 2026-09-28T18:43:02Z

Learner:

Give me a concrete example: the office network is 10.8.0.0/16 and the VPC is 10.1.0.0/16, connected by a Site-to-Site VPN. What must routing on both sides know for a packet to cross, and how do static routes and BGP differ at doing it?

Helper reply (verbatim):

**Concrete example**

Office network: `10.8.0.0/16`  
VPC network: `10.1.0.0/16`  
Connection: Site-to-Site VPN between the office customer gateway device and an AWS virtual private gateway, say `vgw-123`.

A packet from office server `10.8.0.25` to a VPC instance `10.1.0.75` needs two things:

1. **On the office router**  
   A route that says:  
   `10.1.0.0/16 → send into the IPsec tunnel`

2. **On the AWS side**  
   A VPC route table entry that says:  
   `10.8.0.0/16 → target vgw-123`

The second route is for the return traffic. Without it, the packet might reach the VPC instance, but the reply cannot get back to the office.

If you use a transit gateway instead of a virtual private gateway, the principle is the same: the VPC route points to the transit gateway, and the transit gateway route table points to the VPN attachment.

---

**Static routes vs BGP**

**Static routes** are manual:

- Office router:  
  `ip route 10.1.0.0 255.255.0.0 <tunnel interface or next hop>`

- AWS VPC route table:  
  `10.8.0.0/16 → vgw-123`

Problems:

- If either side adds a new network prefix, you must manually update both sides.
- Static routes alone do not react dynamically to tunnel failures.

**BGP** does this automatically:

- The office router advertises: `10.8.0.0/16`
- AWS advertises: `10.1.0.0/16`

Each side learns the other side’s routes dynamically. In AWS, you enable **route propagation** on the VPC route table so learned routes appear automatically.

BGP also helps with the two IPsec tunnels: each tunnel has its own BGP session. If one tunnel fails, its BGP session drops and the routes are withdrawn, allowing the other tunnel to carry the traffic.

That is why the module says: **prefer BGP wherever the customer gateway supports it**.

### Turn 4
- Helper: control-assistant
- Module: modules/03-vpns-and-routing.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=8192)
- Time: 2026-09-28T18:43:24Z

Learner:

In the diagram at the end of the module, trace the path of an engineer's laptop into VPC B, and separately the data center's path into VPC A. Name every component each path passes through.

Helper reply (verbatim):

**Data center → VPC A**

A host in the data center `10.8.0.0/16` sends a packet. The path is:

1. **Data center host** — source of the traffic.
2. **Customer gateway device** — the on-premises router that sends the packet into the VPN.
3. **One of the two IPsec tunnels** — the packet is encrypted and crosses the public internet through one tunnel. The diagram shows this as the `two IPsec tunnels ===========` link.
4. **VPN attachment on the transit gateway** — the AWS-side termination point of the IPsec tunnel.
5. **Transit gateway** — its route table decides where to send the traffic.
6. **VPC A attachment** — the connection from the transit gateway into VPC A.
7. **Destination in VPC A** — the instance or resource in `10.1.0.0/16`.

---

**Engineer laptop → VPC B**

1. **Engineer laptop** — source of the traffic.
2. **Client VPN TLS session** — the encrypted connection from the laptop. The diagram shows this as `Client VPN (TLS)`.
3. **AWS Client VPN endpoint** — the AWS-side service that terminates the TLS connection.
4. **Transit gateway** — in this architecture, the Client VPN endpoint is associated with the transit gateway.
5. **VPC B attachment** — the connection from the transit gateway into VPC B.
6. **Destination in VPC B**.

A note: the **route tables** inside the transit gateway and the VPCs are not drawn, but they are the hidden decision points that actually direct traffic to VPC A or VPC B in these paths.

### Turn 5
- Helper: control-assistant
- Module: modules/03-vpns-and-routing.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=8192)
- Time: 2026-09-28T18:43:49Z

Learner:

How would I set up a WireGuard tunnel into my VPC instead of using IPsec?

Helper reply (verbatim):

**Short answer:** AWS does not offer a managed WireGuard VPN service. AWS Site-to-Site VPN and AWS Client VPN are IPsec/OpenVPN-based. To use WireGuard into a VPC, you run your own WireGuard endpoint on an EC2 instance and manage it yourself.

Here is the general setup.

---

### Scenario: connecting an office network (10.8.0.0/16) to a VPC (10.1.0.0/16) with WireGuard

**AWS side**

1. Launch an EC2 instance in a public subnet of the VPC.
2. Give it an Elastic IP so its public address is stable.
3. In its security group:
   - Allow **inbound UDP 51820** from your office router’s public IP.
   - Allow outbound traffic as needed.
4. Disable **source/destination check** on the instance.
   - This lets the instance forward traffic that is not addressed to itself.
5. Install WireGuard on the instance.
6. Create a WireGuard interface, for example:

```ini
[Interface]
Address = 169.254.10.1/30
ListenPort = 51820
PrivateKey = <AWS-private-key>

[Peer]
PublicKey = <office-public-key>
AllowedIPs = 10.8.0.0/16
```

7. Enable IP forwarding on the instance:

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

8. In the VPC route tables for subnets that need to reach the office, add a route:

```
10.8.0.0/16 → target = the WireGuard EC2 instance network interface
```

**Office side**

1. Configure your on-premises WireGuard device with the reverse setup:

```ini
[Interface]
Address = 169.254.10.2/30
PrivateKey = <office-private-key>

[Peer]
PublicKey = <AWS-public-key>
Endpoint = <Elastic-IP>:51820
AllowedIPs = 10.1.0.0/16
```

2. On the office router, make sure traffic to `10.1.0.0/16` is sent into its WireGuard interface.

**Result**

- Office host `10.8.0.25` sends to `10.1.0.75`.
- Traffic is encrypted by WireGuard and sent to the EC2 instance’s Elastic IP.
- The EC2 instance decrypts it and forwards it into the VPC.
- Return traffic follows the VPC route table entry back through the instance and into the tunnel.

---

### For individual engineers or laptops

Instead of a site-to-site route, you can use the same EC2 WireGuard endpoint as a road-warrior server:

- Each laptop has its own WireGuard peer configuration.
- The EC2 instance usually uses **NAT** so that VPC resources see traffic as coming from the WireGuard instance’s private IP.
- This avoids adding many client subnets to VPC route tables.

Example NAT rule on the EC2 instance:

```bash
sudo iptables -t nat -A POSTROUTING -o eth0 -s 10.44.0.0/24 -j MASQUERADE
```

Where `10.44.0.0/24` is the WireGuard client address pool.

---

### Important differences from AWS Site-to-Site VPN

| AWS Site-to-Site VPN | Self-managed WireGuard on EC2 |
|---|---|
| Managed by AWS | Managed by you |
| IPsec, two tunnels automatically | WireGuard, typically one tunnel unless you build HA |
| BGP route propagation available | No native BGP; you maintain routes manually |
| Integrated with VGW/TGW | Plain EC2 instance in a VPC |
| AWS support and SLAs | You are responsible for patching, scaling, and HA |

For production, a single WireGuard EC2 instance is a single point of failure. You would typically run at least two instances in different Availability Zones and handle failover yourself.
