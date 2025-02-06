resource "aws_ecs_cluster" "this" {
  name = "voice-hue"
}

resource "aws_ecs_task_definition" "this" {
  family = "voice-hue"

  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_execution.arn

  container_definitions = jsonencode([
    {
      name  = "voice-hue-api"
      image = "${data.aws_caller_identity.current.account_id}.dkr.ecr.us-west-1.amazonaws.com/projects/voice-hue:latest"
      portMappings = [{
        containerPort = 80
        hostPort      = 80
        protocol      = "tcp"
      }]
    }
  ])
}

resource "aws_ecs_service" "this" {
  name            = "voice-hue"
  cluster         = aws_ecs_cluster.this.id
  task_definition = aws_ecs_task_definition.this.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = [aws_subnet.private.id]
    assign_public_ip = false
    security_groups  = [aws_security_group.fargate.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.this.arn
    container_name   = "voice-hue-api"
    container_port   = 80
  }
}