# =============================================================================
# SSM Parameter Exports - Lambda Configuration
# =============================================================================
# Export Lambda function details to SSM for use by other services
# Standard path: /{env}/{project_name}/lambda/{function_name}/{parameter}

resource "aws_ssm_parameter" "function_arn" {
  name        = "/${var.environment}/${local.project_name}/lambda/${local.function_name}/function_arn"
  description = "ARN of the ${local.full_name} Lambda function"
  type        = "String"
  value       = aws_lambda_function.main.arn

  tags = local.common_tags
}

resource "aws_ssm_parameter" "function_name" {
  name        = "/${var.environment}/${local.project_name}/lambda/${local.function_name}/function_name"
  description = "Name of the ${local.full_name} Lambda function"
  type        = "String"
  value       = aws_lambda_function.main.function_name

  tags = local.common_tags
}

resource "aws_ssm_parameter" "invoke_arn" {
  name        = "/${var.environment}/${local.project_name}/lambda/${local.function_name}/invoke_arn"
  description = "Invoke ARN of the ${local.full_name} Lambda function"
  type        = "String"
  value       = aws_lambda_function.main.invoke_arn

  tags = local.common_tags
}

resource "aws_ssm_parameter" "role_arn" {
  name        = "/${var.environment}/${local.project_name}/lambda/${local.function_name}/role_arn"
  description = "Execution role ARN for ${local.full_name}"
  type        = "String"
  value       = aws_iam_role.lambda.arn

  tags = local.common_tags
}
