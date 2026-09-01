# Module 1 — Networking foundations

- **Title**: Networking foundations
- **Position**: 1 of 7
- **Concepts introduced**: IP address, CIDR, subnet, packet, routing, route table, default route, default gateway, TCP, port, DNS, public and private IP address ranges (RFC 1918), network address translation (NAT)
- **Prerequisites**: none
- **Content files**: `modules/01-networking-foundations.md`
- **Summary**: By the end of this module the learner can explain how a packet travels from one host to another, what a route table and a default route do, what a TCP port identifies, why private address ranges exist, and what NAT is for.

## Packets and addresses

Every host on an IP network has an IP address (for example `10.0.1.5`). Data moves as packets; each packet carries a source address, a destination address, and a payload. Routers use the destination address to decide where the packet goes next. A router is simply a device that forwards packets between networks.

## CIDR: expressing address ranges

CIDR notation expresses a range of addresses as a prefix: `10.1.0.0/16` means "the first 16 bits are fixed; the rest identify hosts", so the range runs from `10.1.0.0` to `10.1.255.255`. A `/24` prefix fixes 24 bits and leaves 8, giving 254 usable host addresses. A subnet is a division of a larger range into such prefixes.

## Routing: the next-hop decision

When a router receives a packet it looks up the destination in its route table: entries mapping a prefix to a next hop (another router, or "local" for directly attached networks). The most specific matching prefix wins. The entry `0.0.0.0/0` matches everything and is the default route — where traffic goes when nothing more specific matches. A host applies the same logic in miniature: traffic for its own subnet goes directly to the destination; everything else goes to its default gateway.

## Ports and connections

An IP address names a host, not the application on that host. TCP ports solve this: a number between 1 and 65535 attached to an address. A service listens on a well-known port (for example 443). A connection is identified by the four-tuple (source address, source port, destination address, destination port), which lets one host hold many simultaneous connections to the same server.

## DNS: names to addresses

The Domain Name System (DNS) translates names such as `api.example.com` into IP addresses. Before a client can connect it resolves the name; the packet is sent to the returned address.

## Private address ranges

RFC 1918 reserves three ranges for private networks: `10.0.0.0/8`, `172.16.0.0/12`, and `192.168.0.0/16`. Packets with these destinations are never routed across the public internet, so many organizations can use the same ranges without conflict. The price: a host on a private range cannot talk to the internet directly — a NAT device must translate its private source address to a public one, and translate the replies back. Every AWS VPC builds on these ideas, which is where the next module starts.

## Diagram

```text
host A (10.0.1.5)                                    host B (10.0.2.9)
      |                                                    ^
      | packet: dst 10.0.2.9                               |
      v                                                    |
   router A  ────────────────── network ────────────────> router B
   route table of router A:
     10.0.1.0/24  -> local        (A's own subnet)
     10.0.2.0/24  -> 10.0.9.2     (router B)
     0.0.0.0/0    -> 10.0.9.1     (default route: everything else)
```

## Go deeper

- [RFC 1918 — Address Allocation for Private Internets](https://datatracker.ietf.org/doc/html/rfc1918)
- [How Amazon VPC works](https://docs.aws.amazon.com/vpc/latest/userguide/how-it-works.html) (CIDR and subnets in the AWS context)
