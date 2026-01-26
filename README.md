# Cloud-Native Resume Infrastructure 🚀

[![Build Status](https://github.com/ofirrosilyo/ofir-cloud-resume/actions/workflows/k8s-validate.yaml/badge.svg)](https://github.com/ofirrosilyo/ofir-cloud-resume/actions)
![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)
![Linkerd](https://img.shields.io/badge/Linkerd-00A2AA?style=for-the-badge&logo=Linkerd&logoColor=white)
![Cloudflare](https://img.shields.io/badge/Cloudflare-F38020?style=for-the-badge&logo=Cloudflare&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

A production-grade, hardened personal resume ecosystem hosted on a private **K3s (Kubernetes)** cluster. This project demonstrates a **Zero-Trust** architecture utilizing a service mesh, granular network policies, and automated maintenance lifecycles.

## 🛡️ Security & Hardening (Newly Implemented)
This infrastructure follows a "Defense in Depth" strategy:
* **Service Mesh (Linkerd):** Enforces **mutual TLS (mTLS)** for all pod-to-pod communication, ensuring data-in-transit encryption within the cluster.
* **Layer 4 Firewalling:** Custom **Kubernetes Network Policies** implement a least-privilege model, restricting Redis access exclusively to the API and backup services.
* **Zero Exposure:** Cloudflare Tunnels eliminate open inbound ports; traffic is only accessible via authenticated tunnels.

## 🏗️ Architecture Overview

* **Orchestration:** K3s (Lightweight Kubernetes)
* **Mesh & Identity:** Linkerd Service Mesh
* **Database:** Redis (StatefulSet with Persistent Volume Claims)
* **Automated Backups:** Kubernetes CronJobs with mesh-aware lifecycle management (`shutdown-proxy-on-exit`).
* **Observability:** Loki-stack & Grafana (Designing LogQL alerts for backup success/failure).

## 📂 Repository Structure
- `k8s/base/`: Core manifests.
  - `components/api/`: Backend service logic and Linkerd injection.
  - `components/redis/`: StatefulSet, Service, and Network Policies.
  - `components/backups/`: CronJob definitions for database persistence.
  - `tunnel-connector.yaml`: Cloudflare Zero Trust configuration.

## 🚀 Deployment
```bash
kubectl apply -k k8s/base/
