# AWS Lambda Python Template

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python)](https://www.python.org/)
[![Poetry](https://img.shields.io/badge/Poetry-1.8%2B-60A5FA?logo=poetry)](https://python-poetry.org/)
[![Docker](https://img.shields.io/badge/Docker-ECR-2496ED?logo=docker)](https://aws.amazon.com/ecr/)
[![Terraform](https://img.shields.io/badge/Terraform-1.10%2B-7B42BC?logo=terraform)](https://www.terraform.io/)

Production-ready AWS Lambda template using Python, Poetry for dependency management, and Docker container deployment to ECR.

---

## 📋 Table of Contents

- [Features](#features)
- [Repository Structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Local Development](#local-development)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Testing](#testing)
- [SSM Parameters](#ssm-parameters)

---

## Features

- ✅ **Python 3.12** - Latest Python runtime
- ✅ **Poetry** - Modern dependency management with lock file
- ✅ **Docker** - Container-based Lambda deployment
- ✅ **ECR** - AWS Elastic Container Registry for images
- ✅ **Terraform** - Infrastructure as Code
- ✅ **GitHub Actions** - CI/CD pipeline with OIDC authentication
- ✅ **Multi-environment** - dev, qa, prod support
- ✅ **SSM Integration** - Read datalake bucket/KMS ARNs from Parameter Store
- ✅ **Structured Logging** - AWS Lambda Powertools
- ✅ **Type Hints** - Full type annotation support

---

## Repository Structure

```
aws-lambda-python-template/
├── .github/
│   └── workflows/
│       └── deploy.yml              # CI/CD pipeline
├── src/
│   └── handler/
│       ├── __init__.py
│       ├── main.py                 # Lambda entry point
│       ├── config.py               # Configuration management
│       └── utils/
│           ├── __init__.py
│           ├── s3.py               # S3 utilities
│           └── ssm.py              # SSM parameter utilities
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # Pytest fixtures
│   └── test_handler.py             # Unit tests
├── terraform/
│   ├── config.tf                   # ⭐ PROJECT CONFIG (edit this!)
│   ├── main.tf                     # Lambda + ECR resources
│   ├── variables.tf                # Runtime variables (env, image_tag)
│   ├── outputs.tf                  # Output values
│   ├── iam.tf                      # IAM role and policies
│   ├── backend.tf                  # S3 backend (uses -backend-config)
│   ├── ssm_imports.tf              # Datalake SSM parameters
│   └── ssm_exports.tf              # Lambda SSM exports
├── Dockerfile                      # Lambda container image
├── pyproject.toml                  # Poetry configuration
├── poetry.lock                     # Locked dependencies
├── docker-compose.yml              # Local development
├── Makefile                        # Development commands
├── CHANGELOG.md
└── README.md
```

---

## Prerequisites

- **Python 3.12+**
- **Poetry 1.8+**
- **Docker**
- **AWS CLI v2**
- **Terraform 1.10+**

### Install Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

---

## Quick Start

### 1. Create New Repository from Template

```bash
# Clone template
git clone https://github.com/vigalcontec/aws-lambda-python-template.git my-lambda-function
cd my-lambda-function

# Remove template git history
rm -rf .git
git init
```

### 2. Configure Your Project

Edit `terraform/config.tf`:

```hcl
locals {
  function_name = "my-data-processor"   # Your function name
  project_name  = "my-project"          # Your project name
  company_name  = "vigalcontec"         # Your company name
  
  # Lambda settings
  timeout     = 30
  memory_size = 256
}
```

Update `pyproject.toml`:

```toml
[tool.poetry]
name = "my-data-processor"
```

### 3. Install Dependencies

```bash
poetry install
```

### 4. Run Locally

```bash
# Using Docker
make docker-run

# Or using Poetry
make run-local
```

---

## Local Development

### Install Dependencies

```bash
poetry install --with dev
```

### Run Tests

```bash
make test
```

### Format Code

```bash
make format
```

### Lint Code

```bash
make lint
```

### Build Docker Image

```bash
make docker-build
```

---

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ENVIRONMENT` | Environment name (dev/qa/prod) | Yes |
| `AWS_REGION` | AWS region | Yes |
| `LOG_LEVEL` | Logging level (DEBUG/INFO/WARNING/ERROR) | No |

### SSM Parameters (Auto-discovered)

The Lambda automatically reads these from SSM Parameter Store:

| Parameter | Description |
|-----------|-------------|
| `/{env}/datalake/raw/bucket_name` | Raw layer S3 bucket |
| `/{env}/datalake/raw/kms_key_arn` | Raw layer KMS key |
| `/{env}/datalake/staging/bucket_name` | Staging layer S3 bucket |
| `/{env}/datalake/staging/kms_key_arn` | Staging layer KMS key |
| `/{env}/datalake/business/bucket_name` | Business layer S3 bucket |
| `/{env}/datalake/business/kms_key_arn` | Business layer KMS key |

---

## Deployment

### GitHub Actions (Recommended)

Push to branch triggers automatic deployment:

| Branch | Environment |
|--------|-------------|
| `main` | prod |
| `release/*` | qa |
| `develop`, `feature/*` | dev |

**No GitHub Variables needed!** Configuration is read from `terraform/config.tf`.

### Manual Deployment

```bash
# Build and push Docker image
make docker-push ENV=dev

# Deploy infrastructure
cd terraform
terraform init \
  -backend-config="bucket=tfstate-vigalcontec-dev-123456789012" \
  -backend-config="key=lambda/my-lambda-function/terraform.tfstate" \
  -backend-config="region=eu-west-1" \
  -backend-config="encrypt=true"

terraform apply -var="environment=dev"
```

---

## Testing

### Unit Tests

```bash
make test
```

### Coverage Report

```bash
make coverage
```

### Integration Tests (requires AWS credentials)

```bash
make test-integration
```

---

## SSM Parameters

This template is designed to work with the `aws-datalake-layers` infrastructure. It automatically discovers bucket names and KMS keys from SSM Parameter Store.

### Reading Parameters in Code

```python
from handler.utils.ssm import get_datalake_config

config = get_datalake_config(environment="dev")
print(config.raw_bucket_name)
print(config.raw_kms_key_arn)
```

---

## License

MIT
