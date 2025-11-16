# # # # # # # # # # # # # 
# Cluster Configuration # 
# # # # # # # # # # # # # 

# The name of the cluster
variable "cluster_name" {
  type        = string
  default     = "llm_boilerplate"
  description = "The name of the cluster to create"
}

# the node instance to use for the cluster
variable "cluster_node_size" {
  type = string
  # default = "g4g.40.kube.small"  # GPU node
  # default = "g4s.kube.small"     # GPU node
  default     = "g4s.kube.large"  # CPU node (4 cores, 8GB RAM, 60GB storage)
  description = "The size of the node instance for the cluster"
}

# the number of nodes to provision in the cluster
variable "cluster_node_count" {
  type        = number
  default     = "2"
  description = "The number of nodes to provision in the cluster"

}

# # # # # # # # # # # 
# Civo configuration # 
# # # # # # # # # # # 

# The Civo API token, this is set in terraform.tfvars
variable "civo_token" {}

# The Civo Region to deploy the cluster in
variable "region" {
  type        = string
  default     = "LON1" #LON1
  description = "The region to provision the cluster against"
}


# # # # # # # # # # # # # # # # # # 
# LLM Boilerplate deployment flags # 
# # # # # # # # # # # # # # # # # # 

# Deploy the Ollama Helm chart
variable "deploy_ollama" {
  description = "Deploy the Ollama inference server."
  type        = bool
  default     = true
}

# Deploy the Ollama UI
variable "deploy_ollama_ui" {
  description = "Deploy the Ollama Web UI."
  type        = bool
  default     = true
}

# deploy the example application 
variable "deploy_app" {
  description = "Deploy the example application."
  type        = bool
  default     = true
}

# deploy the Nvidia Device plugin to enable GPU Support
variable "deploy_nv_device_plugin_ds" {
  description = "Deploy the Nvidia GPU Device Plugin for enabling GPU support. Set to false for CPU-only deployments."
  type        = bool
  default     = false  # Disabled by default for CPU-only nodes
}

variable "default_models" {
  description = "List of default models to use in Ollama Web UI."
  type        = list(string)
  # Using llama3.2 - same model as local development
  default = ["llama3.2"]
}

variable "ollama_ui_image_version" {
  description = "The image tag to use in the Ollama Web UI Helm Chart."
  type        = string
  default     = "latest"
}

# # # # # # # # # # # # # # # # # # 
# Application Secrets Configuration # 
# # # # # # # # # # # # # # # # # # 

# Inngest Configuration
variable "inngest_signing_key" {
  description = "Inngest signing key for authentication"
  type        = string
  sensitive   = true
  default     = ""
}

variable "inngest_event_key" {
  description = "Inngest event key for event publishing"
  type        = string
  sensitive   = true
  default     = ""
}

# Redis Configuration
variable "redis_host" {
  description = "Redis hostname or IP address"
  type        = string
  default     = "redis-18179.c311.eu-central-1-1.ec2.cloud.redislabs.com"
}

variable "redis_port" {
  description = "Redis port number"
  type        = string
  default     = "18179"
}

variable "redis_username" {
  description = "Redis username"
  type        = string
  default     = "default"
  sensitive   = true
}

variable "redis_password" {
  description = "Redis password"
  type        = string
  sensitive   = true
  default     = ""
}

variable "redis_db" {
  description = "Redis database number"
  type        = string
  default     = "0"
}

# Application Environment Configuration
variable "inngest_env" {
  description = "Inngest environment (dev, prod, etc.)"
  type        = string
  default     = "prod"
}

variable "inngest_app_id" {
  description = "Inngest application ID"
  type        = string
  default     = "llm-agent-app"
}
