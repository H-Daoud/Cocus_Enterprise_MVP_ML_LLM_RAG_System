"""
Pydantic models for data validation
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

from src.models.shipping import Shipping


class OrderStatus(str, Enum):
    """Valid order statuses"""

    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class Order(BaseModel):
    """
    Order data model with comprehensive validation
    Implements GDPR-compliant data handling
    """

    order_id: str = Field(..., pattern=r"^ORD-\d{4}$", description="Order ID in format ORD-XXXX")
    customer_email: EmailStr = Field(..., description="Customer email address (PII)")
    quantity: int = Field(..., gt=0, description="Order quantity (must be positive)")
    unit_price: float = Field(..., ge=0, description="Unit price (must be non-negative)")
    is_gift: bool = Field(default=False, description="Whether order is a gift")
    status: OrderStatus = Field(..., description="Order status")
    created_at: datetime = Field(..., description="Order creation timestamp (ISO 8601)")
    shipping: Shipping = Field(..., description="Shipping information")
    tags: Optional[List[str]] = Field(default=None, description="Order tags")
    referrer_url: Optional[str] = Field(default=None, description="Referrer URL")
    coupon_code: Optional[str] = Field(default=None, description="Applied coupon code")
    priority: int = Field(..., ge=1, le=5, description="Order priority (1-5)")

    class Config:
        """Pydantic configuration"""

        json_schema_extra = {
            "example": {
                "order_id": "ORD-0001",
                "customer_email": "customer@example.com",
                "quantity": 2,
                "unit_price": 19.99,
                "is_gift": False,
                "status": "pending",
                "created_at": "2025-01-10T09:15:00Z",
                "shipping": {"country_code": "US", "city": "New York", "postal_code": "10001"},
                "tags": ["new", "promo"],
                "referrer_url": "https://google.com",
                "coupon_code": "WELCOME10",
                "priority": 3,
            }
        }

    @field_validator("quantity", mode="before")
    @classmethod
    def normalize_quantity(cls, v):
        """Normalize quantity to integer"""
        if isinstance(v, str):
            if v.lower() in ["n/a", "na", "none", ""]:
                raise ValueError("Quantity cannot be N/A or empty")
            try:
                return int(v)
            except ValueError:
                raise ValueError(f"Invalid quantity: {v}")
        return v

    @field_validator("unit_price", mode="before")
    @classmethod
    def normalize_price(cls, v):
        """Normalize price to float"""
        if isinstance(v, str):
            try:
                return float(v)
            except ValueError:
                raise ValueError(f"Invalid price: {v}")
        return v

    @field_validator("is_gift", mode="before")
    @classmethod
    def normalize_boolean(cls, v):
        """Normalize various boolean representations"""
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            v_lower = v.lower()
            if v_lower in ["true", "yes", "1", "y"]:
                return True
            elif v_lower in ["false", "no", "0", "n"]:
                return False
            else:
                raise ValueError(f"Invalid boolean value: {v}")
        if isinstance(v, int):
            return bool(v)
        raise ValueError(f"Cannot convert {v} to boolean")

    @field_validator("tags", mode="before")
    @classmethod
    def normalize_tags(cls, v):
        """Normalize tags to list"""
        if v is None or v == "":
            return None
        if isinstance(v, str):
            # Split comma-separated string
            return [tag.strip() for tag in v.split(",") if tag.strip()]
        return v

    @field_validator("priority", mode="before")
    @classmethod
    def normalize_priority(cls, v):
        """Normalize priority to integer"""
        if isinstance(v, str):
            v_lower = v.lower()
            priority_map = {"low": 5, "medium": 3, "high": 1, "urgent": 1}
            if v_lower in priority_map:
                return priority_map[v_lower]
            try:
                return int(v)
            except ValueError:
                raise ValueError(f"Invalid priority: {v}")
        return v

    @model_validator(mode="after")
    def validate_business_rules(self):
        """Apply business rules validation"""
        # Check for zero-price items with quantity
        if self.unit_price == 0 and self.quantity > 0:
            raise ValueError("Zero-price items require manual review")

        # Validate total amount
        total = self.quantity * self.unit_price
        if total > 100000:  # $100k limit
            raise ValueError("Order total exceeds maximum allowed amount")

        return self

    def anonymize_pii(self) -> "Order":
        """
        Anonymize personally identifiable information (GDPR compliance)
        Returns a new Order instance with anonymized data
        """
        anonymized_data = self.model_dump()
        anonymized_data["customer_email"] = "anonymized@example.com"
        return Order(**anonymized_data)

    def to_audit_log(self) -> dict:
        """Generate audit log entry (EU AI Act compliance)"""
        return {
            "order_id": self.order_id,
            "timestamp": datetime.utcnow().isoformat(),
            "action": "order_processed",
            "status": self.status.value,
            "total_amount": self.quantity * self.unit_price,
        }
