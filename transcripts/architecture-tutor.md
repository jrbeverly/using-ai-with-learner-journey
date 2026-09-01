# Learner conversation transcript
## Run — 2026-09-28T18:09:35Z (replay)
- Helper: architecture-tutor (helpers/architecture-tutor.md)
- Module: modules/07-combined-architecture.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Base URL: https://api.deepseek.com/anthropic

### Turn 1
- Helper: architecture-tutor
- Module: modules/07-combined-architecture.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Time: 2026-09-28T18:09:45Z

Learner:

Walk me through what happens when an engineer's laptop calls the API.

Helper reply (verbatim):

From the engineer’s laptop, the call to `api.internal.example.com` enters the **Client VPN (TLS)** tunnel and crosses the **transit gateway** into the VPC `[module]`. DNS resolves the name to the **ALB listener :443** `[module]`. At the listener, the TLS handshake begins: the ALB presents its **ACM server certificate**, requests the laptop’s **client certificate**, then validates the client chain against the **Private CA bundle + CRL in the trust store** `[module]`. Only after that validation succeeds does the listener forward the request to a **service instance** in the private subnets as plain HTTP with `X-Amzn-Mtls` identity headers `[module]`.

The instance’s **security group** accepts traffic only from the ALB, so this listener-to-target path is the sole route into the service `[module]`. The application authorizes the request from the header identity, such as the subject or serial, and returns a response that travels back through the ALB, transit gateway, and Client VPN to the laptop `[module]`. Every hop after the listener validation runs on private addresses inside the VPC; the trust boundaries crossed are the **VPN edge**, the **ALB listener**, and the **instance security group** `[module]`.

### Turn 2
- Helper: architecture-tutor
- Module: modules/07-combined-architecture.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Time: 2026-09-28T18:09:51Z

Learner:

What would break if the client certificate had been revoked?

Helper reply (verbatim):

The request stops at the **ALB listener :443**, which is the trust boundary that enforces client authentication `[module]`. The listener's trust store holds the **Private CA bundle + CRL**, and the listener checks the CRL as part of validating the client chain `[module]`. Since a revoked certificate appears on that CRL, the validation fails `[derived]`. The TLS handshake does not complete, so the ALB never forwards the request to the **service instances** and never generates the `X-Amzn-Mtls` identity headers `[derived]`. The instance security group and application never see the request; from the caller's side, the connection is rejected at the listener `[general]`. The relevant boundary is the ALB listener's mTLS validation, not the VPN edge or the instance security group `[derived]`.

### Turn 3
- Helper: architecture-tutor
- Module: modules/07-combined-architecture.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Time: 2026-09-28T18:10:02Z

Learner:

Why is client authentication done at the edge instead of in the service?

Helper reply (verbatim):

The module’s position is explicit: client authentication happens at the edge, with the **ALB listener** terminating mTLS in verify mode, while **service instances** receive plain HTTP plus validated `X-Amzn-Mtls` identity headers `[module]`. The listener is one of the named trust boundaries, and the **instance security groups** allow traffic only from the ALB, so the sole route to a service is through that listener `[module]`. That makes the ALB the single place responsible for chain validation, CRL checking, and the trust store; the instances never handle client certificates or TLS termination and can rely on the already-validated header identity `[derived]`.

This fits the module’s larger opinions: certificates are the only credentials, and network privacy is layered rather than single `[module]`. The edge enforces client authentication as one layer, while the security groups provide port-level reachability as another, and the application still authorizes from the header identity `[module]`. Moving client authentication into the service would put trust decisions on every instance instead of at the boundary the architecture already draws `[derived]`.
