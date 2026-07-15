# Lab 7: Local Variables and Tag Formatting Rules
locals {
  name_prefix = "${var.project_name}-${var.environment}"
  
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_s3_bucket" "local_test" {
  bucket = "${local.name_prefix}-storage-bucket"
  tags   = local.common_tags
}
