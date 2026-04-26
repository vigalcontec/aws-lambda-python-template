# =============================================================================
# SSM Parameter Exports - Lambda Configuration
# =============================================================================
# Export Lambda function details to SSM for use by other services

resource "aws_ssm_parameter" "function_arn" {
  name        = "/${var.environment}/lambda/${local.function_name}/function_arn"
  description = "ARN of the ${local.function_name} Lambda function"
  type        = "SecureString"
  value       = aws_lambda_function.main.arn

  tags = merge(local.common_tags, {
    Name = "${local.full_name}-function-arn"
  })
}

resource "aws_ssm_parameter" "function_name" {
  name        = "/${var.environment}/lambda/${local.function_name}/function_name"
  description = "Name of the ${local.function_name} Lambda function"
  type        = "SecureString"
  value       = aws_lambda_function.main.function_name

  tags = merge(local.common_tags, {
    Name = "${local.full_name}-function-name"
  })
}

resource "aws_ssm_parameter" "invoke_arn" {
  name        = "/${var.environment}/lambda/${local.function_name}/invoke_arn"
  description = "Invoke ARN of the ${local.function_name} Lambda function"
  type        = "SecureString"
  value       = aws_lambda_function.main.invoke_arn

  tags = merge(local.common_tags, {
    Name = "${local.full_name}-invoke-arn"
  })
}

resource "aws_ssm_parameter" "ecr_repository_url" {
  name        = "/${var.environment}/lambda/${local.function_name}/ecr_repository_url"
  description = "ECR repository URL for ${local.function_name}"
  type        = "SecureString"
  value       = aws_ecr_repository.lambda.repository_url

  tags = merge(local.common_tags, {
    Name = "${local.full_name}-ecr-url"
  })
}

resource "aws_ssm_parameter" "role_arn" {
  name        = "/${var.environment}/lambda/${local.function_name}/role_arn"
  description = "Execution role ARN for ${local.function_name}"
  type        = "SecureString"
  value       = aws_iam_role.lambda.arn

  tags = merge(local.common_tags, {
    Name = "${local.full_name}-role-arn"
  })
}
