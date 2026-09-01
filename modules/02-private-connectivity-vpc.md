# Module 2 — Private connectivity in a VPC

- **Title**: Private connectivity in a VPC
- **Position**: 2 of 7
- **Concepts introduced**: VPC, availability zone, AWS subnet, public subnet, private subnet, internet gateway, NAT gateway, elastic IP address, elastic network interface (ENI), security group, VPC interface endpoint, AWS PrivateLink
- **Prerequisites**: Module 1 (networking foundations)
- **Content files**: `modules/02-private-connectivity-vpc.md`
- **Summary**: By the end of this module the learner can describe how a VPC carves private address space into subnets, the difference between public and private subnets, what a NAT gateway does and does not do, how security groups filter traffic, and how VPC endpoints reach AWS services without the internet.

## The VPC: your private address space

A Virtual Private Cloud (VPC) is an isolated, region-scoped network defined by a CIDR range from the private space of Module 1 (for example `10.1.0.0/16`). Everything launched into the VPC gets a private IP from that range and is unreachable from the internet unless a path is deliberately built. A VPC spans all availability zones (AZs) in its region.

## Subnets and availability zones

A subnet is a slice of the VPC's CIDR that lives in exactly one AZ (for example `10.1.1.0/24` in one AZ, `10.1.2.0/24` in another). The distinction that matters for private networking is public versus private:

- A public subnet has a route to an internet gateway (IGW), so its resources can receive traffic from the internet, if permitted.
- A private subnet has no route to the internet at all: no inbound internet traffic can reach it, and it cannot initiate outbound traffic without help.

## Reaching out: the NAT gateway

Instances in a private subnet still need outbound access (updates, external APIs). A NAT gateway provides it: it lives in a public subnet, holds an elastic IP address, and translates the private source addresses of outbound packets to its own public address, translating replies back. Because the mapping only exists for flows the private instances initiated, the internet cannot initiate connections inward. Each AZ should have its own NAT gateway; otherwise that AZ's private subnets lose egress when the other AZ fails. Position: a NAT gateway is for outbound-only traffic — a service that must be reachable from outside belongs behind an ingress point in a public subnet instead.

## Filtering: security groups

A security group is a stateful firewall attached to a resource: it allows traffic by port, protocol, and source. Stateful means a reply to an allowed outbound flow is automatically allowed back. Security groups are the primary "who may talk to whom" control inside a VPC.

## Reaching AWS services: VPC endpoints

AWS service APIs live on public endpoints, which a private subnet can only reach through a NAT gateway — unless it uses VPC endpoints. An interface endpoint places an elastic network interface with private IPs into your subnets and connects, via AWS PrivateLink, to the service's API: traffic never leaves the AWS network and never uses a public IP. Interface endpoints exist per service (for example EC2, SSM, Secrets Manager). Position: private subnets should reach AWS services through endpoints rather than a NAT gateway wherever an endpoint exists.

## Diagram

```text
                        Internet
                           |
  +--------------------------------------------------------+
  | VPC 10.1.0.0/16                                        |
  |                                                        |
  |  public subnet 10.1.1.0/24 (AZ a)                      |
  |    +-------------------+   +-----------------------+   |
  |    | instance A        |   | NAT gateway           |---|--> outbound (source NAT)
  |    |                   |   | (elastic IP address)  |   |
  |    +-------------------+   +-----------------------+   |
  |                                                        |
  |  private subnet 10.1.2.0/24 (AZ a)                     |
  |    +-------------------+   +-----------------------+   |
  |    | instance B        |-->| VPC endpoint (ENI)    |---|--> AWS service API
  |    |                   |   |                       |   |    via PrivateLink
  |    +-------------------+   +-----------------------+   |
  +--------------------------------------------------------+
```

## Go deeper

- [What is Amazon VPC?](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
- [Subnets for your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html)
- [Configure route tables](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html)
- [NAT devices for your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat.html)
- [What is AWS PrivateLink?](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
