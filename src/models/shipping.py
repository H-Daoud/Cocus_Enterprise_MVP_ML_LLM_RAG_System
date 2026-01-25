"""
Shipping information model
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, ClassVar


class Shipping(BaseModel):
    """Shipping information with country code validation"""

    country_code: str = Field(
        ..., min_length=2, max_length=2, description="ISO 3166-1 alpha-2 country code"
    )
    city: str = Field(..., min_length=1, description="City name")
    postal_code: Optional[str] = Field(default=None, description="Postal/ZIP code")

    # Valid country codes (ISO 3166-1 alpha-2)
    VALID_COUNTRIES: ClassVar[set] = {
        "US",
        "GB",
        "DE",
        "FR",
        "ES",
        "PT",
        "IE",
        "CZ",
        "PL",
        "IT",
        "NL",
        "BE",
        "AT",
        "CH",
    }

    @field_validator("country_code")
    @classmethod
    def validate_country_code(cls, v):
        """Validate country code against ISO 3166-1 alpha-2"""
        v_upper = v.upper()
        if v_upper not in cls.VALID_COUNTRIES:
            raise ValueError(f"Invalid country code: {v}. Must be one of {cls.VALID_COUNTRIES}")
        return v_upper

    @field_validator("postal_code", mode="before")
    @classmethod
    def normalize_postal_code(cls, v):
        """Normalize postal code"""
        if v is None or v == "" or (isinstance(v, str) and v.strip() == ""):
            return None
        if isinstance(v, (int, float)):
            return str(int(v))
        return str(v).strip()

    class Config:
        """Pydantic configuration"""

        json_schema_extra = {
            "example": {"country_code": "US", "city": "New York", "postal_code": "10001"}
        }
