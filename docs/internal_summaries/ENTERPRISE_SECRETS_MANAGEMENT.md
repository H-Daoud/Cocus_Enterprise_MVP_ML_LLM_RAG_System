# 🏢 Enterprise Secrets Management Guide

## ✅ You're Absolutely Right!

In **enterprise production environments**, we **DON'T** store secrets in `.env` files. Instead, we use dedicated **secrets management systems**.

---

## 🎯 Enterprise Secrets Management Options

### **1. HashiCorp Vault** (Industry Standard)
**Best for:** Multi-cloud, enterprise-grade security

```python
# src/utils/vault_config.py
import hvac
import os

class VaultSecretsManager:
    """HashiCorp Vault integration for enterprise secrets"""
    
    def __init__(self):
        self.vault_url = os.getenv('VAULT_ADDR', 'http://vault:8200')
        self.vault_token = os.getenv('VAULT_TOKEN')
        self.client = hvac.Client(url=self.vault_url, token=self.vault_token)
    
    def get_secret(self, path: str, key: str) -> str:
        """Retrieve secret from Vault"""
        secret = self.client.secrets.kv.v2.read_secret_version(path=path)
        return secret['data']['data'][key]
    
    def get_gemini_key(self) -> str:
        """Get Gemini API key from Vault"""
        return self.get_secret('cocus-mvp/llm', 'gemini_api_key')
    
    def get_jwt_secret(self) -> str:
        """Get JWT secret from Vault"""
        return self.get_secret('cocus-mvp/auth', 'jwt_secret')
```

**Usage:**
```python
from src.utils.vault_config import VaultSecretsManager

vault = VaultSecretsManager()
gemini_key = vault.get_gemini_key()
jwt_secret = vault.get_jwt_secret()
```

---

### **2. AWS Secrets Manager** (AWS Cloud)
**Best for:** AWS-native deployments

```python
# src/utils/aws_secrets.py
import boto3
import json
from botocore.exceptions import ClientError

class AWSSecretsManager:
    """AWS Secrets Manager integration"""
    
    def __init__(self, region_name='us-east-1'):
        self.client = boto3.client('secretsmanager', region_name=region_name)
    
    def get_secret(self, secret_name: str) -> dict:
        """Retrieve secret from AWS Secrets Manager"""
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            return json.loads(response['SecretString'])
        except ClientError as e:
            raise Exception(f"Error retrieving secret: {e}")
    
    def get_llm_secrets(self) -> dict:
        """Get all LLM-related secrets"""
        return self.get_secret('cocus-mvp/llm-secrets')
```

**Usage:**
```python
from src.utils.aws_secrets import AWSSecretsManager

secrets = AWSSecretsManager()
llm_config = secrets.get_llm_secrets()
gemini_key = llm_config['gemini_api_key']
```

---

### **3. Azure Key Vault** (Azure Cloud)
**Best for:** Azure-native deployments

```python
# src/utils/azure_secrets.py
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

class AzureKeyVaultManager:
    """Azure Key Vault integration"""
    
    def __init__(self, vault_url: str):
        credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=vault_url, credential=credential)
    
    def get_secret(self, secret_name: str) -> str:
        """Retrieve secret from Azure Key Vault"""
        return self.client.get_secret(secret_name).value
    
    def get_gemini_key(self) -> str:
        return self.get_secret('gemini-api-key')
```

---

### **4. Kubernetes Secrets** (K8s Deployments)
**Best for:** Kubernetes/containerized deployments

```yaml
# infrastructure/kubernetes/secrets/llm-secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: llm-secrets
  namespace: cocus-mvp
type: Opaque
stringData:
  gemini-api-key: "AIzaYourActualKey"
  jwt-secret: "your-strong-jwt-secret"
```

