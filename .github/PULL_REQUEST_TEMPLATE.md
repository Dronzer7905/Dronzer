## Description

<!-- Briefly describe the changes in this PR. What problem does it solve? -->

## Related Issues

<!-- Link to related issues (e.g., Fixes #123, Closes #456) -->

## Type of Change

- [ ] 🐛 Bug fix (non-breaking change that fixes an issue)
- [ ] ✨ New feature (non-breaking change that adds functionality)
- [ ] 🔌 New provider integration
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to change)
- [ ] 📝 Documentation update
- [ ] ♻️ Refactor (code change that neither fixes a bug nor adds a feature)
- [ ] 🔧 Infrastructure / CI change

## Quality Checklist

- [ ] Code compiles and passes all static analysis (`ruff check .`, `ruff format .`, `mypy .`).
- [ ] Unit tests have been added or updated and pass (`pytest tests/`).
- [ ] **Clean Architecture boundaries are respected** — no infrastructure imports in domain, no domain bypasses.
- [ ] All new Python functions have complete type annotations (no `Any` escapes).
- [ ] No magic strings — all new constants are defined as enums or named constants.
- [ ] Documentation has been updated (README, guides, CHANGELOG if applicable).
- [ ] If adding a new provider: `SUPPORT_MATRICES.md` has been updated.

## Testing Notes

<!-- Describe how you tested this change. What test cases did you add or verify? -->
