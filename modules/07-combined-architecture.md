# Module 7 — Combined architecture

- **Title**: Combined architecture
- **Position**: 7 of 7
- **Concepts introduced**: target group, certificate renewal and rotation
- **Prerequisites**: Module 1 (networking foundations), Module 2 (private connectivity in a VPC), Module 3 (VPNs and routing), Module 4 (TLS foundations), Module 5 (certificates and trust), Module 6 (mutual TLS)
- **Content files**: `modules/07-combined-architecture.md`
- **Summary**: By the end of this module the learner can trace a request through the full architecture from a caller's certificate to a service instance, name every trust boundary it crosses, and explain the certificate lifecycle that keeps it working.

## The architecture, in one opinion

One internal API runs in one region, reachable only by callers holding certificates issued by our own CA. This course takes the position that:

- Client authentication happens at the edge: an ALB terminates mTLS in verify mode; instances behind it receive plain HTTP plus validated identity headers.
- Certificates are the only credentials: client certificates issued by AWS Private CA, server certificate from ACM.
- Network privacy is layered, not single: VPC isolation, security groups for port-level reachability, VPC endpoints for AWS APIs, VPNs for remote networks and people.

## The pieces

- A VPC (`10.1.0.0/16`) with public and private subnets across two AZs (Module 2).
- An ALB in the public subnets with an HTTPS listener — a listener terminates TLS, and a target group names the instances that receive traffic. The listener's server certificate is an ACM certificate; its mTLS trust store holds the Private CA bundle plus a CRL, in verify mode (Modules 5–6).
- Service instances in the private subnets. Security groups allow traffic only from the ALB, so the sole route to a service is through the listener.
- Egress: a NAT gateway per AZ, used only for traffic that must leave the VPC; AWS API calls go through VPC interface endpoints instead (Module 2).
- The data center reaches the VPC over Site-to-Site VPN terminating on a transit gateway — two IPsec tunnels, BGP (Module 3).
- Engineers reach the VPC over AWS Client VPN (Module 3). The API itself is internal-only and never published to the internet.

## Certificate lifecycle

Public and private certificates age differently here. The ALB's ACM certificate renews automatically. Private CA client certificates do not renew themselves: their validity is what limits the damage of a lost key, so the design choice is short-lived certificates (Private CA short-lived mode, at most 7 days) re-issued with every deployment. Rotation is routine, not an incident; the CRL in the ALB trust store is the backstop for keys known to be compromised.

## Walking a request

An engineer's laptop (Client VPN, client certificate) calls `api.internal.example.com`:

1. DNS resolves the name to the ALB.
2. TLS handshake: the ALB presents its ACM server certificate and requests a client certificate.
3. The ALB validates the client chain against the trust store (Private CA anchor) and checks the CRL.
4. The ALB forwards the request to a target instance with X-Amzn-Mtls headers carrying the validated identity.
5. The application authorizes the request from the header identity (for example the subject or serial) and responds; the response takes the reverse path.

Every hop after step 3 runs on private addresses inside the VPC. The trust boundaries are the VPN edge, the ALB listener, and the security groups around the instances.

## Diagram

```text
on-premises DC 10.8.0.0/16                engineer laptop
        |                                      |
        | two IPsec tunnels                    | Client VPN (TLS)
        v                                      v
   transit gateway <---------------------------+
        |
        v
+-----------------------------------------------------------+
| VPC 10.1.0.0/16                                           |
|                                                           |
|  public subnets (AZ a + AZ b)                             |
|    ALB listener :443 (TLS + mTLS verify)                  |
|      server certificate: ACM (auto-renewing)              |
|      trust store: Private CA bundle + CRL                 |
|        |  plain HTTP + X-Amzn-Mtls identity headers       |
|        v                                                  |
|  private subnets (AZ a + AZ b)                            |
|    service instances                                      |
|      security group: traffic from the ALB only            |
|                                                           |
|  NAT gateway per AZ (outbound egress only)                |
|  VPC interface endpoints (AWS APIs, no NAT)               |
+-----------------------------------------------------------+
```

## Go deeper

- [Mutual authentication with TLS in Application Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/mutual-authentication.html)
- [Access an AWS service using an interface endpoint](https://docs.aws.amazon.com/vpc/latest/privatelink/create-interface-endpoint.html)
- [Amazon VPC connectivity options (whitepaper)](https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/)
