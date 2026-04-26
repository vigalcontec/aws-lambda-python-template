# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - YYYY-MM-DD

### Added

- Initial Lambda function template
- Python 3.12 with Poetry dependency management
- Docker container deployment to ECR
- Terraform infrastructure (Lambda, ECR, IAM)
- GitHub Actions CI/CD pipeline with OIDC
- AWS Lambda Powertools integration (Logger, Tracer)
- SSM Parameter Store integration for datalake config
- S3 utilities with KMS encryption support
- Unit tests with pytest and moto
- Code quality tools (ruff, mypy)
- Makefile for common development tasks
