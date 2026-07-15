# Dronzer AI Gateway - Enterprise Platform Guide

Welcome to the Dronzer Enterprise Platform. This guide covers how to operate the Gateway in a massive multi-tenant environment, supporting thousands of projects and enforcing strict B2B compliance.

## Multi-Tenancy Hierarchy
The Gateway uses a Strict isolation model based on two primary concepts:
1. **Organizations**: The top-level tenant representing a Company or Business Unit.
2. **Projects**: Isolated execution environments beneath an Organization (e.g., `Prod-Marketing-App`, `Dev-Backend`). 
API Keys are vaulted at the Project level. No key can ever access data across Organizations.

## Identity & Single Sign-On (SSO)
Dronzer supports SAML 2.0 and OpenID Connect (OIDC).
- To sync Azure Entra ID or Okta groups into Dronzer, configure the SCIM 2.0 provisioner URL in the Organization settings.
- The built-in ABAC (Attribute-Based Access Control) engine will automatically map SSO groups to Gateway Roles.

## Governance & PII Redaction
If your Enterprise requires HIPAA or GDPR compliance:
1. Navigate to the **Governance** tab in the Dashboard.
2. Enable the **PII Redaction Engine**.
3. All prompts routed through the Gateway will be synchronously masked for SSNs, Emails, and Credit Cards before reaching public models like OpenAI.

## Quotas & Billing
- **RPM & Tokens**: Rate limiters are enforced via Redis sliding-windows. Configure these at the Project level to prevent runaway inference costs.
- **Invoices**: The Billing Engine asynchronously tracks token consumption and maps it to the provider pricing matrices. Monthly CSV/PDF reports are generated automatically.

## Audit Logs
Dronzer logs every configuration change, secret rotation, and API request into an immutable Audit Log format, satisfying SOC2 requirements. Use the Enterprise API to stream these logs into Datadog, Splunk, or Elasticsearch.
