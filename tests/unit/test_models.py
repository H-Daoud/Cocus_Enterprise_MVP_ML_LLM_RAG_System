"""
Unit tests for Order model
"""

import pytest
from pydantic import ValidationError

from src.models.order import Order, OrderStatus


def test_valid_order(sample_order_data):
    """Test creating a valid order"""
    order = Order(**sample_order_data)
    assert order.order_id == "ORD-0001"
    assert order.customer_email == "test@example.com"
    assert order.quantity == 2
    assert order.unit_price == 19.99


def test_invalid_email():
    """Test order with invalid email"""
    data = {
        "order_id": "ORD-0001",
        "customer_email": "not-an-email",
        "quantity": 1,
        "unit_price": 10.0,
        "status": "pending",
        "created_at": "2025-01-10T09:15:00Z",
        "shipping": {"country_code": "US", "city": "Test", "postal_code": "12345"},
        "priority": 1,
    }
    with pytest.raises(ValidationError):
        Order(**data)


def test_negative_quantity():
    """Test order with negative quantity"""
    data = {
        "order_id": "ORD-0001",
        "customer_email": "test@example.com",
        "quantity": -1,
        "unit_price": 10.0,
        "status": "pending",
        "created_at": "2025-01-10T09:15:00Z",
        "shipping": {"country_code": "US", "city": "Test", "postal_code": "12345"},
        "priority": 1,
    }
    with pytest.raises(ValidationError):
        Order(**data)


def test_boolean_normalization():
    """Test boolean field normalization"""
    data = {
        "order_id": "ORD-0001",
        "customer_email": "test@example.com",
        "quantity": 1,
        "unit_price": 10.0,
        "is_gift": "yes",  # String that should be normalized to True
        "status": "pending",
        "created_at": "2025-01-10T09:15:00Z",
        "shipping": {"country_code": "US", "city": "Test", "postal_code": "12345"},
        "priority": 1,
    }
    order = Order(**data)
    assert order.is_gift is True


def test_priority_normalization():
    """Test priority normalization from string"""
    data = {
        "order_id": "ORD-0001",
        "customer_email": "test@example.com",
        "quantity": 1,
        "unit_price": 10.0,
        "status": "pending",
        "created_at": "2025-01-10T09:15:00Z",
        "shipping": {"country_code": "US", "city": "Test", "postal_code": "12345"},
        "priority": "high",  # Should be normalized to 1
    }
    order = Order(**data)
    assert order.priority == 1


def test_anonymize_pii(sample_order_data):
    """Test PII anonymization (GDPR compliance)"""
    order = Order(**sample_order_data)
    anonymized = order.anonymize_pii()
    assert anonymized.customer_email == "anonymized@example.com"
    assert anonymized.order_id == order.order_id  # Other fields unchanged


def test_audit_log(sample_order_data):
    """Test audit log generation (EU AI Act compliance)"""
    order = Order(**sample_order_data)
    audit_log = order.to_audit_log()
    assert "order_id" in audit_log
    assert "timestamp" in audit_log
    assert "action" in audit_log
    assert audit_log["action"] == "order_processed"
