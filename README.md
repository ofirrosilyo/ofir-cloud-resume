# High-Availability Cloud Resume 🚀

A full-stack resume application deployed on a **K3s Kubernetes cluster**, featuring automated CI/CD and real-time observability.

![Build Status](https://github.com/ofirrosilyo/ofir-cloud-resume/actions/workflows/deploy.yml/badge.svg)

## 🏗️ Architecture
- **Frontend:** HTML5/CSS3 hosted on Nginx.
- **Backend:** Python Flask API handling visitor metrics.
- **Database:** Redis for high-speed data persistence.
- **Orchestration:** K3s (Lightweight Kubernetes) on a private VM.
- **Ingress:** Synology Reverse Proxy with Let's Encrypt SSL.

## 🛠️ DevOps Stack
- **CI/CD:** GitHub Actions with a self-hosted runner for automated deployments.
- **Monitoring:** Prometheus & Grafana for cluster health and resource tracking.
- **Infrastructure:** Hosted on local hardware, exposed via Cloudflare.

## 📈 Monitoring
Live metrics are tracked via Grafana, monitoring CPU/Memory usage of the Pods and API request latency.
