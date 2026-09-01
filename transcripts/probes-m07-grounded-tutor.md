# Learner conversation transcript
## Run — 2026-09-28T18:53:27Z (replay)
- Helper: grounded-tutor (helpers/grounded-tutor.md)
- Module: modules/07-combined-architecture.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=8192)
- Base URL: https://api.deepseek.com/anthropic

### Turn 1
- Helper: grounded-tutor
- Module: modules/07-combined-architecture.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=8192)
- Time: 2026-09-28T18:53:42Z

Learner:

The module names the trust boundaries as the VPN edge, the ALB listener, and the security groups around the instances. Explain what each boundary checks, drawing on Modules 3, 6, and 2.

Helper reply (verbatim):

The module names the trust boundaries as the VPN edge, the ALB listener, and the security groups around the instances [module].

- **VPN edge (Module 3):** The data center reaches the VPC over Site-to-Site VPN terminating on a transit gateway with two IPsec tunnels and BGP, and engineers reach it over AWS Client VPN [module]. This boundary checks that remote networks and people enter through an authenticated, encrypted VPN path before their traffic can address anything inside the VPC [derived].

- **ALB listener (Module 6):** The listener terminates TLS in mTLS verify mode: it presents the ACM server certificate, requests a client certificate, validates the client chain against the Private CA bundle, and checks the CRL [module]. So this boundary checks the client’s certificate chain to the Private CA and its revocation status before forwarding plain HTTP with `X-Amzn-Mtls` identity headers to the instances [module].

- **Security groups around the instances (Module 2):** The service instances sit in private subnets and their security groups allow traffic only from the ALB [module]. This boundary checks the source of traffic at the instance network interface, so the sole route to a service is through the listener [module].

### Turn 2
- Helper: grounded-tutor
- Module: modules/07-combined-architecture.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=8192)
- Time: 2026-09-28T18:53:47Z

Learner:

Explain that more simply.

Helper reply (verbatim):

More simply, think of three checkpoints a request must pass.

1. **VPN edge (Module 3)**: before anyone from the data center or an engineer's laptop can reach the VPC at all, they must come through an encrypted VPN tunnel [module]. This checkpoint asks: *"Is this coming in through the trusted private path?"* [derived]

2. **ALB listener (Module 6)**: when a request reaches the load balancer, the ALB demands a client certificate, checks that it was issued by our Private CA, and checks the CRL to see if it was revoked [module]. This checkpoint asks: *"Does this caller have a valid, un-revoked certificate from our CA?"* [derived]

3. **Security groups around the instances (Module 2)**: the instances only accept traffic whose source is the ALB [module]. This checkpoint asks: *"Is this traffic coming from the ALB, and not from anywhere else?"* [derived]

After the ALB checks the certificate, the rest of the hop to the instance is plain HTTP inside the VPC, with the validated identity passed in headers [module].

### Turn 3
- Helper: grounded-tutor
- Module: modules/07-combined-architecture.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=8192)
- Time: 2026-09-28T18:54:03Z

Learner:

Give me a concrete example of the certificate lifecycle: client certificates are issued in short-lived mode and re-issued with every deployment. Walk through what happens to the old certificates, and what happens if one key is lost mid-week.

Helper reply (verbatim):

A concrete timeline works well here. Suppose a client certificate is issued on Monday morning in Private CA short-lived mode, so it can last at most 7 days [module]. On Tuesday a deployment re-issues a fresh short-lived certificate for that client; the Monday certificate is not renewed, so it simply ages out and becomes unusable when its short validity period ends [module][derived]. The module does not describe old certificates being revoked automatically on each deployment; the design relies on the short lifetime itself to cap the exposure window [module][derived].

If a key is lost on Wednesday, that specific certificate is added to the CRL held in the ALB trust store [derived]. Because the ALB validates the client chain and checks the CRL in verify mode, the next handshake presenting that lost key's certificate is rejected [module]. The short-lived design means even a lost key that goes unnoticed cannot be abused past its at-most-7-day expiry, and the CRL acts as the immediate backstop once the loss is known [module].

### Turn 4
- Helper: grounded-tutor
- Module: modules/07-combined-architecture.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=8192)
- Time: 2026-09-28T18:54:17Z

Learner:

In the diagram at the end of the module, trace a request from the engineer's laptop all the way to a service instance and back, naming every component and trust boundary it crosses.

Helper reply (verbatim):

From the laptop, the request follows the “Walking a request” path: DNS resolves `api.internal.example.com` to the ALB [module]. The laptop crosses the first trust boundary, the VPN edge, over the Client VPN TLS connection to the transit gateway [module][derived]. From the transit gateway the request enters the VPC and reaches the ALB listener [module]. At the second trust boundary, the ALB listener terminates TLS in mTLS verify mode: it presents its ACM server certificate, requests the client certificate, validates the client chain against the Private CA bundle, and checks the CRL [module]. After validation, the ALB forwards plain HTTP with `X-Amzn-Mtls` identity headers to a target instance selected through its target group [module]. Crossing the third trust boundary, the instance’s security group allows traffic only from the ALB, making the listener the sole route to the service [module]. The application then authorizes the request from the header identity, for example the subject or serial, and responds [module].

The response takes the reverse path: service instance back to the ALB, then through the transit gateway and Client VPN back to the laptop [module][derived]. Every hop after the ALB validation step runs on private addresses inside the VPC [module].

### Turn 5
- Helper: grounded-tutor
- Module: modules/07-combined-architecture.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=8192)
- Time: 2026-09-28T18:54:25Z

Learner:

How would this architecture change if we used OAuth2 tokens instead of client certificates?

Helper reply (verbatim):

OAuth2 tokens are outside this module, so the following is general knowledge, not course material [general]. The module's design deliberately uses client certificates as the only credentials, validated at the ALB in mTLS verify mode, with the validated identity passed to instances in `X-Amzn-Mtls` headers [module]. With OAuth2 tokens instead, the ALB would no longer need the Private CA trust store, CRL, or client-certificate validation; instead, a component would validate the token, usually by checking its signature, issuer, audience, and expiry, and the application would derive identity from token claims rather than from the mTLS headers [general].

This would shift the credential check at the ALB listener boundary from "valid client certificate chain and not revoked" to "valid, unexpired token from a trusted issuer" [general]. The VPN edge and the instance security groups could remain largely the same, since those boundaries control network reachability and source traffic rather than the credential format [general].
