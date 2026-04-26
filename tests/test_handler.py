"""Tests for Lambda handler."""

from unittest.mock import patch, MagicMock

import pytest

from handler.utils.ssm import DatalakeConfig


class TestHandler:
    """Tests for main handler function."""

    @patch("handler.main.get_datalake_config")
    def test_handler_success(
        self, mock_get_config: MagicMock, lambda_event: dict, lambda_context
    ) -> None:
        """Test successful handler execution."""
        # Arrange
        mock_get_config.return_value = DatalakeConfig(
            raw_bucket_name="test-raw-bucket",
            raw_bucket_arn="arn:aws:s3:::test-raw-bucket",
            raw_kms_key_arn="arn:aws:kms:eu-west-1:123:key/raw",
            staging_bucket_name="test-staging-bucket",
            staging_bucket_arn="arn:aws:s3:::test-staging-bucket",
            staging_kms_key_arn="arn:aws:kms:eu-west-1:123:key/staging",
            business_bucket_name="test-business-bucket",
            business_bucket_arn="arn:aws:s3:::test-business-bucket",
            business_kms_key_arn="arn:aws:kms:eu-west-1:123:key/business",
        )

        # Act
        from handler.main import handler

        result = handler(lambda_event, lambda_context)

        # Assert
        assert result["statusCode"] == 200
        assert result["body"]["message"] == "Success"
        assert "result" in result["body"]

    @patch("handler.main.get_datalake_config")
    def test_handler_error(
        self, mock_get_config: MagicMock, lambda_event: dict, lambda_context
    ) -> None:
        """Test handler error handling."""
        # Arrange
        mock_get_config.side_effect = Exception("SSM error")

        # Act
        from handler.main import handler

        result = handler(lambda_event, lambda_context)

        # Assert
        assert result["statusCode"] == 500
        assert "error" in result["body"]


class TestSSMUtils:
    """Tests for SSM utilities."""

    def test_get_datalake_config(self, ssm_client) -> None:
        """Test loading datalake config from SSM."""
        from handler.utils.ssm import get_datalake_config

        # Clear cache for test
        get_datalake_config.cache_clear()

        # Act
        config = get_datalake_config("dev")

        # Assert
        assert config.raw_bucket_name == "datalake-raw-test-dev-123456789012"
        assert config.staging_bucket_name == "datalake-staging-test-dev-123456789012"
        assert config.business_bucket_name == "datalake-business-test-dev-123456789012"
        assert "kms" in config.raw_kms_key_arn


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
