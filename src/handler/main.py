"""AWS Lambda Handler - Main Entry Point."""

from typing import Any

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext

from handler.config import Settings
from handler.utils.ssm import get_datalake_config

# Initialize Powertools
logger = Logger()
tracer = Tracer()

# Load settings
settings = Settings()


@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def handler(event: dict[str, Any], _context: LambdaContext) -> dict[str, Any]:
    """
    Lambda handler function.

    Args:
        event: Lambda event payload
        context: Lambda context object

    Returns:
        Response dictionary with statusCode and body
    """
    logger.info("Processing event", extra={"environment": settings.environment})

    try:
        # Get datalake configuration from environment variables
        datalake_config = get_datalake_config()

        logger.info(
            "Datalake configuration loaded",
            extra={
                "raw_bucket": datalake_config.raw_bucket_name,
                "staging_bucket": datalake_config.staging_bucket_name,
                "business_bucket": datalake_config.business_bucket_name,
            },
        )

        # TODO: Implement your business logic here
        result = process_event(event, datalake_config)

        return {
            "statusCode": 200,
            "body": {
                "message": "Success",
                "result": result,
            },
        }

    except Exception as e:
        logger.exception("Error processing event")
        return {
            "statusCode": 500,
            "body": {
                "message": "Internal server error",
                "error": str(e),
            },
        }


@tracer.capture_method
def process_event(event: dict[str, Any], _datalake_config: Any) -> dict[str, Any]:
    """
    Process the Lambda event.

    Args:
        event: Lambda event payload
        datalake_config: Datalake configuration from SSM

    Returns:
        Processing result
    """
    # TODO: Implement your business logic here
    return {
        "processed": True,
        "event_keys": list(event.keys()),
    }
