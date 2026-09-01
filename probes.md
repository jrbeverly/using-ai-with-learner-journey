# Probe set — learner journey comparison

Fixed before any run. Round 1 (first comparison) used probes 1.1-7.5 and
left this file unchanged afterwards. Round 2 (specialization, learner-state,
and knowledge-check experiments) adds the scoping probes below — 6.6-6.8 and
7.6-7.8, each asking about an earlier module's concept by name — and froze the
file again before the round-2 runs. One section per module; the module path in
the section heading is the `--module` argument for that section's run. Each
probe is one learner message, asked in order in a single replay conversation
per module. The follow-up probe is asked immediately after the answer to the
probe it names, so "that" refers to the preceding answer.

Probe categories: concept, follow-up, example, diagram, out-of-corpus,
scoping (round 2). Connect-to-an-earlier-module is exercised by the concept
probes of Modules 2-7, which ask for the link to an earlier module explicitly.

Written without consulting either instruction set's text beyond their headers.

## Module 1 — modules/01-networking-foundations.md

### Probe 1.1 — concept
What is network address translation (NAT), and why do hosts on private ranges need it to reach the internet?

### Probe 1.2 — follow-up on 1.1
Explain that more simply.

### Probe 1.3 — example
Give me a concrete example: a host at 10.0.1.5 opens two connections at the same time to the same service at api.example.com on port 443. Walk through what happens from the DNS lookup onward, and what keeps the two connections apart.

### Probe 1.4 — diagram
In the diagram at the end of the module, host A sends a packet to host B at 10.0.2.9. Trace the packet step by step, including every route-table lookup and decision along the way.

### Probe 1.5 — out-of-corpus
How would all of this change if my network used IPv6 instead of RFC 1918 private ranges?

## Module 2 — modules/02-private-connectivity-vpc.md

### Probe 2.1 — concept (connects to Module 1)
The module says the VPC is defined by a CIDR range from the private space of Module 1. Which Module 1 concept is that, and what carries over from that module into the VPC?

### Probe 2.2 — follow-up on 2.1
Explain that more simply.

### Probe 2.3 — example
Give me a concrete example: one instance in the private subnet needs to download a package from the internet, and another needs to call the Secrets Manager API. Walk through both traffic paths step by step.

### Probe 2.4 — diagram
In the diagram at the end of the module, trace both paths it shows: instance B reaching the AWS service API, and outbound traffic from the private subnet leaving through the NAT gateway. What does each component do along the way?

### Probe 2.5 — out-of-corpus
How do I connect two VPCs together with VPC peering?

## Module 3 — modules/03-vpns-and-routing.md

### Probe 3.1 — concept (connects to Modules 1 and 2)
The module says a Site-to-Site VPN makes two private networks behave as if directly connected. Connect this to Modules 1 and 2: why is a path across the public internet needed at all, and what does the tunnel hide?

### Probe 3.2 — follow-up on 3.1
Explain that more simply.

### Probe 3.3 — example
Give me a concrete example: the office network is 10.8.0.0/16 and the VPC is 10.1.0.0/16, connected by a Site-to-Site VPN. What must routing on both sides know for a packet to cross, and how do static routes and BGP differ at doing it?

### Probe 3.4 — diagram
In the diagram at the end of the module, trace the path of an engineer's laptop into VPC B, and separately the data center's path into VPC A. Name every component each path passes through.

### Probe 3.5 — out-of-corpus
How would I set up a WireGuard tunnel into my VPC instead of using IPsec?

## Module 4 — modules/04-tls-foundations.md

### Probe 4.1 — concept
What does the TLS handshake accomplish, and why does the connection end up encrypted with a symmetric session key rather than the server's public key?

### Probe 4.2 — follow-up on 4.1
Explain that more simply.

### Probe 4.3 — example
Give me a concrete example: a browser opens https://api.example.com against a server that hosts many names. Walk through the handshake and say which part lets the server present the right certificate.

### Probe 4.4 — diagram
In the diagram at the end of the module, walk through the handshake message by message and say what each side learns or proves at each step.

### Probe 4.5 — out-of-corpus
How do I pin the server certificate in a mobile app so it only ever trusts one specific certificate?

## Module 5 — modules/05-certificates-and-trust.md

### Probe 5.1 — concept (connects to Module 4)
The module says validation means building a chain from the presented certificate to an anchor in the trust store. Connect this to Module 4: at which point in the handshake does this happen, and what does it give the client that the rest of the handshake does not?

### Probe 5.2 — follow-up on 5.1
Explain that more simply.

### Probe 5.3 — example
Give me a concrete example: a client connects to api.example.com and is presented a leaf certificate and an intermediate. Walk through every check the client performs before accepting the connection.

### Probe 5.4 — diagram
In the diagram at the end of the module, walk from the trust anchor down to the leaf certificate: who signs what, and what does the client have to check to trust the leaf?

### Probe 5.5 — out-of-corpus
How would I run my own CA on-premises with OpenSSL instead of using AWS Private CA?

## Module 6 — modules/06-mutual-tls.md

### Probe 6.1 — concept (connects to Modules 4 and 5)
The module says mutual TLS mirrors Module 4 in reverse. What exactly is reversed, and which Module 5 machinery does the server now use?

### Probe 6.2 — follow-up on 6.1
Explain that more simply.

### Probe 6.3 — example
Give me a concrete example: an ALB in verify mode receives a request from a client with a certificate issued by the private CA. Walk through what the ALB checks and what the application behind it receives.

### Probe 6.4 — diagram
In the diagram at the end of the module, walk through the mutual TLS handshake and point out which messages a one-way TLS handshake does not have, and what the ALB validates before any application data flows.

### Probe 6.5 — out-of-corpus
How does mutual TLS work in a Kubernetes service mesh like Istio?

### Probe 6.6 — scoping (Module 1 concept)
Why does a private host need NAT to reach the internet, and how do the reply packets find their way back to the host?

### Probe 6.7 — scoping (Module 5 concept)
What is a certificate, and how does a chain of CAs let the client trust a certificate it has never seen before?

### Probe 6.8 — scoping (Module 4 concept)
Remind me how the client validated the server's certificate in one-way TLS.

## Module 7 — modules/07-combined-architecture.md

### Probe 7.1 — concept (connects to Modules 2, 3, and 6)
The module names the trust boundaries as the VPN edge, the ALB listener, and the security groups around the instances. Explain what each boundary checks, drawing on Modules 3, 6, and 2.

### Probe 7.2 — follow-up on 7.1
Explain that more simply.

### Probe 7.3 — example
Give me a concrete example of the certificate lifecycle: client certificates are issued in short-lived mode and re-issued with every deployment. Walk through what happens to the old certificates, and what happens if one key is lost mid-week.

### Probe 7.4 — diagram
In the diagram at the end of the module, trace a request from the engineer's laptop all the way to a service instance and back, naming every component and trust boundary it crosses.

### Probe 7.5 — out-of-corpus
How would this architecture change if we used OAuth2 tokens instead of client certificates?

### Probe 7.6 — scoping (Module 1 concept)
What does a route table do, and what makes a route the default route?

### Probe 7.7 — scoping (Module 5 concept)
What is a certificate chain, and what does the client check during validation?

### Probe 7.8 — scoping (Module 6 concept)
How do the ALB's verify and passthrough modes differ in mutual TLS?
