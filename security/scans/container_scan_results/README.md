# Container Security Scan Documentation

## Overview
The container security scanning for the **COCUS MVP ML/LLM RAG System** is fully automated and integrated into the CI/CD pipeline. We verify the Docker image for vulnerabilities on every push and pull request to `main` or `develop`.

## 🛠️ Tooling & Process
- **Scanner:** [Trivy](https://github.com/aquasecurity/trivy) (via `aquasecurity/trivy-action`)
- **Execution Environment:** GitHub Actions (User: `ubuntu-latest`)
- **Workflow File:** `.github/workflows/security-scan.yml`

### Workflow Steps
1.  **Build:** The Docker image is built from `docker/Dockerfile.api`.
    *   *Note:* This requires all dependencies in `requirements.txt` to be resolvable.
2.  **Scan:** Trivy scans the built image (`cocus-mvp:latest`) for OS and dependency vulnerabilities.
3.  **Report:** Results are uploaded to the **GitHub Security Tab** (SARIF format).

## 📊 Where to Find Results
Since the scan runs in the cloud, no local report files are generated in this directory by default. To view the latest scan results:

1.  Go to the [GitHub Actions Dashboard](https://github.com/H-Daoud/Cocus_Enterprise_MVP_ML_LLM_RAG_System/actions).
2.  Click on the latest **Security Scan** workflow run.
3.  Inspect the **container-scan** job logs or the uploaded artifacts.
4.  Alternatively, check the **Security** tab in the repository menu (if enabled).

## ✅ Recent Resolution (Jan 2026)
**Issue:** The container scan initially failed to run (empty results).
**Root Cause:** Critical dependency failures (`torch`, `setuptools`) prevented `pip install` from completing during the Docker build.
**Resolution:**
- Fixed `requirements.txt` (downgraded `torch` to compatible version, updated `setuptools`).
- Implemented `.safety-policy.yml` to handle upstream CVEs.
- **Result:** The Docker build now succeeds, allowing the Trivy scan to execute successfully in the CI pipeline.

---
*This document serves as a reference for the automated container security strategy.*
