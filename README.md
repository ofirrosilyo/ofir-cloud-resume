# Cloud-Native Resume Infrastructure 🚀

[![Build Status](https://github.com/ofirrosilyo/ofir-cloud-resume/actions/workflows/k8s-validate.yaml/badge.svg)](https://github.com/ofirrosilyo/ofir-cloud-resume/actions)
![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)
![Linkerd](https://img.shields.io/badge/Linkerd-00A2AA?style=for-the-badge&logo=Linkerd&logoColor=white)
![Cloudflare](https://img.shields.io/badge/Cloudflare-F38020?style=for-the-badge&logo=Cloudflare&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

A production-grade, hardened personal resume ecosystem hosted on a private **K3s (Kubernetes)** cluster. This project demonstrates a **Zero-Trust** architecture utilizing a service mesh, granular network policies, and automated maintenance lifecycles.

## 🏗️ Architecture Overview

```mermaid
graph LR
    subgraph External
        Internet((Internet))
        CF[Cloudflare Tunnel]
    end

    subgraph Cluster ["K3s Cluster (Private Node)"]
        direction TB
        subgraph Mesh ["Linkerd Service Mesh (mTLS)"]
            API[Resume API Pod]
            Redis[(Redis StatefulSet)]
        end

        Cron[Backup CronJob]
        PVC[[Persistent Volume]]
        NetPol{Network Policy}

        Internet --> CF
        CF --> API
        API -- "Authorized Port 6379" --> NetPol
        NetPol --> Redis
        Redis <--> PVC
        Cron -- "SAVE Command" --> Redis
    end

    subgraph Monitoring
        Loki[(Loki Stack)]
        Grafana[Grafana Dashboard]
        Loki --> Grafana
    end
