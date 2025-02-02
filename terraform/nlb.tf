resource "aws_lb" "this" {
  name               = "voice-hue-lb"
  internal           = true
  load_balancer_type = "network"
  subnets            = [aws_subnet.private.id]
  security_groups    = [aws_security_group.fargate.id]
}

resource "aws_lb_listener" "this" {
  load_balancer_arn = aws_lb.this.arn
  port              = 80
  protocol          = "TCP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.this.arn
  }
}

resource "aws_lb_target_group" "this" {
  name        = "voice-hue-target-group"
  port        = 80
  protocol    = "TCP"
  target_type = "ip"
  vpc_id      = aws_vpc.main.id

  health_check {
    port     = 80
    protocol = "TCP"
  }
}
