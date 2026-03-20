terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {
    resource_group {
      # SRE Tip: Allows Terraform to wipe the RG even if it contains "ghost" resources
      prevent_deletion_if_contains_resources = false
    }
  }
}