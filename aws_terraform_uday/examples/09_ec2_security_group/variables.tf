variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "allowed_http_cidr" {
  type    = list(string)
  default = ["0.0.0.0/0"]
}
