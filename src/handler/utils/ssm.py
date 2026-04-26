"""Datalake configuration from environment variables."""

import os
from dataclasses import dataclass
from functools import lru_cache

from aws_lambda_powertools import Logger

logger = Logger()


@dataclass
class DatalakeConfig:
    """Datalake configuration from environment variables."""

    # Raw layer
    raw_bucket_name: str
    raw_bucket_arn: str
    raw_kms_key_arn: str

    # Staging layer
    staging_bucket_name: str
    staging_bucket_arn: str
    staging_kms_key_arn: str

    # Business layer
    business_bucket_name: str
    business_bucket_arn: str
    business_kms_key_arn: str


@lru_cache(maxsize=1)
def get_datalake_config() -> DatalakeConfig:
    """
    Get datalake configuration from environment variables.

    Environment variables are set by Terraform from SSM parameters.

    Returns:
        DatalakeConfig with all bucket names and KMS key ARNs
    """
    logger.info("Loading datalake config from environment variables")

    return DatalakeConfig(
        raw_bucket_name=os.environ.get("RAW_BUCKET_NAME", ""),
        raw_bucket_arn=os.environ.get("RAW_BUCKET_ARN", ""),
        raw_kms_key_arn=os.environ.get("RAW_KMS_KEY_ARN", ""),
        staging_bucket_name=os.environ.get("STAGING_BUCKET_NAME", ""),
        staging_bucket_arn=os.environ.get("STAGING_BUCKET_ARN", ""),
        staging_kms_key_arn=os.environ.get("STAGING_KMS_KEY_ARN", ""),
        business_bucket_name=os.environ.get("BUSINESS_BUCKET_NAME", ""),
        business_bucket_arn=os.environ.get("BUSINESS_BUCKET_ARN", ""),
        business_kms_key_arn=os.environ.get("BUSINESS_KMS_KEY_ARN", ""),
    )
