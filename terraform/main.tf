variable "aws_region" {
  default     = "eu-west-2"
  description = "AWS region to deploy resources"
}

data "aws_caller_identity" "current" {}

provider "aws" {
  region = var.aws_region
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda_execution_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "lambda_basic_execution" {
  name       = "lambda_basic_execution_attachment"
  roles      = [aws_iam_role.lambda_role.name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "search_broker_lambda" {
  function_name    = "searchBrokerFunction"
  filename         = "deployment.zip"
  source_code_hash = filebase64sha256("deployment.zip")
  role             = aws_iam_role.lambda_role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.9"
  timeout          = 30
  memory_size      = 256

  environment {
    variables = {
      TARGET_QUEUE = "your-queue-name"
    }
  }
}

output "lambda_function_arn" {
  value = aws_lambda_function.search_broker_lambda.arn
}

resource "aws_iam_policy" "lambda_secrets_manager_access" {
  name        = "LambdaSecretsManagerAccess"
  description = "Allow Lambda to access secrets in AWS Secrets Manager"
  
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "secretsmanager:GetSecretValue",
      "Resource": "arn:aws:secretsmanager:eu-west-2:${data.aws_caller_identity.current.account_id}:secret:guardian_key-*"
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "lambda_secrets_manager" {
  name       = "lambda_secrets_manager_attachment"
  roles      = [aws_iam_role.lambda_role.name]
  policy_arn = aws_iam_policy.lambda_secrets_manager_access.arn
}

resource "aws_iam_policy" "lambda_sqs_access" {
  name        = "LambdaSQSAccess"
  description = "Allow Lambda to create and send messages to any SQS queue"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "sqs:CreateQueue",
        "sqs:GetQueueUrl",
        "sqs:SendMessage",
        "sqs:ReceiveMessage",
        "sqs:DeleteMessage",
        "sqs:GetQueueAttributes"
      ],
      "Resource": "arn:aws:sqs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:*"
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "lambda_sqs_attachment" {
  name       = "lambda_sqs_attachment"
  roles      = [aws_iam_role.lambda_role.name]
  policy_arn = aws_iam_policy.lambda_sqs_access.arn
}
