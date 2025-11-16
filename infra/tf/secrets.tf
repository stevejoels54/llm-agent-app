# Kubernetes Secrets for App Deployment

# Create namespace for apps if it doesn't exist
resource "kubernetes_namespace" "apps" {
  count = var.deploy_app ? 1 : 0
  
  metadata {
    name = "apps"
  }

  depends_on = [local_file.cluster-config]
}

# Inngest Secrets
resource "kubernetes_secret" "inngest" {
  count = var.deploy_app ? 1 : 0
  
  metadata {
    name      = "inngest-secrets"
    namespace = kubernetes_namespace.apps[0].metadata[0].name
  }

  data = {
    "signing-key" = var.inngest_signing_key
    "event-key"   = var.inngest_event_key
  }

  type = "Opaque"

  depends_on = [kubernetes_namespace.apps]
}

# Redis Secrets
resource "kubernetes_secret" "redis" {
  count = var.deploy_app ? 1 : 0
  
  metadata {
    name      = "redis-secrets"
    namespace = kubernetes_namespace.apps[0].metadata[0].name
  }

  data = {
    "redis-host"     = var.redis_host
    "redis-port"     = var.redis_port
    "redis-username" = var.redis_username
    "redis-password" = var.redis_password
    "redis-db"       = var.redis_db
  }

  type = "Opaque"

  depends_on = [kubernetes_namespace.apps]
}

