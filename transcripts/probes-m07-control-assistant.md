# Learner conversation transcript
## Run — 2026-09-28T18:51:02Z (replay)
- Helper: control-assistant (helpers/control-assistant.md)
- Module: modules/07-combined-architecture.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=8192)
- Base URL: https://api.deepseek.com/anthropic

### Turn 1
- Helper: control-assistant
- Module: modules/07-combined-architecture.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=8192)
- Time: 2026-09-28T18:51:22Z

Learner:

The module names the trust boundaries as the VPN edge, the ALB listener, and the security groups around the instances. Explain what each boundary checks, drawing on Modules 3, 6, and 2.

Helper reply (verbatim):

Each boundary checks a different layer of the request, so no single check has to do everything.

### VPN edge — “Is this coming from a trusted network path?”

This is the Module 3 boundary. It has two forms:

- **Site-to-Site VPN from the data center:** IPsec/IKE authenticates the on-premises VPN peer and establishes encrypted tunnels. BGP then controls which routes are accepted and advertised.
- **Client VPN for engineers:** TLS and client certificates authenticate the remote laptop or engineer before any private VPC address is reachable.

The VPN edge checks that traffic is coming from an authorized network or user over an encrypted tunnel. It does **not** authorize individual API calls.

### ALB listener — “Is this caller presenting a valid client certificate?”

This is the Module 6 boundary. The ALB listener terminates TLS in **mutual TLS verify mode**:

1. The ALB presents its server certificate.
2. It requires and validates the caller’s client certificate.
3. It checks the certificate chain against the Private CA trust store.
4. It checks revocation through the CRL.

If the client certificate is valid, the ALB forwards the request over plain HTTP inside the VPC with `X-Amzn-Mtls` headers carrying the validated identity. The listener checks **who the caller is**, based on the certificate.

### Security groups around the instances — “Did this packet come from the ALB?”

This is the Module 2 boundary. The service instances’ security groups allow traffic from the ALB security group only, on the expected port and protocol. Every other source is denied.

Security groups do not inspect certificates or user identity. They enforce **network reachability**: the only system that can send requests to the instances is the ALB. That is what makes the identity headers from the ALB trustworthy to the application — there is no other path to the service.

### Turn 2
- Helper: control-assistant
- Module: modules/07-combined-architecture.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=8192)
- Time: 2026-09-28T18:51:27Z

Learner:

Explain that more simply.

Helper reply (verbatim):

In simple terms, each boundary asks one basic question:

1. **VPN edge** — “Are you allowed into the private network at all?”  
   It checks that the connection comes over an encrypted tunnel from a known office network or an approved engineer laptop.

2. **ALB listener** — “Is your client certificate valid, and are you who it says you are?”  
   It checks the caller’s certificate, verifies the chain, and checks the CRL to make sure the certificate is not revoked.

3. **Security groups around the instances** — “Is this request coming from the ALB, and nothing else?”  
   They only allow traffic from the ALB. They don’t look at identity — they just make sure the ALB is the only path to the service.

So each boundary checks a different layer: the network, the identity, and the final network hop.

### Turn 3
- Helper: control-assistant
- Module: modules/07-combined-architecture.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=8192)
- Time: 2026-09-28T18:52:03Z

Learner:

Give me a concrete example of the certificate lifecycle: client certificates are issued in short-lived mode and re-issued with every deployment. Walk through what happens to the old certificates, and what happens if one key is lost mid-week.

Helper reply (verbatim):

Concrete example: an on-premises calling service, `orders-client`, deploys every Monday morning and gets a new short-lived client certificate from AWS Private CA as part of the deployment.

### Normal rotation

**Monday, Jan 6 at 09:00**

- The deployment pipeline requests a new certificate: serial `C42`, private key `K42`, valid until **Jan 13 at 09:00**.
- The new key and certificate are installed on the caller.
- Last week’s certificate, `C41`, expires around the same time. It is not renewed. If it was not compromised, it is not revoked. It simply stops working when its 7-day validity ends.

**What normally happens to old certificates:**

- They are replaced at deployment time.
- They are **not** renewed or extended.
- If not compromised, they expire naturally within 7 days.
- Once expired, the ALB rejects them during the mTLS handshake.

### Key lost mid-week

**Thursday, Jan 9**

- The private key `K42` is exposed: a laptop is lost, a secret is committed to a repo, or a backup is leaked.
- The team revokes certificate `C42` in AWS Private CA.
- The CA’s CRL now marks `C42` as revoked.
- The ALB checks the CRL during the mTLS handshake, so a client presenting `C42` is rejected.

**What happens next:**

1. A replacement certificate, `C43`, is issued with a new private key `K43`.
2. `C43` is valid for at most 7 more days.
3. The caller is redeployed or updated out of band with `K43`.
4. The stolen `K42` becomes useless once the CRL is in effect.

Even in a worst-case delay where the CRL has not yet propagated, the stolen certificate could only remain valid until **Jan 13 at 09:00**, because it was issued in short-lived mode.

So normal rotation is just “next deployment, new certificate.” A lost key is handled the same way, plus an immediate revocation. The short lifetime keeps the compromise window small, and the CRL is the immediate backstop.

### Turn 4
- Helper: control-assistant
- Module: modules/07-combined-architecture.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=8192)
- Time: 2026-09-28T18:52:39Z

Learner:

In the diagram at the end of the module, trace a request from the engineer's laptop all the way to a service instance and back, naming every component and trust boundary it crosses.

Helper reply (verbatim):

Here is the full path from the engineer’s laptop to the service instance and back, following the diagram.

The request is: `GET https://api.internal.example.com/...`

### Outbound path

