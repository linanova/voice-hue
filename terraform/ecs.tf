resource "aws_ecs_cluster" "this" {
  name = "voice-hue"
}

resource "aws_ecs_task_definition" "this" {
  family = "voice-hue"

  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"

  container_definitions = jsonencode([
    {
      name      = "voice-hue-api"
      image     = "ubuntu"
      cpu       = 10
      memory    = 512
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
    subnets          = data.aws_subnets.default.ids
    assign_public_ip = true
  }
}