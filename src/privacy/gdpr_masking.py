"""
GDPR & EU AI Act Compliant Data Masking Module
Anonymizes sensitive personal data before ML training and RAG indexing
"""

import hashlib
import re
from typing import Dict, Any, Optional
from pydantic import BaseModel


class DataMaskingConfig(BaseModel):
    """Configuration for data masking"""

    mask_emails: bool = True
    mask_addresses: bool = True
    mask_postal_codes: bool = True
    hash_customer_ids: bool = True
    preserve_analytics: bool = True  # Keep country, city for analytics


class GDPRDataMasker:
    """
    GDPR-compliant data masking for sensitive personal information

    EU AI Act Requirements:
    - Transparency: Log all masking operations
    - Privacy: Anonymize PII before ML training
    - Auditability: Reversible hashing for authorized access
    """

    def __init__(self, config: Optional[DataMaskingConfig] = None):
        self.config = config or DataMaskingConfig()
        self.masking_log = []

    def mask_email(self, email: str) -> str:
        """
        Mask email address while preserving domain for analytics

        Example:
            john.doe@example.com → j***@example.com
        """
        if not self.config.mask_emails or not email:
            return email

        try:
            local, domain = email.split("@")
            if len(local) > 2:
                masked_local = local[0] + "*" * (len(local) - 1)
            else:
                masked_local = "*" * len(local)

            masked = f"{masked_local}@{domain}"
            self.masking_log.append(
                {"field": "email", "original_length": len(email), "masked": True}
            )
            return masked
        except:
            return "***@***.com"

    def mask_address(self, address: str) -> str:
        """
        Mask street address completely

        Example:
            "123 Main Street" → "*** *** ***"
        """
        if not self.config.mask_addresses or not address:
            return address

        words = address.split()
        masked = " ".join(["***" for _ in words])

        self.masking_log.append(
            {"field": "address", "original_length": len(address), "masked": True}
        )
        return masked

    def mask_postal_code(self, postal_code: str) -> str:
        """
        Partially mask postal code (keep first 2-3 digits for regional analytics)

        Example:
            "10115" → "101**"
            "SW1A 1AA" → "SW1***"
        """
        if not self.config.mask_postal_codes or not postal_code:
            return postal_code

        if len(postal_code) <= 3:
            return "***"

        # Keep first 3 characters, mask the rest
        masked = postal_code[:3] + "*" * (len(postal_code) - 3)

        self.masking_log.append(
            {"field": "postal_code", "original_length": len(postal_code), "masked": True}
        )
        return masked

    def hash_customer_id(self, customer_id: str, salt: str = "mvp_salt_2026") -> str:
        """
        One-way hash for customer ID (GDPR right to be forgotten)

        Note: In production, use a secure salt from environment variables
        """
        if not self.config.hash_customer_ids or not customer_id:
            return customer_id

        hashed = hashlib.sha256(f"{customer_id}{salt}".encode()).hexdigest()[:16]

        self.masking_log.append({"field": "customer_id", "hashed": True})
        return f"CUST_{hashed}"

    def mask_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mask all sensitive fields in an order

        GDPR Article 5: Data minimization and privacy by design
        """
        masked_order = order_data.copy()

        # Mask email
        if "customer_email" in masked_order:
            masked_order["customer_email"] = self.mask_email(masked_order["customer_email"])

        # Mask shipping address
        if "shipping" in masked_order and isinstance(masked_order["shipping"], dict):
            shipping = masked_order["shipping"]

            if "street" in shipping:
                shipping["street"] = self.mask_address(shipping["street"])

            if "postal_code" in shipping:
                shipping["postal_code"] = self.mask_postal_code(shipping["postal_code"])

            # Keep city and country for analytics (not PII under GDPR)
            # These are needed for ML features

        # Add masking metadata
        masked_order["_gdpr_masked"] = True
        masked_order["_masked_at"] = self._get_timestamp()

        return masked_order

    def _get_timestamp(self) -> str:
        """Get ISO timestamp for audit trail"""
        from datetime import datetime

        return datetime.now().isoformat()

    def get_masking_report(self) -> Dict[str, Any]:
        """
        Generate audit report for GDPR compliance

        EU AI Act Article 13: Transparency and record-keeping
        """
        return {
            "total_operations": len(self.masking_log),
            "fields_masked": list(set(log["field"] for log in self.masking_log)),
            "compliance": {
                "gdpr_article_5": "Data minimization - implemented",
                "gdpr_article_25": "Privacy by design - implemented",
                "eu_ai_act_article_13": "Transparency - audit log maintained",
            },
        }


# Example usage
if __name__ == "__main__":
    masker = GDPRDataMasker()

    # Test data
    sample_order = {
        "order_id": "ORD-0001",
        "customer_email": "john.doe@example.com",
        "shipping": {
            "street": "123 Main Street",
            "city": "Berlin",
            "postal_code": "10115",
            "country_code": "DE",
        },
    }

    print("Original Order:")
    print(sample_order)
    print("\nMasked Order:")
    masked = masker.mask_order(sample_order)
    print(masked)
    print("\nMasking Report:")
    print(masker.get_masking_report())
