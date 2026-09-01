# Learner conversation transcript
## Run — 2026-09-28T18:05:27Z (replay)
- Helper: mtls-tutor (helpers/mtls-tutor.md)
- Module: modules/06-mutual-tls.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Base URL: https://api.deepseek.com/anthropic

### Turn 1
- Helper: mtls-tutor
- Module: modules/06-mutual-tls.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Time: 2026-09-28T18:05:35Z

Learner:

What's the difference between the ALB's verify and passthrough modes, and which one should I use?

Helper reply (verbatim):

In verify mode, the ALB validates the client certificate chain against its trust store and, optionally, against CRLs you supply, rejecting invalid certificates at the edge; it then forwards the validated identity to the application in `X-Amzn-Mtls` headers — leaf serial number, issuer, subject, validity dates, and the leaf certificate itself [module]. In passthrough mode, the ALB performs no validation and forwards the entire chain to the application in a single `X-Amzn-Mtls-Clientcert` header, leaving validation to the application [module].

Use verify mode [module]. The module’s position is that pushing chain validation into each application duplicates what the ALB already does, and unvalidated traffic reaching an application is the failure mode mTLS exists to prevent [module].

### Turn 2
- Helper: mtls-tutor
- Module: modules/06-mutual-tls.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Time: 2026-09-28T18:05:42Z

Learner:

Which extra messages does mTLS add to the handshake, and what does each one prove?

Helper reply (verbatim):

mTLS adds a server-side **CertificateRequest** after the server’s Certificate message, listing the CAs it accepts; this signals the server’s demand for client authentication and tells the client which certificate chains the server will consider [module]. The client then sends two additional messages: its **Certificate** and a **CertificateVerify** [module].

The client Certificate message presents the client’s identity, while the CertificateVerify message is a signature over the handshake transcript made with the client’s private key — this proves the client actually holds the private key matching the certificate, not just a copy of the certificate [module]. After that, the server validates the client’s chain against its trust store, with optional revocation checks, using the same machinery as the client-side validation from Module 5 [module].

### Turn 3
- Helper: mtls-tutor
- Module: modules/06-mutual-tls.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Time: 2026-09-28T18:05:49Z

Learner:

Remind me how the client validated the server's certificate in one-way TLS.

Helper reply (verbatim):

In one-way TLS, the client validated the server’s certificate chain against its own trust store, with optional revocation checks — this module references that as the same machinery the server now applies to the client certificate in mTLS [derived]. From general TLS, that validation typically includes verifying the chain of signatures up to a trusted root, checking the certificate’s validity dates, and confirming the server’s hostname matches the certificate [general]. That’s exactly the validation the ALB performs in verify mode, except it uses the ALB’s trust store rather than the client’s [module].
