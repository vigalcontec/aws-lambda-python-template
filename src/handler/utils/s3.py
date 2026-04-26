"""S3 utilities for reading and writing data."""

from typing import Any

import boto3
from aws_lambda_powertools import Logger

logger = Logger()


class S3Client:
    """S3 client wrapper with KMS encryption support."""

    def __init__(self, bucket_name: str, kms_key_arn: str | None = None) -> None:
        """
        Initialize S3 client.

        Args:
            bucket_name: S3 bucket name
            kms_key_arn: Optional KMS key ARN for encryption
        """
        self.bucket_name = bucket_name
        self.kms_key_arn = kms_key_arn
        self._client = boto3.client("s3")

    def read_json(self, key: str) -> dict[str, Any]:
        """
        Read JSON file from S3.

        Args:
            key: S3 object key

        Returns:
            Parsed JSON content
        """
        import json

        logger.info(f"Reading JSON from s3://{self.bucket_name}/{key}")

        response = self._client.get_object(Bucket=self.bucket_name, Key=key)
        content = response["Body"].read().decode("utf-8")

        return json.loads(content)

    def write_json(self, key: str, data: dict[str, Any]) -> None:
        """
        Write JSON file to S3 with KMS encryption.

        Args:
            key: S3 object key
            data: Data to write as JSON
        """
        import json

        logger.info(f"Writing JSON to s3://{self.bucket_name}/{key}")

        body = json.dumps(data, indent=2, default=str)

        put_args: dict[str, Any] = {
            "Bucket": self.bucket_name,
            "Key": key,
            "Body": body.encode("utf-8"),
            "ContentType": "application/json",
        }

        if self.kms_key_arn:
            put_args["ServerSideEncryption"] = "aws:kms"
            put_args["SSEKMSKeyId"] = self.kms_key_arn

        self._client.put_object(**put_args)

    def read_parquet(self, key: str) -> Any:
        """
        Read Parquet file from S3.

        Args:
            key: S3 object key

        Returns:
            Pandas DataFrame (requires pandas and pyarrow)
        """
        try:
            import pandas as pd
        except ImportError as err:
            raise ImportError("pandas and pyarrow required for Parquet support") from err

        logger.info(f"Reading Parquet from s3://{self.bucket_name}/{key}")

        s3_path = f"s3://{self.bucket_name}/{key}"
        return pd.read_parquet(s3_path)

    def write_parquet(self, key: str, df: Any) -> None:
        """
        Write Parquet file to S3.

        Args:
            key: S3 object key
            df: Pandas DataFrame to write
        """
        import importlib.util
        import io

        if importlib.util.find_spec("pandas") is None:
            raise ImportError("pandas and pyarrow required for Parquet support")

        logger.info(f"Writing Parquet to s3://{self.bucket_name}/{key}")

        buffer = io.BytesIO()
        df.to_parquet(buffer, index=False)
        buffer.seek(0)

        put_args: dict[str, Any] = {
            "Bucket": self.bucket_name,
            "Key": key,
            "Body": buffer.getvalue(),
            "ContentType": "application/octet-stream",
        }

        if self.kms_key_arn:
            put_args["ServerSideEncryption"] = "aws:kms"
            put_args["SSEKMSKeyId"] = self.kms_key_arn

        self._client.put_object(**put_args)

    def list_objects(self, prefix: str) -> list[str]:
        """
        List objects in S3 bucket with prefix.

        Args:
            prefix: S3 key prefix

        Returns:
            List of object keys
        """
        logger.info(f"Listing objects in s3://{self.bucket_name}/{prefix}")

        paginator = self._client.get_paginator("list_objects_v2")
        keys: list[str] = []

        for page in paginator.paginate(Bucket=self.bucket_name, Prefix=prefix):
            for obj in page.get("Contents", []):
                keys.append(obj["Key"])

        return keys