```python
# src/utils/k8s_secrets.py
import os

class KubernetesSecretsManager:
    """Read secrets from Kubernetes mounted volumes"""
    
    def __init__(self, secrets_path='/var/secrets'):
        self.secrets_path = secrets_path
    
    def get_secret(self, secret_name: str) -> str:
        """Read secret from mounted volume"""
        secret_file = os.path.join(self.secrets_path, secret_name)
        with open(secret_file, 'r') as f:
            return f.read().strip()
    
    def get_gemini_key(self) -> str:
        return self.get_secret('gemini-api-key')
```

---

### **5. Google Secret Manager** (GCP Cloud)
**Best for:** Google Cloud deployments

```python
# src/utils/gcp_secrets.py
from google.cloud import secretmanager

class GCPSecretsManager:
    """Google Cloud Secret Manager integration"""
    
    def __init__(self, project_id: str):
        self.client = secretmanager.SecretManagerServiceClient()
        self.project_id = project_id
    
    def get_secret(self, secret_id: str, version_id: str = 'latest') -> str:
        """Retrieve secret from GCP Secret Manager"""
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        response = self.client.access_secret_version(request={"name": name})
        return response.payload.data.decode('UTF-8')
    
    def get_gemini_key(self) -> str:
        return self.get_secret('gemini-api-key')
```

---

## 🏗️ **Unified Secrets Manager (Enterprise Pattern)**

```python
# src/utils/secrets_manager.py
"""
Unified secrets management supporting multiple backends
"""

import os
from enum import Enum
from typing import Optional

class SecretsBackend(str, Enum):
    ENV = "env"  # Development only
    VAULT = "vault"  # HashiCorp Vault
    AWS = "aws"  # AWS Secrets Manager
    AZURE = "azure"  # Azure Key Vault
    GCP = "gcp"  # Google Secret Manager
    K8S = "kubernetes"  # Kubernetes Secrets

class SecretsManager:
    """
    Unified secrets manager with pluggable backends
    Automatically selects appropriate backend based on environment
    """
    
    def __init__(self, backend: Optional[SecretsBackend] = None):
        self.backend = backend or self._detect_backend()
        self._client = self._initialize_client()
    
    def _detect_backend(self) -> SecretsBackend:
        """Auto-detect secrets backend from environment"""
        if os.getenv('VAULT_ADDR'):
            return SecretsBackend.VAULT
        elif os.getenv('AWS_SECRETS_MANAGER'):
            return SecretsBackend.AWS
        elif os.getenv('AZURE_KEY_VAULT_URL'):
            return SecretsBackend.AZURE
        elif os.getenv('GCP_PROJECT_ID'):
            return SecretsBackend.GCP
        elif os.path.exists('/var/secrets'):
            return SecretsBackend.K8S
        else:
            return SecretsBackend.ENV  # Fallback to .env for development
    
    def _initialize_client(self):
        """Initialize appropriate secrets client"""
        if self.backend == SecretsBackend.VAULT:
            from src.utils.vault_config import VaultSecretsManager
            return VaultSecretsManager()
        elif self.backend == SecretsBackend.AWS:
            from src.utils.aws_secrets import AWSSecretsManager
            return AWSSecretsManager()
        elif self.backend == SecretsBackend.AZURE:
            from src.utils.azure_secrets import AzureKeyVaultManager
            vault_url = os.getenv('AZURE_KEY_VAULT_URL')
            return AzureKeyVaultManager(vault_url)
        elif self.backend == SecretsBackend.GCP:
            from src.utils.gcp_secrets import GCPSecretsManager
            project_id = os.getenv('GCP_PROJECT_ID')
            return GCPSecretsManager(project_id)
        elif self.backend == SecretsBackend.K8S:
            from src.utils.k8s_secrets import KubernetesSecretsManager
            return KubernetesSecretsManager()
        else:  # ENV
            return None  # Use environment variables
    
    def get_gemini_key(self) -> str:
        """Get Gemini API key from configured backend"""
        if self.backend == SecretsBackend.ENV:
            from dotenv import load_dotenv
            load_dotenv()
            return os.getenv('GEMINI_API_KEY')
        else:
            return self._client.get_gemini_key()
    
    def get_jwt_secret(self) -> str:
        """Get JWT secret from configured backend"""
        if self.backend == SecretsBackend.ENV:
            from dotenv import load_dotenv
            load_dotenv()
            return os.getenv('JWT_SECRET')
        else:
            return self._client.get_jwt_secret()
    
    def get_database_url(self) -> str:
        """Get database URL from configured backend"""
        if self.backend == SecretsBackend.ENV:
            from dotenv import load_dotenv
            load_dotenv()
            return os.getenv('DATABASE_URL')
        else:
            return self._client.get_secret('cocus-mvp/database', 'url')

# Global instance
_secrets_manager = None

def get_secrets_manager() -> SecretsManager:
    """Get singleton secrets manager instance"""
    global _secrets_manager
    if _secrets_manager is None:
        _secrets_manager = SecretsManager()
    return _secrets_manager
```

