# Learner conversation transcript
## Run — 2026-09-28T18:43:49Z (replay)
- Helper: grounded-tutor (helpers/grounded-tutor.md)
- Module: modules/03-vpns-and-routing.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=8192)
- Base URL: https://api.deepseek.com/anthropic

### Turn 1
- Helper: grounded-tutor
- Module: modules/03-vpns-and-routing.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=8192)
- Time: 2026-09-28T18:44:07Z

Learner:

The module says a Site-to-Site VPN makes two private networks behave as if directly connected. Connect this to Modules 1 and 2: why is a path across the public internet needed at all, and what does the tunnel hide?

Helper reply (verbatim):

The path across the public internet is needed because a VPC is private and an office or data center is private, but these are separate networks in different places, so traffic between them must cross the public internet [module]. Modules 1 and 2 set up that problem: Module 1 gives the networking foundations for routing between networks, and Module 2 establishes the VPC as a private network [derived]. Without a dedicated physical connection such as AWS Direct Connect, which is out of scope here [module], the public internet is the path between the two private networks.

The IPsec tunnel hides the private traffic by wrapping the original packets from the private networks in IPsec and carrying them as ciphertext across the internet [module]. That means the public internet sees encrypted tunnel traffic, not the private payload or the internal addressing inside the wrapped packet [derived]. This is what makes the two ends behave as if they were directly connected even though the actual path crosses the public internet [module].

### Turn 2
- Helper: grounded-tutor
- Module: modules/03-vpns-and-routing.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=8192)
- Time: 2026-09-28T18:44:15Z

Learner:

Explain that more simply.

Helper reply (verbatim):

The VPC and the office or data center are both private networks, but they sit in different places. To reach each other, their traffic has to travel across the public internet, because the alternative mentioned in the module — a dedicated physical connection called AWS Direct Connect — is out of scope [module]. Modules 1 and 2 give the background: Module 1 covers how networks route traffic, and Module 2 establishes that a VPC is a private network [derived].

The tunnel hides the private traffic by encrypting it. The private packets are wrapped inside IPsec and sent as ciphertext, so anyone on the internet in between sees only unreadable encrypted data, not the private network addresses or the actual contents [module]. That is what lets the two private networks behave as if they were directly connected even though the real path is public [module].

### Turn 3
- Helper: grounded-tutor
- Module: modules/03-vpns-and-routing.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=8192)
- Time: 2026-09-28T18:44:34Z

Learner:

Give me a concrete example: the office network is 10.8.0.0/16 and the VPC is 10.1.0.0/16, connected by a Site-to-Site VPN. What must routing on both sides know for a packet to cross, and how do static routes and BGP differ at doing it?

Helper reply (verbatim):

For a packet to cross from the office network 10.8.0.0/16 to the VPC network 10.1.0.0/16, the office side must know that 10.1.0.0/16 is reachable through the tunnel, and the AWS side must know that 10.8.0.0/16 is reachable through the tunnel [module][derived]. That is what the module means by both sides knowing which networks are reachable through the tunnel [module].

With static routes, an administrator enters those routes manually on both sides — for example, the office router gets “10.1.0.0/16 via the VPN tunnel,” and AWS gets “10.8.0.0/16 via the VPN” [derived]. With BGP, each side announces its networks: the office advertises 10.8.0.0/16 and AWS advertises 10.1.0.0/16, so the routes propagate automatically [module][derived]. The difference is that static routes stay fixed until someone edits them, while BGP adapts automatically to prefix changes — for example, if the office later adds 10.9.0.0/16, BGP can advertise it without manual route changes [module]. That is why the module prefers BGP wherever the device supports it [module].

### Turn 4
- Helper: grounded-tutor
- Module: modules/03-vpns-and-routing.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=8192)
- Time: 2026-09-28T18:44:47Z

Learner:

In the diagram at the end of the module, trace the path of an engineer's laptop into VPC B, and separately the data center's path into VPC A. Name every component each path passes through.

Helper reply (verbatim):

Engineer laptop into VPC B: the laptop connects to the AWS Client VPN endpoint, which terminates the OpenVPN-based TLS connection, then the traffic enters the transit gateway and passes to VPC B [module][derived]. The transit gateway’s route table decides whether that path is allowed [module].

Data center into VPC A: traffic starts in the on-premises network 10.8.0.0/16, passes through the customer gateway device, travels over one of the two IPsec tunnels, enters the transit gateway, and then reaches VPC A [module][derived]. The two tunnels are equivalent, not primary/backup, so traffic can use either one while the other is available if one fails [module]. This matches the module’s architecture: Client VPN for engineers, Site-to-Site VPN for the data center [module].

### Turn 5
- Helper: grounded-tutor
- Module: modules/03-vpns-and-routing.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=8192)
- Time: 2026-09-28T18:44:55Z

Learner:

How would I set up a WireGuard tunnel into my VPC instead of using IPsec?

Helper reply (verbatim):

WireGuard is outside this module’s scope. The module’s AWS-side options use IPsec for Site-to-Site VPN and OpenVPN for Client VPN; it does not mention WireGuard [module]. If you choose WireGuard anyway, it would be a self-managed setup rather than one of the managed components in this module [general].

A common approach is to run a WireGuard peer on an EC2 instance inside the VPC, give that instance a public IP, allow UDP traffic to its WireGuard port, configure the instance’s OS routing and the VPC route tables to send VPC-bound traffic through that instance, and use security groups to control access [general]. This paragraph is general knowledge, not course material.
