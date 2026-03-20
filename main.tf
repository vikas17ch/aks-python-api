# 1. Resource Group
resource "azurerm_resource_group" "rg" {
  name     = "aks-python-pg-rg"
  location = "Sweden Central"
}

# 2. Random suffix for unique naming (Required for ACR and DB)
resource "random_string" "suffix" {
  length  = 4
  special = false
  upper   = false
}

# 3. Azure Container Registry (ACR) - Where your Docker images live
resource "azurerm_container_registry" "acr" {
  name                = "vikasreg${random_string.suffix.result}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
  admin_enabled       = true
}

# 4. Azure Kubernetes Service (AKS) - Your compute power
resource "azurerm_kubernetes_cluster" "aks" {
  name                = "python-api-cluster"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "vikasapi"

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_B2s_v2" # Available in Sweden Central
  }

  identity {
    type = "SystemAssigned"
  }
}

# 5. PostgreSQL Flexible Server - Your data storage
resource "azurerm_postgresql_flexible_server" "db" {
  name                   = "vikas-pg-server-${random_string.suffix.result}"
  resource_group_name    = azurerm_resource_group.rg.name
  location               = azurerm_resource_group.rg.location
  version                = "14"
  administrator_login    = "psqladmin"
  administrator_password = "Password1234!" # In production, use Azure Key Vault
  storage_mb             = 32768
  sku_name               = "B_Standard_B1ms" # Burstable tier
}

# 6. Firewall rule to allow AKS to reach the Database
resource "azurerm_postgresql_flexible_server_firewall_rule" "allow_azure" {
  name             = "AllowAllAzureServices"
  server_id        = azurerm_postgresql_flexible_server.db.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}