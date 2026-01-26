# Cloud-Native Resume Infrastructure 🚀

[![Build Status](https://github.com/ofirrosilyo/ofir-cloud-resume/actions/workflows/k8s-validate.yaml/badge.svg)](https://github.com/ofirrosilyo/ofir-cloud-resume/actions)
![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)
![Linkerd](https://img.shields.io/badge/Linkerd-00A2AA?style=for-the-badge&logo=Linkerd&logoColor=white)
![Cloudflare](https://img.shields.io/badge/Cloudflare-F38020?style=for-the-badge&logo=Cloudflare&logoColor=white)

A production-grade, hardened personal resume ecosystem hosted on a private **K3s (Kubernetes)** cluster.

## 🏗️ Architecture Overview

```mermaid
graph TD
    subgraph Public_Internet
        User((User))
    end

    subgraph Cloudflare_Zero_Trust
        Tunnel[Cloudflare Tunnel]
        Access[Cloudflare Access]
    end

    subgraph K3s_Cluster_Private_Network
        direction TB
        subgraph Mesh_mTLS_Encryption
            Proxy_API[Linkerd Proxy]
            Proxy_Redis[Linkerd Proxy]
        end

        API[Resume API Pod]
        Redis[(Redis StatefulSet)]
        Backup[CronJob Backup]
        
        User --> Tunnel
        Tunnel --> API
        
        API -.-> Proxy_API
        Proxy_API -- "mTLS (Encrypted)" --> Proxy_Redis
        Proxy_Redis -.-> Redis
        
        Backup -- "SAVE" --> Redis
    end

    subgraph Observability
        Loki[(Loki Stack)]
        Grafana[Grafana Dashboards]
    end
