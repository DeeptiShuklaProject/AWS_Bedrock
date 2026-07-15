variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "The target AWS Region for deployment"
}

variable "environment" {
  type        = string
  description = "Application deployment environment (dev, staging, prod)"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "The environment variable must be dev, staging, or prod."
  }
}

variable "web_instance_type" {
  type        = string
  default     = "t3.micro"
  description = "EC2 instance family type"
}
