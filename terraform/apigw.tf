resource "aws_apigatewayv2_api" "http" {
  name          = "voice-hue-http-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "http" {
  name   = "$default"
  api_id = aws_apigatewayv2_api.http.id
}

resource "aws_apigatewayv2_deployment" "http" {
  api_id = aws_apigatewayv2_api.http.id

  triggers = {
    redeployment = sha1(join(",", tolist([
      jsonencode(aws_apigatewayv2_integration.http),
      jsonencode(aws_apigatewayv2_route.http),
    ])))
  }

  lifecycle {
    create_before_destroy = true
  }

  depends_on = [
    aws_apigatewayv2_route.http,
    aws_apigatewayv2_integration.http,
  ]
}

resource "aws_apigatewayv2_route" "http" {
  api_id             = aws_apigatewayv2_api.http.id
  route_key          = "ANY /{proxy+}"
  target             = "integrations/${aws_apigatewayv2_integration.http.id}"
  authorization_type = "CUSTOM"
  authorizer_id      = aws_apigatewayv2_authorizer.this.id
}

resource "aws_apigatewayv2_integration" "http" {
  api_id           = aws_apigatewayv2_api.http.id
  integration_type = "HTTP_PROXY"
  integration_uri  = aws_lb_listener.this.arn

  integration_method = "ANY"
  connection_type    = "VPC_LINK"
  connection_id      = aws_apigatewayv2_vpc_link.http_api.id
}

resource "aws_apigatewayv2_authorizer" "this" {
  name             = "api-authorizer"
  api_id           = aws_apigatewayv2_api.http.id
  authorizer_type  = "REQUEST"
  authorizer_uri   = aws_lambda_function.authorizer.invoke_arn
  identity_sources = ["$request.header.Authorization"]

  authorizer_payload_format_version = "2.0"
}
