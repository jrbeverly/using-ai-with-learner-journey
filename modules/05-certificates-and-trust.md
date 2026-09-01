# Module 5 — Certificates and trust

- **Title**: Certificates and trust
- **Position**: 5 of 7
- **Concepts introduced**: X.509 certificate, public key, private key, certificate authority (CA), root CA, intermediate CA, certificate chain, trust anchor, trust store, subject alternative name (SAN), validity period, revocation (CRL, OCSP), AWS Certificate Manager (ACM), AWS Private CA
- **Prerequisites**: Module 4 (TLS foundations)
- **Content files**: `modules/05-certificates-and-trust.md`
- **Summary**: By the end of this module the learner can explain what a certificate binds together, how a chain of CAs lets a stranger's certificate be trusted, what a client actually checks during validation, and the division of labor between ACM and AWS Private CA.

## What a certificate is

An X.509 certificate is a signed statement binding a public key to an identity: a subject name plus subject alternative names (SANs — the hostnames the certificate is valid for), a validity period, and the issuer that vouches for it. Whoever holds the matching private key can prove ownership of that identity. Anyone can mint a certificate; one is only worth what its issuer's signature is worth.

## Chains and trust anchors

A client does not trust a server's certificate directly. It walks a chain: the certificate is signed by an intermediate CA's private key, the intermediate by a root CA, and the root is self-signed. The root is a trust anchor — a certificate the client has been configured to trust, held in its trust store (typically shipped with the operating system, or installed by an operator). Validation means: build the chain from the presented certificate to an anchor in the trust store, check that a SAN matches the hostname, check the validity dates, and check revocation. Trust is therefore a local decision: a CA can issue a certificate for anything, but it only matters if the peer trusts that CA.

## Revocation

A compromised private key makes a certificate worthless before its expiry date. CRLs (certificate revocation lists) are CA-published lists of revoked serials; OCSP lets a client query the revocation status of one certificate. Not every TLS endpoint checks both; AWS's mutual-TLS feature checks CRLs that you supply, which Module 6 builds on.

## Where AWS fits

Two services cover the two certificate worlds:

- AWS Certificate Manager (ACM) provisions and renews public certificates for use with integrated AWS services such as load balancers; the certificates themselves cost nothing and renewal is automatic.
- AWS Private CA runs your own private CAs for internal identities. A private CA costs about $400/month in general-purpose mode, or $50/month in short-lived mode (certificates valid at most 7 days) — a constraint that shapes the architecture in Module 7.

## Diagram

```text
trust store of the client
    |
    | trust anchor: "I trust this root"
    v
root CA certificate (self-signed)
    | signed by the root's private key
    v
intermediate CA certificate
    | signed by the intermediate's private key
    v
leaf certificate (SAN: api.example.com)
    | paired with the leaf private key held by the server
```

## Go deeper

- [RFC 5280 — X.509](https://datatracker.ietf.org/doc/html/rfc5280)
- [What is AWS Certificate Manager?](https://docs.aws.amazon.com/acm/latest/userguide/acm-overview.html)
- [What is AWS Private CA?](https://docs.aws.amazon.com/privateca/latest/userguide/PcaWelcome.html)
- [AWS Private CA pricing](https://aws.amazon.com/private-ca/pricing/)
