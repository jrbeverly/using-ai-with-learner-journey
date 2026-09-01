# Module 6 — Mutual TLS

- **Title**: Mutual TLS
- **Position**: 6 of 7
- **Concepts introduced**: mutual TLS (mTLS), client certificate, CertificateRequest, CertificateVerify, Application Load Balancer (ALB), ALB listener, ALB trust store, verify mode, passthrough mode, X-Amzn-Mtls headers
- **Prerequisites**: Module 4 (TLS foundations), Module 5 (certificates and trust)
- **Content files**: `modules/06-mutual-tls.md`
- **Summary**: By the end of this module the learner can explain what mTLS adds to one-way TLS, which extra messages appear in the handshake, what a server-side trust store is for, and how ALB mTLS's verify and passthrough modes differ.

## What mutual TLS adds

Mutual TLS (mTLS) is TLS with client authentication: the server additionally demands that the client prove its identity with a certificate. The mechanics mirror Module 4 in reverse — the client holds its own certificate and private key, and the server holds a trust store of the CAs it accepts. mTLS authenticates at the transport layer, before any application logic runs: the connection itself carries identity.

## The handshake difference

In the handshake, the server sends a CertificateRequest listing the CAs it accepts. The client replies with its certificate and a CertificateVerify message: a signature over the handshake transcript made with the client's private key, proving it holds the key and not just a copy of the certificate. The server then validates the client's chain against its trust store (with optional revocation checks), exactly as the client validated the server in Module 5. Both directions of authentication use the same machinery.

## mTLS on an Application Load Balancer

An Application Load Balancer (ALB) — AWS's layer-7 load balancer — can terminate mTLS at the edge of a network. An ALB trust store holds a bundle of CA certificates (roots and intermediates); AWS Private CA can act as the issuer. The listener then operates in one of two modes:

- Verify mode: the ALB validates the client certificate chain against the trust store and, optionally, against CRLs you supply. Invalid certificates are rejected at the edge. The ALB forwards the validated identity to the application in X-Amzn-Mtls headers: leaf serial number, issuer, subject, validity dates, and the leaf certificate itself.
- Passthrough mode: the ALB performs no validation and forwards the entire chain to the application in a single X-Amzn-Mtls-Clientcert header, leaving validation to the application.

Position: use verify mode. Pushing chain validation into each application duplicates what the ALB already does, and unvalidated traffic reaching an application is the failure mode mTLS exists to prevent. Note also that ALB mTLS does not support TLS session resumption — every connection pays a fresh handshake.

## Diagram

```text
client (own certificate + key)              ALB (server certificate + trust store)
  |---- ClientHello -------------------------------->|
  |<--- ServerHello, Certificate,                    |
  |     CertificateRequest ("CAs I accept"),         |
  |     Finished ------------------------------------|
  |---- Certificate (client's),                      |
  |     CertificateVerify (signature over the        |
  |     handshake, proves key possession) ---------->|  ALB validates chain
  |<=== encrypted application data ==================|  against trust store
```

## Go deeper

- [Mutual authentication with TLS in Application Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/mutual-authentication.html)
- [Configuring mutual TLS on an Application Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/configuring-mtls-with-elb.html)