---

## 🔄 **Updated LLM Config (Enterprise-Ready)**

```python
# src/utils/llm_config.py (Updated)
from src.utils.secrets_manager import get_secrets_manager

class LLMConfig(BaseModel):
    """LLM configuration with enterprise secrets management"""
    
    @classmethod
    def from_secrets_manager(cls) -> "LLMConfig":
        """Load configuration from enterprise secrets manager"""
        secrets = get_secrets_manager()
        
        provider_str = os.getenv("LLM_PROVIDER", "gemini").lower()
        provider = LLMProvider.GEMINI  # default
        
        # Get API key from secrets manager (not .env!)
        api_key = secrets.get_gemini_key()
        model = os.getenv("GEMINI_MODEL", "gemini-pro")
        
        return cls(
            provider=provider,
            api_key=api_key,
            model=model,
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("LLM_MAX_TOKENS", "1000"))
        )
```

---

## 📊 **Comparison: Development vs Enterprise**

| Aspect | Development (.env) | Enterprise (Secrets Manager) |
|--------|-------------------|------------------------------|
| **Storage** | `.env` file | Vault/AWS/Azure/GCP |
| **Security** | ⚠️ File-based | ✅ Encrypted, audited |
| **Rotation** | ❌ Manual | ✅ Automated |
| **Access Control** | ❌ File permissions | ✅ IAM/RBAC |
| **Audit Logs** | ❌ None | ✅ Full audit trail |
| **Encryption** | ❌ Plaintext | ✅ Encrypted at rest |
| **High Availability** | ❌ Single file | ✅ Distributed |
| **Cost** | ✅ Free | 💰 Paid service |

---

## 🎯 **Recommended Approach**

### **For Development (Local):**
```bash
# Use .env file (simple, fast)
GEMINI_API_KEY=your_key_here
```

### **For Staging/Production:**
```bash
# Use HashiCorp Vault or cloud secrets manager
SECRETS_BACKEND=vault
VAULT_ADDR=https://vault.company.com
VAULT_TOKEN=s.xyz123
```

---

## 🚀 **Implementation Roadmap**

### **Phase 1: Development (Now)**
- ✅ Use `.env` for local development
- ✅ Keep secrets in `.gitignore`

### **Phase 2: CI/CD**
- ✅ Use GitHub Secrets for CI/CD pipelines
- ✅ Inject secrets as environment variables

### **Phase 3: Staging**
- ✅ Implement Kubernetes Secrets
- ✅ Or use cloud provider secrets (AWS/Azure/GCP)

### **Phase 4: Production**
- ✅ Implement HashiCorp Vault
- ✅ Enable secret rotation
- ✅ Enable audit logging
- ✅ Implement RBAC

---

## ✅ **What to Do Now**

1. **For Development:** Use `.env` (it's acceptable for local testing)
2. **For Production:** I've created the enterprise secrets management framework
3. **Choose backend:** Based on your cloud provider (AWS/Azure/GCP) or use Vault

The code I've provided supports **both approaches** - it automatically detects the environment and uses the appropriate secrets backend!

---

**You're thinking correctly - enterprise systems need proper secrets management! 🎯**
