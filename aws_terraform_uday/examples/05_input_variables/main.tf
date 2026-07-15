# Lab 5: Parameterized EC2 instance using Variables
resource "aws_instance" "templated" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = var.web_instance_type

  tags = {
    Name        = "instance-${var.environment}"
    Environment = var.environment
  }
}
