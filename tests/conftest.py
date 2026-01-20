"""
Test configuration for pytest
"""

import pytest
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))


@pytest.fixture
def sample_order_data():
    """Sample order data for testing"""
    return {
        "order_id": "ORD-0001",
        "customer_email": "test@example.com",
        "quantity": 2,
        "unit_price": 19.99,
        "is_gift": False,
        "status": "pending",
        "created_at": "2025-01-10T09:15:00Z",
        "shipping": {
            "country_code": "US",
            "city": "New York",
            "postal_code": "10001"
        },
        "tags": ["test"],
        "referrer_url": "https://example.com",
        "coupon_code": "TEST10",
        "priority": 3
    }


@pytest.fixture
def invalid_order_data():
    """Invalid order data for testing"""
    return {
        "order_id": "INVALID",
        "customer_email": "not-an-email",
        "quantity": -1,
        "unit_price": -10.00,
        "is_gift": "maybe",
        "status": "unknown",
        "created_at": "invalid-date",
        "shipping": {
            "country_code": "XX",
            "city": "",
            "postal_code": None
        },
        "priority": 10
    }
