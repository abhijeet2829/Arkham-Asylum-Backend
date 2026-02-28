# Arkham Asylum Security Deployment Report

<br>

## Native Configuration Audit

This report explicitly details the security warnings flagged natively by Django's production checklist.

**Execution Command:**

```bash
python manage.py check --deploy
```

**Terminal Output:**

```text
System check identified some issues:

WARNINGS:
?: (security.W004) You have not set a value for the SECURE_HSTS_SECONDS setting. If your entire site is served only over SSL, you may want to consider setting a value and enabling HTTP Strict Transport Security. Be sure to read the documentation first; enabling HSTS carelessly can cause serious, irreversible problems.
?: (security.W008) Your SECURE_SSL_REDIRECT setting is not set to True. Unless your site should be available over both SSL and non-SSL connections, you may want to either set this setting True or configure a load balancer or reverse-proxy server to redirect all connections to HTTPS.
?: (security.W009) Your SECRET_KEY has less than 50 characters, less than 5 unique characters, or it's prefixed with 'django-insecure-' indicating that it was generated automatically by Django. Please generate a long and random value, otherwise many of Django's security-critical features will be vulnerable to attack.
?: (security.W012) SESSION_COOKIE_SECURE is not set to True. Using a secure-only session cookie makes it more difficult for network traffic sniffers to hijack user sessions.
?: (security.W016) You have 'django.middleware.csrf.CsrfViewMiddleware' in your MIDDLEWARE, but you have not set CSRF_COOKIE_SECURE to True. Using a secure-only CSRF cookie makes it more difficult for network traffic sniffers to steal the CSRF token.
?: (security.W018) You should not have DEBUG set to True in deployment.
?: (security.W020) ALLOWED_HOSTS must not be empty in deployment.

System check identified 7 issues (0 silenced).
```

<br>

## Layman's Vulnerability Dictation

The 7 flagged issues fundamentally break down into three primary security risks:

### 1. The Blueprint Exposure Risk (`DEBUG` & `ALLOWED_HOSTS`)

- **The Threat:** When the application crashes, `DEBUG = True` tells the system to print out a highly detailed, colorful error page showcasing exact lines of code, database configurations, and active memory variables. If a hacker intentionally crashes the server, they are basically handed the architectural blueprints to the entire Asylum. Additionally, an empty `ALLOWED_HOSTS` means the server will talk to any internet domain that knocks, opening us up to host-header injection attacks.
- **Why we don't fix it locally:** When we are actively coding on the Batcomputer, we *need* to see those detailed crash pages to fix bugs. Disabling debug mode locally makes programming incredibly difficult because we would only see blank "500 Server Error" screens when things break.

### 2. The Cryptographic Key Risk (`SECRET_KEY`)

- **The Threat:** The `SECRET_KEY` acts as the master combination lock for the entire framework. It mathematically signs our JWT authentication tokens and session cookies to ensure they haven't been forged. Django detected our current key is a generic placeholder. If left unchanged in production, attackers can guess the key and forge fake identity badges (tokens) granting themselves Super Admin access.
- **Why we don't fix it locally:** Development keys are generally hardcoded so other engineers can easily download the repository and start the server immediately without complicated local setups.

### 3. The Unencrypted Intercept Risk (`SSL`, `HSTS`, `SECURE COOKIES`)

- **The Threat:** The system is warning us that we are not aggressively forcing all network traffic through an encrypted HTTPS tunnel. If an Arkham guard logs in at a public coffee shop on unencrypted HTTP, a nearby hacker can effortlessly snatch their digital cookies out of the air and impersonate them.
- **Why we don't fix it locally:** Our local `localhost` IP address does not have a registered SSL/TLS certificate from a certificate authority. If we activate these HTTPS-forcing settings on the Batcomputer right now, our local web browser will physically refuse to connect to the server, breaking our ability to test the frontend.

<br>

## Production Mitigation Demonstration

When the time comes to physically hoist Arkham Asylum onto a live cloud server (like AWS or Heroku), we do not delete our development settings. Instead, we use Environmental Variables to inject secure configurations seamlessly into `settings.py`.

Here is a demonstration of how these exact 7 vulnerabilities are mitigated in a production setting:

```python
import os

# 1. Block Blueprint Exposure (W018, W020)
# Debug is STRICTLY turned off, and only our official domain is allowed to connect.
DEBUG = False
ALLOWED_HOSTS = ['api.arkham-asylum.com', 'www.arkham-asylum.com']

# 2. Inject a Cryptographically Secure Master Key (W009)
# The key is never written in the code. It is pulled from a hidden, encrypted server vault.
SECRET_KEY = os.environ.get('DJANGO_PROD_SECRET_KEY')

# 3. Force Aggressive HTTPS Encryption & Secure Cookies (W004, W008, W012, W016)
# Forces all traffic to use HTTPS, and ensures cookies are ONLY sent over encrypted connections.
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # Enforce HTTPS strictly for 1 full year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```
