# DevOps & Infrastructure as Code (IaaC) Guide

This document outlines the infrastructure strategy, automation tools, and lifecycle management for the COCUS MVP system, focusing on **Docker**, **Google Cloud Platform (GCP)**, and **Kubernetes (K8s)**.

---

## 🏗️ Infrastructure Strategy

We follow the **Infrastructure as Code (IaaC)** philosophy to ensure environments are reproducible, version-controlled, and modular.

### Tooling Stack:
- **Terraform**: For provisioning cloud infrastructure (GCP VPCs, Cloud Run, GKE Clusters).
- **Docker**: For platform-agnostic application packaging.
- **Kubernetes (GKE)**: For production-grade container orchestration.
- **Helm**: For managing complex Kubernetes application deployments.
- **Ansible**: For configuration management and server hardening (on-premise).

---

## 🐳 Containerization (Docker)

The application lifecycle starts with a Docker image, ensuring "Developer-to-Production" parity.

### Implementation:
- **Multi-stage Builds**: The [`docker/Dockerfile`](../../docker/Dockerfile) uses a builder stage to compile dependencies and a slim runner stage to keep the final image size under **400MB**.
- **Context Awareness**: Images are built with the root project context to include all necessary source and data modules.
- **Security**: Images run as non-root users and are scanned for vulnerabilities via GitHub Actions using **Trivy**.

---

## ☁️ Cloud Automation (GCP & Cloud Run)

For rapid iteration and cost-efficiency, we primarily use **Google Cloud Run** for serverless deployments.

### Lifecycle Automation:
1.  **Provisioning**: Terraform scripts in `infrastructure/terraform/` define the Cloud Run service, IAM permissions, and Secret Manager integration.
2.  **Environment Sync**: Secrets are fetched from GCP Secret Manager and injected into the container at runtime, avoiding `.env` file exposure in production.
3.  **Traffic Management**: Cloud Run handles auto-scaling (0-N) and can perform blue/green deployments with traffic splitting.

---

## ☸️ Kubernetes (K8s / GKE)

For complex, high-availability production needs, we provide a complete Kubernetes manifest ecosystem in `infrastructure/kubernetes/`.

### Key Components:
- **Deployments**: Standardized definitions for the API with RollingUpdate strategies.
- **HPA (Horizontal Pod Autoscaler)**: Scalability based on CPU/Memory metrics.
- **Ingress**: Managed via NGINX or GCP Load Balancer with TLS termination.
- **ConfigMaps & Secrets**: Separation of configuration from the container logic.

### Helm Charts:
The `infrastructure/helm/` folder contains a packaged version of the system, allowing for:
```bash
helm install cocus-mvp ./infrastructure/helm/cocus-mvp
```
This automates the deployment of the API, Redis, and Prometheus/Grafana in one command.

---

## 🔄 Deployment Lifecycle (GitOps)

We utilize a GitOps approach where the state of the infrastructure is defined in Git.

1.  **Code Commit**: Developer pushes to `main`.
2.  **Validation**: CI/CD pipeline runs tests and security scans.
3.  **Image Promotion**: A new Docker image is pushed to Google Artifact Registry.
4.  **Infras Update**: Terraform (via GitHub Actions) applies plan changes to the GCP environment.
5.  **K8s Sync**: Helm/Kubectl updates the cluster state in GKE.

---

## 📊 Monitoring & Observability
- **Prometheus**: Scrapes metrics from the FastAPI `/metrics` endpoint.
- **Grafana**: Provides centralized dashboards for infrastructure health and RAG performance.
- **Cloud Logging**: Structured JSON logs are exported to Google Cloud Logging for easy auditing.

---
**📍 Location**: `docs/technical/DEVOPS_IAAC_GUIDE.md`  
**🚀 Scalable. Reliable. Automated.**
