# Module 3 — VPNs and routing

- **Title**: VPNs and routing
- **Position**: 3 of 7
- **Concepts introduced**: IPsec tunnel, AWS Site-to-Site VPN, virtual private gateway, customer gateway, transit gateway, AWS Client VPN, BGP, route propagation
- **Prerequisites**: Module 1 (networking foundations), Module 2 (private connectivity in a VPC)
- **Content files**: `modules/03-vpns-and-routing.md`
- **Summary**: By the end of this module the learner can explain how Site-to-Site VPN extends a private network into a VPC over encrypted IPsec tunnels, the roles of the virtual private gateway and the transit gateway, why a connection carries two tunnels, and what Client VPN offers individual engineers.

## Why VPNs

A VPC is private; an office or data center is private; the path between them crosses the public internet. A VPN bridges the two with an encrypted tunnel: packets from the private networks are wrapped in IPsec and travel over the internet as ciphertext, so both ends behave as if directly connected. The alternative is AWS Direct Connect, a dedicated physical connection that never traverses the internet; it is out of scope for this course.

## Site-to-Site VPN components

An AWS Site-to-Site VPN connection has two ends:

- On the AWS side, a virtual private gateway (VGW) attached to a single VPC, or a transit gateway (TGW) shared by many networks.
- On your side, a customer gateway device — a physical router or software appliance — represented in AWS by a customer gateway resource.

Every connection carries two IPsec tunnels to different AWS endpoints so that one tunnel can fail while the other carries traffic. The tunnels are equivalent, not primary/backup.

## Routing across the tunnel

For traffic to flow, both sides must know which networks are reachable through the tunnel. Two options: static routes entered on both sides, or BGP, where each side announces its networks and routes propagate automatically. AWS uses BGP pervasively here — a virtual private gateway even has its own autonomous system number (64512 by default). Position: prefer BGP wherever the device supports it, because it survives prefix changes without manual edits.

## Transit gateway as the hub

Attaching a VPN to a VGW serves exactly one VPC. A transit gateway is a regional routing hub: VPCs, Site-to-Site VPNs, and other networks all attach to it, and its route tables decide who can reach whom. Position: once more than one VPC or one VPN is involved, terminate VPNs on a transit gateway rather than per-VPC gateways.

## Client VPN for people

Site-to-Site VPN connects networks. AWS Client VPN connects individual people: a managed, OpenVPN-based service whose endpoint terminates encrypted connections from engineers' laptops and drops them into a VPC or onto a transit gateway, with per-user or per-group authorization. This course's architecture uses Client VPN for engineers and Site-to-Site for the data center.

## Diagram

```text
on-premises network                     AWS
+--------------------------+           +----------------------------------+
| 10.8.0.0/16              |           | transit gateway (TGW)            |
| customer gateway device  |===========|   +---------> VPC A              |
| (router)                 | two IPsec |   +---------> VPC B              |
+--------------------------+  tunnels  +----------------------------------+
                                                    ^
 engineer laptop  ---- Client VPN (TLS) ------------+
```

## Go deeper

- [How AWS Site-to-Site VPN works](https://docs.aws.amazon.com/vpn/latest/s2svpn/how_it_works.html)
- [Site-to-Site VPN tunnels](https://docs.aws.amazon.com/vpn/latest/s2svpn/VPNTunnels.html)
- [What is a transit gateway?](https://docs.aws.amazon.com/vpc/latest/tgw/what-is-transit-gateway.html)
- [What is AWS Client VPN?](https://docs.aws.amazon.com/vpn/latest/clientvpn-admin/what-is.html)
- [Amazon VPC connectivity options (whitepaper)](https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/)
