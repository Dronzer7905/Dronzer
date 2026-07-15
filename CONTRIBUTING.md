# Contributing to Dronzer

First off, thank you for considering contributing to Dronzer AI Gateway! 

## How Can I Contribute?

### Reporting Bugs
- Use the issue tracker to report bugs.
- Describe the bug clearly, including steps to reproduce.

### Suggesting Enhancements
- Open an issue describing the feature.
- Explain why this enhancement would be useful.

### Pull Requests
1. Fork the repo and create your branch from `main`.
2. Run `poetry run pytest` and ensure tests pass.
3. Run `poetry run ruff check .` and `poetry run black .` to adhere to code styles.
4. Open the Pull Request and describe the changes thoroughly.

We enforce a strict "No Magic Strings" policy and mandate type-hints across the entire Python backend.
