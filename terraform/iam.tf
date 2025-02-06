# ------------------- ECS Execution Role
resource "aws_iam_role" "ecs_execution" {
  name               = "ecs-execution-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume.json
}

resource "aws_iam_role_policy" "ecs_execution" {
  name   = "ecs-execution-policy"
  role   = aws_iam_role.ecs_execution.id
  policy = data.aws_iam_policy_document.ecs_ecr_access.json
}

# ---------------- ECS Task Role
resource "aws_iam_role" "ecs_task" {
  name               = "ecs-task-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume.json
}

resource "aws_iam_role_policy" "ecs_task" {
  name   = "ecs-task-policy"
  role   = aws_iam_role.ecs_task.id
  policy = data.aws_iam_policy_document.ecs_ddb_access.json
}

# ------------ Lambda Authorizer Role
resource "aws_iam_role" "lambda_exec" {
  name               = "lambda-execution-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
}

resource "aws_iam_policy" "lambda_ddb" {
  name   = "lambda-dynamodb-policy"
  policy = data.aws_iam_policy_document.lambda_ddb_access.json
}

resource "aws_iam_role_policy_attachment" "lambda_ddb" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.lambda_ddb.arn
}

resource "aws_iam_role_policy_attachment" "lambda_basic_exec" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
