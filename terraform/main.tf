terraform {
  backend "s3" {
    bucket         = "voice-hue-terraform-state"
    key            = "terraform.tfstate"
    region         = "us-west-1"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.84.0"
    }
  }
}

provider "aws" {
  region = "us-west-1"
}

provider "aws" {
  region = "us-east-1"
  alias  = "east"
}
