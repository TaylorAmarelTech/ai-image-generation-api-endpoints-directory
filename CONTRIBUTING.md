# Contributing to AI Image Generation API Endpoints Directory

Thank you for your interest in contributing! This guide will help you get started.

## How to Add a New Provider

1. **Edit `providers.py`** -- Add a new entry to the providers list with the following fields:
   - `name`: The provider's display name
   - `slug`: A URL-safe identifier (lowercase, hyphens)
   - `endpoint`: The base API endpoint URL
   - `tier`: One of `free`, `freemium`, or `paid`
   - `auth_type`: Authentication method (e.g., `api_key`, `bearer`, `oauth2`)
   - `models`: List of supported models
   - `docs_url`: Link to the provider's API documentation
   - `free_limits`: Description of free-tier limits (if applicable)

2. **Add the environment variable** -- Add the provider's API key variable to `.env.example`:
   ```
   NEWPROVIDER_API_KEY=your_api_key_here
   ```

3. **Run the scanner** -- Verify the new provider is detected and reachable:
   ```bash
   python scanner.py
   ```

4. **Submit a pull request** -- See the PR process below.

## How to Report Issues

- **Bugs**: Use the [Bug Report](.github/ISSUE_TEMPLATE/bug-report.md) template.
- **New providers**: Use the [New Provider](.github/ISSUE_TEMPLATE/new-provider.md) template.
- **Provider updates**: Use the [Provider Update](.github/ISSUE_TEMPLATE/provider-update.md) template.

Please search existing issues before opening a new one to avoid duplicates.

## Code Style

This project uses the following tools to enforce consistent code style:

- **[Black](https://github.com/psf/black)** -- Code formatter (line length: 88)
- **[Ruff](https://github.com/astral-sh/ruff)** -- Linter

Before submitting a PR, run:

```bash
black .
ruff check --fix .
```

## PR Process

1. Fork the repository and create a feature branch from `main`.
2. Make your changes, following the code style guidelines above.
3. Add or update tests if applicable.
4. Run the scanner to verify nothing is broken.
5. Fill out the pull request template completely.
6. A maintainer will review your PR. Please be patient and responsive to feedback.

## Issue Templates

All issue templates are located in [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/):

- [New Provider](.github/ISSUE_TEMPLATE/new-provider.md)
- [Provider Update](.github/ISSUE_TEMPLATE/provider-update.md)
- [Bug Report](.github/ISSUE_TEMPLATE/bug-report.md)

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
