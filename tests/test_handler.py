"""Tests for Lambda handler."""

import pytest

from handler.utils.ssm import DatalakeConfig, get_datalake_config


class TestHandler:
    """Tests for main handler function."""

    def test_handler_success(self, lambda_event: dict, lambda_context) -> None:
        """Test successful handler execution."""
        # Clear cache to ensure fresh config
        get_datalake_config.cache_clear()

        # Act
        from handler.main import handler

        result = handler(lambda_event, lambda_context)

        # Assert
        assert result["statusCode"] == 200
        assert result["body"]["message"] == "Success"
        assert "result" in result["body"]

    def test_handler_processes_event_keys(self, lambda_event: dict, lambda_context) -> None:
        """Test handler returns event keys in result."""
        get_datalake_config.cache_clear()

        from handler.main import handler

        result = handler(lambda_event, lambda_context)

        assert result["body"]["result"]["processed"] is True
        assert "key1" in result["body"]["result"]["event_keys"]
        assert "key2" in result["body"]["result"]["event_keys"]


class TestDatalakeConfig:
    """Tests for datalake configuration from environment variables."""

    def test_get_datalake_config(self) -> None:
        """Test loading datalake config from environment variables."""
        # Clear cache for test
        get_datalake_config.cache_clear()

        # Act
        config = get_datalake_config()

        # Assert
        assert config.raw_bucket_name == "datalake-raw-test-dev-123456789012"
        assert config.staging_bucket_name == "datalake-staging-test-dev-123456789012"
        assert config.business_bucket_name == "datalake-business-test-dev-123456789012"
        assert "kms" in config.raw_kms_key_arn

    def test_datalake_config_all_fields(self) -> None:
        """Test all datalake config fields are populated."""
        get_datalake_config.cache_clear()

        config = get_datalake_config()

        # Raw layer
        assert config.raw_bucket_name != ""
        assert config.raw_bucket_arn.startswith("arn:aws:s3:::")
        assert config.raw_kms_key_arn.startswith("arn:aws:kms:")

        # Staging layer
        assert config.staging_bucket_name != ""
        assert config.staging_bucket_arn.startswith("arn:aws:s3:::")
        assert config.staging_kms_key_arn.startswith("arn:aws:kms:")

        # Business layer
        assert config.business_bucket_name != ""
        assert config.business_bucket_arn.startswith("arn:aws:s3:::")
        assert config.business_kms_key_arn.startswith("arn:aws:kms:")


class TestS3Utils:
    """Tests for S3 utilities."""

    def test_s3_client_init(self) -> None:
        """Test S3 client initialization."""
        from handler.utils.s3 import S3Client

        client = S3Client(
            bucket_name="test-bucket",
            kms_key_arn="arn:aws:kms:eu-west-1:123:key/test",
        )

        assert client.bucket_name == "test-bucket"
        assert client.kms_key_arn == "arn:aws:kms:eu-west-1:123:key/test"

    def test_read_json(self, s3_client) -> None:
        """Test reading JSON from S3."""
        import json

        from handler.utils.s3 import S3Client

        # Arrange
        bucket_name = "test-bucket"
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-1"},
        )
        s3_client.put_object(
            Bucket=bucket_name,
            Key="test.json",
            Body=json.dumps({"key": "value"}),
        )

        # Act
        client = S3Client(bucket_name=bucket_name)
        result = client.read_json("test.json")

        # Assert
        assert result == {"key": "value"}

    def test_write_json(self, s3_client) -> None:
        """Test writing JSON to S3."""
        import json

        from handler.utils.s3 import S3Client

        # Arrange
        bucket_name = "test-bucket"
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-1"},
        )

        # Act
        client = S3Client(bucket_name=bucket_name)
        client.write_json("output.json", {"result": "success"})

        # Assert
        response = s3_client.get_object(Bucket=bucket_name, Key="output.json")
        content = json.loads(response["Body"].read().decode("utf-8"))
        assert content == {"result": "success"}
