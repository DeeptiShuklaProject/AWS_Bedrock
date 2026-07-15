# Lab 14: Resource deployed via Terraform Cloud VCS
resource "aws_s3_bucket" "cloud_bucket" {
  bucket = "tf-cloud-managed-bucket-998877"
}
