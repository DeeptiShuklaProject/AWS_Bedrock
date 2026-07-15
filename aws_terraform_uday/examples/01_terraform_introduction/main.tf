# Lab 1: S3 Bucket setup with encryption & public access blocks
resource "aws_s3_bucket" "prod_bucket" {
  bucket        = "production-data-lake-lakehouse-98765"
  force_destroy = false

  tags = {
    Name        = "Production Data Lake"
    Environment = "Prod"
    ManagedBy   = "Terraform"
    Project     = "Data Platform"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "prod_bucket_sse" {
  bucket = aws_s3_bucket.prod_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "prod_bucket_block" {
  bucket = aws_s3_bucket.prod_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
