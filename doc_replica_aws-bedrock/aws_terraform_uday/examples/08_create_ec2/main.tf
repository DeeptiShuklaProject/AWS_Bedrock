# Lab 8: Bootstrapped EC2 Instance with UserData Shell Scripts
resource "aws_instance" "web_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
  
  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum install -y httpd
              sudo systemctl start httpd
              sudo systemctl enable httpd
              echo "<h1>Welcome to Production Web Server</h1>" > /var/www/html/index.html
              EOF

  tags = {
    Name = "Web-Server-Instance"
  }
}
