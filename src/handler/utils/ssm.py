"""SSM Parameter Store utilities for datalake configuration."""

from dataclasses import dataclass
from functools import lru_cache

import boto3
from aws_lambda_powertools import Logger

logger = Logger()


@dataclass
class DatalakeConfig:
    """Datalake configuration from SSM Parameter Store."""

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


def _get_parameter(ssm_client: any, name: str) -> str:
    """
    Get a single SSM parameter value.

    Args:
        ssm_client: Boto3 SSM client
        name: Parameter name

    Returns:
        Parameter value (decrypted if SecureString)
    """
    response = ssm_client.get_parameter(Name=name, WithDecryption=True)
    return response["Parameter"]["Value"]


@lru_cache(maxsize=3)
def get_datalake_config(environment: str) -> DatalakeConfig:
    """
    Get datalake configuration from SSM Parameter Store.

    Args:
        environment: Environment name (dev, qa, prod)

    Returns:
        DatalakeConfig with all bucket names and KMS key ARNs
    """
    ssm = boto3.client("ssm")

    logger.info(f"Loading datalake config for environment: {environment}")

    # Define parameter paths
    layers = ["raw", "staging", "business"]
    params = ["bucket_name", "bucket_arn", "kms_key_arn"]

    # Build parameter names
    param_names = [
        f"/{environment}/datalake/{layer}/{param}" for layer in layers for param in params
    ]

    # Fetch all parameters in batch
    response = ssm.get_parameters(Names=param_names, WithDecryption=True)

    # Build lookup dict
    values = {p["Name"]: p["Value"] for p in response["Parameters"]}

    # Check for missing parameters
    missing = set(param_names) - set(values.keys())
    if missing:
        logger.warning(f"Missing SSM parameters: {missing}")

    def get_value(layer: str, param: str) -> str:
        key = f"/{environment}/datalake/{layer}/{param}"
        return values.get(key, "")

    return DatalakeConfig(
        raw_bucket_name=get_value("raw", "bucket_name"),
        raw_bucket_arn=get_value("raw", "bucket_arn"),
        raw_kms_key_arn=get_value("raw", "kms_key_arn"),
        staging_bucket_name=get_value("staging", "bucket_name"),
        staging_bucket_arn=get_value("staging", "bucket_arn"),
        staging_kms_key_arn=get_value("staging", "kms_key_arn"),
        business_bucket_name=get_value("business", "bucket_name"),
        business_bucket_arn=get_value("business", "bucket_arn"),
        business_kms_key_arn=get_value("business", "kms_key_arn"),
    )
