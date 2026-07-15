# Lab 11: PostgreSQL Relational Database Provisioning
resource "aws_db_instance" "prod_postgres" {
  allocated_storage      = 20
  max_allocated_storage  = 100
  engine                 = "postgres"
  engine_version         = "14"
  instance_class         = "db.t3.micro"
  db_name                = "production_db"
  username               = "dbadmin"
  password               = var.db_password
  parameter_group_name   = "default.postgres14"
  skip_final_snapshot    = true
  publicly_accessible    = false

  tags = {
    Environment = "Prod"
  }
}
