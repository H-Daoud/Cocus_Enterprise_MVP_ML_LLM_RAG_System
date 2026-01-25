"""
Unified secrets management supporting multiple backends
Enterprise-grade secrets handling for production deployments
"""

import os
from enum import Enum
from typing import Optional

from src.utils.logger import get_logger

logger = get_logger(__name__)


class SecretsBackend(str, Enum):
    """Supported secrets management backends"""

    ENV = "env"  # Development only - uses .env file
    VAULT = "vault"  # HashiCorp Vault
    AWS = "aws"  # AWS Secrets Manager
    AZURE = "azure"  # Azure Key Vault
    GCP = "gcp"  # Google Secret Manager
    K8S = "kubernetes"  # Kubernetes Secrets


class SecretsManager:
    """
    Unified secrets manager with pluggable backends
    Automatically selects appropriate backend based on environment

    Usage:
        secrets = SecretsManager()
        api_key = secrets.get_gemini_key()
    """

    def __init__(self, backend: Optional[SecretsBackend] = None):
        self.backend = backend or self._detect_backend()
        logger.info(f"Initializing secrets manager with backend: {self.backend.value}")
        self._client = self._initialize_client()

    def _detect_backend(self) -> SecretsBackend:
        """Auto-detect secrets backend from environment"""
        if os.getenv("VAULT_ADDR"):
            return SecretsBackend.VAULT
        elif os.getenv("AWS_SECRETS_MANAGER_ENABLED"):
            return SecretsBackend.AWS
        elif os.getenv("AZURE_KEY_VAULT_URL"):
            return SecretsBackend.AZURE
        elif os.getenv("GCP_PROJECT_ID"):
            return SecretsBackend.GCP
        elif os.path.exists("/var/secrets"):
            return SecretsBackend.K8S
        else:
            logger.warning("No enterprise secrets backend detected, falling back to .env")
            return SecretsBackend.ENV

    def _initialize_client(self):
        """Initialize appropriate secrets client"""
        try:
            if self.backend == SecretsBackend.VAULT:
                import hvac

                vault_url = os.getenv("VAULT_ADDR")
                vault_token = os.getenv("VAULT_TOKEN")
                return hvac.Client(url=vault_url, token=vault_token)

            elif self.backend == SecretsBackend.AWS:
                import boto3

                region = os.getenv("AWS_REGION", "us-east-1")
                return boto3.client("secretsmanager", region_name=region)

            elif self.backend == SecretsBackend.AZURE:
                from azure.identity import DefaultAzureCredential
                from azure.keyvault.secrets import SecretClient

                vault_url = os.getenv("AZURE_KEY_VAULT_URL")
                credential = DefaultAzureCredential()
                return SecretClient(vault_url=vault_url, credential=credential)

            elif self.backend == SecretsBackend.GCP:
                from google.cloud import secretmanager

                return secretmanager.SecretManagerServiceClient()

            elif self.backend == SecretsBackend.K8S:
                # Kubernetes secrets are mounted as files
                return None

            else:  # ENV
                return None

        except Exception as e:
            logger.error(f"Failed to initialize {self.backend.value} client: {e}")
            logger.warning("Falling back to environment variables")
            self.backend = SecretsBackend.ENV
            return None

    def get_secret(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get secret value by key

        Args:
            key: Secret key name
            default: Default value if secret not found

        Returns:
            Secret value or default
        """
        try:
            if self.backend == SecretsBackend.ENV:
                from dotenv import load_dotenv

                load_dotenv()
                return os.getenv(key, default)

            elif self.backend == SecretsBackend.VAULT:
                # HashiCorp Vault
                secret_path = os.getenv("VAULT_SECRET_PATH", "cocus-mvp")
                secret = self._client.secrets.kv.v2.read_secret_version(path=secret_path)
                return secret["data"]["data"].get(key, default)

            elif self.backend == SecretsBackend.AWS:
                # AWS Secrets Manager
                import json

                secret_name = os.getenv("AWS_SECRET_NAME", "cocus-mvp/secrets")
                response = self._client.get_secret_value(SecretId=secret_name)
                secrets = json.loads(response["SecretString"])
                return secrets.get(key, default)

            elif self.backend == SecretsBackend.AZURE:
                # Azure Key Vault
                secret = self._client.get_secret(key)
                return secret.value

            elif self.backend == SecretsBackend.GCP:
                # Google Secret Manager
                project_id = os.getenv("GCP_PROJECT_ID")
                name = f"projects/{project_id}/secrets/{key}/versions/latest"
                response = self._client.access_secret_version(request={"name": name})
                return response.payload.data.decode("UTF-8")

            elif self.backend == SecretsBackend.K8S:
                # Kubernetes mounted secrets
                secrets_path = os.getenv("K8S_SECRETS_PATH", "/var/secrets")
                secret_file = os.path.join(secrets_path, key)
                if os.path.exists(secret_file):
                    with open(secret_file, "r") as f:
                        return f.read().strip()
                return default

        except Exception as e:
            logger.error(f"Error retrieving secret '{key}': {e}")
            return default

    def get_gemini_key(self) -> Optional[str]:
        """Get Gemini API key"""
        return self.get_secret("GEMINI_API_KEY")

    def get_openai_key(self) -> Optional[str]:
        """Get OpenAI API key"""
        return self.get_secret("OPENAI_API_KEY")

    def get_jwt_secret(self) -> Optional[str]:
        """Get JWT secret for authentication"""
        return self.get_secret("JWT_SECRET")

    def get_secret_key(self) -> Optional[str]:
        """Get general application secret key"""
        return self.get_secret("SECRET_KEY")

    def get_database_url(self) -> Optional[str]:
        """Get database connection URL"""
        return self.get_secret("DATABASE_URL")


# Global singleton instance
_secrets_manager: Optional[SecretsManager] = None


def get_secrets_manager() -> SecretsManager:
    """
    Get singleton secrets manager instance

    Returns:
        SecretsManager instance
    """
    global _secrets_manager
    if _secrets_manager is None:
        _secrets_manager = SecretsManager()
    return _secrets_manager
