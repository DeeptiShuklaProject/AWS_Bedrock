# Lab 2: Deploying t2.micro EC2 Instance
resource "aws_instance" "vscode_demo" {
  ami           = "ami-0c55b159cbfafe1f0" # Amazon Linux 2 AMI
  instance_type = "t2.micro"
  key_name      = "production-key"

  root_block_device {
    volume_size           = 20
    volume_type           = "gp3"
    encrypted             = true
    delete_on_termination = true
  }

  tags = {
    Name        = "VSCode-EC2-Demo"
    Environment = "Dev"
    Project     = "Terraform Onboarding"
  }
}
