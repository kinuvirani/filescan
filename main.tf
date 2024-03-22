resource "kubernetes_deployment" "flask_app" {
  metadata {
    name = "flask-app"
  }

  spec {
    replicas = 3

    selector {
      match_labels = {
        app = "flask-app"
      }
    }

    template {
      metadata {
        labels = {
          app = "flask-app"
        }
      }

      spec {
        container {
          name  = "flask-app"
          image = "registry.gitlab.com/ompatel4799/my_project:$CI_COMMIT_SHORT_SHA"
          ports {
            container_port = 5000
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "flask_app_service" {
  metadata {
    name = "flask-app-service"
  }

  spec {
    selector = {
      app = "flask-app"
    }

    port {
      port        = 80
      target_port = 5000
    }
  }
}
# Cleanup resources

resource "null_resource" "cleanup" {
  triggers = {
    always_run = "${timestamp()}"
  }

  provisioner "local-exec" {
    command = "terraform destroy -auto-approve"
  }
}
