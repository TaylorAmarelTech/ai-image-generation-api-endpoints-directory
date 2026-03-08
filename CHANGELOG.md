# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-03-07

### Added

- Initial release of the AI Image Generation API Endpoints Directory.
- Support for 40+ image generation API providers across free, freemium, and paid tiers.
- Automated endpoint scanner (`scanner.py`) to verify provider availability and response times.
- Command-line interface (`cli.py`) for listing, filtering, and querying providers.
- Report generator (`report_generator.py`) for producing Markdown and JSON status reports.
- Provider configuration module (`providers.py`) with structured metadata for each endpoint.
- Environment-based API key management via `.env` with `.env.example` template.
- Comprehensive project documentation including README, contributing guide, and security policy.
