resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  enable_dns_support   = true
  enable_dns_hostnames = true
}

resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
}

resource "aws_apigatewayv2_vpc_link" "http_api" {
  name               = "http-api-vpc-link"
  security_group_ids = [aws_vpc.main.default_security_group_id]
  subnet_ids         = [aws_subnet.private.id]
}

resource "aws_security_group" "fargate" {
  name        = "voice-hue-fargate-sg"
  description = "Allow traffic from NLB to Fargate"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port        = 80
    to_port          = 80
    protocol         = "tcp"
    cidr_blocks      = [aws_subnet.private.cidr_block]

  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_vpc_endpoint" "ecr" {
  vpc_id              = aws_vpc.main.id
  vpc_endpoint_type   = "Interface"
  service_name        = "com.amazonaws.${data.aws_region.current.name}.ecr.dkr"
  subnet_ids          = [aws_subnet.private.id]
  security_group_ids  = [aws_vpc.main.default_security_group_id]
  private_dns_enabled = true
}
