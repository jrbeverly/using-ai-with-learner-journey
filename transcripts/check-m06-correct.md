# Learner conversation transcript
## Run — 2026-09-28T19:22:54Z (replay)
- Helper: knowledge-check (helpers/knowledge-check.md)
- Module: modules/06-mutual-tls.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Base URL: https://api.deepseek.com/anthropic

### Turn 1
- Helper: knowledge-check
- Module: modules/06-mutual-tls.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Time: 2026-09-28T19:22:56Z

Learner:

Let's check my understanding of this module. Ask me about what mTLS adds first, then the handshake messages, then the trust store, then the verify and passthrough modes.

Helper reply (verbatim):

In your own words, what does mutual TLS add to one-way TLS?

### Turn 2
- Helper: knowledge-check
- Module: modules/06-mutual-tls.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Time: 2026-09-28T19:23:00Z

Learner:

mTLS adds client authentication to one-way TLS: the server additionally demands that the client prove its identity with a certificate. The client holds its own certificate and private key, and the server holds a trust store of the CAs it accepts. The connection itself carries identity before any application logic runs.

Helper reply (verbatim):

That's right — you named the key addition: the client authenticates with its own certificate and private key, the server holds a trust store of accepted CAs, and identity is carried at the transport layer before application logic runs `[module]`.

Next: compared with one-way TLS, which extra messages appear in the mTLS handshake, and what does each one do?

### Turn 3
- Helper: knowledge-check
- Module: modules/06-mutual-tls.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Time: 2026-09-28T19:23:05Z

Learner:

The extra messages are CertificateRequest and CertificateVerify. The server sends CertificateRequest listing the CAs it accepts; the client replies with its certificate and a CertificateVerify — a signature over the handshake transcript made with the client's private key, proving it holds the key and not just a copy of the certificate. The server then validates the client's chain against its trust store, exactly as the client validated the server.

Helper reply (verbatim):

Correct — you listed CertificateRequest (the server's list of acceptable CAs) and CertificateVerify (the client's signature over the handshake transcript, proving private-key possession), plus the server validating the client chain against its trust store `[module]`.

Next: what is the server-side trust store for in mTLS?

### Turn 4
- Helper: knowledge-check
- Module: modules/06-mutual-tls.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Time: 2026-09-28T19:23:07Z

Learner:

The server-side trust store is the server's bundle of CA certificates — roots and intermediates — for the CAs it accepts, and the server validates the client's chain against it, with optional revocation checks.

Helper reply (verbatim):

That's correct — the trust store is the bundle of CAs (roots and intermediates) the server accepts, and it's what the server validates the client's chain against, with optional revocation checks `[module]`.

Last topic: how do ALB mTLS's verify and passthrough modes differ, and which mode does the module recommend in general?

### Turn 5
- Helper: knowledge-check
- Module: modules/06-mutual-tls.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Time: 2026-09-28T19:23:11Z

Learner:

In verify mode the ALB validates the client certificate chain against the trust store and, optionally, against CRLs, rejecting invalid certificates at the edge, and forwards the validated identity in X-Amzn-Mtls headers. In passthrough mode the ALB performs no validation and forwards the entire chain in a single X-Amzn-Mtls-Clientcert header, leaving validation to the application.

Helper reply (verbatim):

You've got the differences right: verify mode validates the chain against the trust store and optional CRLs, rejects invalid certificates at the edge, and forwards identity in X-Amzn-Mtls headers; passthrough mode does no validation and forwards the full chain in a single X-Amzn-Mtls-Clientcert header for the application to validate `[module]`.

One part of the question remains: which mode does the module recommend in general, and why?

### Turn 6
- Helper: knowledge-check
- Module: modules/06-mutual-tls.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Time: 2026-09-28T19:23:17Z

Learner:

I'd like to stop here.

Helper reply (verbatim):

Solid: what mTLS adds, the extra handshake messages, and the trust store.

Record in your learner state:  
- Why ALB mTLS recommends verify mode — you described verify and passthrough but didn't give the recommendation or reason.

No score — this is just a check.
