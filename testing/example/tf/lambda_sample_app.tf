provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

data "aws_iam_policy_document" "sample_app_assume_policy_document" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}
resource "aws_iam_role" "sample_app" {
  name               = "sample_app"
  assume_role_policy = data.aws_iam_policy_document.sample_app_assume_policy_document.json
}

data "aws_iam_policy_document" "sample_app_permissions_policy_document" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = ["*"]
  }
}
resource "aws_iam_policy" "sample_app_permissions_policy" {
  policy = data.aws_iam_policy_document.sample_app_permissions_policy_document.json
}
resource "aws_iam_role_policy_attachment" "sample_app_permissions_policy_attach" {
  role       = aws_iam_role.sample_app.name
  policy_arn = aws_iam_policy.sample_app_permissions_policy.arn
}

resource "aws_lambda_function" "sample_app" {
  function_name = "sample_app"
  filename      = "${path.module}/data/dummy_lambda.zip"
  role          = aws_iam_role.sample_app.arn
  handler       = "sample_app.lambda_handler"
  runtime       = "python3.8"
}

resource "aws_apigatewayv2_api" "sample_app_gateway" {
  name          = "sample_app_gateway"
  protocol_type = "HTTP"
  target        = aws_lambda_function.sample_app.arn
}

resource "aws_lambda_permission" "sample_app_gateway" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.sample_app.arn
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.sample_app_gateway.execution_arn}/*/*"
}
