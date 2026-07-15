output "vpc_id" {
  value       = aws_vpc.main.id
  description = "The ID of the primary VPC"
}

output "database_connection_string" {
  value       = "postgresql://dbadmin:supersecurepassword@mydb.us-east-1.rds.amazonaws.com:5432/db"
  description = "Raw database connection endpoint"
  sensitive   = true
}
