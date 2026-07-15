# Lab 12: MariaDB Relational Database Setup
resource "aws_db_instance" "prod_mariadb" {
  allocated_storage      = 20
  engine                 = "mariadb"
  engine_version         = "10.6"
  instance_class         = "db.t3.micro"
  db_name                = "mariadb_db"
  username               = "dbadmin"
  password               = var.db_password
  skip_final_snapshot    = true
  publicly_accessible    = false
}
