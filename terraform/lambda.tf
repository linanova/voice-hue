resource "aws_lambda_function" "authorizer" {
  function_name    = "api-key-authorizer"
  runtime          = "python3.13"
  handler          = "index.handler"
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  role             = aws_iam_role.lambda_exec.arn

  environment {
    variables = {
      API_KEYS_TABLE = "voice-hue-api-keys"
    }
  }
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "../authorizer"
  output_path = "../authorizer/authorizer.zip"
}

resource "aws_lambda_permission" "apigw_invoke" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.authorizer.function_name
  principal     = "apigateway.amazonaws.com"
  statement_id  = "AllowAuthorizerLambdaExecutionFromAPIGateway"
}

resource "aws_cloudwatch_log_group" "authorizer" {
  name = "/aws/lambda/${aws_lambda_function.authorizer.function_name}"
}
