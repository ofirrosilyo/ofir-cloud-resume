# Cloud-Native Resume Infrastructure 🚀

A production-grade, highly available personal resume website hosted on a private **K3s (Kubernetes)** cluster, secured by **Cloudflare Zero Trust**, and managed via **GitOps** principles.

## 🏗️ Architecture Overivew
The infrastructure is designed for security and scalability, bypassing the need for open inbound ports or public IP exposure.



* **Orchestration:** K3s (Lightweight Kubernetes)
* **Networking:** Cloudflare Tunnel (Tunneling traffic from `rosilyo.net` to the cluster)
* **Database:** Redis (State management for visitor tracking)
* **Observability:** Loki-stack (Log aggregation)
* **Security:** Cloudflare Access (Identity-based authentication for administrative routes)

## 📂 Repository Structure
Following industry-standard Kubernetes directory layouts:
- `k8s/base/`: The "Source of Truth" for all cluster manifests.
  - `deployment.yaml`: Pod definitions for Frontend and API.
  - `services.yaml`: LoadBalancer and ClusterIP definitions.
  - `kustomization.yaml`: Orchestrates the application of all manifests.
  - `tunnel-connector.yaml`: Cloudflare sidecar configuration.

## 🔄 GitOps Workflow
This project utilizes a bidirectional sync between the master node and this repository:
- **Push (k-save):** A custom alias that exports live cluster states to YAML and pushes to GitHub.
- **Pull (Cron):** An automated background task (`git-sync.sh`) that pulls changes from GitHub to the node every 5 minutes.

## 🚀 Deployment
To replicate this infrastructure on a clean K3s node:
```bash
git clone https://github.com/ofirrosilyo/ofir-cloud-resume.git
kubectl apply -k k8s/base/
```
