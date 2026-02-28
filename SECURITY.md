# Security Policy

## Supported Versions

Arkham Asylum Backend adheres to strict security standards. We currently only support the latest major release of this repository.

| Version | Supported          |
| ------- | ------------------ |
| v1.0.x  | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

As a highly classified digital infrastructure designed for Gotham's most dangerous inmates, security vulnerabilities are treated with the highest severity.

Please **DO NOT** report security vulnerabilities via public GitHub issues.

If you believe you have found a security vulnerability in this project, please report it immediately via private channel:

1. Email the core maintainer directly at `bruce.wayne@wayneenterprises.com` (or your valid email contact).
2. Include a detailed description of the vulnerability.
3. Include specific steps, payloads, or endpoints required to reproduce the exploit.

You should expect an initial response acknowledging the vulnerability within 24 hours. If the vulnerability is accepted, we will coordinate a timeline with you for a secure patch and responsible disclosure.

### Scope

This policy applies specifically to:

* The Django ORM Admission and Transfer Engines (e.g. bypassing capacity or clearance checks)
* Authentication bypasses (Djoser/JWT circumvention)
* Privilege Escalation leading to unauthorized `MedicalFile` access
* Circumvention of the `AuditLog` immutability protocols

### Out of Scope

* Rate-limiting or DoS attacks (Handled at the ingress/proxy level, not application code).
* Theoretical vulnerabilities without an actionable exploit path.
