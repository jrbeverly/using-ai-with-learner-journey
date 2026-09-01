# Learner conversation transcript
## Run — 2026-09-28T19:21:40Z (replay)
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
- Time: 2026-09-28T19:21:43Z

Learner:

Let's check my understanding of this module. Start with how I see the two certificates, then the handshake messages, then the trust store, then the verify and passthrough modes.

Helper reply (verbatim):

Sounds good. First question: in your own words, what does mTLS add to one-way TLS, and which two certificates are involved?

### Turn 2
- Helper: knowledge-check
- Module: modules/06-mutual-tls.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Time: 2026-09-28T19:21:47Z

Learner:

Here's my picture: the client certificate is what the server presents to prove its identity to the client, and the server certificate is what the client sends to prove its identity to the server. That's the reversal mTLS adds over one-way TLS.

Helper reply (verbatim):

There's a naming mix-up, but it's an easy one to fix: the certificate is named for who *holds* it, not who receives it. In mTLS, the server still presents its **server certificate** to the client, and the client presents its **client certificate** to the server. mTLS adds that client side — the server requires proof of the client's identity.[module]

Smaller re-check: which of those two certificates is the new one mTLS adds, and who presents it?

### Turn 3
- Helper: knowledge-check
- Module: modules/06-mutual-tls.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Time: 2026-09-28T19:21:55Z

Learner:

Right — the client certificate is what the server presents, and the server certificate is what the client sends. And the extra handshake messages are CertificateRequest, where the client asks the server to present a certificate, and CertificateVerify, the server's signature proving the server holds the key for the certificate it presented.

Helper reply (verbatim):

Still swapped, so let's put the two sides side by side:

- **Server certificate** — held and presented by the **server** to the client. That part already exists in one-way TLS.
- **Client certificate** — held and presented by the **client** to the server. This is the part mTLS adds.[module]

Then in the handshake, the **server** sends **CertificateRequest** asking for a client certificate. The **client** responds with its **Certificate** and **CertificateVerify** — the client's signature proving the client holds the matching private key.[module]

That's the same reversal twice, so I'd record this one as unclear. Example for your learner state:

- Which party presents the client certificate and which party sends CertificateRequest/CertificateVerify — I kept reversing client and server roles.

Next concept: what is the server-side trust store for in mTLS?

### Turn 4
- Helper: knowledge-check
- Module: modules/06-mutual-tls.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Time: 2026-09-28T19:22:02Z

Learner:

The server-side trust store holds the server's own certificates, the ones it presents to clients, bundled with the roots and intermediates so the client can validate the server's chain against them.

Helper reply (verbatim):

Partly right: the server does present its own certificate (and chain) to the client — that's the one-way TLS part. But the **server-side trust store** is not for that. In mTLS, it holds the **CA certificates (roots and intermediates) the server trusts**, and the server uses it to validate the **client certificate chain** the client presents. It's the reverse of the client's trust store in one-way TLS.[module]

Smaller re-check: in mTLS, whose certificate chain does the server validate against that trust store — its own or the client's?

### Turn 5
- Helper: knowledge-check
- Module: modules/06-mutual-tls.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Time: 2026-09-28T19:22:08Z

Learner:

And the modes: in verify mode the ALB validates the client certificate chain against the trust store and forwards the validated identity in X-Amzn-Mtls headers, rejecting invalid certificates at the edge. In passthrough mode the ALB performs no validation and forwards the entire chain in a single X-Amzn-Mtls-Clientcert header for the application to validate.

Helper reply (verbatim):

Your description of the two modes is right: verify mode validates the client chain at the edge and forwards identity in X-Amzn-Mtls headers, while passthrough forwards the whole chain in a single X-Amzn-Mtls-Clientcert header and leaves validation to the application.[module]

Back to the trust store — you didn't answer the re-check: whose certificate chain does the server validate against its trust store, its own or the client's?

### Turn 6
- Helper: knowledge-check
- Module: modules/06-mutual-tls.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Time: 2026-09-28T19:22:12Z

Learner:

I'd like to stop here.

Helper reply (verbatim):

What seemed solid: your description of verify vs. passthrough modes.

Record in your learner state:
- Which party presents the client certificate and which party sends CertificateRequest/CertificateVerify — I kept reversing client and server roles.
- What the server-side trust store is for — I initially said it holds the server's own certificates; it actually holds the CAs used to validate the client chain.

This is not a score — just notes for your own review.
