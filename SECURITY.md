# Security Policy

## Supported Versions

The `2.x` branch is the active branch receiving all security updates and patches.

| Version | Supported          |
| ------- | ------------------ |
| 2.x.x   | ✅ Active support  |
| 1.x.x   | ❌ End of Life     |
| < 1.0   | ❌ End of Life     |

---

## Reporting a Vulnerability

We take the security of the Dronzer AI Gateway very seriously. Security issues may relate to:

- API key encryption or storage
- Backend orchestration and request routing
- Authentication and authorization bypasses
- Injection vulnerabilities in prompt handling
- Dependency vulnerabilities

### How to Report

**Please do NOT file public GitHub Issues for security vulnerabilities.** Doing so may expose the vulnerability to bad actors before a patch is released.

Instead, use GitHub's private vulnerability reporting system:

> 🔒 **[Report a Vulnerability Privately](https://github.com/dronzer7905/dronzer/security/advisories/new)**

This creates a private advisory visible only to the maintainers. We will:

1. Acknowledge receipt within **48 hours**.
2. Investigate and confirm the vulnerability within **7 days**.
3. Coordinate a patch and responsible disclosure timeline with you.
4. Credit you in the release notes (unless you prefer to remain anonymous).

---

## Security Best Practices for Self-Hosted Deployments

- Always generate fresh `SECRET_KEY` and `ENCRYPTION_KEY` values using `openssl rand -hex 32`.
- Never commit your `backend/.env` file to version control.
- Use Kubernetes Secrets or a secrets manager (e.g., AWS Secrets Manager, HashiCorp Vault) for production deployments.
- Rotate provider API keys regularly using the built-in Key Rotation Engine.
- Enable the `/health/detailed` endpoint only for authenticated admin users.
