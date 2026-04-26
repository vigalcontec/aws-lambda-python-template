"""Pytest fixtures and configuration."""

import os
from typing import Generator
from unittest.mock import patch

import boto3
import pytest
from moto import mock_aws


@pytest.fixture(autouse=True)
def aws_credentials() -> Generator[None, None, None]:
    """Mock AWS credentials and datalake environment variables."""
    with patch.dict(
        os.environ,
        {
            "AWS_ACCESS_KEY_ID": "testing",
            "AWS_SECRET_ACCESS_KEY": "testing",
            "AWS_SECURITY_TOKEN": "testing",
            "AWS_SESSION_TOKEN": "testing",
            "AWS_DEFAULT_REGION": "eu-west-1",
            "ENVIRONMENT": "dev",
            # Datalake configuration (simulates Lambda environment variables)
            "RAW_BUCKET_NAME": "datalake-raw-test-dev-123456789012",
            "RAW_BUCKET_ARN": "arn:aws:s3:::datalake-raw-test-dev-123456789012",
            "RAW_KMS_KEY_ARN": "arn:aws:kms:eu-west-1:123456789012:key/raw-key",
            "STAGING_BUCKET_NAME": "datalake-staging-test-dev-123456789012",
            "STAGING_BUCKET_ARN": "arn:aws:s3:::datalake-staging-test-dev-123456789012",
            "STAGING_KMS_KEY_ARN": "arn:aws:kms:eu-west-1:123456789012:key/staging-key",
            "BUSINESS_BUCKET_NAME": "datalake-business-test-dev-123456789012",
            "BUSINESS_BUCKET_ARN": "arn:aws:s3:::datalake-business-test-dev-123456789012",
            "BUSINESS_KMS_KEY_ARN": "arn:aws:kms:eu-west-1:123456789012:key/business-key",
        },
    ):
        yield


@pytest.fixture
def s3_client() -> Generator[boto3.client, None, None]:
    """Create mocked S3 client."""
    with mock_aws():
        client = boto3.client("s3", region_name="eu-west-1")
        yield client


@pytest.fixture
def lambda_event() -> dict:
    """Sample Lambda event."""
    return {
        "key1": "value1",
        "key2": "value2",
    }


@pytest.fixture
def lambda_context():
    """Mock Lambda context."""

    class MockContext:
        function_name = "test-function"
        memory_limit_in_mb = 256
        invoked_function_arn = "arn:aws:lambda:eu-west-1:123456789012:function:test"
        aws_request_id = "test-request-id"

    return MockContext()