1. **Engineer’s laptop**  
   The laptop is already connected to **AWS Client VPN**. If needed, it first resolves `api.internal.example.com` to the ALB’s address using private DNS.

2. **Client VPN edge — first trust boundary**  
   The request enters the encrypted Client VPN tunnel. This boundary authenticates the laptop and ensures the traffic is coming from an approved engineer over a secure tunnel. The request then reaches the **transit gateway**.

3. **Transit gateway**  
   The transit gateway routes the request into the VPC through the VPC attachment. It does not inspect application identity; it is a routing component.

4. **ALB listener — second trust boundary**  
   Inside the VPC, the request reaches the **Application Load Balancer** listener on port 443. Here the ALB:
   - presents its server certificate from **ACM**
   - requires the laptop to present a client certificate
   - validates the client certificate chain against the **Private CA trust store**
   - checks the **CRL** to confirm the certificate is not revoked

   This is the mTLS verification boundary. If the client certificate is invalid, the request stops here.

5. **ALB to target instance**  
   After validation, the ALB selects a target through the **target group** and forwards the request over plain HTTP inside the VPC. It adds `X-Amzn-Mtls` identity headers carrying the validated certificate identity.

6. **Instance security group — third trust boundary**  
   The service instance’s security group allows traffic only from the ALB security group. It does not inspect identity or certificates; it enforces that the ALB is the only allowed source. If the request passes, it reaches the **service instance**.

7. **Application authorization**  
   The application reads the identity from the `X-Amzn-Mtls` headers, for example the subject or serial number, and authorizes the request.

### Return path

The response takes the same path in reverse:

1. **Service instance** sends the response back to the ALB. The security group is stateful, so return traffic to the ALB is allowed automatically.
2. **ALB** sends the response back over the mTLS TLS session to the laptop.
3. The response passes through the **transit gateway** and the **Client VPN tunnel** back to the laptop.

### Components not crossed on this request

- **NAT gateways** — not used, because the request stays inside private AWS networking.
- **VPC interface endpoints** — not used, because the request is to an internal service, not an AWS API.
- **On-premises data center VPN** — not used, because the caller is the engineer’s laptop, not a server in the data center.

### Turn 5
- Helper: control-assistant
- Module: modules/07-combined-architecture.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=8192)
- Time: 2026-09-28T18:53:27Z

Learner:

How would this architecture change if we used OAuth2 tokens instead of client certificates?

Helper reply (verbatim):

The biggest change is that client authentication moves out of the TLS handshake and becomes an application-level bearer token. The ALB no longer needs mTLS.

## What stays the same

- The VPC, public/private subnets, two-AZ layout, NAT gateways, and VPC endpoints.
- The VPN edge: Site-to-Site VPN and Client VPN.
- The ALB still terminates TLS and still uses an ACM server certificate.
- The target group and the instance security group that allows traffic only from the ALB.

## What changes

### 1. ALB listener

The mTLS piece goes away:

- No mTLS verify mode.
- No Private CA trust store.
- No CRL check in the listener.

The listener becomes a normal HTTPS listener using one-way TLS.

With OAuth2, the ALB can either:

- forward the `Authorization: Bearer <token>` header to the service for the application to validate, or
- for browser-style flows, use ALB OIDC authentication and pass OIDC claim headers to the target.

For typical machine-to-machine API calls using OAuth2 access tokens, the ALB usually does **not** validate the token itself. Token validation moves to the application or a token-aware edge component.

### 2. Identity headers

Instead of:

```text
X-Amzn-Mtls-Client-Cert-Subject
X-Amzn-Mtls-Client-Cert-Serial
```

you get OAuth2/OIDC claims such as:

```text
sub
client_id
scope
iss
aud
```

The application authorizes based on those claims rather than on certificate subject or serial.

### 3. Credential lifecycle

The short-lived Private CA client certificate lifecycle is replaced by an OAuth2 lifecycle:

- Clients have OAuth2 client IDs and secrets.
- They receive short-lived access tokens, often valid for minutes.
- They may use refresh tokens to obtain new access tokens.
- The IdP signing keys rotate.
- Client secrets can be rotated.
- Tokens can be revoked, but revocation is not equivalent to a CRL in mTLS.

There is no longer a 7-day client certificate reissued at deploy time.

### 4. Trust boundaries

The boundaries change:

| Boundary | In the mTLS architecture | With OAuth2 |
|---|---|---|
| VPN edge | Unchanged | Unchanged |
| ALB listener | Validates client certificate chain and CRL | Terminates TLS only; may forward or exchange OAuth2 tokens |
| Service instances | Trust `X-Amzn-Mtls` headers from ALB | May need to validate the access token or OIDC claims themselves |
| Security groups | Unchanged | Unchanged |

## Security difference

An mTLS client certificate proves possession of a private key during the handshake. If the key is lost, the CRL can revoke it before the certificate expires.

An OAuth2 access token is a bearer token. Anyone holding it can use it until it expires. That makes short expiry, audience and scope checks, and token binding or DPoP more important.

## Example request path

1. Engineer laptop connects to AWS Client VPN.
2. Laptop obtains an OAuth2 access token from the identity provider.
3. Laptop calls `api.internal.example.com` with:

```http
Authorization: Bearer <access-token>
```

4. ALB terminates TLS using its ACM server certificate.
5. ALB forwards the request to the target instance.
6. The instance security group allows the request because it came from the ALB.
7. The application validates the token or uses forwarded OIDC claims, authorizes the request, and responds.

So the architecture is similar, but the edge identity check changes from “valid client certificate” to “valid OAuth2 token,” and the certificate lifecycle is replaced by a token lifecycle.
