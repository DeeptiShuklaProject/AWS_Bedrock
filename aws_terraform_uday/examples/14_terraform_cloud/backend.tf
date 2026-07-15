terraform {
  cloud {
    organization = "production-corp"

    workspaces {
      name = "aws-infrastructure-workspace"
    }
  }
}
