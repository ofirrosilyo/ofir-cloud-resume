# Cloud-Native Resume Infrastructure 🚀

[![Build Status](https://github.com/ofirrosilyo/ofir-cloud-resume/actions/workflows/deploy.yml/badge.svg)](https://github.com/ofirrosilyo/ofir-cloud-resume/actions)
![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)
![Linkerd](https://img.shields.io/badge/Linkerd-00A2AA?style=for-the-badge&logo=Linkerd&logoColor=white)
![Cloudflare](https://img.shields.io/badge/Cloudflare-F38020?style=for-the-badge&logo=Cloudflare&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

A production-grade, hardened personal resume ecosystem hosted on a private **K3s (Kubernetes)** cluster. This project demonstrates a **Zero-Trust** architecture utilizing a service mesh, granular network policies, and automated maintenance lifecycles.

## 🏗️ Architecture Overview

```mermaid
graph TD
    subgraph Public_Internet ["Public Internet"]
        User((User))
        DNS[Domain: rosilyo.net]
    end

    subgraph Home_Network_Physical ["Home Network (Physical)"]
        direction TB
        Modem[Modem: Bridge Mode]
        Router[Router: Port Forwarding/Tunnel]
        NAS[NAS: Hardware Host]
        VM[K3s VM: Ubuntu 22.04]
        
        Modem --> Router
        Router --> NAS
        NAS --> VM
    end

    subgraph K3s_Logic ["Kubernetes Logic (Software)"]
        direction TB
        API[Resume API Pod]
        Redis[(Redis StatefulSet)]
        Mesh{Linkerd mTLS}
        
        API --- Mesh --- Redis
    end

    User --> DNS
    DNS --> Modem
    VM --> API

## 🛠️ Key Technical Features
* **Bare-Metal Infrastructure:** Managed a full-stack deployment on a self-hosted **NAS**, utilizing an **Ubuntu VM** as a **K3s** node.
* **Network Engineering:** Bypassed residential NAT using **Modem Bridge Mode** and **Cloudflare Tunnels** for secure, port-less public access.
* **Zero-Trust Security:** Enforced **mTLS** (Mutual TLS) for all internal traffic via **Linkerd Service Mesh** and Layer 4 **NetworkPolicies**.
* **Automated Persistence:** Implemented **Kubernetes CronJobs** for daily Redis backups with automated sidecar lifecycle management.
* **Full-Stack Observability:** Built real-time monitoring using the **Loki-stack**, with custom **Grafana** dashboards for log aggregation and metric visualization.
