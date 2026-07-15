# Lab 10: IAM User with Access Policies and Login Profiles
resource "aws_iam_user" "readonly_user" {
  name = "dev-read-only-engineer"
  path = "/system/"
}

resource "aws_iam_user_policy_attachment" "readonly_attach" {
  user       = aws_iam_user.readonly_user.name
  policy_arn = "arn:aws:iam::aws:policy/ReadOnlyAccess"
}
