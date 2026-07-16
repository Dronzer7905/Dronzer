# Dronzer Governance Model

The Dronzer project operates under a **meritocratic governance model**. The community is open to everyone — those who contribute consistently and significantly can earn decision-making rights over time.

---

## Roles

| Role | Description |
|---|---|
| **Users** | Anyone using Dronzer in their projects or organization. No formal obligations. |
| **Contributors** | Anyone who submits code, documentation, bug reports, or community support. Recognized in release notes. |
| **Core Maintainers** | Long-term contributors granted commit access and steering committee voting rights. |

---

## Becoming a Core Maintainer

There is no fixed application process. Core Maintainers are recognized organically based on:

- Consistent, high-quality contributions over a sustained period.
- Deep understanding of the codebase and Clean Architecture principles.
- Active participation in code reviews, issues, and design discussions.
- Demonstrated ability to act in the best interests of the project and community.

An existing Core Maintainer will reach out directly to propose membership.

---

## Decision Making

### Routine Decisions
Day-to-day decisions (bug fix approaches, minor feature additions, dependency updates) are made by any Core Maintainer and merged after at least one peer review.

### Major Architectural Decisions
Changes to the fundamental architecture — such as those introduced in v2.0 (Clean Architecture, multi-tenancy, PostgreSQL migration) — require:

1. An **RFC (Request for Comments)** issue opened in the GitHub repository.
2. A minimum **7-day comment period** open to all community members.
3. A **consensus vote** among all active Core Maintainers (majority rules).

> RFC issues are labeled `rfc` and linked from [GitHub Discussions](https://github.com/dronzer7905/dronzer/discussions).

---

## Conflict Resolution

Disagreements between Core Maintainers are resolved through discussion in GitHub Issues or Discussions. If consensus cannot be reached, the project founder casts a deciding vote.
