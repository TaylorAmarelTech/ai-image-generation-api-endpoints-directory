# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | Yes                |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly.

**Do not open a public issue.** Instead, send an email to:

**security@tayloramareltech.com**

Please include:

- A description of the vulnerability.
- Steps to reproduce the issue.
- The potential impact.
- Any suggested fixes, if applicable.

We will acknowledge receipt within 48 hours and aim to provide a resolution or mitigation plan within 7 business days.

## API Key Safety

This project works with third-party API keys. Follow these rules to keep credentials safe:

- **Never commit API keys** to version control. All keys belong in your local `.env` file, which is listed in `.gitignore`.
- **Use `.env.example`** as a reference for required environment variables. It contains placeholder values only.
- **Rotate keys immediately** if you suspect they have been exposed.
- **Do not share `.env` files** in issues, pull requests, or any public channel.
- **Review diffs before committing** to ensure no secrets are included.

## Dependencies

Keep all dependencies up to date. Run periodic audits:

```bash
pip audit
```

Report any dependency-related vulnerabilities through the same email channel listed above.
