# Learner conversation transcript
## Run — 2026-09-28T17:35:11Z (interactive)
- Helper: smoke-tutor (helpers/smoke-tutor.md)
- Module: modules/02-private-connectivity-vpc.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Base URL: https://api.deepseek.com/anthropic

### Turn 1
- Helper: smoke-tutor
- Module: modules/02-private-connectivity-vpc.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Time: 2026-09-28T17:35:14Z

Learner:

What is a NAT gateway for in a VPC?

Helper reply (verbatim):

A NAT gateway gives instances in a private subnet outbound-only internet access. It lives in a public subnet, holds an elastic IP address, and translates the private source addresses of outbound packets to its own public address, then translates replies back [module]. Because the mapping only exists for flows the private instances initiated, the internet cannot initiate connections inward [module].

It is not for hosting services that must be reachable from outside—that belongs behind an ingress point in a public subnet instead [module]. Each AZ should have its own NAT gateway so that AZ’s private subnets don’t lose egress if another AZ fails [module].

### Turn 2
- Helper: smoke-tutor
- Module: modules/02-private-connectivity-vpc.md
- Learner state: none
- Model: deepseek-v4-pro[1m] (max_tokens=1024)
- Time: 2026-09-28T17:35:19Z

Learner:

What would fail without it?

Helper reply (verbatim):

Without a NAT gateway, instances in a private subnet cannot initiate outbound internet traffic at all, so things like downloading updates or calling external APIs would fail [module]. A private subnet has no route to the internet, so it needs that NAT gateway in a public subnet to translate its outbound traffic [module].

For AWS service APIs specifically, you may not need a NAT gateway if you use VPC endpoints instead; the module says private subnets should reach AWS services through endpoints rather than a NAT gateway wherever an endpoint exists [module].
