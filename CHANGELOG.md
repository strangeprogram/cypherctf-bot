# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-03-19

### Added
- Initial release of the CypherCTF bot
- Core IRC bot functionality with async support
- Challenge system with hints and scoring
- User registration and authentication
- Comprehensive test suite
- GitHub Actions CI/CD pipeline
- Linting configuration (flake8, black, isort)
- Package distribution setup (setup.py, pyproject.toml)
- Release automation for PyPI publishing

### Changed
- Enhanced message handling and user interactions
- Improved challenge completion flow
- Updated documentation and code organization

### Fixed
- User querying issues
- Message handling edge cases
- Challenge completion validation

### Security
- Secure environment variable handling
- Input validation and sanitization
- Rate limiting for challenge submissions

## [0.1.0] - 2024-03-19

### Added
- Basic bot structure
- Initial challenge implementation
- Environment configuration
- Basic documentation

[1.0.0]: https://github.com/strangeprogram/cypherctf-bot/releases/tag/v1.0.0
[0.1.0]: https://github.com/strangeprogram/cypherctf-bot/releases/tag/v0.1.0 