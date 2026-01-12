
resource "aws_db_subnet_group" "postgres" {
  name = "lab8-postgres-subnet-group"

  subnet_ids = [
    var.private_subnet_id,
    var.private_subnet_b_id
  ]

  tags = {
    Name = "lab8-postgres-subnet-group"
    Env  = "QA"
  }
}

resource "aws_db_instance" "postgres" {
  identifier = "lab8-postgres-db"

  engine         = "postgres"

  instance_class    = "db.t3.micro"
  allocated_storage = 20

  db_name  = "main_db"
  username = "postgres"
  password = var.db_password

  db_subnet_group_name   = aws_db_subnet_group.postgres.name
  vpc_security_group_ids = [var.security_group_id]

  publicly_accessible = false
  skip_final_snapshot = true

  tags = {
    Name = "lab8-postgres"
    Env  = "QA"
  }
}


