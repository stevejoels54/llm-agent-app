resource "helm_release" "app" {
  count            = var.deploy_app ? 1 : 0
  name = "app"
  chart      = "../helm/app/"
  namespace        = "apps"
  # Namespace is created by kubernetes_namespace.apps, so don't create it here
  create_namespace = false
  replace = true
  timeout = 900
  
  # Configure Inngest environment variables
  set {
    name  = "env.inngestEnv"
    value = var.inngest_env
  }
  
  set {
    name  = "env.inngestAppId"
    value = var.inngest_app_id
  }
  
  # Wait for secrets and namespace to be created before deploying app
  depends_on = [
    local_file.cluster-config,
    kubernetes_secret.inngest,
    kubernetes_secret.redis,
    kubernetes_namespace.apps
  ]
}

resource "time_sleep" "wait_for_app" {
  depends_on = [helm_release.app]
  create_duration = "30s"
}

data "kubernetes_service" "app" {
  metadata {
    name      = "app"
    namespace = "apps"
  }

  depends_on = [time_sleep.wait_for_app]
}