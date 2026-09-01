# Module 4 — TLS foundations

- **Title**: TLS foundations
- **Position**: 4 of 7
- **Concepts introduced**: TLS, HTTPS, handshake, symmetric encryption, asymmetric encryption, session key, cipher suite, Server Name Indication (SNI), server certificate, one-way TLS
- **Prerequisites**: Module 1 (networking foundations)
- **Content files**: `modules/04-tls-foundations.md`
- **Summary**: By the end of this module the learner can describe what the TLS handshake accomplishes, why it ends with symmetric encryption, what the server certificate proves, and why ordinary TLS does not authenticate the client.

## What TLS provides

Transport Layer Security (TLS) sits between TCP and the application; HTTPS is HTTP over TLS. A TLS connection provides three properties: confidentiality (an observer sees ciphertext), integrity (tampering is detected), and authentication of the server (the client knows who it is talking to). Only the first two are automatic; the third depends on certificates, covered properly in Module 5.

## The handshake

Before application data flows, client and server run a handshake (simplified):

1. The client sends ClientHello: supported protocol versions, the cipher suites it accepts, and — because one server often hosts many names — the hostname it wants, via Server Name Indication (SNI).
2. The server replies with its chosen parameters and its certificate, and proves it holds the matching private key.
3. The client validates the server certificate (Module 5) and both sides derive the same session key.
4. Finished messages confirm the handshake, and application data flows encrypted with the session key.

The details differ between TLS 1.2 and 1.3 — TLS 1.3 encrypts most of the handshake itself — but the outcome is the same: agreed symmetric keys and an authenticated server.

## Why symmetric keys

Asymmetric (public-key) cryptography authenticates and agrees on keys, but it is too slow for bulk data. The handshake's job is to bootstrap symmetric encryption, which is fast: both sides end up encrypting the stream with the same session key.

## One-way TLS

In the handshake above the server proves its identity but the client proves nothing; the server knows only what the client chose to send. This is one-way TLS, the default everywhere on the web. That asymmetry is exactly what mutual TLS removes in Module 6.

## Diagram

```text
client                                      server
  |---- ClientHello (versions, ciphers, SNI) ---->|
  |<--- ServerHello, Certificate, key exchange,   |
  |     Finished ---------------------------------|
  |     client validates the server certificate   |
  |     (see Module 5)                            |
  |---- Finished -------------------------------->|
  |<=== application data, encrypted with =========|
        the shared session key
```

## Go deeper

- [RFC 8446 — TLS 1.3](https://datatracker.ietf.org/doc/html/rfc8446)
